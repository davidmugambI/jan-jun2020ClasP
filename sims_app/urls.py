from django.urls import path
from sims_app import views

urlpatterns = [
    path('dashboard',views.dashboardView,name="dashboard"),
    path('courses/',views.coursesView,name="courses"),
    path('student/',views.studentsView,name='students'),
    path('applications/',views.ApplicationsView,name='applications'),
    path('createcourse/',views.createCourse,name='createcourse'),
    path('course/update/<int:course_id>',views.updateCourseView,name='update-course'),
    path('course/delete/<int:course_id>',views.deleteCourseView,name='delete-course'),
    path('student/add/',views.addStudentView,name='add-student'),
    path('student/update/<int:student_id>',views.updateStudentView,name='update-student'),
    path('student/delete/<int:student_id>',views.deleteStudentView,name='delete-student'),



    ###### FRONTEND URLS
    path('',views.homePageView,name='home'),
    path('view/',views.displayCoursesView,name='view'),
    path('student/login',views.studentLoginView,name='student-login'),
    path('student/apply/<int:course_id>',views.applyView,name='apply'),
    path('student/mycourses',views.mycourView,name='mycourses'),
    path('student/logout',views.studentlogoutView,name='student-logout'),

    ### Admin authentication
    path('admin/login',views.admin_login,name='admin-login'),
    path('admin/logout',views.admin_logout,name='admin-logout'),
]

'''
for iterationVariable in iterable:
    print(iterationVariable)
    
writing any login in templates

use {% logic %}  - for loops, if statement

Writing variables
{{ variable name }}
    
    
'''