from django.urls import path

from query import views
 
urlpatterns = [
    path('hello/', views.hello),
    path('hello/xiaoming',views.hello_xiaoming),
    path('hello/xiaohong',views.hello_xiaohong),
    path('pid/<str:pid>',views.query_patient_by_id),
    path('query_patient/',views.query_patient),
    path('patient_filter/',views.patient_filter),
    path('ill_doctor_filter/',views.ill_doctor_filter),
    path('anatomy_doctor_filter/',views.anatomy_doctor_filter),
    path('ill_gender_hospital_filter_exam/',views.ill_gender_hospital_filter_exam),
    path('bootstrap_demo/',views.bootstrap_demo),
    path('cosmo/',views.cosmo),
    path('normalentry/',views.normalentry),
    path('administratorlogin/',views.administratorlogin),
    path('nologinquery/',views.nologinquery),
    path('normalquery/',views.normalquery),
    path('adminquery/',views.adminquery),
    path('pagination/',views.pagination),
    path('admin_delete/',views.admin_delete),
    path('admin_update/',views.admin_update),
    path('admin_insert/',views.admin_insert),
    path('normalregister/',views.normalregister),
    path('administratorregister/',views.administratorregister),
]