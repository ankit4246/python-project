from django.urls import path
from master_data.views import severityCreateView, severitySaveView, severityUpdateView, \
    severityDeleteView, targetCreateView, targetSaveView,targetUpdateView, targetDeleteView
#  , SeverityListView, SeverityUpdateView, SeverityDeleteView

urlpatterns = [
    path("severity/", severityCreateView, name="severity_create"),
    path("severity/save/", severitySaveView, name="severity_save"),
    path("severity/update/", severityUpdateView, name="severity_update"),
    path("severity/delete/", severityDeleteView, name="severity_delete"),
    path('target/',targetCreateView, name="target_create"),
    path("target/save/",targetSaveView, name="target_save"),
    path('target/update/',targetUpdateView, name="target_update"),
    path("target/delete/",targetDeleteView, name="target_delete"),

    # path("severity/list/", SeverityListView.as_view(), name="severity_list"),
    # path("severity/<pk>/update/", SeverityUpdateView.as_view(), name="severity_update"),
    # path("severity/<pk>/delete/", SeverityDeleteView.as_view(), name="severity_delete"),
]