from django.db import models

# Gun Model
class Gun(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, null=True, blank=True)
    is_assigned = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Rank Model
class Rank(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Person Model
class Person(models.Model):
    name = models.CharField(max_length=100)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.rank.name})"

# Assignment Model
class Assignment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    gun = models.ForeignKey(Gun, on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.gun.name} assigned to {self.person.name}"
