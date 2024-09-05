from django import forms
from django.core.exceptions import ValidationError
from .models import Team, Sport, Department
import json


class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = [
            "name",
            "image",
            "registration_deadline",
            "rulebook",
            "fixtures",
            "team_size_min",
            "team_size_max",
            "department_limit",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


class TeamForm(forms.ModelForm):
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control rounded-0", "placeholder": "Select Sport"},
        ),
        label="Sport",
        empty_label="Select",
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control rounded-0", "placeholder": "Name"}
        ),
        help_text="Participant Name or Team Name",
        label="Name",
    )
    phone = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"type": "number", "min": "6000000000", "max": "9999999999", "class": "form-control rounded-0", "placeholder": "Phone"}
        ),
        help_text="Participant/Captain's Phone number",
        label="Phone",
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control rounded-0",
                "placeholder": "Select Department",
            },
        ),
        label="Department",
        empty_label="Select",
    )
    members = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control rounded-0", "Placeholder": "Member"}),
        help_text="Name the Captain first, then the other Members of the Team.",
        label="Member",
        required=False,
    )

    class Meta:
        model = Team
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    def clean(self):
        cleaned_data = super().clean()
        sport = cleaned_data.get('sport')
        department = cleaned_data.get('department')

        if sport and department and sport.department_limit:
            current_count = Team.objects.filter(sport=sport, department=department).count()
            if self.instance.pk is None and current_count >= sport.department_limit:
                raise ValidationError(f'Cannot have more than {sport.department_limit} teams for {sport} from {department}.')

        return cleaned_data

    def clean_members(self):
        members = self.cleaned_data["members"]

        # Attempt to parse as JSON
        try:
            # Normalize quotes: replace single quotes with double quotes for valid JSON
            members = members.replace("'", '"')
            members = json.loads(members)
        except json.JSONDecodeError:
            members = [name.strip() for name in members.split(",") if name.strip()]

        # Retrieve the selected sport
        sport = self.cleaned_data.get("sport")
        if sport and sport.team_size_min > 1:
            # Validate the number of members
            team_size_min = sport.team_size_min
            team_size_max = sport.team_size_max
            num_members = len(members)

            if num_members < team_size_min:
                raise ValidationError(
                    f"The minimum number of members required is {team_size_min}."
                )
            if num_members > team_size_max:
                raise ValidationError(
                    f"The maximum number of members allowed is {team_size_max}."
                )

        return members
