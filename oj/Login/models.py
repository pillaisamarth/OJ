from django.db import models
from django.urls import reverse


# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length = 200)
    statement = models.CharField(max_length=500)
    difficulty = models.IntegerField()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('problemdetail', args=str(self.id))

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add = True)
    solution_file = models.TextField(default="Enter code")
    
    def __str__(self) -> str:
        return self.problem.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.CharField(max_length=100)
    output = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.problem.title




    


