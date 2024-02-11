from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class CartAddProductForm(forms.Form):
    # quantity = forms.IntegerField(
    #     min_value=1,
    #     widget=forms.NumberInput(attrs={
    #         'class': 'form-control text-center px-3',
    #         'value': 1
    #     }))
    quantity = forms.TypedChoiceField(
        label='',
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update(
            {'class': 'form-select d-inline w-25'})
