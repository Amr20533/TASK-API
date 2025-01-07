from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login_user, name= 'login'),
    path('signup', views.register, name= 'signup'),
    path('user', views.currentUser, name= 'user_info'),
    path('updateMe', views.updateCurrentUser, name= 'update_user_info'),
    path('updatePassword', views.updatePassword, name= 'update_password'),

    path('forgotPassword', views.UserForgotPassword, name= 'forgot_password'),
    path('resetPassword', views.UserResetPassword, name= 'reset_password'),


]