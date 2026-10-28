from django import forms
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        common_classes = (
            "w-full px-4 py-3 rounded-xl bg-slate-50 border border-clinical-border "
            "text-clinical-text placeholder-slate-400 focus:outline-none focus:ring-2 "
            "focus:ring-clinical-teal/20 focus:border-clinical-teal transition-all duration-200"
        )
        
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': common_classes})
            field.widget.attrs.update({'placeholder': f"Enter your {field.label.lower()}"})
            field.widget.attrs.update({'required': 'required'})
            
            if 'password' in field_name:
                field.help_text = ""
                field.widget.attrs.update({
                    'class': common_classes + " pr-12" 
                })


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        common_classes = (
            "w-full px-4 py-3 rounded-xl bg-slate-50 border border-clinical-border "
            "text-clinical-text placeholder-slate-400 focus:outline-none focus:ring-2 "
            "focus:ring-clinical-teal/20 focus:border-clinical-teal transition-all duration-200"
        )
        
        
        for field_name, field in self.fields.items():
            if 'password' in field_name:
                field.widget.attrs.update({'class': common_classes + " pr-12"})
            else:
                field.widget.attrs.update({'class': common_classes})
            
            field.widget.attrs.update({'placeholder': f"Enter your {field_name}"})