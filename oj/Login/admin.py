from django.contrib import admin

# Register your models here.


from . import models

admin.site.register(models.Problem)
admin.site.register(models.Solution)
admin.site.register(models.TestCase)