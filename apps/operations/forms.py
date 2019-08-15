from django import forms
from operations.models import UserFavorite, CourseComments


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ["course", "comments"]

