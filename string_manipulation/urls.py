from . import views
from django.urls import path

urlpatterns = [
    path('create/', views.StringAPI.as_view(), name='create-strings'),
    path('get/', views.StringAPI.as_view(), name='get-strings'),
    path('operations/', views.StringOperationsAPI.as_view(), name='string-operations'),
    path('get/transformed/operations/', views.StringOperationsAPI.as_view(), name='get-string-transformed-operations')
]
