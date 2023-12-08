from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User



class MalpracticeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        invigilator = kwargs.pop('invigilator', None)
        super(MalpracticeForm, self).__init__(*args, **kwargs)
        
        if invigilator:
            # Filter candidates and courses based on the invigilator's assigned_hall
            self.fields['candidate'].queryset = Candidate.objects.filter(
                course__in=invigilator.assigned_hall.course_set.all()
            )
            self.fields['course'].queryset = Course.objects.filter(
                id__in=self.fields['candidate'].queryset.values_list('course', flat=True).distinct()
            )
            

    class Meta:
        model = MalpracticeReport
        fields = ['candidate', 'course', 'description', 'evidence']



class InvigilatorForm(forms.ModelForm):
    class Meta:
        model = Invigilator
        fields = ['user', 'assigned_hall']
    
    def __init__(self, faculty_examiner, *args, **kwargs):
        examiner_faculty = kwargs.pop('examiner_faculty', None)
        super().__init__(*args, **kwargs)

        # Filter user field based on user groups
        self.fields['user'].queryset = User.objects.filter(groups__name__in=['Invigilator'])

        # Filter assigned_hall field based on the faculty of the signed-in examiner faculty
        self.fields['assigned_hall'].queryset = ExamHall.objects.filter(center__designated_faculty=faculty_examiner.faculty)


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['course']

    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)

        # Filter the course field queryset based on the candidate's level and programme
        if self.instance and self.instance.programme and self.instance.level:
            self.fields['course'].queryset = Course.objects.filter(
                programme=self.instance.programme,
                level=self.instance.level
            )






