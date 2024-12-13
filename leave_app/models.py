from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('cdt', 'Cadet'),
        ('lcpl', 'Lance Corporal'),
        ('cpl', 'Corporal'),
        ('sgt', 'Sergeant'),
        ('cqms', 'Company Quartermaster Sergeant'),
        ('csm', 'Company Sergeant Major'),
        ('juo', 'Junior Under Officer'),
        ('suo', 'Senior Under Officer'),
        ('ano', 'Assistant National Officer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cdt')

from django.utils import timezone

class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leaves')
    leave_text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_on = models.DateTimeField(auto_now_add=True)
    current_holder = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='holding_leaves')
    forwarded_on = models.DateTimeField(null=True, blank=True)
    approved_or_rejected_on = models.DateTimeField(null=True, blank=True)
    decision_reason = models.TextField(null=True, blank=True)  # Reason for approval/rejection/forwarding
    approved_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves',
        help_text="The user who approved the leave"
    )

    def __str__(self):
        return f"{self.applicant.username} - {self.status}"

    def forward_to_next_rank(self):
        """Forward the leave to the next higher rank."""
        if not self.current_holder:
            raise ValueError("The current holder of the leave is not set.")
        
        role_hierarchy = [ 'lcpl', 'cpl', 'sgt', 'cqms', 'csm', 'juo', 'suo', 'ano']
        
        try:
            current_index = role_hierarchy.index(self.current_holder.role)
        except ValueError:
            raise ValueError("Current holder's role is not valid.")
        
        # Get all users who are at a higher rank than the current holder
        next_rank_users = CustomUser.objects.filter(role__in=role_hierarchy[current_index + 1:])

        if next_rank_users.exists():
            # Set the current holder to the next available user
            self.current_holder = next_rank_users.first()
            self.forwarded_on = timezone.now()  # Record when it was forwarded
            self.status = 'Pending'  # Status is still pending as it is waiting approval from the next rank
            self.save()
        else:
            # If no higher rank user is available, leave is still in pending status
            self.status = 'Pending'
            self.save()











from django.db import models
from django.core.exceptions import ValidationError

# Custom validator for Aadhar number
def validate_aadhar_no(value):
    if len(value) != 12 or not value.isdigit():
        raise ValidationError("Aadhar number must be 12 digits.")

# Student Info Model
class StudentInfo(models.Model):
    RANK_CHOICES = [
        ('cdt', 'Cadet'),
        ('lcpl', 'Lance Corporal'),
        ('cpl', 'Corporal'),
        ('sgt', 'Sergeant'),
        ('cqms', 'Company Quartermaster Sergeant'),
        ('csm', 'Company Sergeant Major'),
        ('juo', 'Junior Under Officer'),
        ('suo', 'Senior Under Officer'),
        ('ano', 'Assistant National Officer'),
    ]
    
    # Fields
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    rank = models.CharField(max_length=10, choices=RANK_CHOICES)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    aadhar_no = models.CharField(max_length=12, unique=True, validators=[validate_aadhar_no])
    pan_no = models.CharField(max_length=10, blank=True, null=True)
    driving_license = models.CharField(max_length=20, blank=True, null=True)
    register_no = models.CharField(max_length=20, unique=True)
    campus = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)

    # Timestamps for record creation and modification
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # String representation of the object
    def __str__(self):
        return self.name
    
    # Meta class for human-readable model name
    class Meta:
        verbose_name = "Student Info"
        verbose_name_plural = "Student Infos"

























from django.db import models

# Choices for attendance
ATTENDANCE_CHOICES = [
    ('Present', 'Present'),
    ('Absent', 'Absent'),
    ('Holiday', 'Holiday'),
]

# Base model with percentage calculation logic to avoid repetition
class AttendanceBase(models.Model):
    student = models.CharField(max_length=100)
    nov_1 = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='Holiday')
    nov_2 = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='Holiday')
    nov_3 = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='Holiday')
    nov_4 = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='Holiday')
    percentage = models.FloatField(default=0.0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Count 'Present' and 'Absent' entries
        attendance_days = [self.nov_1, self.nov_2, self.nov_3, self.nov_4]
        present_count = attendance_days.count('Present')
        absent_count = attendance_days.count('Absent')
        total_days = present_count + absent_count
        # Calculate percentage
        self.percentage = (present_count / total_days * 100) if total_days > 0 else 0
        super().save(*args, **kwargs)

# Specific models for each table
class OneO(AttendanceBase):
    pass

class OneS(AttendanceBase):
    pass

class TwoO(AttendanceBase):
    pass

class TwoS(AttendanceBase):
    pass

class ThreeO(AttendanceBase):
    pass

class ThreeS(AttendanceBase):
    pass
class MarkAttendance(models.Model):
    # Define relationships to existing models
    one_o = models.ForeignKey(OneO, null=True, blank=True, on_delete=models.SET_NULL)
    one_s = models.ForeignKey(OneS, null=True, blank=True, on_delete=models.SET_NULL)
    two_o = models.ForeignKey(TwoO, null=True, blank=True, on_delete=models.SET_NULL)
    two_s = models.ForeignKey(TwoS, null=True, blank=True, on_delete=models.SET_NULL)
    three_o = models.ForeignKey(ThreeO, null=True, blank=True, on_delete=models.SET_NULL)
    three_s = models.ForeignKey(ThreeS, null=True, blank=True, on_delete=models.SET_NULL)

    # Attendance fields for the days
    nov_1 = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Holiday', 'Holiday')], default='Holiday')
    nov_2 = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Holiday', 'Holiday')], default='Holiday')
    nov_3 = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Holiday', 'Holiday')], default='Holiday')
    nov_4 = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Holiday', 'Holiday')], default='Holiday')

    class Meta:
        verbose_name = "Mark Attendance"
        verbose_name_plural = "Mark Attendance"

    def __str__(self):
        return f"Attendance for {self.one_o or self.one_s or self.two_o or self.two_s or self.three_o or self.three_s}"