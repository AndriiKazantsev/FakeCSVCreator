from django import forms
from extra_views import InlineFormSetFactory

from .models import FakeCSVSchemes, FakeCSVSchemesInline


# INITIAL_VALUES = [
#     {},
# ]


class FakeCSVSchemeForm(forms.ModelForm):
    class Meta:
        model = FakeCSVSchemes
        fields = "__all__"

        widgets = {
            "author": forms.HiddenInput(),
            "name": forms.TextInput(),
            "delimiters": forms.Select(),
            "quotes": forms.Select(),
        }


class FakeCSVSchemeInlinesForm(forms.ModelForm):
    class Meta:
        model = FakeCSVSchemesInline
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(),
            "order": forms.NumberInput(),
            "data_type": forms.Select(choices=FakeCSVSchemesInline.FIELD_DROPDOWN_CHOICES),
            "data_range_from": forms.NumberInput(),
            "data_range_to": forms.NumberInput(),
        }


class FakeSchemeColumnInline(InlineFormSetFactory):
    model = FakeCSVSchemesInline
    form_class = FakeCSVSchemeInlinesForm
    fields = "__all__"
    #initial = INITIAL_VALUES

    factory_kwargs = {
            "extra": 1,
            "max_num": None,
            "can_order": False,
            "can_delete": True,
    }


class ExportDatasetForm(forms.Form):
    rows = forms.IntegerField(label="Rows", required=True)
