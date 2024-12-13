from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import LeaveApplicationForm
from .models import LeaveApplication, CustomUser
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import LeaveApplication



@login_required
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard/')
        else:
            return render(request, 'leave_app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'leave_app/login.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    print(request.user.is_authenticated)  # Check if the user is authenticated
    return render(request, 'leave_app/dashboard.html')

@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.applicant = request.user

            # Determine the next higher rank to forward the leave
            role_hierarchy = ['cdt', 'lcpl', 'cpl', 'sgt', 'cqms', 'csm', 'juo', 'suo', 'ano']

            # Find the current rank of the applicant
            try:
                current_index = role_hierarchy.index(request.user.role)
            except ValueError:
                raise ValueError("The applicant's role is not valid.")
            
            # Get all users who are at a higher rank than the current holder
            next_rank_users = CustomUser.objects.filter(role__in=role_hierarchy[current_index + 1:])
            
            if next_rank_users.exists():
                # Set the current holder to the next available user (the first one)
                leave.current_holder = next_rank_users.first()  # Forward leave to the next rank
                leave.status = 'Pending'  # Set status to 'Pending' as it is awaiting approval
                leave.forwarded_on = timezone.now()  # Record when it was forwarded
            else:
                # If no higher rank user is available, the leave remains in pending status
                leave.status = 'REAPPly'

            leave.save()
            return redirect('leave_status')  # Redirect to leave status page
    else:
        form = LeaveApplicationForm()

    return render(request, 'leave_app/apply_leave.html', {'form': form})


@login_required
def leave_requests(request):
    # Fetch leave requests assigned to the currently logged-in user
    requests = LeaveApplication.objects.filter(current_holder=request.user, status='Pending')
    user = request.user

    # Get the leave requests based on user's role
   
    return render(request, 'leave_app/leave_requests.html', {'requests': requests})
    



@login_required
def process_leave(request, leave_id, action):
    leave = get_object_or_404(LeaveApplication, id=leave_id)

    if leave.current_holder != request.user:
        return redirect('leave_requests')  # Prevent unauthorized access to process leave requests

    if request.method == 'POST':
        reason = request.POST.get('reason', '')

        if action == 'approve':
            leave.status = 'Approved'
            leave.decision_reason = reason
            leave.approved_or_rejected_on = timezone.now()
        elif action == 'reject':
            leave.status = 'Rejected'
            leave.decision_reason = reason
            leave.approved_or_rejected_on = timezone.now()
        elif action == 'forward':
            leave.decision_reason = reason  # Reason is optional for forward
            leave.forward_to_next_rank()  # This will call the correct method
            # Adding success message after forwarding the leave
            messages.success(request, "Leave has been forwarded to the next rank successfully!")
        
        leave.save()
        return redirect('dashboard')  # Redirecting to the dashboard

    return render(request, 'leave_app/process_leave.html', {'leave': leave, 'action': action})

@login_required
def leave_status(request):
    # Show the leave status for the logged-in user
    leaves = LeaveApplication.objects.filter(applicant=request.user).order_by('-submitted_on')
    return render(request, 'leave_app/leave_status.html', {'leaves': leaves})


def user_logout(request):
    logout(request)
    return redirect('login')















from django.shortcuts import render, redirect
from .forms import StudentInfoForm
from django.contrib import messages
@login_required
def student_info_view(request):
    if request.method == 'POST':
        form = StudentInfoForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()  # Save form data
            messages.success(request, "Student information saved successfully!")
            return redirect('student_info')  # Redirect after successful save
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentInfoForm()  # Display empty form for GET request

    return render(request, 'leave_app/student_info.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentInfoForm
@login_required
def add_student_info(request):
    if request.method == 'POST':
        form = StudentInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Student information saved successfully!")
            return redirect('display_student_info')  # Redirect after saving
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentInfoForm()

    return render(request, 'leave_app/student_info.html', {'form': form})




from django.shortcuts import render
from .models import StudentInfo
@login_required
def display_student_info(request):
    # Fetch all student records
    students = StudentInfo.objects.all()

    return render(request, 'leave_app/display_student_info.html', {'students': students})





from django.shortcuts import render, redirect
from .models import OneO, OneS, TwoO, TwoS, ThreeO, ThreeS  # Import your models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages
from django.shortcuts import redirect

@login_required
def mark_attendance_view(request):
    # Check if the user has the required role to access the view
    if request.user.role not in ['juo', 'suo', 'ano']:
        messages.error(request, "You do not have permission to mark attendance.")
        return redirect('dashboard')  # Redirect to a safe page, such as the home page

    if request.method == 'POST':
        # Step 1: Handle the table selection
        if 'table_name' in request.POST:
            table_name = request.POST.get('table_name')
            # Save the table name in the session
            request.session['table_name'] = table_name
            
            # Fetch records based on the selected table
            if table_name == 'OneS':
                records = OneS.objects.all()
            elif table_name == 'OneO':
                records = OneO.objects.all()
            elif table_name == 'TwoS':
                records = TwoS.objects.all()
            elif table_name == 'TwoO':
                records = TwoO.objects.all()
            elif table_name == 'ThreeS':
                records = ThreeS.objects.all()
            elif table_name == 'ThreeO':
                records = ThreeO.objects.all()
            else:
                records = []

            # List of columns to select from
            columns = ['nov_1', 'nov_2', 'nov_3', 'nov_4']

            return render(request, 'leave_app/mark_attendance_step2.html', {
                'records': records,
                'table_name': table_name,
                'columns': columns,
            })

        # Handle attendance submissions (Step 2)
        attendance_data = request.POST.getlist('attendance')
        selected_column = request.POST.get('column_name')  # Get selected column from form

        for record in attendance_data:
            record_id, attendance_value = record.split('-')  # record format: 'id-attendance_value'
            record_id = int(record_id)  # Get the actual ID

            # Update attendance based on the selected table
            table_name = request.session.get('table_name')  # Get the table name from session
            if table_name == 'OneS':
                record = OneS.objects.get(id=record_id)
            elif table_name == 'OneO':
                record = OneO.objects.get(id=record_id)
            elif table_name == 'TwoS':
                record = TwoS.objects.get(id=record_id)
            elif table_name == 'TwoO':
                record = TwoO.objects.get(id=record_id)
            elif table_name == 'ThreeS':
                record = ThreeS.objects.get(id=record_id)
            elif table_name == 'ThreeO':
                record = ThreeO.objects.get(id=record_id)
            else:
                record = None
            
            if record:  # Ensure the record exists
                # Assign attendance value to the selected day
                if selected_column == 'nov_1':
                    record.nov_1 = attendance_value
                elif selected_column == 'nov_2':
                    record.nov_2 = attendance_value
                elif selected_column == 'nov_3':
                    record.nov_3 = attendance_value
                elif selected_column == 'nov_4':
                    record.nov_4 = attendance_value
                
                record.save()  # Save the updated record

        return redirect('success_url')  # Replace with your actual success URL

    # If not a POST request, render the first step
    tables = ['OneO', 'OneS', 'TwoO', 'TwoS', 'ThreeO', 'ThreeS']
    return render(request, 'leave_app/mark_attendance_step1.html', {'tables': tables})

def success_view(request):
    return render(request, 'leave_app/success.html')
@login_required
def view_percentage(request):
    # Ensure only staff users can access the page
    if not request.user.is_staff:
        return redirect('view_percentage_login')  # Redirect to the login page if not staff

    if request.method == 'POST':
        # Get the selected table name
        table_name = request.POST.get('table_name')
        
        # Fetch records based on the selected table
        if table_name == 'OneO':
            records = OneO.objects.all()
        elif table_name == 'OneS':
            records = OneS.objects.all()
        elif table_name == 'TwoO':
            records = TwoO.objects.all()
        elif table_name == 'TwoS':
            records = TwoS.objects.all()
        elif table_name == 'ThreeO':
            records = ThreeO.objects.all()
        elif table_name == 'ThreeS':
            records = ThreeS.objects.all()
        else:
            records = []

        return render(request, 'leave_app/view_percentage.html', {
            'records': records,
            'table_name': table_name,
        })

    # Render the initial selection form for the tables
    tables = ['OneO', 'OneS', 'TwoO', 'TwoS', 'ThreeO', 'ThreeS']
    return render(request, 'leave_app/select_table.html', {'tables': tables})
from django.contrib.auth import authenticate, login

from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # Ensure that only staff users are allowed
                login(request, user)
                return redirect('/mark-attendance/')  # Redirect to the attendance page after login
            else:
                messages.error(request, "You do not have permission to access this site.")
                return redirect('/login/')  # Redirect back to login if user is not staff
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/login/')  # Redirect back to login if authentication fails

    return render(request, 'login.html')  # Render the login page
class StaffLoginView(LoginView):
    template_name = 'leave_app/login.html'  # Specify your login template

    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff:
            return super().form_valid(form)
        else:
            messages.error(self.request, "You do not have permission to access this site.")
            return redirect('login')  # Redirect to login page if user is not staff
        

class ViewPercentageLoginView(LoginView):
    template_name = 'leave_app/view_percentage_login.html'

@login_required
def custom_redirect_view(request):
    if request.user.is_staff:
        return redirect('/view-percentage/')
    else:
        return redirect('/mark-attendance/')
    
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on whether the user is staff or not
            if user.is_staff:
                return redirect('/select-page/')  # Redirect staff to the selection page
            else:
                return redirect('/view-percentage/')  # Non-staff users are redirected directly to view percentage page
    else:
        form = AuthenticationForm()

    return render(request, 'leave_app/login.html', {'form': form})
def select_page(request):
    if request.user.is_staff:
        # Staff users see both options
        return render(request, 'leave_app/select_page.html', {'is_staff': True})
    else:
        # Non-staff users only see the option for view-percentage
        return render(request, 'leave_app/select_page.html', {'is_staff': False})