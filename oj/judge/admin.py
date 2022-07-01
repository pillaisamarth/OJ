from django.contrib import admin

# Register your models here.


from . import models

admin.site.register(models.Problem)
admin.site.register(models.Submission)
admin.site.register(models.TestCase)