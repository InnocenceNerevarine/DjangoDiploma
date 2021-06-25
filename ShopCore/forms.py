from django import forms
from .models import Contact, Commentary, User


class ContactForm(forms.Form):

        subject = forms.CharField(label='Тема', required=True, widget=forms.TextInput
        (attrs={'placeholder': 'Тема обращения', 'class': 'form-group'}))
        from_email = forms.EmailField(label='Ваш Email', required=True, widget=forms.EmailInput
        (attrs={'placeholder': 'Электронная почта', 'class': 'form-group'}))
        message = forms.CharField(label='Сообщение', required=True, widget=forms.Textarea
        (attrs={'placeholder': 'Сообщение', 'class': 'form-group message'}))


class SubscribeForm(forms.ModelForm):

    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(
            attrs={'placeholder': 'Ваша электронная почта', 'class': '.newsletter-inner input'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if Contact.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Такая электронная почта уже существует в системе')
        return email

    class Meta:
        model = Contact
        fields = ['email']


class CommentaryForm(forms.ModelForm):

    email = forms.EmailField(required=True, label='Электронная почта', widget=forms.EmailInput(
        attrs={'placeholder': 'Ваша электронная почта', 'class': '.blog-single .reply .form-group textarea'}))
    name = forms.CharField(required=True, label='Имя', widget=forms.TextInput(
        attrs={'placeholder': 'Ваше имя/псевдоним', 'class': '.blog-single .reply .form-group textarea'}))
    body = forms.CharField(required=True, label='Сообщение', widget=forms.Textarea(
        attrs={'placeholder': 'Ваше сообщение', 'class': '.blog-single .reply .form-group input'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if Commentary.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Комментарий с такой электронной почтой уже существует в системе')
        return email

    class Meta:
        model = Commentary
        fields = ['email', 'name', 'body']


class UpdateInfoForm(forms.ModelForm):


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'address', 'profile_pic']
