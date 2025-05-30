from django import forms

class CommentForm(forms.Form):
    service_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    commenting_user = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    comment_text = forms.CharField(label="", error_messages={'required':'این فیلد نمیتواند خالی باشد'} ,widget=forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'متن نظر' , 'rows': '4'}))