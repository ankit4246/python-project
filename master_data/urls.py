from django.urls import path
from master_data.views import SeverityCreateView, SeverityListView, SeverityUpdateView, SeverityDeleteView

urlpatterns = [
    path("severity/create/", SeverityCreateView.as_view(), name="severity_create"),
    path("severity/list/", SeverityListView.as_view(), name="severity_list"),
    path("severity/<pk>/update/", SeverityUpdateView.as_view(), name="severity_update"),
    path("severity/<pk>/delete/", SeverityDeleteView.as_view(), name="severity_delete"),
]