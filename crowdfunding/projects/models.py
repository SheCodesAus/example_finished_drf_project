from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Exam(models.Model):
    name=models.CharField(max_length=200)
    created_by=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_exams'
    )
    created_date=models.DateTimeField(auto_now_add=True)

class ExamResult(models.Model):
    examinee=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='exam_results'
    )
    exam=models.ForeignKey(
        'Exam',
        on_delete=models.CASCADE,
        related_name='results'
    )
    score=models.FloatField()
    date_recorded=models.DateTimeField(auto_now_add=True)

class TutorProject(models.Model):
    name=models.CharField(max_length=200)
    created_by=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    
    tutor_for=models.ForeignKey(
        'Exam',
        on_delete=models.CASCADE,
        related_name='tutoring_projects'
    )

    description=models.TextField()
    image=models.URLField()
    required_grade=models.FloatField()
    required_tutoring_hours=models.IntegerField()
    is_open=models.BooleanField()
    created_date=models.DateTimeField(auto_now_add=True)
    

class TutorPledge(models.Model):
    hours_pledged = models.IntegerField()
    comment = models.CharField(max_length=200)
    pledged_to = models.ForeignKey(
        'TutorProject',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    pledged_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )
