from django.db import models
from django.urls import reverse
import os
from oj import settings
from . import constant


# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length = 200)
    statement = models.CharField(max_length=500)
    difficulty = models.IntegerField()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('problemdetail', args=str(self.id))


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add = True)
    language = models.CharField(max_length=255, choices=constant.AVAILABLE_LANGUAGES
    , default='cpp')
    submittedFilePath = models.FilePathField(path=settings.MEDIA_ROOT, max_length=255)

    
    def __str__(self) -> str:
        return self.problem.title

    def get_absolute_url(self):
        return reverse('submission', args = [str(self.id)])
    
    class Meta:
        ordering = ['-submitted_at']

# file path field not letting store path within the app.
# allowing to store path outside the project
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    inputPath = models.FilePathField(path=settings.MEDIA_ROOT, max_length=255)
    outputPath = models.FilePathField(path=settings.MEDIA_ROOT, max_length=255)

    def __str__(self) -> str:
        return self.problem.title
    



    




    


