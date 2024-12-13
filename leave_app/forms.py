from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, LeaveApplication

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['leave_text']
        widgets = {
            'leave_text': forms.Textarea(attrs={'placeholder': 'Enter leave reason here...', 'rows': 4}),
        }








from django import forms
from .models import StudentInfo

class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = [
            'photo', 'rank', 'name', 'dob', 'father_name', 'mother_name', 
            'aadhar_no', 'pan_no', 'driving_license', 'register_no',
            'campus', 'school_name', 'course'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }






from django import forms
from .models import MarkAttendance

class MarkAttendanceForm(forms.ModelForm):
    class Meta:
        model = MarkAttendance
        fields = ['one_o', 'one_s', 'two_o', 'two_s', 'three_o', 'three_s', 'nov_1', 'nov_2', 'nov_3', 'nov_4']
