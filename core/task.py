# tasks.py

import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User




def send_enrollment_email(user, course_title, email, community_link):

    try:
        email_body = render_to_string('enrolled_course_notification.html', {
            'user': user,
            'course_title': course_title,
            'community_link': community_link
        })

        plain_text = strip_tags(email_body)

        email_message = EmailMultiAlternatives(
            subject=f'Enrollment Confirmation for {course_title}',
            body=plain_text,
            from_email='Pylearn Hub Team',
            to=[email]
        )

        email_message.attach_alternative(email_body, 'text/html')
        email_message.send()

    except Exception as e:
        pass



def task_submission_email(user, course_title,   email, community_link):

    try:
        email_body = render_to_string('task_submission_notification.html', {
            'user': user,
            'course_title': course_title,
            'community_link': community_link
        })

        plain_text = strip_tags(email_body)

        email_message = EmailMultiAlternatives(
            subject=f'Task Submission for {course_title}',
            body=plain_text,
            from_email='Pylearn Hub Team',
            to=[email]
        )

        email_message.attach_alternative(email_body, 'text/html')
        email_message.send()

    except Exception as e:
       print(e)

def task_notifiy_admin(user, course_task_file, course_task_read, course_title, time):
    superuser_emails = User.objects.filter(is_superuser=True).values_list('email', flat=True)
    if superuser_emails:
       admin_email= EmailMessage(
            f'New Task Submission from  {user.username}',
            f'A username:{user.username}  has submitted a task for {course_title} at {time} UTC\nkindly review the task as soon as possible',
            'PYLEARN HUB TEAM',
            list(superuser_emails),


        )
       admin_email.attach(course_task_file.name, course_task_read, course_task_file.content_type)

       admin_email.send()

def task_completions_email(user, course_title,   email, community_link):

    try:
        email_body = render_to_string('task_completion_notification.html', {
            'user': user,
            'course_title': course_title,
            'community_link': community_link
        })

        plain_text = strip_tags(email_body)

        email_message = EmailMultiAlternatives(
            subject=f'Course Completion for {course_title}',
            body=plain_text,
            from_email='Pylearn Hub Team',
            to=[email]
        )

        email_message.attach_alternative(email_body, 'text/html')
        email_message.send()

    except Exception as e:
       print(e)

def admin_post_notify_user_email(username, description,   email, post_link ):

    try:
        email_body = render_to_string('admin_post_notification_email.html', {
            'username': username,
            'description': description,
            'post_link':post_link
        })

        plain_text = strip_tags(email_body)

        email_message = EmailMultiAlternatives(
            subject=f'Check Out the Latest Post by Our Admin on Pylearn HUB Community!',
            body=plain_text,
            from_email='Pylearn Hub Team',
            to=[email]
        )

        email_message.attach_alternative(email_body, 'text/html')
        email_message.send()

    except Exception as e:
       print(e)

def weekly_task_completions_email(user,  email, community_link):

    try:
        email_body = render_to_string('weekly_task_submission.html', {
            'user': user,

            'community_link': community_link
        })

        plain_text = strip_tags(email_body)

        email_message = EmailMultiAlternatives(
            subject=f'Weekly Task Completion',
            body=plain_text,
            from_email='Pylearn Hub Team',
            to=[email]
        )

        email_message.attach_alternative(email_body, 'text/html')
        email_message.send()

    except Exception as e:
       print(e)

def weekly_task_notifiy_admin(user, course_task_file, course_task_read, time):
    superuser_emails = User.objects.filter(is_superuser=True).values_list('email', flat=True)
    if superuser_emails:
       admin_email= EmailMessage(
            f'weekly Task Submission from  {user.username}',
            f'A username:{user.username}  has submitted a weekly task  at {time} UTC\nkindly review the task as soon as possible',
            'LEARNHUB TEAM',
            list(superuser_emails),


        )
       admin_email.attach(course_task_file.name, course_task_read, course_task_file.content_type)

       admin_email.send()

