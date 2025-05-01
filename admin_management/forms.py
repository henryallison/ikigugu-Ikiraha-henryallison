from django import forms
from django.contrib.auth.models import User


class AdminUserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Password'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the fields required, except for is_active and is_superuser
        self.fields['is_active'].required = False
        self.fields['is_superuser'].required = False

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password is required for new admin users.")
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please choose another.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True  # Ensure user is marked as staff/admin
        if commit:
            user.save()
        return user


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AdminUserEditForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Password'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'password']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')  # current user being edited
        super().__init__(*args, **kwargs)

        # Make all fields required except 'is_active' and 'is_superuser'
        for field_name in self.fields:
            if field_name not in ['is_active', 'is_superuser']:
                self.fields[field_name].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("Password is required.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user