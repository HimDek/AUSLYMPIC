from django.views.generic.base import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from .models import Sport, Department, SportGroup
from .forms import TeamForm


# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["sports"] = Sport.objects.all()
        context["groups"] = SportGroup.objects.all()

        return context


class SportView(TemplateView):
    template_name = "sport.html"

    def get(self, request, pk):
        if not Sport.objects.filter(pk=pk).exists():
            raise ObjectDoesNotExist()
        return super().get(request, pk)

    def post(self, request, pk, **kwargs):
        form = TeamForm(request.POST)
        sport = Sport.objects.get(pk=pk)
        context = self.get_context_data(sport=sport)
        if form.is_valid():
            obj = form.save()
            context["created"] = obj
            return self.render_to_response(context)
        else:
            context["team_form"] = form
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        sport = Sport.objects.get(pk=self.kwargs["pk"])
        teams = sport.teams.all().order_by(
            "-gold_winner", "-silver_winner", "-bronze_winner"
        )

        context = super().get_context_data(**kwargs)
        context["sports"] = Sport.objects.all()
        context["sport"] = sport
        context["teams"] = teams
        context["team_form"] = TeamForm(initial={"sport": sport.id})

        return context


class LeaderBoard(TemplateView):
    template_name = "leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sports"] = Sport.objects.all()
        context["departments"] = Department.objects.all().annotate(
            gold_winner_count=Count("teams", filter=Q(teams__gold_winner=True)),
            silver_winner_count=Count("teams", filter=Q(teams__silver_winner=True)),
            bronze_winner_count=Count("teams", filter=Q(teams__bronze_winner=True)),
        ).order_by(
            "-gold_winner_count", "-silver_winner_count", "-bronze_winner_count"
        )

        return context
