from django.contrib.auth.decorators import login_required
from django.urls import path
from project import views

urlpatterns = [
    path('', login_required(views.ListProjectsView.as_view()), name='list_projects'),
    # path('create_project/', login_required(views.CreateProjectView.as_view()), name='create_project'),
    path('retrieve_project/<int:pk>/', login_required(views.ListProjectsView.as_view()), name='create_project'),
    # path('update_project/', login_required(views.ListProjectsView.as_view()), name='create_project'),
    path('delete_project/<int:pk>/', login_required(views.ListProjectsView.as_view()), name='create_project'),

]