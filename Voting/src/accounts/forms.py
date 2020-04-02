from django import forms
from django.contrib.auth import get_user_model,authenticate,login
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget,PhoneNumberInternationalFallbackWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
User=get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phonenumber', 'fullname')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phonenumber', 'fullname','password', 'active', 'admin', 'staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class registerForm(forms.ModelForm):

    phonenumber=PhoneNumberField(label="Phone Number",widget=PhoneNumberInternationalFallbackWidget(attrs={"class":"form-control","id":"Phone Number"}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control","id":"Password"}))
    password_confirm=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={"class":"form-control","id":"Confirm Password"}))

    class Meta:
        model=User
        fields=('fullname','address_line_1','address_line_2','city','state','pincode')
        widgets={
            'fullname':forms.TextInput(attrs={"class":"form-control","id":"Full Name"}),
            'address_line_1':forms.TextInput(attrs={"class":"form-control","id":"Address Line 1"}),
            'address_line_2':forms.TextInput(attrs={"class":"form-control","id":"Address Line 2"}),
            'city':forms.TextInput(attrs={"class":"form-control","id":"City"}),
            'state':forms.TextInput(attrs={"class":"form-control","id":"State"}),
            'pincode':forms.NumberInput(attrs={"class":"form-control","id":"Pincode"}),
        }

        labels={
            'fullname':'Full Name',
            'address_line_1':'Address Line 1',
            'address_line_2':'Address Line 2',
            'city':'City',
            'state':'State',
            'pincode':'Pincode',
        }



    def save(self,commit=True):
        user=super(registerForm,self).save(commit=False)
        user.phonenumber=self.cleaned_data["phonenumber"]
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user

class loginForm(forms.Form):
    phonenumber=PhoneNumberField(label="Phone Number",widget=PhoneNumberInternationalFallbackWidget(attrs={"class":"form-control",'id':"Phone Number"}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control","id":"Password"}))

    def clean(self):
        data=self.cleaned_data
        return data

    def clean_phonenumber(self):
        phonenumber=self.cleaned_data.get("phonenumber")
        qs=User.objects.filter(phonenumber=phonenumber)
        if not qs.exists():
            raise forms.ValidationError("Phone Number does not exist")
        return phonenumber

