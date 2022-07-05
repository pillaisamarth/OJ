from xml.etree.ElementInclude import include
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


def submission_path():
    return os.path.join(settings.FILE_PATH_FIELD_DIR, 'submissions')

def testcase_input():
    return os.path.join(settings.FILE_PATH_FIELD_DIR, 'testcases', 'input')

def testcase_output():
    return os.path.join(settings.FILE_PATH_FIELD_DIR, 'testcases', 'output')


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add = True)
    language = models.CharField(max_length=255, choices=constant.AVAILABLE_LANGUAGES
    , default='cpp')
    submission = models.FilePathField(max_length=255, path = submission_path, recursive=True)
    
    def __str__(self) -> str:
        return self.problem.title

    def get_absolute_url(self):
        return reverse('viewsubmission', args = [str(self.id)])

# file path field not letting store path within the app.
# allowing to store path outside the project
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.FilePathField(max_length=255, path=testcase_input)
    output = models.FilePathField(max_length=255, path=testcase_output)

    def __str__(self) -> str:
        return self.problem.title




    


