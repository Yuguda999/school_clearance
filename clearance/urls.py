from django.urls import path
from . import views

urlpatterns = [
    # Admin Panel URLs
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('fee/', views.add_fee, name='add_fee'),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('student-record/',views.student_record, name='student_record'),
    path('register-student/',views.register_student, name='register_student'),
    path('admin-login/',views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('status/', views.status, name='status'),

    # Student Panel URLs
    path('student-dashboard/<uuid:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('student-login/',views.student_login, name='student_login'),
    path('payment/<uuid:student_id>/',views.payment, name='payment'),
    path('student-payment-history/<uuid:student_id>/',views.student_payment_history, name='student_payment_history'),
    path('std-logout/', views.std_logout, name='std_logout'),

    ]
