from django.db import models
from django.urls import reverse
import os
from oj import settings
from . import constant
from django.contrib.auth.models import AbstractUser


# # Create your models here.

class UserProfile(AbstractUser):
    pass

class Problem(models.Model):
    title = models.CharField(max_length = 200)
    statement = models.CharField(max_length=500)
    difficulty = models.IntegerField()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('problemdetail', args=str(self.id))


def get_testcase_input_upload_path(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, 'problems', str(instance.problem.id), 'testcases', str(instance.id), filename)

def get_testcase_output_upload_path(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, 'problems', str(instance.problem.id), 'testcases', str(instance.id), filename)

def get_submission_upload_path(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, 'problems', str(instance.problem.id), 'submissions', filename)

class SubmissionManager(models.Manager):
    def create_submission(self, problem):
        submission = self.create(problem=problem)
        return submission


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=255, null=True)
    submitted_at = models.DateTimeField(auto_now_add = True)
    submittedFile = models.FileField(null=False, blank=False, upload_to=get_submission_upload_path)
    language = models.CharField(max_length=255, choices=constant.AVAILABLE_LANGUAGES
    , default='cpp')
    submittedFilePath = models.FilePathField(path=settings.MEDIA_ROOT, max_length=255)
    objects = SubmissionManager()

    
    def __str__(self) -> str:
        return self.problem.title

    def get_absolute_url(self):
        return reverse('submission', args = [str(self.id)])
    
    class Meta:
        ordering = ['-submitted_at']

# file path field not letting store path within the app.
# allowing to store path outside the project


class TestCaseManager(models.Manager):
    def create_testcase(self, problem):
        testcase = self.create(problem=problem)
        return testcase



class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    inputFile = models.FileField(blank=False, null=False, upload_to=get_testcase_input_upload_path)
    outputFile = models.FileField(blank=False, null=False, upload_to=get_testcase_output_upload_path)
    inputPath = models.FilePathField(path=settings.MEDIA_ROOT, max_length=255)
    outputPath = models.FilePathField(path=settings.MEDIA_ROOT, max_length=255)
    objects = TestCaseManager()

    def __str__(self) -> str:
        return self.problem.title
    



    




    


