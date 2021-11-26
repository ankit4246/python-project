from django.contrib.auth.decorators import login_required
from django.urls import path
from users import views

urlpatterns = [
    path('personal_info/', login_required(views.PersonalInfoView.as_view()), name='personal_info'),
    path('address_info/', login_required(views.AddressInfoView.as_view()), name='address_info'),
    path('education_info/', login_required(views.EducationInfoView.as_view()), name='education_info'),
    path('training_info/', login_required(views.TrainingInfoView.as_view()), name='training_info'),
    path('work_info/', login_required(views.WorkInfoView.as_view()), name='work_info'),
    path('social_info/', login_required(views.SocialInfoView.as_view()), name='social_info'),
    # path('register/', views.RegistrationView.as_view(), name='register'),
    path('register/', views.user_register, name='register'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name='logout'),
    # path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'),
    # path('activate-user/<uidb64>/<token>/', views.activate_user, name="activate"),
    path('education_info/<pk>/delete/', views.delete_single_form, name="delete-single-form"),
    path('user_confirm/<token>/', views.user_confirm_email, name='confirm-email'),
    path('password_reset/', views.passwordReset, name='password-reset'),
    path('confirm_password_reset/<token>/', views.passwordConfirmFromEmail, name='confirm-password-reset'),
    path('change_password/', views.changePassword, name="change-password"),
]