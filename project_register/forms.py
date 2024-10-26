# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from .models import PDFUpload




class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    user_type = forms.ChoiceField(choices=[('student', 'Student'), ('professor', 'Professor')])
    school_year = forms.ChoiceField(choices=[('1', '1ère année'), ('2', '2ème année'), ('3', '3ème année')], required=False)
    field = forms.ChoiceField(choices=[('1', '2IA'), ('2', 'IDSIT'), ('3', 'IDF'), ('4', 'BI&A'), ('5', 'GL'), ('6', 'GD'), ('7', 'SSI'), ('8', 'SSE')], required=False)
    department = forms.ChoiceField(choices=[('1', '2IA'), ('2', 'IDSIT'), ('3', 'IDF'), ('4', 'BI&A'), ('5', 'GL'), ('6', 'GD'), ('7', 'SSI'), ('8', 'SSE')], required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type', 'school_year', 'field', 'department']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create or update profile
            profile, created = Profile.objects.get_or_create(user=user)
            if self.cleaned_data['user_type'] == 'student':
                profile.school_year = self.cleaned_data['school_year']
                profile.field = self.cleaned_data['field']
                profile.department = None  # Clear department for students
            elif self.cleaned_data['user_type'] == 'professor':
                profile.department = self.cleaned_data['department']
                profile.school_year = None  # Clear school year for professors
                profile.field = None  # Clear field for professors
            profile.user_type = self.cleaned_data['user_type']
            profile.save()
        return user

    
class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFUpload
        fields = ['file', 'description','sujet']  # Add 'description' here

class SearchStudentForm(forms.Form):
    username = forms.CharField(max_length=150)

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = PDFUpload
        fields = ['status']
