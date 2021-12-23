from django.urls import path
from master_data.views import severityCreateView, severitySaveView, severityUpdateView, severityDeleteView
from master_data.views import targetTypeCreateView, targetTypeSaveView, targetTypeUpdateView, targetTypeDeleteView
from master_data.views import reportTypeCreateView, reportTypeSaveView, reportTypeUpdateView, reportTypeDeleteView

#  , SeverityListView, SeverityUpdateView, SeverityDeleteView

urlpatterns = [
    # for Severity
    path("severity/", severityCreateView, name="severity_create"),
    path("severity/save/", severitySaveView, name="severity_save"),
    path("severity/update/", severityUpdateView, name="severity_update"),
    path("severity/delete/", severityDeleteView, name="severity_delete"),

    # for Target
    path("target/", targetTypeCreateView, name="target_create"),
    path("target/save/", targetTypeSaveView, name="target_save"),
    path("target/update/", targetTypeUpdateView, name="target_update"),
    path("target/delete/", targetTypeDeleteView, name="target_delete"),

    # for Report
    path("report/", reportTypeCreateView, name="report_create"),
    path("report/save/", reportTypeSaveView, name="report_save"),
    path("report/update/", reportTypeUpdateView, name="report_update"),
    path("report/delete/", reportTypeDeleteView, name="report_delete"),

    # path("severity/list/", SeverityListView.as_view(), name="severity_list"),
    # path("severity/<pk>/update/", SeverityUpdateView.as_view(), name="severity_update"),
    # path("severity/<pk>/delete/", SeverityDeleteView.as_view(), name="severity_delete"),
]