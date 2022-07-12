from django import forms
from . import models, utils

from PIL import Image


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["title", "body", "category", "tags", "feature_image"]

    tags = forms.ModelMultipleChoiceField(
        queryset=models.Tag.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    category = forms.ModelChoiceField(
        queryset=models.Category.objects.all(), widget=forms.RadioSelect
    )
