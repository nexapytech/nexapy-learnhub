import os.path
import threading
import uuid

from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes,DjangoUnicodeDecodeError
from .models import Profile, Email_Verification, Notification, Post, PostFileGroup, Like_Post, Comment, Course_Enrollment, Task_Submission
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .utils import generate_token, resend_verfication
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.contrib.auth.models import User
from django_countries import countries
from django.contrib.auth.signals import user_logged_in
from .models import UserSession
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import auth
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
from .task import send_enrollment_email, task_submission_email, task_notifiy_admin, admin_post_notify_user_email, weekly_task_notifiy_admin, weekly_task_completions_email
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
import concurrent.futures
from concurrent.futures import  ThreadPoolExecutor
import random
from django.contrib.sites.models import Site
from django.http import JsonResponse



def serve_validation_file(request):
    validation_content = "8375F54BE9585F6CD339DEB9662EEC87"
    return HttpResponse(validation_content, content_type="text/plain")

def index(request):
    contact_email = "samdeveloper360@gmail.com"
    if request.user.is_authenticated:
        return redirect('/home')

    else:
        context = {
            'contact_email': contact_email
        }
        return render(request,'index.html', context)
@login_required(login_url='signin')
def community_terms_and_conditions(request):
    email_verify = Email_Verification.objects.get(user=request.user)
    if email_verify.is_email_verified:
        user_profile = Profile.objects.get(user=request.user)
        if request.method=="POST":
            agreement = request.POST.get('terms-and-conditions')
            if agreement:
                user_profile.terms_and_condition = True
                user_profile.save()
                return redirect('community')

        else:
            if user_profile.terms_and_condition:
                return redirect('community')
    else:
        return redirect('home')


    return render(request, 'terms.html')



def Courses(request):
    contact_email= "samdeveloper360@gmail.com"
    file_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'course_data.json')
    course_json = open(file_path, 'r')
    data =  json.load(course_json)
    beginner_course_data = data.get("Beginner_Courses")
    intermidiate_course_data = data.get("Intermediate_Courses")
    advanced_course_data = data.get("Advanced_Courses")
    # If the user is logged in, check their enrolled courses
    enrolled_courses = []
    under_review = []
    task_completed =[]
    if request.user.is_authenticated:
        # Get a list of course IDs the user is enrolled in
        enrolled_course = Course_Enrollment.objects.filter(user=request.user, is_course_enrolled=True)
        for course in enrolled_course:

            enrolled_courses.append(str(course.course_id))
            if course.is_course_review:
                under_review.append(str(course.course_id))
            if course.is_course_completed:
                task_completed.append(str(course.course_id))



    context = {
            'contact_email':contact_email,
            'task_completed':task_completed,
            'enrolled_courses':enrolled_courses,
            'under_review': under_review,
            'beginner_courses': beginner_course_data,
            'intermidiate_courses': intermidiate_course_data,
            'advanced_courses': advanced_course_data,






    }
    return render(request,'courses.html', context)

@login_required(login_url='signin')

def Task(request):
     file_path =  os.path.join(settings.BASE_DIR, 'core',  'data', 'course_title.json')
     courses_file_data = open(file_path, 'r')
     courses_data= json.load(courses_file_data)
     courses = courses_data.get('courses',[])
     if request.method =="POST":
         user = request.user
         task_courses = request.POST.get('courses')
         task_file = request.FILES.get('taskFile')
         task_file_read_only = task_file.read()
         task_description = request.POST.get('taskDescription')
         try:
             course_enrollment = Course_Enrollment.objects.get(user=request.user, course=task_courses)
             existing_enrollment = Course_Enrollment.objects.filter(user=request.user, course=task_courses)
             existing_task = Task_Submission.objects.filter(user=request.user, course_title=task_courses).exists()
             if request.user.is_authenticated and existing_enrollment.exists():
                 if existing_task:
                     return JsonResponse(
                         {
                             'tasktaken': f'you have already  submitted your task  for  {task_courses}. Kindly wait for updates from admin'})
                 else:

                        Task_Submission.objects.create(user=request.user, course_title=task_courses,
                                                        description=task_description,
                                                        task_file=task_file)

                        course_enrollment.is_course_review = True
                        course_enrollment.save()
                        # Create and save a notification for the user
                        notification_message = f' hi {user.username} you have successfully submitted your task for {task_courses}. It is under review by  admin kindly check back later for updates'
                        Notification.objects.create(
                         user=user,
                         message=notification_message

                        )

                        # Send email asynchronously
                        def email_task_submittion():
                            task_submission_email(user=user, course_title=task_courses, email=user.email,
                                              community_link='https://chat.whatsapp.com/JQAG5DZUC98DxT3ZKy5gCo')
                            # Notify admin about the task submission and attach the task file
                            task_notifiy_admin(
                                user=user,
                                course_title=task_courses,
                                course_task_read=task_file_read_only,
                                course_task_file=task_file,  # Pass the task file here
                                time=timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                            )



                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            executor.submit(email_task_submittion)


                        return JsonResponse(
                         {
                             'success': f'you have successfully  submitted your task  for  {task_courses}. Kindly wait for updates by our admin '})







         except:
             if task_courses == "WEEKLY TASK":
                 def email_weekly_task_submittion():
                     weekly_task_completions_email(user=user,  email=user.email,
                                           community_link='https://chat.whatsapp.com/JQAG5DZUC98DxT3ZKy5gCo')
                     # Notify admin about the task submission and attach the task file
                     weekly_task_notifiy_admin(
                         user=user,
                         course_task_read=task_file_read_only,
                         course_task_file=task_file,  # Pass the task file here
                         time=timezone.now().strftime('%Y-%m-%d %H:%M:%S')

                     )

                 with ThreadPoolExecutor() as task_thread:
                    task_thread.submit(email_weekly_task_submittion)
                 return JsonResponse(
                   {
                      'success': f'you have successfully  submitted your weekly task, Kindly wait for updates on the group chat from the admin '})

             else:
                 return JsonResponse(
                     {'error': f'something went wrong contact support'})



     context = {
         'courses': courses
     }
     return render(request, 'assesment.html', context)





@login_required(login_url='signin')
def Courses_enrollment(request):
   if request.method=='POST':
        user= request.user
        email_verify = Email_Verification.objects.get(user=user)
        email = user.email
        course_id = str(request.POST.get('course_id'))
        course_title = request.POST.get('courseEnroll')
        course_description = request.POST.get('courseDescription')



        if  user and email_verify.is_email_verified:

            try:
                existing_enrollment = Course_Enrollment.objects.filter(user=user, course=course_title).exists()

                if existing_enrollment:
                    return JsonResponse({ 'enrolled': mark_safe(f'You have already enrolled in the &nbsp<strong>{course_title}</strong>&nbsp course. To re-enroll, please contact support.')})

                else:
                 course_credential =Course_Enrollment.objects.create(user=user, email=email,
                 course=course_title, course_id=course_id,  course_description=course_description, is_course_enrolled=True)
                 course_credential.save()


                 # Send email asynchronously
                 def email_task():
                     # Create and save a notification for the user
                     notification_message = mark_safe(f'You have successfully registered for the &nbsp<strong>{course_title}</strong>.&nbsp Please check your email for further details')
                     Notification.objects.create(
                         user=user,
                         link='courses',
                         message_id=course_id,
                         message=notification_message
                     )

                     send_enrollment_email(user=user, course_title=course_title, email=email,
                                           community_link='https://chat.whatsapp.com/JQAG5DZUC98DxT3ZKy5gCo')

                 with concurrent.futures.ThreadPoolExecutor() as executor:
                         executor.submit(email_task)

                 return JsonResponse({'success': f'you have succesfully applied for the {course_title} kindly your check your email'})

            except:
                return JsonResponse(
                    {'error': 'something went wrong saving your data contact support'})
        else:
            return JsonResponse({'error': 'email not verified, kindly verify your email'})


def comment_truncate_caption(caption, limit=30):
    if len(caption) > limit:
        return caption[:limit] + "..."
    return caption

@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        text_comment = comment_truncate_caption(instance.text_comment)
        # Get the post that the comment is associated with
        # Fetch the Post instance

        # Get the owner of the post
        post_owner = instance.post.user
        comment_messages = [
            mark_safe(f"🌟 &nbsp<strong>{instance.user.username}</strong>&nbsp just shared their thoughts on your post! &nbsp<strong>{text_comment}</strong>&nbsp"),
            mark_safe(f"✨ &nbsp<strong>{instance.user.username}</strong>&nbsp left a lovely comment on your post! &nbsp<strong>{text_comment}</strong>&nbsp"),
            mark_safe(f"🎉 &nbsp<strong>{instance.user.username}</strong>&nbsp just added their voice to your post! &nbsp<strong>{text_comment}</strong>&nbsp"),
            mark_safe(f"📝 &nbsp<strong>{instance.user.username}</strong>&nbsp has something to say about your post! &nbsp<strong>{text_comment}</strong>&nbsp"),
            mark_safe(f"🌈 &nbsp<strong>{instance.user.username}</strong>&nbsp appreciated your post with a comment! &nbsp<strong>{text_comment}</strong>&nbsp"),
            mark_safe(f"💖 &nbsp<strong>{instance.user.username}</strong>&nbsp found your post inspiring and commented! &nbsp<strong>{text_comment}</strong>&nbsp"),
            mark_safe(f"🌼 &nbsp<strong>{instance.user.username}</strong>&nbsp shared their thoughts &nbsp<strong>{text_comment}</strong>&nbsp"),
            mark_safe(f"🎈 &nbsp<strong>{instance.user.username}</strong>&nbsp just brightened your post with a comment! &nbsp<strong>{text_comment}</strong>&nbsp"),
            mark_safe(f"🔍 &nbsp<strong>{instance.user.username}</strong>&nbsp discovered something interesting in your post! &nbsp<strong>{text_comment}</strong>&nbsp")
        ]

        # Create a notification for the post owner
        if instance.user != post_owner:
            Notification.objects.create(
                user=post_owner,
                message=random.choice(comment_messages),
                link='community',
                message_id=instance.post.post_id
            )





@login_required(login_url='signin')
def create_comment(request):
    if request.method=='POST':

        comment  =  request.POST['comment']
        file_upload = request.FILES.get('comment-image-file')
        id_post = request.POST.get('post_id')
        try:
            user = request.user
            email_verify = Email_Verification.objects.get(user=user)
            post = get_object_or_404(Post, post_id=id_post)
            if  user and email_verify.is_email_verified and not file_upload:
                try:
                 new_comment = Comment.objects.create(user=user, post=post, text_comment=comment)
                 new_comment.save()
                 # Prepare the response data
                 return JsonResponse({
                     'success': 'Comment posted successfully!'
                 })

                except Exception as e:
                    return JsonResponse({'error': f'unable to comment '})

            if user and email_verify.is_email_verified and file_upload:
               try:
                 new_comment = Comment.objects.create(user=user, post=post, file_uploaded=file_upload,  text_comment=comment)
                 new_comment.save()
                 return JsonResponse({'success': 'comment succesfully posted'})

               except Exception as e:
                  return JsonResponse({'error': f'unable to comment '})
            else:
                return JsonResponse({
                        'error': 'Unknown user contact support'
                })

        except:
            return JsonResponse({
                'error': 'something went wrong'
            })

def truncate_caption(caption, limit=30):
    if len(caption) > limit:
        return caption[:limit] + "..."
    return caption

@receiver(post_save, sender=Post)
def create_notifications(sender, instance, created, **kwargs):
    if created:
        # Get all users except the one who created the post
        users = User.objects.exclude(id=instance.user.id)
        caption = truncate_caption(instance.caption)
        messages = [
            mark_safe(f"🎉&nbsp <strong> {instance.user.username} </strong> &nbsp just shared a new post!&nbsp <strong>{caption}</strong>&nbsp Check it out!"),
            mark_safe(f"🚀 New Post Alert!&nbsp <strong>{instance.user.username}</strong>&nbsp  has just posted something new.&nbsp <strong>{caption}</strong> &nbsp Don't miss it!"),
            mark_safe(f"👀&nbsp <strong>{instance.user.username} </strong> &nbsp has dropped a new post! &nbsp <strong>{caption}</strong>&nbsp Take a look and see what they have to say!"),
            mark_safe(f"✨ Hey there! &nbsp <strong> {instance.user.username}</strong> &nbsp has created a new post.&nbsp <strong>{caption} </strong>&nbsp Join the conversation!"),
            mark_safe(f"📢&nbsp <strong>{instance.user.username}</strong>&nbsp has just added a new post! &nbsp<strong>{caption}</strong>&nbsp  Give it a read!   "),
        ]
        # Loop through all users and create a notification for each
        for user in users:
            Notification.objects.create(
                user=user,
                message=random.choice(messages),
                link='community',  # Or the actual link to the community page
                message_id= instance.post_id,
            )
            pass
    try:
        if created and instance.user.is_staff:
            users = User.objects.exclude(id=instance.user.id)
            current_site = get_current_site(request)  # Ensure you pass the request if needed
            domain = current_site.domain  # Get the domain as a string
            description = instance.caption
            post_link = f'{domain}/community#{instance.post_id}'

            with ThreadPoolExecutor() as executor:
                futures = []
                for user in users:
                    email = user.email
                    future = executor.submit(
                        admin_post_notify_user_email,
                        description=description,
                        username=user.username,
                        email=email,
                        post_link=post_link
                    )
                    futures.append(future)

                # Optional: Wait for all futures to complete and handle exceptions
                for future in futures:
                    try:
                        future.result()  # This will re-raise any exceptions caught in the thread
                    except Exception as e:
                        print(f"Error sending email to {user.username}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")


@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        user = request.user

        caption = request.POST.get('caption')
        chat_caption = request.POST.get('chatmsg')
        img_vid_list = request.FILES.getlist('input-imgvid-code')
        document_files = request.FILES.getlist('input-file')
        email_verify = Email_Verification.objects.get(user=user)
        if email_verify.is_email_verified and img_vid_list:
            group = PostFileGroup.objects.create(user=user)
            for file in img_vid_list:
                try:
                    new_post  = Post.objects.create(user=user, group_data=group, file_uploaded=file, caption=caption)
                    new_post.save()



                except:
                    return JsonResponse({'error':'something went wrong'})
            return JsonResponse({'success': 'post successfully created'})



        if  email_verify.is_email_verified and chat_caption:
                group = PostFileGroup.objects.create(user=user)
                try:

                    new_post  = Post.objects.create(user=user, group_data=group, caption=chat_caption)
                    new_post.save()
                    return JsonResponse({'success':'post successfully created'})


                except:
                    return JsonResponse({'error':'something went wrong'})


        if  email_verify.is_email_verified and document_files:
            group = PostFileGroup.objects.create(user=user)
            for file in document_files:
                print(file)
                try:
                    new_post = Post.objects.create(user=user, group_data=group, file_uploaded=file, caption=caption)
                    new_post.save()
                    return JsonResponse({'success': 'post successfully created'})


                except:
                    return JsonResponse({'error':'something went wrong'})
        else:
         return JsonResponse({'error': 'unknown user contact support'})

    return render(request,'create_post.html')


def Filter_posts(request):
 if request.method=='POST':
     filter_time = request.POST.get('filter_time')
     print(filter_time)
     user_model = User.objects.get(username=request.user.username)
     user_profile = Profile.objects.get(user=user_model)
     user_profile.filter_time = filter_time
     user_profile.save()
     return redirect('community')


@never_cache
def Load_More(request):
    user_model = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_model)
    if request.method=="POST":
        user_profile.filter_post+=3
        user_profile.filter_post_time = timezone.now()
        user_profile.save()
        return JsonResponse({'loadmore': "data loaded sucessfully "})



@login_required(login_url='signin')
@never_cache
def join_community(request):
          user_profile = get_object_or_404(Profile, user=request.user)
          if user_profile.terms_and_condition:
            notificationallcount = []
            related_posts_dict = {}
            try:
                if request.user.is_authenticated:
                    notification_is_all_read = Notification.objects.filter(user=request.user)
                    liked_post_ids = list(Like_Post.objects.filter(user=request.user).values_list('post_id', flat=True))
                    #liked_post_ids = [str(post_id) for post_id in liked_post_ids]  # Convert to strings

                    for notification_all_read in notification_is_all_read:
                        notificationcount = notification_all_read.is_notification_read
                        if notificationcount == False:
                            notificationallcount.append(str(notificationcount))


            except Exception as e:
                print(e)

            user_model = User.objects.get(username=request.user.username)

            user_profile = Profile.objects.get(user=user_model)
            post_profile = Profile.objects.all()
            like_posts = Like_Post.objects.all()
            all_comment  = Comment.objects.all()
            # post filter timeexpirationto returntodefault
            current_time = timezone.now()
            expiration_load_more_post =  user_profile.filter_post_time + timedelta(minutes=1)
            if current_time > expiration_load_more_post:
                user_profile.filter_post = 5
                user_profile.save()

            # Get filter option from URL query parameter (defaults to 'all')







            # Get all unique PostFileGroup instances
            post_file_groups = PostFileGroup.objects.order_by('-created_at').all()
            #post_file_groups = post_file_groups.order_by('-created_at')

            # Iterate over each PostFileGroup to find related Posts
            for group in post_file_groups[:user_profile.filter_post]:
                # Get all posts related to this group
                related_posts = Post.objects.filter(group_data=group)
                # Get the number of days specified by the user
                # Get the number of days specified by the user, default to 1 if not specified

                days = int(user_profile.filter_time)
                if days==1:
                    pass


                else:
                    # Set the time threshold based on the specified days
                    if days == 30:
                        time_threshold = timezone.now() - timedelta(days=30)
                    elif days == 90:
                        time_threshold = timezone.now() - timedelta(days=60)
                    elif days == 360:
                        time_threshold = timezone.now() - timedelta(days=360)

                    else:
                        # For less than 30 days but more than 1 day
                        time_threshold = timezone.now() - timedelta(days=days)

                    # Filter for posts older than the specified threshold
                    # Example: Get the first 10 posts (index 0 to 9)
                    related_posts = related_posts.filter(created_at__lte=time_threshold)

                # Limit the number of posts returned to the specified post_limit


                if  related_posts.exists():
                    related_posts_dict[group] = related_posts
            context = {

                'user_profile': user_profile,
                'posts': related_posts_dict,
                'post_profiles': post_profile,
                'like_posts': like_posts,
                'all_comment': all_comment,
                'liked_post_ids': (liked_post_ids),
                'notificationallcount': len(notificationallcount)}

            return render(request, 'community.html', context)


          else:      # Add the group and its related posts to the dictionary

            return redirect('community_rules')












@login_required(login_url='signin')
def Delete_Post(request):
    if request.method=='POST':
            id_post = request.POST.get('post_id')
            post = get_object_or_404(PostFileGroup, unique_id=id_post)
            post.delete()
            return JsonResponse({'deletepost': f'post deleted succesfully'})


'''@receiver(post_save, sender=Like_Post)
def like_post_notification(sender, instance, created, **kwargs):
    if created:
        # Get the post that the comment is associated with
        post = Post.objects.get(post_id=instance.post_id)  # Fetch the Post instance

        # Get the owner of the post
        post_owner = post.user

        # Create a notification for the post owner
        if instance.user != post_owner:
            Notification.objects.create(
                user=post_owner,
                message= mark_safe(f"👍 &nbsp<strong>{instance.user.username}</strong>&nbsp just liked your post!"),  # Thumbs up emoji,
                link='community',
                message_id=post.post_id
            )
'''
@login_required(login_url='signin')
def Like_post(request):
    user=request.user
    if request.method=="POST":
        user_model = User.objects.get(username=request.user.username)
        id_post = request.POST.get('post_id')
        post =get_object_or_404(Post, post_id=id_post)
        old_like= Like_Post.objects.filter(post_id =id_post, user=user).exists()
        if old_like:
            old_like = get_object_or_404(Like_Post, post_id=id_post, user=user)
            old_like.delete()
            post.no_of_likes-= 1
            post.save()
            return JsonResponse({'info': f' you  unlike  this post'})





        else:
           Like_Post.objects.create(post_id=id_post, user=user, like_clicked=True)
           post.no_of_likes+=1
           post.save()
           return JsonResponse({'success': f' you  like  this post'})


@login_required(login_url='signin')
def homepage(request):
    notificationallcount = []
    try:
        if request.user.is_authenticated:
                notification_is_all_read = Notification.objects.filter(user=request.user)
                for  notification_all_read in notification_is_all_read:
                    notificationcount = notification_all_read.is_notification_read
                    if notificationcount== False:
                        notificationallcount.append(str(notificationcount))


    except:
      pass



    try:

        email_verify = Email_Verification.objects.get(user=request.user)
        if email_verify:
            if not email_verify.is_email_verified:
                messages.info(request,"A verification Email was successfully sent kindly verify your email.   didn't  receive")
        else:
            return redirect('home')
    except:
        messages.info(request, "A verification Email was successfully sent kindly verify your email.   didn't  receive")
    context={'notificationallcount':len(notificationallcount)}


    return render(request, 'home_index.html', context)



def delete_notification(request, notification_id):
    try:
        # Assuming you're using DRF's authentication, you can access the user like this:
        if request.user.is_authenticated:
            # Assuming Notification model exists and has a field id_user
            notification = Notification.objects.get(id_user=notification_id)
            notification.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Notification does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def notification_is_read(request, notification_id):
    try:
        if request.user.is_authenticated:
            notification_is_read = Notification.objects.get(id_user=notification_id)
            notification_is_read.is_notification_read = True
            notification_is_read.save()
            return JsonResponse({'redirect': '/home'})
    except:
         return JsonResponse({'error': 'something went wrong'})
#---@login_required(login_url='signin')-------------------------mark notification as all read ----------------------------------------------
@login_required(login_url='signin')
def notification_all_read(request):
    try:
        if request.user.is_authenticated:
                notification_is_all_read = Notification.objects.filter(user=request.user)
                for notification_all_read in notification_is_all_read:
                    if not notification_all_read.is_notification_read:
                        notification_all_read.is_notification_read=True
                        notification_all_read.save()

                return JsonResponse({'success':'notification marked as read'})

    except:
        return JsonResponse({'error': 'something went wrong'})


@login_required(login_url='signin')
def get_Notification_Time(request, user):
    try:
        # Retrieve the existing notification for the user
        notifications_time = Notification.objects.all()
        # Calculate time difference
        for notification in  notifications_time:
            notification_timestamp = notification.timestamp
            latest_time = timezone.now()
            time_diff = latest_time - notification_timestamp
            total_time   = notification.time
            # Calculate time difference in minutes, hours, and days
            minutes = int(time_diff.total_seconds() // 60)
            hours = int(minutes // 60)
            days = int(hours // 24)
            months = int(days//30)
            years = int(months//12)
            if minutes == 0:
                total_time = 'now'
            elif minutes < 60:
                total_time = f'{minutes}m'
            elif hours < 24:
                total_time = f'{hours}h'
            elif days < 30:
                total_time = f'{days}d'
            elif months < 12:
                total_time = f'{months}mo'
            else:
                total_time = f'{years}y'
            # Update the notification with the calculated time differences
            notification.minutes = minutes
            notification.hours = hours
            notification.days = days
            notification.months= months
            notification.years =years
            notification.time=total_time
            notification.save()

    except Notification.DoesNotExist:
        # If the notification doesn't exist, return None or handle it as needed
        return None


@login_required(login_url='signin')
def Notification_center(request):
      user_profile = Profile.objects.get(user=request.user)
      notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
      total_time= get_Notification_Time(request, request.user)
      context={
        'user_profile':user_profile,
        'notifications':notifications,


        }

      return render(request, 'notification.html', context)

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    try:
        session_key = request.session.session_key
        browser_info = request.META.get('HTTP_USER_AGENT', '')[:200]
        usersessions = UserSession.objects.filter(user=user)

        # If the session is new, create a UserSession object
        if not usersessions.exists():
            # New device login
            message = f'New device logged in at {browser_info}'
            subject = 'login notification'
            UserSession.objects.create(
                user=user,
                session_key=session_key,
                browser_info=browser_info,
            )
            email_body = render_to_string('signin_notification_center.html', {'user': user, 'message': message})
            send_mail = EmailMultiAlternatives(subject=subject, body=email_body, from_email='Pylearn Hub', to=[user.email])
            send_mail.attach_alternative(email_body, 'text/html')
            send_mail.send(fail_silently=False)
        else:
            message = f'Unknown device logged in at {browser_info}'
            subject = 'unknown device'
            # Create new UserSession for the current login
            UserSession.objects.create(
                user=user,
                session_key=session_key,
                browser_info=browser_info,
            )
            email_body = render_to_string('signin_notification_center.html', {'user': user, 'message': message})
            send_mail = EmailMultiAlternatives(subject=subject, body=email_body, from_email='Pylearn Hub', to=[user.email])
            send_mail.attach_alternative(email_body, 'text/html')
            send_mail.send(fail_silently=False)
    except:
        pass









@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    session_key = request.session.session_key
    UserSession.objects.filter(session_key=session_key).delete()

@login_required(login_url='signin')
def Account_Settings(request):
    email_verify = Email_Verification.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=request.user)
    email_address = request.user.email
    all_countries = list(countries)
    context = {
        'email_verify': email_verify,
        'email_address': email_address,
        'countries': all_countries,
        'user_profile':user_profile
    }


    if request.method == "POST":
        # Get the new values from the POST request
        firstname = request.POST.get('firstname')
        images = request.FILES.get('profileImage')
        lastname = request.POST.get('lastname')
        dateofbirth = request.POST.get('dateofbirth')
        gender = request.POST.get('gender')
        bio = request.POST.get('bio')
        location = request.POST.get('country')
        email = request.POST.get('email')

        try:
            if request.user:
                    # Update the user profile with new values
                    if bio:
                        user_profile.bio = bio
                    if firstname:
                        user_profile.firstname = firstname
                    if lastname:
                        user_profile.lastname = lastname
                    if dateofbirth:
                        user_profile.dateofbirth = dateofbirth
                    if gender:
                        user_profile.gender = gender
                    if images:
                        user_profile.profileimg = images
                    if location:
                        user_profile.location = location

                    user_profile.save()
                    old_email=request.user.email
                    if old_email !=email:
                         user_model = User.objects.get(username=request.user)
                         user_model.email= email
                         user_model.save()
                         try:
                            user = request.user
                            current_site = get_current_site(request)
                            email_subject = 'Verify your email'
                            token = resend_verfication.make_token(user)
                            resend_email_user = Email_Verification.objects.get(user=user)
                            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                            resend_email_user.make_token=token
                            resend_email_user.save()
                            email_body = render_to_string('verification_center.html', {'user': user, 'domain': current_site,
                                                                                    'uidb64': uidb64, 'token': token})
                            plain_text = strip_tags(email_body)
                            send_mails = EmailMultiAlternatives(subject=email_subject, body=plain_text, from_email='Pylearn Hub',
                                                                to=[user.email])
                            send_mails.attach_alternative(email_body, 'text/html')
                            send_mails.send()
                            if send_mails:
                                #messages.info(request, 'Email verification sent succesfully')
                                return JsonResponse({'success':'new Email verification  sent succesfully. kindly check your mails'})
                            else:
                                #messages.error(request, 'something went wrong')
                                return JsonResponse({'error':'unable to send verification link'})
                         except:
                            return JsonResponse({'badrequest':'something went wrong'})

                        #resend_email_verification = Send_Email_Verification_msg(request, request.user)



                    return JsonResponse({'success': 'credentials successfully saved'})
            else:
                return JsonResponse({'error': 'Unable to save credentials'})
        except Exception as e:
            return JsonResponse({"error": f'Something went wrong: {e}'})






    return render(request, 'setting.html', context)



def Send_Email_Verification_msg(request, user):
    current_site = get_current_site(request)
    email_subject = 'Verify your email'
    token=generate_token.make_token(user)
    make_token_user = Email_Verification.objects.get(user=user)
    make_token_user.make_token = token
    make_token_user.save()
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    email_body = render_to_string('verification_center.html',{'user':user, 'domain': current_site,
                                                              'uidb64':uidb64, 'token':token})
    plain_text=strip_tags(email_body)
    send_mails= EmailMultiAlternatives(subject=email_subject, body=plain_text, from_email='Pylearn Hub', to=[user.email])
    send_mails.attach_alternative(email_body,'text/html')
    send_mails.send()
    if send_mails:
        return JsonResponse({'verification': 'Successfully Registered'})
    else:
     return JsonResponse({'error': 'unable to send verification mail'})







def activate_user(request, uidb64, token):
    try:
         User = get_user_model()
         uid = force_str(urlsafe_base64_decode(uidb64))
         user = User.objects.get(pk=uid)
         verification = Email_Verification.objects.get(user=user)
         if request.method == "GET":
            if user is not None and Email_Verification.objects.filter(user=user).exists():
                verification = Email_Verification.objects.get(user=user)
                current_time = timezone.now()
                expiration_time = verification.timestamp + timedelta(minutes=30)  # Expiration time set to 24 hours

                if current_time <= expiration_time and verification.make_token == token and not verification.is_email_verified:
                    verification.is_email_verified = True
                    updated_token = f'{verification.token}{verification.timestamp}{verification.is_email_verified}'
                    verification.full_token = updated_token
                    verification.save()
                    return HttpResponse('Email successfully verified')
                elif current_time > expiration_time and verification.make_token == token :
                    return HttpResponse('Link expired')
                elif verification.is_email_verified and verification.make_token == token:
                    return HttpResponse(f'Email already verified, kindly login ')
                else:
                    return HttpResponse('something went wrong')


            else:
                return HttpResponse('User unknown')
         else:
            return HttpResponse('something went wrong')
    except Exception as e:
        print(e)  # Log or handle the exception appropriately
        return HttpResponse('Invalid link')
def resent_verification_email(user, current_site, uidb64, token, email_subject):
    email_body = render_to_string('verification_center.html', {'user': user, 'domain': current_site,
                                                               'uidb64': uidb64, 'token': token})
    plain_text = strip_tags(email_body)
    send_mails = EmailMultiAlternatives(subject=email_subject, body=plain_text, from_email='Pylearn Hub',
                                        to=[user.email])
    send_mails.attach_alternative(email_body, 'text/html')
    send_mails.send()
@login_required(login_url='signin')
def resend_verification_link(request):
   try:
    user = request.user
    current_site = get_current_site(request)
    email_subject = 'Verify your email'
    token = resend_verfication.make_token(user)
    resend_email_user = Email_Verification.objects.get(user=user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    resend_email_user.make_token=token
    resend_email_user.save()

    #email_thread = threading.Thread(target= resent_verification_email, args=(user,current_site, uidb64, token, email_subject))
    #email_thread.start()
    with concurrent.futures.ThreadPoolExecutor() as executor:
                         executor.submit(resent_verification_email, user,current_site, uidb64, token, email_subject )
    return JsonResponse({'success':'new Email verification  sent succesfully. kindly check your mails'})

   except Exception as e:
      return JsonResponse({'error':f'unable to send verification link, {e}'})








def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if len(password1)< 8:
                return JsonResponse({'error': 'password should be in 8 characters'})
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': f'{email} already exists'})
            elif User.objects.filter(username=username).exists():
                return JsonResponse({'error': f'{username} already taken'})
            else:
                User.objects.create_user(username=username, email=email, password=password1)
                user_model = User.objects.get(username=username)
                Profile.objects.create(user=user_model, id_user=user_model.id)
                #email_verify =Send_Email_Verification_msg(request, user)
                # Send email verification asynchronously using ThreadPoolExecutor
                user = auth.authenticate(username=username, password=password1)
                auth.login(request, user)

                try:
                 with concurrent.futures.ThreadPoolExecutor() as executor:
                     executor.submit(Send_Email_Verification_msg, request, user)

                 return  JsonResponse({'success':'you have successfully created an account\nkindly check you mail to activate your account'})
                except:
                    return JsonResponse({'error': 'unable to send email verification link'})


        else:
            return JsonResponse({'error': 'Passwords do not match'})
    else:
        return redirect('/')

def signin(request):
    if request.method == 'POST':
        username = request.POST['susername']
        password = request.POST['spassword']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # Redirect to home page after login
            data = {
                'success': True,
                'redirect': '/home'  # Redirect URL after sign-in
            }
            return JsonResponse({'success':'/home'})
        else:
            return JsonResponse({'error': 'Email address or password is invalid'})
    else:
        if request.user.is_authenticated:
             return redirect('/home')
        else:
             return redirect('/')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


