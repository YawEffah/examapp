from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils import timezone
from django.db.models.signals import m2m_changed
from django.dispatch import receiver



# Create your models here.

#Model for faculty
class Faculty(models.Model):
    name = models.CharField(max_length=120)
    faculty_dean = models.CharField(max_length=128)


    def __str__(self):
        return f"{self.name}"


#Model for department
class Department(models.Model):
    name = models.CharField(max_length=120)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments")


    def __str__(self):
        return f"{self.name}"
    

#Model for programme
class Programme(models.Model):
    name = models.CharField(max_length=120)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name = 'programmes')


    def __str__(self):
        return f"{self.name}"


#Model for Exam Centers
class ExamCenter(models.Model):
    name = models.CharField(max_length=64)
    block = models.CharField(max_length=64)
    designated_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name = "examcenters")


    def __str__(self):    
        return f"{self.name} - {self.block}"


#Model for Exam Hall
class ExamHall(models.Model):
    name = models.CharField(max_length=12)
    capacity = models.PositiveIntegerField()
    center = models.ForeignKey(ExamCenter, on_delete=models.CASCADE, related_name="examhalls")
    current_occupancy = models.PositiveIntegerField(default=0, blank=True)
   
    @property
    def available_seats(self):
        return self.capacity - self.current_occupancy
    

    def __str__(self):
        return f"{self.name}"


#Model for Invigilaor
class Invigilator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_hall = models.ForeignKey(ExamHall, on_delete=models.CASCADE, related_name='invigilators')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} - {self.user.first_name}"


LEVEL_CHOICES = [
        (100, 'Level 100'),
        (200, 'Level 200'),
        (300, 'Level 300'),
        (400, 'Level 400'),
        # Add more choices as needed
    ]

#Model for Course
class Course(models.Model):
    title = models.CharField(max_length=64)
    code = models.CharField(max_length=12)
    credit_hours = models.PositiveIntegerField(default=0)
    date = models.DateField(default=timezone.now)  
    venue = models.ForeignKey(ExamHall, on_delete=models.CASCADE)
    start_time = models.TimeField(default=timezone.now)  
    end_time = models.TimeField(default=timezone.now)  
    level = models.IntegerField(choices=LEVEL_CHOICES, default=100)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name="courses")
    # Add more fields as needed, such as instructor, syllabus, etc.


    def __str__(self):
        return f" {self.code} - {self.title}"


#Model for Candidate
class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=100)
    course = models.ManyToManyField(Course, related_name='candidates', blank=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    # Add other candidate details like name, contact information, etc.


    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} - {self.programme}"


class DepartmentHead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} - {self.user.first_name}"


class FacultyExaminer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} - {self.user.first_name}"


class MalpracticeReport(models.Model):
    report_date_time = models.DateTimeField(default=timezone.now)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='malpractice_reports')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    evidence = models.FileField(upload_to='malpractice_evidence/')
    handled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='handled_malpractice_reports')
      


    def __str__(self):
        return f"Malpractice Report for {self.candidate.user.username} - {self.report_date_time}"


#Models for different user groups
department_head_group, created = Group.objects.get_or_create(name='HOD')
faculty_examiner_group, created = Group.objects.get_or_create(name='Examiner')
exam_invigilator_group, created = Group.objects.get_or_create(name="Invigilator")
candidate_group, created = Group.objects.get_or_create(name="Candidate")


