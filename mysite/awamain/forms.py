from django import forms
from .models import Post, Category, Comment

choices = Category.objects.all().values_list('name', 'name')
choice_list = [choice for choice in choices]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'book_cover', 'description', 'category', 'body']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'book_cover': forms.FileInput(attrs={'class': 'form'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'introduce your Book to the '
                                                                                         'other AWAs!'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'book_cover', 'description', 'category', 'body']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'category': cat,
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
