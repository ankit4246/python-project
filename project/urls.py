from django.contrib.auth.decorators import login_required
from django.urls import path
from project import views

urlpatterns = [
    path('', login_required(views.ListProjectsView.as_view()), name='list_projects'),
    path('project-details/', login_required(views.ProjectDetailsView.as_view()), name='create_project_details'),
    path('project-details/<int:project_id>/', login_required(views.ProjectDetailsView.as_view()), name='update_project_details'),
    path('project-delete/<int:pk>/', login_required(views.ProjectDeleteView.as_view()), name='delete_project'),
    path('project-target-delete/<int:pk>/', login_required(views.ProjectTargetDeleteView.as_view()), name='delete_project_target'),
    path('project-targets/<int:project_id>/', login_required(views.ProjectTargetsView.as_view()), name='create_project_targets'),
    path('review-and-submit/<int:project_id>/', login_required(views.ReviewSubmitView.as_view()),name='review_and_submit'),

    path('project-user/', views.create_project_users_view, name='create_project_user'),

    # path('retrieve_project/<int:pk>/', login_required(views.ListProjectsView.as_view()), name='create_project'),
    # path('update_project/', login_required(views.ListProjectsView].as_view()), name='create_project'),
    # path('delete_project/<int:pk>/', login_required(views.ListProjectsView.as_view()), name='create_project'),
]