from django.db import models

# Create your models here.
class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

'''
>>> from choices.models import Person
>>> p = Person(name="Fred Flintstone", shirt_size="L")
>>> p.save()
>>> p.shirt_size
'L'
>>> p.get_shirt_size_display()
'Large'

 - or -

>>> p = Person()
>>> p.name
''
>>> p.name = "john" 
>>> p.name
'john'
>>> p.shirt_size = "A" 
>>> p.shirt_size
'A'
>>> p.get_shirt_size_display()
'A'
>>> p.shirt_size = "L" 
>>> p.get_shirt_size_display()
'Large'
'''