from django.shortcuts import render, redirect
from django.http import HttpResponse
from sims_app.models import Course,Student,Application
from datetime import date
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def dashboardView(request):
    no_of_stud = Student.objects.all().count()
    no_of_courses = Course.objects.all().count()
    no_of_applications = Application.objects.all().count()
    dict = {'c_stud': no_of_stud,'c_course': no_of_courses,'c_apps':no_of_applications}
    return render(request, 'sims_app/dashboard.html',dict)

############# COURSES SECTION ###########################
@login_required
def coursesView(request):
    courses = Course.objects.all() # get all the courses
    dict = {'courses':courses}
    return render(request, 'sims_app/courses.html',dict)

@login_required
def createCourse(request):
    if request.method == 'POST':
        # check if data is not empty
        if (request.POST.get('Course_Name') and
                request.POST.get('Course_Duration') and
                request.POST.get('Course_Fee')):
            # if not empty grab the data
            courseName = request.POST.get('Course_Name')
            courseDuration = request.POST.get('Course_Duration')
            CourseFee = request.POST.get('Course_Fee')

            # bind the data with the Model/Table
            course_instance = Course()  # instance or object of the Course Model/Table
            course_instance.Course_Name = courseName
            course_instance.Course_Duration = courseDuration
            course_instance.Course_Fee = CourseFee
            # save the data
            course_instance.save()
            messages.success(request,'Course added')
            return redirect('courses')
        else:
            messages.error(request,"Errol! All fields are required")
            return redirect('courses')
    else:
        return redirect('courses')

@login_required
def updateCourseView(request,course_id):
    if request.method == "POST":
        # check if all fields have data
        if (request.POST.get('Course_Name') and
            request.POST.get('Course_Duration') and
            request.POST.get('Course_Fee')):
            # update
            Course.objects.filter(id=course_id).update(
                Course_Name=request.POST.get('Course_Name'),
                Course_Duration = request.POST.get('Course_Duration'),
                Course_Fee = request.POST.get('Course_Fee')
            )
            messages.success(request,"Message added successfully")
            return redirect('courses')
        else:
            messages.error(request,"Error updating the course")
            return redirect('courses')
    else:
         redirect('courses')

@login_required
def deleteCourseView(request,course_id):
    if request.method == "POST":
        Course.objects.filter(id=course_id).delete()
        # message here
        messages.warning(request,"Course deleted")
        return redirect('courses')
    else:
        return redirect('courses')

####### END COURSE SECTION ##########

@login_required
def studentsView(request):
    students = Student.objects.all() # SELECT * FROM Student
    dict = {'students':students}
    return render(request, 'sims_app/student.html',dict)

@login_required
def addStudentView(request):
    if request.method == 'POST':
        # check if any if the fields is empty
        if (request.POST.get('First_Name') and
            request.POST.get('Last_Name') and
            request.POST.get('Surname') and
            request.POST.get('Email') and
            request.POST.get('Phone_Number')
        ):
            fname = request.POST.get('First_Name')
            lname = request.POST.get('Last_Name')
            surname = request.POST.get('Surname')
            email = request.POST.get('Email')
            phone = request.POST.get('Phone_Number')

            # GENERATE STUDENT REGISTRATION NO # ZAL/2020/1
            year = date.today().year

            # check id of the last student to be added
            lastStudent = Student.objects.last() # get the last item in student table
            # check if last student was found
            if lastStudent:
                NewStudentId = lastStudent.id + 1
            else:
                NewStudentId = 1

            # REG NO
            regno = "ZAL/" + str(year) + '/' + str(NewStudentId)

            # create instance of Student model/table
            try:
                student = Student()
                student.Reg_No = regno
                student.First_Name = fname
                student.Last_Name = lname
                student.Surname = surname
                student.Email = email
                student.Phone_Number = phone
                student.save()
                messages.success(request,"Student Added")
                return redirect('students')
            except Exception:
                messages.error(request,f"Failed to add student")
                return redirect('students')
        else:
            # message here
            pass
    else:
        return redirect('students')

@login_required
def updateStudentView(request,student_id):
    if request.method == 'POST':
        # check if any if the fields is empty
        if (request.POST.get('First_Name') and
                request.POST.get('Last_Name') and
                request.POST.get('Surname') and
                request.POST.get('Email') and
                request.POST.get('Phone_Number')
        ):
            Student.objects.filter(id=student_id).update(
                First_Name=request.POST.get('First_Name'),
                Last_Name=request.POST.get('Last_Name') ,
                Surname = request.POST.get('Surname') ,
                Email=request.POST.get('Email') ,
                Phone_Number=request.POST.get('Phone_Number')
            )
            messages.success(request,"Student Updated")
            return redirect('students')
        else:
            messages.error(request,"Error Updating student")
            return redirect('students')
    else:
        return redirect('students')


@login_required
def deleteStudentView(request,student_id):
    if request.method == "POST":
        Student.objects.filter(id=student_id).delete()
        # message here
        messages.warning(request,"Course deleted")
        return redirect('students')
    else:
        return redirect('students')

@login_required
def ApplicationsView(request):
    applications = Application.objects.all()
    dict = {'applications': applications}
    return render(request, 'sims_app/application.html',dict)



################# FRONTEND #####################

def homePageView(request):
    return render(request, 'frontend/home.html')

def displayCoursesView(request):
    courses_list = Course.objects.all()

    ## Pagination
    paginator = Paginator(courses_list,3)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    dict = {'courses': courses}
    return render(request,'frontend/viewcourses.html',dict)

## student custom login

def studentLoginView(request):
    if request.method == 'POST':
        regno = request.POST['reg_no']
        phone_no = request.POST['phone_no']
        # find if student with above info exist in the db
        student_exist = Student.objects.filter(Reg_No=regno,Phone_Number=phone_no)
        if student_exist:
            # create session for the student
            request.session['registration'] = regno
            request.session['phone'] = phone_no
            messages.success(request,"Authenticated successfully")
            return redirect('view')
        else:
            messages.error(request,"Invalid Login")
            return render(request,'frontend/login.html')
            # return HttpResponse("Failed")
    else:
        return render(request, 'frontend/login.html')

def applyView(request,course_id):
    # check if student has been authenticated
    if request.session.has_key('registration') and request.session.has_key('phone'):
        getstudent = Student.objects.get(Reg_No=request.session['registration'])
        # check if student is already enrolled to this course
        IsEnrolledToThiscourse = Application.objects.filter(course=course_id,student=getstudent.id)
        if IsEnrolledToThiscourse:
            messages.error(request, "You are already enrolled to this course")
            return redirect('mycourses')
        else:
            newApplication = Application()
            newApplication.course_id = course_id
            newApplication.student_id = getstudent.id
            newApplication.save()
            messages.success(request,"Successfully enrolled to this course")
            return redirect('mycourses')
    else:
        return redirect('student-login')

def mycourView(request):
    if request.session.has_key('registration') and request.session.has_key('phone'):
        getstudent = Student.objects.get(Reg_No=request.session['registration'])
        mycourses = Application.objects.filter(student=getstudent.id)
        dict = {'mycourses': mycourses}
        return render(request,'frontend/mycourses.html', dict)
    else:
        return redirect('student-login')

def studentlogoutView(request):
    try:
        del request.session['registration']
        del request.session['phone']
        return redirect('student-login')
    except:
        pass
    return render(request, 'frontend/login.html')


#### Admin authicatication #####
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                messages.success(request, "Logged In")
                return redirect('dashboard')
            else:
                messages.warning(request,"Your account has been deactivated")
                return render(request,'registration/adminlogin.html')

        else:
            messages.error(request,"Invalid login credentials")
            return render(request,"registration/adminlogin.html")
    else:
        return render(request,"registration/adminlogin.html")

def admin_logout(request):
    logout(request)
    messages.warning(request,"logged out")
    return redirect('admin-login')