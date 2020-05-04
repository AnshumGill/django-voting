from django import forms

partyChoices=[
	('BJP','BJP'),
	('Congress','Congress'),
	('Independent','Independent'),
]

class partyInfoForm(forms.Form):
	partyname=forms.ChoiceField(choices=partyChoices,label="Party Name",widget=forms.Select(attrs={"class":"form-control","id":"Party Name"}))
