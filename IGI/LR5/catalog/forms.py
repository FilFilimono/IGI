from django import forms
from .models import FurnitureItem, FurnitureCategory


class FurnitureItemForm(forms.ModelForm):
    class Meta:
        model = FurnitureItem
        fields = ['product_code', 'name', 'category', 'model', 'price', 'is_active',
                  'image', 'description', 'weight', 'dimensions', 'material', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class FurnitureFilterForm(forms.Form):
    SORT_CHOICES = [
        ('', 'По умолчанию'), ('name', 'По названию А-Я'),
        ('-name', 'По названию Я-А'), ('price', 'Цена ↑'),
        ('-price', 'Цена ↓'), ('-created_at', 'Новые'),
    ]
    q = forms.CharField(required=False, label='Поиск', widget=forms.TextInput(attrs={'placeholder': 'Название, код...'}))
    category = forms.ModelChoiceField(queryset=FurnitureCategory.objects.all(), required=False, label='Категория', empty_label='Все категории')
    is_active = forms.NullBooleanField(required=False, label='В производстве')
    price_min = forms.DecimalField(required=False, label='Цена от', min_value=0)
    price_max = forms.DecimalField(required=False, label='Цена до', min_value=0)
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Сортировка')
