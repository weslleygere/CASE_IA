from django.urls import path

from .views import (
    DashboardView,
    ConfigView,
    ModelTestView,
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('config/', ConfigView.as_view(), name='config'),
    path('ia-model/', ModelTestView.as_view(), name='test_model'),
    ]
