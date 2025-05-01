from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login_view, name='admin-login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.admin_logout_view, name='admin-logout'),
    path('sale/new/', views.create_sale, name='create-sale'),
    path('', views.product_list_view, name='product-list'),  # Correct reference
    path('add/', views.product_create_view, name='product-create'),  # products/add/
    path('edit/<int:pk>/', views.product_edit_view, name='product-edit'),  # products/edit/<pk>/
    path('delete/<int:pk>/', views.product_delete_view, name='product-delete'),  # products/delete/<pk>/
# urls.py
path('sales/', views.sales_history, name='sales-history'),
path('sales/<int:sale_id>/', views.view_sale, name='sale-view'),
path('sales/<int:sale_id>/edit/', views.edit_sale, name='sale-edit'),
path('sales/<int:sale_id>/delete/', views.delete_sale, name='sale-delete'),
path('sales/<int:sale_id>/print/', views.print_sale, name='sale-print'),
path('sales/<int:sale_id>/email/', views.email_sale, name='sale-email'),
path('sales/history/', views.sales_history, name='sales_history'),

]
