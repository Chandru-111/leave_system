from django.contrib import admin
from .models import CustomUser, LeaveApplication

# Custom admin for CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'role')
    ordering = ('role',)

# Custom admin for LeaveApplication
@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'leave_text', 'status', 'submitted_on', 'get_approver')  # Updated list_display
    list_filter = ('status', 'submitted_on')
    search_fields = ('applicant__username', 'leave_text')
    actions = ['approve_leave', 'reject_leave']

    # Method to display the approver (if it exists)
    def get_approver(self, obj):
        return obj.approved_by.username if obj.approved_by else "N/A"
    get_approver.short_description = 'Approved By'

    # Actions to approve or reject leave
    def approve_leave(self, request, queryset):
        queryset.update(status='Approved')
    approve_leave.short_description = "Approve selected leaves"

    def reject_leave(self, request, queryset):
        queryset.update(status='Rejected')
    reject_leave.short_description = "Reject selected leaves"




from django.contrib import admin
from django.utils.html import format_html
from .models import OneO, OneS, TwoO, TwoS, ThreeO, ThreeS
from .models import MarkAttendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('colored_student', 'nov_1', 'nov_2', 'nov_3', 'nov_4', 'colored_percentage')
    list_editable = ('nov_1', 'nov_2', 'nov_3', 'nov_4')

    # Method to display student name with conditional color formatting
    def colored_student(self, obj):
        if obj.percentage < 75:
            color = 'red'
        else:
            color = 'Light blue'
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.student
        )
    
    colored_student.short_description = 'Student'

    # Method to display percentage with conditional color formatting
    def colored_percentage(self, obj):
        if obj.percentage < 75:
            color = 'red'
        else:
            color = 'Light blue'
        formatted_percentage = f"{obj.percentage:.2f}%"
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            formatted_percentage
        )
    
    colored_percentage.short_description = 'Percentage'

from django.contrib import admin
from .models import StudentInfo


class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'dob', 'father_name', 'mother_name', 'register_no', 'campus', 'school_name', 'course')
    readonly_fields = ('name', 'rank', 'dob', 'father_name', 'mother_name', 'register_no', 'campus', 'school_name', 'course')
    search_fields = ('name', 'register_no', 'aadhar_no')
    list_filter = ('rank', 'campus', 'course')

admin.site.register(StudentInfo, StudentInfoAdmin)

admin.site.register(OneO, AttendanceAdmin)
admin.site.register(OneS, AttendanceAdmin)
admin.site.register(TwoO, AttendanceAdmin)
admin.site.register(TwoS, AttendanceAdmin)
admin.site.register(ThreeO, AttendanceAdmin)
admin.site.register(ThreeS, AttendanceAdmin)
admin.site.register(MarkAttendance)