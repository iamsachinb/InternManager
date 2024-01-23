from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Intern

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add title'})
        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add title'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields =  ['name', 'email', 'username', 'regno']

    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add title'})
        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add title'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class InternForm(ModelForm):
    class Meta:
        model = Intern
        fields = ['name', 'permission',  'certificate', 'report']

    def __init__(self, *args, **kwargs):
        super(InternForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add title'})
        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add title'})

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input', 'required': 'true'})

