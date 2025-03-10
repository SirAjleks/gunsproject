from django.shortcuts import render, redirect, get_object_or_404
from .models import Gun, Person, Rank, Assignment

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('soldier_dashboard')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def soldier_dashboard(request):
    return render(request, 'soldier_dashboard.html')

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

@login_required
def gun_add(request):
    if request.method == 'POST':
        # Form submission: get data from request and save a new Gun
        name = request.POST.get('name')
        category = request.POST.get('category')  # if using category field; otherwise ignore
        if name:  # basic validation: ensure name is not empty
            Gun.objects.create(name=name, category=category)  # category=category if applicable
        return redirect('gun_add')
    else:
        # GET request: show the add gun form
        guns = Gun.objects.all()  # Fetch all existing guns
        return render(request, 'gun_add.html', {'guns': guns})

# Person List View
def person_list(request):
    people = Person.objects.select_related('rank').all()
    return render(request, 'people_list.html', {'people': people})

# Add Person View
@login_required
def person_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rank_id = request.POST.get('rank')  # this will be the selected rank’s ID from the form
        if name and rank_id:
            rank = Rank.objects.get(id=rank_id)
            Person.objects.create(name=name, rank=rank)
        return redirect('person_add')
    else:
        # Fetch all existing soldiers and ranks
        ranks = Rank.objects.all()
        soldiers = Person.objects.select_related('rank').all()
        return render(request, 'person_add.html', {'ranks': ranks, 'soldiers': soldiers})

# Assign Gun View
@login_required
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
        return redirect('assign_gun')
    else:
        # Fetch all existing soldiers and available guns
        people = Person.objects.all()
        available_guns = Gun.objects.filter(is_assigned=False)
        issued_guns = Assignment.objects.select_related('gun', 'person').filter(date_returned__isnull=True)
        return render(request, 'assign_gun.html', {'people': people, 'guns': available_guns, 'issued_guns': issued_guns})


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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def soldier_dashboard(request):
    return render(request, 'soldier_dashboard.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

# Check if user is in 'Soldier' group
def is_soldier(user):
    return user.groups.filter(name='Soldier').exists()

@login_required
@user_passes_test(is_soldier)
def soldier_dashboard(request):
    return render(request, 'soldier_dashboard.html')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.groups.filter(name='Soldier').exists():
        return redirect('soldier_dashboard')
    else:
        return redirect('login')

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Assignment, Gun

# Check if user is in 'Soldier' group
def is_soldier(user):
    return user.groups.filter(name='Soldier').exists()

@login_required
@user_passes_test(is_soldier)
def view_assigned_guns(request):
    # Get the Person object linked to the logged-in user
    try:
        person = Person.objects.get(user=request.user)
    except Person.DoesNotExist:
        # If no Person linked, redirect to dashboard with error message
        return redirect('soldier_dashboard')

    # Get the logged-in soldier's assignments
    assignments = Assignment.objects.filter(person=person, date_returned__isnull=True)
    return render(request, 'view_assigned_guns.html', {'assignments': assignments})


from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Assignment

# Check if user is in 'Soldier' group
def is_soldier(user):
    return user.groups.filter(name='Soldier').exists()

@login_required
@user_passes_test(is_soldier)
def view_all_assigned_guns(request):
    # Get all gun assignments (read-only for soldiers)
    assignments = Assignment.objects.filter(date_returned__isnull=True)
    return render(request, 'view_all_assigned_guns.html', {'assignments': assignments})


from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Gun, Assignment, Person


# Check if user is in 'Soldier' group
def is_soldier(user):
    return user.groups.filter(name='Soldier').exists()


@login_required
@user_passes_test(is_soldier)
def request_gun(request):
    # Get the logged-in soldier's person profile
    person = Person.objects.get(user=request.user)
    # Show guns that are not assigned and match the soldier's rank
    eligible_guns = Gun.objects.filter(is_assigned=False)

    if request.method == 'POST':
        gun_id = request.POST.get('gun_id')
        gun = Gun.objects.get(id=gun_id)
        # Create a request entry by setting requested=True
        Assignment.objects.create(person=person, gun=gun, requested=True)
        return redirect('soldier_dashboard')

    return render(request, 'request_gun.html', {'eligible_guns': eligible_guns})

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Assignment

# Check if user is an admin
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def issued_guns_list(request):
    # Get all issued guns
    issued_guns = Assignment.objects.filter(date_returned__isnull=True)
    return render(request, 'issued_guns_list.html', {'issued_guns': issued_guns})
