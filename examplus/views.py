from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse 
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .forms import *

# Create your views here.

#This function loads the about page
def about(request):
    return render(request, 'examplus/about.html')


#This function authenticates and authorises the user
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            if request.user.groups.filter(name='Candidate').exists():
                return HttpResponseRedirect(reverse('examplus:candidate/dashboard'))
            elif request.user.groups.filter(name='Invigilator').exists():
                return HttpResponseRedirect(reverse('examplus:invigilator/dashboard'))
            elif request.user.groups.filter(name='HOD').exists():
                return HttpResponseRedirect(reverse('examplus:hod/dashboard'))
            elif request.user.groups.filter(name='Examiner').exists():
                return HttpResponseRedirect(reverse('examplus:examiner/dashboard'))
        else:
            return render(request, 'examplus/login.html', {
                'message':' Invalid credentials'
            })
    return render(request, 'examplus/login.html')


#This function loads the candidate dashboard
def candidate_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('examplus:login'))
    
    if not request.user.groups.filter(name='Candidate').exists():
        return HttpResponseRedirect(reverse('examplus:login'))

    user = request.user
    current_date = timezone.now().date()
    candidate = Candidate.objects.get(user=user)
    courses = candidate.course.filter(date=current_date)
    upcoming_courses = candidate.course.filter(date__gt=current_date)


    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.instance.department = candidate.department
            form.instance.programme = candidate.programme
            form.instance.faculty = candidate.faculty
            form.save()
            return HttpResponseRedirect(reverse('examplus:candidate/dashboard'))
        else:
            return render(request, 'examplus/candidate.html', {
                'candidate_form':form
            })

    return render(request, 'examplus/candidate.html', {
        'courses': courses,
        'upcoming_courses': upcoming_courses,
        'candidate_form': CandidateForm(instance=candidate)
    })
    

#This function loads the Invigilator dashboard
def invigilator_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('examplus:login'))
    
    if not request.user.groups.filter(name='Invigilator').exists():
        return HttpResponseRedirect(reverse('examplus:login'))

    user = request.user
    invigilator = Invigilator.objects.get(user=user)

    courses_at_venue = Course.objects.filter(venue=invigilator.assigned_hall)

    # Get candidates associated with those courses
    candidates = Candidate.objects.filter(course__in=courses_at_venue)
   
    if request.method == 'POST':
        form = MalpracticeForm(request.POST, request.FILES, invigilator=invigilator)
        if form.is_valid():
            form.instance.handled_by = user
            form.instance.report_date_time = timezone.now()
            form.save()
            return HttpResponseRedirect(reverse('examplus:invigilator/dashboard'))
        else:
            return render(request, 'examplus/invigilator.html', {
                'malpractice_form':form
            })
    
    return render(request, 'examplus/invigilator.html', {
        'invigilator': invigilator,
        'candidates': candidates,
        'malpractice_form': MalpracticeForm(invigilator=invigilator)
    })


#This function loads the HOD dashboard
def department_head_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('examplus:login'))
    
    if not request.user.groups.filter(name='HOD').exists():
        return HttpResponseRedirect(reverse('examplus:login'))

    
    user = request.user
    department_head = DepartmentHead.objects.get(user=user)

    # Get candidates associated with this departments
    active_candidates = Candidate.objects.filter(department=department_head.department)
    reported_candidates = MalpracticeReport.objects.filter(candidate__department=department_head.department)

    return render(request, 'examplus/hod.html', {
        'active_candidates': active_candidates,
        'malpractice_report': reported_candidates
    })


# This function loads the Faculty Examiner dashboard
def faculty_examiner_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('examplus:login'))
    
    if not request.user.groups.filter(name='Examiner').exists():
        return HttpResponseRedirect(reverse('examplus:login'))

    user = request.user
    faculty_examiner = FacultyExaminer.objects.get(user=user)
    faculty_name = faculty_examiner.faculty

    # Candidates associated with his faculty
    candidates = Candidate.objects.filter(faculty=faculty_name)
    reported_candidates = MalpracticeReport.objects.filter(candidate__faculty=faculty_examiner.faculty)
    invigilators = Invigilator.objects.filter(faculty=faculty_examiner.faculty)

    if request.method == 'POST':
        form = InvigilatorForm(data=request.POST, faculty_examiner=faculty_examiner)
        if form.is_valid():
            form.instance.faculty = faculty_examiner.faculty
            form.save()
            return HttpResponseRedirect(reverse('examplus:examiner/dashboard'))
    else:
        form = InvigilatorForm(faculty_examiner=faculty_examiner)

    return render(request, 'examplus/examiner.html', {
        'active_candidates': candidates,
        'malpractice_report': reported_candidates,
        'invigilators': invigilators,
        'invigilator_form': form
    })



def delete_report(request, report_id):
    report = MalpracticeReport.objects.get(pk=report_id)
    report.delete()
    return HttpResponseRedirect(reverse('examplus:examiner/dashboard'))


#This functions clears user sesssion and logs the user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('examplus:login'))

