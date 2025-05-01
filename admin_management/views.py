from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import AdminUserCreateForm, AdminUserEditForm  # Correct placement of imports
from django.db import IntegrityError
from django.views.decorators.http import require_POST

# Decorator to allow only superusers
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@superuser_required
def admin_user_list(request):
    # Explicitly fetch all staff users (admins)
    users = User.objects.filter(is_staff=True).order_by('username')

    # Optional: Print in console to verify what's being fetched
    print(f"[DEBUG] Admin list loaded: {[user.username for user in users]}")

    return render(request, 'admin_management/admin_user_list.html', {'users': users})

# ✅ Delete admin user safely
@superuser_required
@require_POST
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Prevent a superuser from deleting themselves
    if request.user == user:
        messages.error(request, "You cannot delete your own admin account.")
        return redirect('admin-user-list')

    try:
        user.delete()
        messages.success(request, "Admin user deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the admin user: {e}")

    return redirect('admin-user-list')

# Create a new admin user (only superusers can access)
@superuser_required
def admin_user_create(request):
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin user created successfully.')
            return redirect('admin-user-list')
    else:
        form = AdminUserCreateForm()
    return render(request, 'admin_management/admin_user_form.html', {'form': form, 'title': 'Add Admin'})

# Edit an existing admin user (only superusers can access)
@superuser_required
def admin_user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin user updated successfully.')
            return redirect('admin-user-list')
    else:
        form = AdminUserEditForm(instance=user)
    return render(request, 'admin_management/admin_user_form.html', {'form': form, 'title': 'Edit Admin'})

# Manage Admin users (list all users who are superusers)
def manage_admins(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")

    admin_users = User.objects.filter(is_superuser=True)
    return render(request, 'admin_management/admin_user_list.html', {'users': admin_users})
