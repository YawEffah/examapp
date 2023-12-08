from django.contrib import admin

from .models import *


class ExamHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'current_occupancy', 'available_seats')

class ExamCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'block', 'designated_faculty')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')

class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code','title','programme')

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user','programme','department','faculty')

class InvigilatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'assigned_hall', 'faculty')

class DepartmentHeadAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'faculty')

class FacultyExaminerAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty')

class MalpracticeReportAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'description', 'report_date_time')

# Register your models here.

admin.site.register(Faculty)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(ExamCenter, ExamCenterAdmin)
admin.site.register(ExamHall, ExamHallAdmin)
admin.site.register(Invigilator, InvigilatorAdmin)
admin.site.register(FacultyExaminer, FacultyExaminerAdmin)
admin.site.register(DepartmentHead, DepartmentHeadAdmin)
admin.site.register(MalpracticeReport, MalpracticeReportAdmin)





