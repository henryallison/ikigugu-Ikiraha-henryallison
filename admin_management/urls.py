from django.urls import path
from . import views

urlpatterns = [
    # Manage admins list (show all admin users)
    path('manage-admins/', views.admin_user_list, name='manage-admins'),

    # Admin users list page (show all admin users, available to superusers)
    path('admin-users/', views.admin_user_list, name='admin-user-list'),

    # Create new admin user
    path('admin-users/create/', views.admin_user_create, name='admin-user-create'),

    # Edit an existing admin user
    path('admin-users/<int:pk>/edit/', views.admin_user_edit, name='admin-user-edit'),  # Use function-based view

    # Delete an admin user
    path('admin-users/<int:pk>/delete/', views.admin_user_delete, name='admin-user-delete'),
]
