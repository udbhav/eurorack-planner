from django import forms

from apps.modules.models import Module, Setup

class CustomModuleForm(forms.ModelForm):
    def clean_hp(self):
        hp = self.cleaned_data['hp']
        if not hp:
            raise forms.ValidationError("HP is required.")

        return hp

    def clean_image(self):
        image = self.cleaned_data['image']
        if not image:
            raise forms.ValidationError("An image is required.")

        return image

    class Meta:
        model = Module
        fields = (
            'name',
            'image',
            'hp',
            'current_12v',
            'negative_current_12v',
            'current_5v',
            'msrp',
            )

class SetupForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = ('name','preset')
