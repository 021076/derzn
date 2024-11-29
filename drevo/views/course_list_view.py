from django.views.generic import ListView
from ..models import Znanie, Tz
from loguru import logger

logger.add(
    "logs/main.log", format="{time} {level} {message}", rotation="100Kb", level="ERROR"
)


class CourseListView(ListView):
    """
    Выводит список курсов
    """

    template_name = "drevo/all_courses.html"
    model = Znanie
    context_object_name = "all_courses"

    def get_queryset(self):
        course_type = Tz.objects.get(name="Курс")
        return Znanie.objects.filter(tz=course_type, is_published=True)
