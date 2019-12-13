from django import forms
from .models import Post, Rating, Recommand

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'picture','type',)

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ('rating_grade',)

class RecommandForm(forms.ModelForm):

    class Meta:
        model = Recommand
        fields = ('recomm_user','recomm_post',)