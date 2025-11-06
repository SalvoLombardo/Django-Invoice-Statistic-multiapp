from django.forms import ModelForm
from .models import CrochetComment, CrochetPost


class NewPostCrochet(ModelForm):
    class Meta:
        model=CrochetPost
        exclude=['author','created_at']


class NewCommentCrochet(ModelForm):
    class Meta:
        model=CrochetComment
        fields=['text']
        