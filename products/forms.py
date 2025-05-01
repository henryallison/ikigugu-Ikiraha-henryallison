from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from .models import Sale, Customer, SaleItem, Product


from django import forms
from django.core.validators import RegexValidator
from .models import Customer

class CustomerForm(forms.ModelForm):
    phone = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+\d{10,15}$',
                message="Phone number must start with '+' followed by 10-15 digits"
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+250123456789',
            'pattern': '^\+\d{10,15}$',
            'title': 'Enter phone number starting with + and 10-15 digits'
        })
    )

    class Meta:
        model = Customer
        fields = ['name', 'location', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'required': True
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@gmail.com',
                'required': True
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+'):
            raise forms.ValidationError("Phone number must start with '+'")
        if len(phone) < 11 or len(phone) > 16:  # + plus 10-15 digits
            raise forms.ValidationError("Phone number must be 10-15 digits after '+'")
        return phone


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'})
        }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate dropdown with all products
        self.fields['product'].queryset = Product.objects.all()

        # Customize dropdown display format
        self.fields['product'].label_from_instance = lambda obj: (
            f"{obj.name} (Stock: {obj.quantity}, Price: {obj.price})"
        )

        # Add classes and constraints
        self.fields['product'].widget.attrs.update({
            'class': 'form-select',
        })
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Quantity',
            'min': 1,
        })


# Formset to handle multiple sale items dynamically
SaleItemFormSet = inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'min': 0}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'min': 0}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product Description'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be a number greater than 0.")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        for field in ['name', 'category', 'description']:
            value = cleaned_data.get(field)
            if not value:
                self.add_error(field, f"{field.capitalize()} is required.")


class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
