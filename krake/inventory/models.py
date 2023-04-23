from django.db import models
import random

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=200)

class Owner(models.Model):
    name = models.CharField(max_length=200)

class ForeignSystem(models.Model):
    name = models.CharField(max_length=200)
    Link = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return str(self.name)

class Item(models.Model):
    id = models.DecimalField(max_digits=10, decimal_places=0, primary_key=True, editable=False)
    name = models.CharField(max_length=200, blank=True)
    documentationLink = models.CharField(max_length=200, blank=True)
    place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.CASCADE, related_name="items")
    owner = models.ForeignKey(Owner, null=True, blank=True, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return str(self.id)

    def save(self, **kwargs):
        if not self.id:
            self.id = self.generateId()
        super().save(*kwargs)

    def generateId(self):
        id = "".join([str(random.randint(0, 9)) for i in range(10)])
        # TODO check if exists 
        # while not Item.objects.filter(id=id).exists():
        #     id = foo
        return id
    

class ForeignSystemLink(models.Model):
    ForeignSystem = models.ForeignKey(ForeignSystem, null=True, blank=True, on_delete=models.CASCADE, related_name="Items")
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE, related_name="ForeignSystem")
    Link = models.CharField(max_length=200, blank=True) 

    def __str__(self):
        return str(self.item) + " -> " + str(self.ForeignSystem)