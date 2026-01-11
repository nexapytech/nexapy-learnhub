import threading

from django.contrib import admin
from .models import Profile, Email_Verification,Notification,UserSession, Post, PostFileGroup, Like_Post, Comment, Course_Enrollment, Task_Submission
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .task import task_completions_email
admin.site.site_header = "PYLEARN HUB ADMIN"
admin.site.site_title = "PYLEARN HUB CONTROL PANEL"
admin.site.index_title = "Welcome to the Admin Interface"


# Custom Action: Block Users
def block_users(modeladmin, request, queryset):
    queryset.update(is_active=False)  # Deactivate selected users
    modeladmin.message_user(request, "Selected users have been blocked.")

# Custom Action: Unblock Users
def unblock_users(modeladmin, request, queryset):
    queryset.update(is_active=True)  # Activate selected users
    modeladmin.message_user(request, "Selected users have been unblocked.")
def is_course_completed(modeladmin, request, queryset):

        queryset.update(is_course_completed=True)  # Activate selected users
        modeladmin.message_user(request, "Selected users have course as been  tick completed.")
        # List to track which enrollments are updated
        updated_users = []

        for Course_Enrollment in queryset:
            # Update the enrollment to mark it as completed
            if  Course_Enrollment.is_course_completed:

                updated_users.append((Course_Enrollment.user.username, Course_Enrollment.user.email, Course_Enrollment.course))  # Collect user emails

        if updated_users:
            # Send email to each updated user
            def send_email():

                for user, email , course in updated_users:
                    task_completions_email(user=user,course_title=course, email=email, community_link='https://chat.whatsapp.com/JQAG5DZUC98DxT3ZKy5gCo')

                modeladmin.message_user(request, f"Selected users have been marked as completed and notified by email.",
                                        level='success')
            threading.Thread(target=send_email).start()
        else:
            modeladmin.message_user(request, "No updates made. No users were marked as completed.", level='warning')


is_course_completed.short_description = "Mark selected courses as completed and notify users"


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    actions = [block_users, unblock_users]  # Add custom actions

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Email_Verification)
admin.site.register(Notification)
admin.site.register(UserSession)
admin.site.register(Post)
admin.site.register(PostFileGroup)
admin.site.register(Like_Post)
admin.site.register(Comment)


@admin.register(Course_Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_course_enrolled', 'is_course_review','is_course_completed')
    actions = [is_course_completed]  # Add custom actions

admin.site.register(Task_Submission)



