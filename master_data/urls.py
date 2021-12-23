from django.urls import path
from master_data.views import severityCreateView, severitySaveView, severityUpdateView, severityDeleteView
from master_data.views import targetTypeCreateView, targetTypeSaveView, targetTypeUpdateView, targetTypeDeleteView
from master_data.views import reportTypeCreateView, reportTypeSaveView, reportTypeUpdateView, reportTypeDeleteView
from master_data.views import degreeCreateView, degreeSaveView, degreeUpdateView, degreeDeleteView
from master_data.views import provinceCreateView, provinceSaveView, provinceUpdateView, provinceDeleteView

#  , SeverityListView, SeverityUpdateView, SeverityDeleteView

urlpatterns = [

    # For Severity
    path("severity/", severityCreateView, name="severity_create"),
    path("severity/save/", severitySaveView, name="severity_save"),
    path("severity/update/", severityUpdateView, name="severity_update"),
    path("severity/delete/", severityDeleteView, name="severity_delete"),

    # For Target
    path("target/", targetTypeCreateView, name="target_create"),
    path("target/save/", targetTypeSaveView, name="target_save"),
    path("target/update/", targetTypeUpdateView, name="target_update"),
    path("target/delete/", targetTypeDeleteView, name="target_delete"),

    # For Report
    path("report/", reportTypeCreateView, name="report_create"),
    path("report/save/", reportTypeSaveView, name="report_save"),
    path("report/update/", reportTypeUpdateView, name="report_update"),
    path("report/delete/", reportTypeDeleteView, name="report_delete"),
    
    # For Degree
    path("degree/", degreeCreateView, name="degree_create"),
    path("degree/save/", degreeSaveView, name="degree_save"),
    path("degree/update/", degreeUpdateView, name="degree_update"),
    path("degree/delete/", degreeDeleteView, name="degree_delete"),

    # For Province
    path("province/", provinceCreateView, name="province_create"),
    path("province/save/", provinceSaveView, name="province_save"),
    path("province/update/", provinceUpdateView, name="province_update"),
    path("province/delete/", provinceDeleteView, name="province_delete"),

    # path("severity/list/", SeverityListView.as_view(), name="severity_list"),
    # path("severity/<pk>/update/", SeverityUpdateView.as_view(), name="severity_update"),
    # path("severity/<pk>/delete/", SeverityDeleteView.as_view(), name="severity_delete"),
]