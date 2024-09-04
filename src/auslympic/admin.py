from django.contrib import admin
from .models import Department, Sport, Team, Notice, SportGroup
from .forms import TeamForm, SportForm


# Admin configuration for the Team model
class UserInline(admin.StackedInline):
    model = Sport.coordinators.through
    extra = 1


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class SportAdmin(admin.ModelAdmin):
    form = SportForm
    list_display = ("name", "custom_coordinators")
    search_fields = ("name",)
    inlines = [UserInline]

    def custom_coordinators(self, obj):
        return ", ".join([f"{coordinator.first_name} {coordinator.last_name}" for coordinator in obj.coordinators.all()])


class TeamAdmin(admin.ModelAdmin):
    form = TeamForm
    list_display = [
        "name",
        "sport",
        "department",
        "display_members",
        "gold_winner",
        "silver_winner",
        "bronze_winner",
    ]
    list_filter = ("sport", "department")
    search_fields = ("name", "members")
    ordering = ("-gold_winner", "-silver_winner", "-bronze_winner")

    def display_members(self, obj):
        # Nicely format members list in the admin display
        return ", ".join(obj.members)

    display_members.short_description = "Members"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(sport__coordinators=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj is None:
            return super().has_change_permission(request, obj)

        if request.user in obj.sport.coordinators.all():
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj is None:
            return super().has_change_permission(request, obj)

        if request.user in obj.sport.coordinators.all():
            return True

        return False


# Register the models with the admin
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Notice)
admin.site.register(SportGroup)
