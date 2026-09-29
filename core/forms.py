from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    texture = forms.ChoiceField(
        choices=[("", "—")] + [(s, s) for s in ["fine", "medium", "coarse"]],
        required=False,
    )
    pattern = forms.ChoiceField(
        choices=[("", "—")] + [(s, s) for s in ["straight", "wavy", "curly", "coily"]],
        required=False,
    )
    length = forms.ChoiceField(
        choices=[("", "—")] + [(s, s) for s in ["short", "shoulder", "long"]],
        required=False,
    )
    porosity = forms.ChoiceField(
        choices=[("", "—")] + [(s, s) for s in ["low", "medium", "normal", "high"]],
        required=False,
    )
    elasticity = forms.ChoiceField(
        choices=[("", "—")] + [(s, s) for s in ["good", "normal", "reduced"]],
        required=False,
    )

    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "phone",
            "birthday",
            "texture",
            "pattern",
            "length",
            "porosity",
            "elasticity",
            "notes",
        ]


SERVICES = [
    "cutService",
    "colorService",
    "highlightService",
    "treatmentService",
    "permService",
]
CURRENCIES = ["USD", "BRL", "EUR", "GBP"]
DETAILS = [
    "desired",
    "budget",
    "time",
    "home",
    "challenges",
    "desiredLength",
    "elevation",
    "direction",
    "styling",
    "predry",
    "finish",
    "tools",
    "frequency",
    "natural",
    "base",
    "target",
    "pigment",
    "tone",
    "formula",
    "perm",
    "relaxer",
    "processing",
    "bowls",
    "recommend",
    "returnDate",
    "observation",
]


class VisitForm(forms.Form):
    date = forms.DateField()
    service = forms.ChoiceField(choices=[(s, s) for s in SERVICES])
    price = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)
    currency = forms.ChoiceField(choices=[(s, s) for s in CURRENCIES])
    request_id = forms.UUIDField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in DETAILS:
            self.fields[key] = forms.CharField(required=False, max_length=4000)
        for key in ["time", "processing", "bowls"]:
            self.fields[key] = forms.IntegerField(
                required=False, min_value=0, max_value=100000
            )
        self.fields["budget"] = forms.DecimalField(
            required=False, min_value=0, max_digits=10, decimal_places=2
        )
        self.fields["returnDate"] = forms.DateField(required=False)
