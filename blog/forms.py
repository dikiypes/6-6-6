from django import forms
from .models import BlogPost
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'content', 'preview_image', 'is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'slug',
            'content',
            'preview_image',
            'is_published',
            Submit('submit', 'Сохранить')
        )
