from django import forms

class selectAreaForm(forms.Form):
    city=forms.CharField(max_length=100,label="City",widget=forms.TextInput(attrs={'class':'form-control','id':'city'}))
    locality=forms.CharField(max_length=100,label="Locality",widget=forms.TextInput(attrs={'class':'form-control','id':'locality'}))

class castVoteForm(forms.Form):
    city=forms.CharField(max_length=100,label="City",widget=forms.TextInput(attrs={'class':'form-control','id':'city'}))
    locality=forms.CharField(max_length=100,label="Locality",widget=forms.TextInput(attrs={'class':'form-control','id':'locality'}))
    candidate=forms.ChoiceField(choices=[],label="Candidate Name",widget=forms.Select(attrs={"class":"form-control","id":"Candidate Name"}))

class otpForm(forms.Form):
    city=forms.CharField(max_length=100,label="City",widget=forms.TextInput(attrs={'class':'form-control','id':'city'}))
    locality=forms.CharField(max_length=100,label="Locality",widget=forms.TextInput(attrs={'class':'form-control','id':'locality'}))
    candidate=forms.CharField(max_length=100,label="Candidate Name",widget=forms.TextInput(attrs={"class":"form-control","id":"Candidate Name"}))
    otp=forms.CharField(max_length=20,label="OTP",widget=forms.TextInput(attrs={'class':'form-control','id':'OTP'}))