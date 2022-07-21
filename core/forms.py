from django import forms

class CambiaContrasenaForm(forms.Form):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Ingrese su nueva contraseña...',
                'id':'password1',
                'required': 'required',
            }
        )
    )   
    password2 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Ingrese su nueva contraseña...',
                'id':'password2',
                'required': 'required',
            }
        )
    )
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden !')
        return password2
