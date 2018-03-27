from django import forms
from .models import Post
from .models import Comment, CommentChild
from django.utils.text import slugify


class PostForm(forms.ModelForm):
    # title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'content',
            'draft',
            'img',
        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            # if field != 'draft' and field != 'img' :
            print(field)
            self.fields[field].widget.attrs = {'class': 'form-control'}

        self.fields['draft'].widget.attrs['class'] = ''
        self.fields['img'].widget.attrs['class'] = ''
        self.fields['content'].widget.attrs['rows'] = '15'
        self.fields['content'].widget.attrs['cols'] = '100'

    # Cleaned Data = Kullanıcının yazdığı bölümleri kısıtlamak (En az 8 harf)
    def clean_title(self):
        title = self.cleaned_data['title']

        if title.isdigit():
            raise forms.ValidationError('Lütfen Sadece Sayı Girmeyiniz')

        if '@' in title:
            raise forms.ValidationError('Lütfen @ işareti girmeyiniz')

        return title



class PostFilterForm(forms.Form):
    Options = (
        ('A', 'All'),
        ('D', 'Draft'),
        ('ND', 'Not Draft')
    )
    option = forms.CharField(label='Filtre', widget=forms.Select(choices=Options, attrs={'class': 'form-control'}))


class CommentFrom(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentFrom, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

        self.fields['c_content'].widget.attrs['rows'] = '10'
        self.fields['c_content'].widget.attrs['cols'] = '50'

    class Meta:
        model = Comment
        fields = [
            'c_content'
        ]

    # def clean_name_surname(self):
    #     user = self.cleaned_data['']
    #
    #     if not name_surname.isalpha():
    #         raise  forms.ValidationError('Lütfen Sadece Karakter Giriniz !!!!11!!1')
    #
    #     return user



