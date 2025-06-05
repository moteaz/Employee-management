from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_employee, name='add_employee'),
    path('delete/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]


