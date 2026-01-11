from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import  timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimg =models.ImageField( default='profile_image.jpg' , upload_to='profile_image')
    bio =  models.TextField(blank=True)
    firstname =models.CharField(max_length=100, blank=True)
    lastname=models.CharField(max_length=100, blank=True)
    dateofbirth = models.DateField(default=timezone.now().date())
    gender = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    filter_time = models.CharField(max_length=100, default=1)
    filter_post = models.IntegerField(default=20)
    filter_post_time = models.DateTimeField(auto_now_add=True)
    terms_and_condition =  models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Email_Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200, default=uuid.uuid4, editable=False)
    full_token = models.CharField(max_length=500, blank=True,  editable=False)
    make_token = models.CharField(max_length=500, blank=True,  editable=False)
    timestamp = models.DateTimeField(max_length=100, default=timezone.now)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id= models.CharField(max_length=200)
    link = models.CharField(max_length=100, default='home')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_notification_read = models.BooleanField(default=False)
    minutes = models.IntegerField(default=0 ,editable= False)  # Field to store the calculated minutes
    hours = models.IntegerField(default=0, editable=False)    # Field to store the calculated hours
    days = models.IntegerField(default=0, editable=False)
    months = models.IntegerField(default=0, editable=False)    # Field to store the calculated hours
    years = models.IntegerField(default=0, editable=False)
    time =  models.TextField(blank=True)

    def __str__(self):
        return self.user.username
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    browser_info = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.browser_info}"
class PostFileGroup(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4,  unique=True)
    def __str__(self):
            return f"{str(self.unique_id)}"


class Post(models.Model):
    post_id = models.UUIDField(primary_key= True, default=uuid.uuid4)
    slug = models.SlugField(default=1)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    caption= models.TextField()
    group_data = models.ForeignKey(PostFileGroup, default=None, related_name='posts', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    no_of_likes  = models.IntegerField(default=0)
    updated_at  = models.DateTimeField(auto_now=True)



    ALLOWED_EXTENSIONS = ['doc', 'docx', 'py', 'txt', 'ipynb', 'csv', 'xlsx', 'pdf', 'jpeg','jpg', 'png', 'webp' , '.zip','.rar',
                          ]
    file_uploaded = models.FileField(upload_to='post_media',
                            validators = [FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)], blank=True)
    def get_absolute_url(self):
        return f"/community/{self.slug}/"

    def __str__(self):
        return f"{self.user.username}| {self.group_data}"
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',  on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ALLOWED_EXTENSIONS = ['doc', 'docx', 'py', 'txt', 'ipynb', 'csv', 'xlsx', 'pdf', 'jpeg','jpg', 'png', 'webp', '.zip',
                          '.rar',
                          ]
    file_uploaded = models.FileField(upload_to='post_media',
                                     validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)],
                                     blank=True)

    def __str__(self):
        return self.user.username

class  Course_Enrollment(models.Model):
   user =  models.ForeignKey(User, on_delete=models.CASCADE)
   course_id = models.CharField( max_length=100)
   email = models.EmailField()
   course = models.CharField( max_length=100)
   course_description = models.TextField( max_length=1000)
   is_course_enrolled = models.BooleanField(default=False)
   is_course_review = models.BooleanField(default=False)
   is_course_completed = models.BooleanField(default=False)
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return f'{self.user.username} | {self.course} '


class  Like_Post(models.Model):
    post_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_clicked = models.BooleanField(default=False)



    def __str__(self):
        return self.user.username
class Task_Submission(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        course_title = models.CharField(max_length= 100)
        description = models.CharField(max_length=2000, blank=True)
        ALLOWED_EXTENSIONS = ['txt', 'py', '.zip',
                              '.rar',
                              ]
        task_file = models.FileField(upload_to='task_files',
                                         validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)],
                                         blank=True)
        def __str__(self):
            return f"{self.user.username} | {self.course_title}"












