from django import forms

class PostForm(forms.Form):
    caption = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': "What's happening?"}))
    input_imgvid_code = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    input_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


