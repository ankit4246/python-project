from django.urls import path
from users import views

urlpatterns = [
    path('personal_info/', views.PersonalInfoView.as_view(), name='personal_info'),
    path('address_info/', views.AddressInfoView.as_view(), name='address_info'),
    path('education_info/', views.EducationInfoView.as_view(), name='education_info'),
    path('training_info/', views.TrainingInfoView.as_view(), name='training_info'),
    path('work_info/', views.WorkInfoView.as_view(), name='work_info'),
    path('social_info/', views.SocialInfoView.as_view(), name='social_info'),
    # path('register/', views.RegistrationView.as_view(), name='register'),
    path('register/', views.user_register, name='register'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name='logout'),
]