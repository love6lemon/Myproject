from django.urls import path
from login import views

app_name = 'login'

urlpatterns = [
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:asset_id>/', views.detail, name="detail"),
    path('', views.dashboard),
]