from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Fee, Payment
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from school_clearance.settings import BASE_DIR




# Admin Panel Views
@login_required(login_url='admin_login')
@staff_member_required
def admin_panel(request):
    students = Student.objects.filter(is_staff=0)
    cleared_students = len(Student.objects.filter(status=True))
    return render(request, 'admin_panel.html', {'total_students': len(students), 'cleared':cleared_students})

@login_required(login_url='admin_login')
@staff_member_required
def status(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        student = Student.objects.get(id=student_id)
        department_fee =  Fee.objects.filter(department=student.department).first().amount
        total_fee_paid = student.total_fee_paid
        if total_fee_paid == department_fee:
            student.status=True
            student.save()
            messages.error(request, 'Student approved successfully')
            return redirect('student_record')
        else:
            messages.error(request, 'The student has not made complete payment')
            return redirect('student_record')





@login_required(login_url='admin_login')
@staff_member_required
def add_fee(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        session = request.POST['session']
        faculty = request.POST['faculty']
        department = request.POST['department']
        fee = Fee(amount=amount, session=session, department=department, faculty=faculty)
        fee.save()
        messages.error(request, 'Fee added successfully')
        return redirect('add_fee')
    fees = Fee.objects.all()
    return render(request, 'add_fee.html', {'fees':fees})
    
@login_required(login_url='admin_login')
@staff_member_required
def register_student(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        mat_num = request.POST.get('matric_number')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        session = request.POST.get('session')
        dept = request.POST.get('department')
        faculty = request.POST.get('faculty')
        student = Student(first_name=fname, last_name=lname, matric_number=mat_num , email=email, phone=phone, session=session, department=dept, faculty=faculty, username=mat_num, password=lname)
        student.set_password(lname.lower())
        student.save()
        messages.error(request, 'Added new student successfully')
        return redirect('admin_panel')
    return render(request, 'register_student.html')

@login_required(login_url='admin_login')
@staff_member_required
def student_record(request):
    students = Student.objects.filter(is_staff=0)
    return render(request, 'student_record.html', {'students':students, 'Payment':Payment})

def admin_login(request):
    print(BASE_DIR)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            print('welcome')
            return redirect('admin_panel') 
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('admin_login')

    else:
        return render(request, 'admin_login.html')

def logout_view(request):
    logout(request)
    return redirect('admin_login')




# Student-Side Views
@login_required(login_url='student_login')
def student_dashboard(request, student_id):
    user = Student.objects.get(id=student_id)
    department_fee =  Fee.objects.filter(department=user.department).first().amount
    payments = Payment.objects.filter(student=user)
    total_payments = sum([payment.amount for payment in payments])
    outstanding_fee = department_fee - total_payments
    user.total_fee_paid = total_payments
    user.save()
    return render(request, 'student_dashboard.html', {'student':user, 'total_fee':department_fee, 'amount_paid':total_payments, 'outstanding':outstanding_fee})

@login_required(login_url='student_login')
def payment_history(request):
    payments = Payment.objects.all()
    return render(request, 'payment_history.html', {'payments':payments})


@login_required(login_url='student_login')
def payment(request, student_id):
    user = Student.objects.get(id=student_id)
    if request.method == 'POST':
        amount = request.POST['amount']
        student = Student.objects.get(id=student_id)
        payment = Payment.objects.create(student=student, amount=amount)
        messages.error(request, 'Payment Successful')
        return redirect('student_dashboard', student_id=student_id)
    return render(request, 'payment.html', {'student':user})

@login_required(login_url='student_login')
def student_payment_history(request, student_id):
    user = Student.objects.get(id=student_id)
    payments = Payment.objects.filter(student=user)
    return render(request, 'student_payment_history.html', {'payments':payments, 'student':user})

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username , password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('welcome')
            return redirect('student_dashboard', student_id=user.id) 
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('student_login')

    else:
        return render(request, 'student_login.html')

def std_logout(request):
    logout(request)
    return redirect('student_login')