from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='pylab'),
    path('signup', views.signup, name='signup'),
    path('courses', views.Courses, name='courses'),
    path('verification/<uidb64>/<token>', views.activate_user, name='verification'),
    path('resend-verification', views.resend_verification_link, name='verification'),
    path('accounts', views.Account_Settings, name='accounts'),
    path('home', views.homepage, name='home'),
    path('create_post', views.create_post, name='create_post'),
    path('signin', views.signin, name='signin'),
    path('delete-notification/<notification_id>', views.delete_notification, name='delete-notification'),
    path('notification-message/<notification_id>', views.notification_is_read, name='notification-message'),
    path('notifications', views.Notification_center, name='notifications'),
    path('notifications-allread', views.notification_all_read, name='notifications-allread'),
    path('community', views.join_community, name='community'),
    path('like_post', views.Like_post, name='like_post'),
    path('logout', views.logout, name='logout'),
    path('chat_Post', views.logout, name='chat_Post'),
    path('create_comment', views.create_comment, name='create_comment'),
    path('community_rules', views.community_terms_and_conditions, name='community_rules'),
    path('course_enrollment', views.Courses_enrollment ,name='course_enrollment'),
    path('course_task', views.Task, name='course_task'),
    path('delete_post', views.Delete_Post, name='delete_post'),
    path('filter_post', views.Filter_posts, name='filter_post'),
    path('loadmore', views.Load_More, name='loadmore'),
 

















]
