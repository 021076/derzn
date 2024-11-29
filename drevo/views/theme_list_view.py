from django.views.generic import ListView
from ..models import Znanie, Tz
from loguru import logger

logger.add(
    "logs/main.log", format="{time} {level} {message}", rotation="100Kb", level="ERROR"
)


class ThemeListView(ListView):
    """
    Выводит список тем
    """

    template_name = "drevo/all_themes.html"
    model = Znanie
    context_object_name = "all_themes"

    def get_queryset(self):
        theme_type = Tz.objects.get(name="Тема")
        return Znanie.objects.filter(tz=theme_type, is_published=True)
