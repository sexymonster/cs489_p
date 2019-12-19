from django import forms
from .models import Post, Rating, Recommand, Theme

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','theme','temp_theme','author')

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ('rating_grade',)

class RecommandForm(forms.ModelForm):

    class Meta:
        model = Recommand
        fields = ('recomm_user','recomm_post',)

class ThemeForm(forms.ModelForm):

    class Meta:
        model = Theme
        fields = ('theme_title', 'theme_type',)