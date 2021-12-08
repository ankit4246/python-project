from django.urls import path
from master_data.views import severityCreateView, severitySaveView, severityUpdateView, severityDeleteView
#  , SeverityListView, SeverityUpdateView, SeverityDeleteView

urlpatterns = [
    path("severity/", severityCreateView, name="severity_create"),
    path("severity/save/", severitySaveView, name="severity_save"),
    path("severity/update/", severityUpdateView, name="severity_update"),
    path("severity/delete/", severityDeleteView, name="severity_delete"),

    # path("severity/list/", SeverityListView.as_view(), name="severity_list"),
    # path("severity/<pk>/update/", SeverityUpdateView.as_view(), name="severity_update"),
    # path("severity/<pk>/delete/", SeverityDeleteView.as_view(), name="severity_delete"),
]