from django import forms
from django.contrib.auth import get_user_model
from .models import Revenue, Message, Topic

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Insira uma senha', 'autocomplete':'off'}), label='senha')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirme a senha', 'autocomplete':'off'}), label='confirmar senha')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Insira um email'}))
    photo_user = forms.ImageField(widget=forms.FileInput(attrs={'class':'photo-user'}), label='Foto do usuário')
    class Meta:
        model = get_user_model()

        fields = [
            'email',
            'password',
            'photo_user',
            'name'
        ]

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['photo_user'].required = False

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


    def verify_password(self, password):
        self.errors_password = {'error1': (password.isdecimal(),'A senha contêm apenas números'), 'error2': (self.verify_numbers(password),'A senha não contêm números'),'error3':(password.isalnum(),'A senha não contêm caracter especial como !,@,#,_ ou letras maiúsculas'), 'error4': (self.verify_len_password(password),'A senha tem menos de 8 caracteres'), 'error5': (self.compared_passwords(), 'As senhas não são iguas!!!')}

        for checker in self.errors_password:
            if self.errors_password[checker][0]:
                self.error = self.errors_password[checker][1]
                return True
        return False

    
    def verify_len_password(self, password):
        if len(password) < 8:
            return True
        return False
    

    def verify_numbers(self, password):
        for caracter in password:
            if caracter.isdigit():
                return False
        return True
    

    def compared_passwords(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            return True
        return False


class RevenueForm(forms.ModelForm):
    name_revenue = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Insira o nome para sua receita'}))
    ingredients = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Coloque os ingredients da sua receita'}))
    preparation_mode = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Coloque o modo de preparo da sua receita'}))
    class Meta:
        model = Revenue

        fields = [
            'name_revenue',
            'ingredients',
            'preparation_mode',
            'topic',
            'revenue_image'
        ]