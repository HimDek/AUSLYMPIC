from django import forms
from django.core.exceptions import ValidationError
from .models import Team, Sport, Department
import json


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
        help_text="Team name or Player name",
        label="Name",
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
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control rounded-0"}),
        help_text="Enter full name of members comma-separated. (Only for Team Sport)",
        label="Members",
        required=False,
    )

    class Meta:
        model = Team
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    def clean_members(self):
        members = self.cleaned_data["members"]

        # Attempt to parse as JSON
        try:
            # Normalize quotes: replace single quotes with double quotes for valid JSON
            members = members.replace("'", '"')
            parsed_members = json.loads(members)
            # Ensure it's a list of strings
            if isinstance(parsed_members, list) and all(
                isinstance(name, str) for name in parsed_members
            ):
                return parsed_members
        except json.JSONDecodeError:
            pass  # If JSON parsing fails, fallback to comma-separated parsing

        # Fallback: treat as a comma-separated list if not valid JSON
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
