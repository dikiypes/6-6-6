from django import forms
from .models import Product, Version


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'product_description',
                  'product_image', 'product_category_name', 'product_sale_price']
        widgets = {
            'create_date': forms.HiddenInput(),
            'update_date': forms.HiddenInput(),
        }

    def clean_product_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта',
                           'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        product_name = self.cleaned_data['product_name'].lower()

        for word in forbidden_words:
            if word in product_name:
                raise forms.ValidationError(f'Недопустимое слово "{word}" в названии продукта.')

        return self.cleaned_data['product_name']

    def clean_product_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта',
                           'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        product_description = self.cleaned_data['product_description'].lower()

        for word in forbidden_words:
            if word in product_description:
                raise forms.ValidationError(f'Недопустимое слово "{word}" в описании продукта.')

        return self.cleaned_data['product_description']


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name']
