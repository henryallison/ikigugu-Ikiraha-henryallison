from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from decimal import Decimal
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
import smtplib

from .models import Product, Customer, Sale, SaleItem
from .forms import ProductForm, AdminLoginForm, CustomerForm, SaleForm, SaleItemFormSet


# Create Sale
def create_sale(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        sale_form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)

        if customer_form.is_valid() and sale_form.is_valid() and formset.is_valid():
            selected_products = {}
            with transaction.atomic():
                customer = customer_form.save()
                sale = sale_form.save(commit=False)
                sale.customer = customer

                total = Decimal('0.00')
                tax_rate = Decimal('0.02')
                sale_items = []

                for form in formset:
                    product = form.cleaned_data.get('product')
                    quantity = form.cleaned_data.get('quantity')

                    if not product or not quantity:
                        continue  # Skip empty forms

                    if quantity <= 0:
                        form.add_error('quantity', 'Quantity must be greater than 0.')
                        break

                    if product.id in selected_products:
                        selected_products[product.id] += quantity
                    else:
                        selected_products[product.id] = quantity

                    if selected_products[product.id] > product.quantity:
                        form.add_error('quantity', f'Total quantity for "{product.name}" exceeds available stock ({product.quantity}).')
                        break

                    item_total = product.price * quantity
                    total += item_total
                    sale_items.append((form, product, quantity, product.price))

                else:
                    tax = total * tax_rate
                    final_amount = total + tax
                    sale.total_amount = total
                    sale.tax = tax
                    sale.final_amount = final_amount
                    sale.save()

                    for form, product, quantity, price in sale_items:
                        sale_item = form.save(commit=False)
                        sale_item.sale = sale
                        sale_item.price = price
                        sale_item.save()

                        product.quantity -= quantity
                        product.save()

                    messages.success(request, '✅ Sale successfully completed!')
                    return redirect('sales-history')

    else:
        customer_form = CustomerForm()
        sale_form = SaleForm()
        formset = SaleItemFormSet()

    return render(request, 'products/sale_form.html', {
        'customer_form': customer_form,
        'sale_form': sale_form,
        'formset': formset,
        'products': Product.objects.all(),
        'title': 'New Sale'
    })


# Admin Login
def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AdminLoginForm()
    return render(request, 'products/login.html', {'form': form})


# Logout
def admin_logout_view(request):
    logout(request)
    return redirect('admin-login')


# Dashboard
@login_required
def dashboard_view(request):
    return render(request, 'products/dashboard.html')


# Product List
@login_required
def product_list_view(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query if query else ''
    })


# Add Product
@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add Product'})


# Edit Product
@login_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product'})


# Delete Product
@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product-list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


# =========================
# ✅ NEW SALES HISTORY VIEWS
# =========================

from django.contrib.auth.decorators import login_required


@login_required
def sales_history(request):
    query = request.GET.get('q', '')  # Get search query from URL parameters
    sales = Sale.objects.select_related('customer').prefetch_related('items').order_by('-created_at')

    if query:
        sales = sales.filter(
            Q(customer__name__icontains=query) |  # Search by customer name
            Q(created_at__icontains=query) |  # Search by date (partial match)
            Q(id__icontains=query)  # Search by sale ID
        )

    context = {
        'sales': sales,
        'query': query  # Pass query back to template for display
    }
    return render(request, 'products/sales_history.html', context)


# Replace this function:
# def sale_detail(request, sale_id):

# With this corrected version:
@login_required
def view_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'products/sale_detail.html', {'sale': sale})



@login_required
def edit_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    customer = sale.customer

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, instance=customer)
        sale_form = SaleForm(request.POST, instance=sale)
        formset = SaleItemFormSet(request.POST, instance=sale)

        if customer_form.is_valid() and sale_form.is_valid() and formset.is_valid():
            customer_form.save()
            sale_form.save()
            formset.save()
            messages.success(request, 'Sale updated successfully!')
            return redirect('sales-history')

    else:
        customer_form = CustomerForm(instance=customer)
        sale_form = SaleForm(instance=sale)
        formset = SaleItemFormSet(instance=sale)

    return render(request, 'products/sale_form.html', {
        'customer_form': customer_form,
        'sale_form': sale_form,
        'formset': formset,
        'title': 'Edit Sale'
    })


@login_required
def delete_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    sale.delete()
    messages.success(request, 'Sale deleted successfully.')
    return redirect('sales-history')


@login_required
def print_sale(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    sale_items = SaleItem.objects.filter(sale=sale).select_related('product')

    tax = sale.total_amount * Decimal('0.02')
    final_amount = sale.total_amount + tax

    context = {
        'sale': sale,
        'customer': sale.customer,
        'items': sale_items,
        'tax': tax,
        'final_amount': final_amount,
        'title': f"Receipt for Sale #{sale_id}"
    }
    return render(request, 'products/print_sale.html', context)


@login_required
def email_sale(request, sale_id):
    try:
        sale = Sale.objects.get(pk=sale_id)
        customer = sale.customer
        sale_items = SaleItem.objects.filter(sale=sale)

        tax = sale.total_amount * Decimal('0.02')
        final_amount = sale.total_amount + tax

        # Render the email content
        email_html = render_to_string('products/email_receipt.html', {
            'sale': sale,
            'customer': customer,
            'items': sale_items,
            'tax': tax,
            'final_amount': final_amount,
        })

        subject = f"Receipt for your purchase on {sale.created_at.strftime('%Y-%m-%d')}"
        to_email = customer.email

        email = EmailMessage(subject, email_html, 'hyallison5050@gmail.com', [to_email])
        email.content_subtype = 'html'
        email.send()

        # Add a success message and redirect
        messages.success(request, f"Receipt was successfully sent to {customer.name} ({to_email})")
        return redirect(reverse('sales_history'))

    except Exception as e:
        messages.error(request, f"Failed to send email: {str(e)}")
        return redirect(reverse('sales_history'))