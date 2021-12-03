from django.contrib.auth.decorators import login_required
from django.urls import path
from users.views import auth_views, kyc_views, management_views

# auth url
urlpatterns = [
    path('register/', auth_views.user_register, name='register'),
    path('login/', auth_views.login_user, name="login"),
    path('logout/', auth_views.logout_user, name='logout'),
    path('user_confirm/<token>/', auth_views.user_confirm_email, name='confirm_email'),
    path('password-reset/', auth_views.password_reset, name='password_reset'),
    path('confirm-password-reset/<token>/', auth_views.password_confirm_from_email, name='confirm_password_reset'),
    path('change-password/', auth_views.change_password, name="change_password"),
    path('resend-email/', auth_views.resend_email, name='resend_email'),
]

# kyc urls
urlpatterns += [
    path('personal-info/', login_required(kyc_views.PersonalInfoView.as_view()), name='personal_info'),
    path('address-info/', login_required(kyc_views.AddressInfoView.as_view()), name='address_info'),
    path('education-info/', login_required(kyc_views.EducationInfoView.as_view()), name='education_info'),
    path('training-info/', login_required(kyc_views.TrainingInfoView.as_view()), name='training_info'),
    path('work-info/', login_required(kyc_views.WorkInfoView.as_view()), name='work_info'),
    path('social-info/', login_required(kyc_views.SocialInfoView.as_view()), name='social_info'),
    path('<str>/<pk>/delete', kyc_views.delete_single_form, name="delete-single-form"),
]

# management urls
urlpatterns += [
    path("list/user/", management_views.UserListView.as_view(), name="list_user"),
    path("create/user/", management_views.UserCreateView.as_view(), name="create_user"),
    path("update/<pk>/user/", management_views.UserUpdateView.as_view(), name="update_user"),
    path('delete/<pk>/user/', management_views.user_delete_view, name='delete_user'),
    path("activate/user/<int:user_id>/", management_views.user_activate, name="activate_user"),
    path("deactivate/user/<int:user_id>/", management_views.user_deactivate, name="deactivate_user"),
]
