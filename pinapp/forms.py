
from django import forms
from pinapp.models import Comments,Image

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']  

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'description', 'image', 'category']
        # Add widgets and other form configurations as needed

