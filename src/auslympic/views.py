import json
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min, Count, Q
from .models import Sport, Department, SportGroup, Notice
from .forms import TeamForm


# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["groups"] = (
            SportGroup.objects.all()
            .annotate(first_sport_id=Min("sports__id"))
            .order_by("first_sport_id")
        )

        return context


class SportView(TemplateView):
    template_name = "sport.html"

    def get(self, request, pk):
        if not Sport.objects.filter(pk=pk).exists():
            raise ObjectDoesNotExist()
        return super().get(request, pk)

    def post(self, request, pk, **kwargs):
        members = request.POST.getlist("members")
        post_data = request.POST.copy()
        post_data["members"] = json.dumps([s for s in members if s and s.strip()])

        form = TeamForm(post_data)
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
        context["groups"] = (
            SportGroup.objects.all()
            .annotate(first_sport_id=Min("sports__id"))
            .order_by("first_sport_id")
        )
        context["sport"] = sport
        context["teams"] = teams

        if sport.registration_deadline >= timezone.datetime.now().date():
            context["team_form"] = TeamForm(initial={"sport": sport.id})

        return context


class LeaderBoard(TemplateView):
    template_name = "leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = (
            SportGroup.objects.all()
            .annotate(first_sport_id=Min("sports__id"))
            .order_by("first_sport_id")
        )
        context["departments"] = (
            Department.objects.annotate(
                gold_winner_count=Count("teams", filter=Q(teams__gold_winner=True)),
                silver_winner_count=Count("teams", filter=Q(teams__silver_winner=True)),
                bronze_winner_count=Count("teams", filter=Q(teams__bronze_winner=True)),
                winner_count=Count(
                    "teams",
                    filter=Q(
                        Q(teams__gold_winner=True)
                        | Q(teams__silver_winner=True)
                        | Q(teams__bronze_winner=True)
                    ),
                ),
            )
            .filter(
                Q(gold_winner_count__gt=0)
                | Q(silver_winner_count__gt=0)
                | Q(bronze_winner_count__gt=0)
            )
            .order_by(
                "-gold_winner_count", "-silver_winner_count", "-bronze_winner_count"
            )
        )

        return context


class NoticeView(TemplateView):
    template_name = "notices.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = (
            SportGroup.objects.all()
            .annotate(first_sport_id=Min("sports__id"))
            .order_by("first_sport_id")
        )
        context["notices"] = Notice.objects.all().order_by("-modified", "-added")

        return context


class MerchandiseView(TemplateView):
    template_name = "merchandise.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = (
            SportGroup.objects.all()
            .annotate(first_sport_id=Min("sports__id"))
            .order_by("first_sport_id")
        )

        return context
