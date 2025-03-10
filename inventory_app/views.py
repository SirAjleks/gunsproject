from django.shortcuts import render, redirect, get_object_or_404
from .models import Gun, Person, Rank, Assignment

# Gun List View
def gun_list(request):
    guns = Gun.objects.all()
    active_assignments = {assign.gun_id: assign for assign in Assignment.objects.filter(date_returned__isnull=True)}

    # Attach holder name to each gun if assigned
    for gun in guns:
        gun.holder = None  # Default: no holder
        if gun.id in active_assignments:
            gun.holder = active_assignments[gun.id].person.name  # Set holder name if assigned

    context = {'guns': guns}
    return render(request, 'guns_list.html', context)  # Consistent template path

# Home View (Fixed: Removed duplicate)
def home(request):
    num_guns = Gun.objects.count()
    num_people = Person.objects.count()
    num_issued = Assignment.objects.filter(date_returned__isnull=True).count()
    return render(request, 'index.html', {'num_guns': num_guns, 'num_people': num_people, 'num_issued': num_issued})

# Add Gun View
def gun_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        if name:
            Gun.objects.create(name=name)
        return redirect('guns_list')
    else:
        return render(request, 'gun_add.html')

# Person List View
def person_list(request):
    people = Person.objects.select_related('rank').all()
    return render(request, 'people_list.html', {'people': people})

# Add Person View
def person_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rank_id = request.POST.get('rank')
        if name and rank_id:
            rank = Rank.objects.get(id=rank_id)
            Person.objects.create(name=name, rank=rank)
        return redirect('people_list')
    else:
        ranks = Rank.objects.all()
        return render(request, 'person_add.html', {'ranks': ranks})

# Assign Gun View
def assign_gun(request):
    if request.method == 'POST':
        person_id = request.POST.get('person')
        gun_id = request.POST.get('gun')
        if person_id and gun_id:
            person = Person.objects.get(id=person_id)
            gun = Gun.objects.get(id=gun_id)
            if not gun.is_assigned:
                Assignment.objects.create(person=person, gun=gun)
                gun.is_assigned = True
                gun.save()
        return redirect('guns_list')
    else:
        people = Person.objects.all()
        available_guns = Gun.objects.filter(is_assigned=False)
        context = {'people': people, 'guns': available_guns}
        return render(request, 'assign_gun.html', context)  # Consistent template path

# Return Gun View
def return_gun(request, gun_id):
    try:
        assignment = Assignment.objects.get(gun_id=gun_id, date_returned__isnull=True)
    except Assignment.DoesNotExist:
        assignment = None
    if assignment:
        from django.utils import timezone
        assignment.date_returned = timezone.now()
        assignment.save()
        gun = assignment.gun
        gun.is_assigned = False
        gun.save()
    return redirect('guns_list')
