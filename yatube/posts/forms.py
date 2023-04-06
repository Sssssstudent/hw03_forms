from django import forms
from django.contrib.auth import get_user_model
from .models import Post


User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ('text', 'group')
        labels = {
            'text': 'Текст поста',
            'group': 'Группа',
        }
        help_texts = {
            'text': 'Введите текст',
            'group': 'Выберите группу из списка',
        }

    def clean_text(self):
        data = self.cleaned_data['text']

        if not data:
            raise forms.ValidationError('Заполните поле')

        return data
