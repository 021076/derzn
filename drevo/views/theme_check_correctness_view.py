from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drevo.models import Znanie, Relation
from drevo.relations_tree import get_descendants_for_knowledge


def check_theme_correctness(theme_id):
    """
    Проверка корректности темы.
    Используется атрибут «минимальное количество внутренних связей».
    В ходе проверки, если количество внутренних связей меньше минимального значения, выдается ошибка.
    Примечание: в ходе проверки никогда не учитываются связи вида «Далее».
    """
    theme = get_object_or_404(Znanie, id=theme_id)
    all_znaniya = [theme] + list(get_descendants_for_knowledge(theme))
    less_than_min = []
    for zn in all_znaniya:
        inner_rels_with_zn = Relation.objects.filter(bz=zn).exclude(tr__name='Далее')
        if inner_rels_with_zn.count() < zn.tz.min_number_of_inner_rels:
            less_than_min.append(f"{zn.tz.name} «{zn.name}»")
    if not less_than_min:
        return None
    return {'less_than_min': less_than_min}


@require_http_methods(['GET'])
def check_theme_correctness_from_request(request):
    """Проверка темы с данными из GET-запроса"""
    theme_id = request.GET.get('id')
    check_theme = check_theme_correctness(theme_id)
    if check_theme is None:
        return JsonResponse({}, status=200)
    return JsonResponse(check_theme, status=200)
