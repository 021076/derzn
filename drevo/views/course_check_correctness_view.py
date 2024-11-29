from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drevo.models import Znanie, Relation
from drevo.relations_tree import get_descendants_for_knowledge


def check_course_correctness(course_id):
    """
    Проверка корректности курса.
    Используется атрибут «минимальное количество внутренних связей».
    В ходе проверки, если количество внутренних связей меньше минимального значения, выдается ошибка.
    Примечание: в ходе проверки никогда не учитываются связи вида «Далее».
    """
    course = get_object_or_404(Znanie, id=course_id)
    all_znaniya = [course] + list(get_descendants_for_knowledge(course))
    less_than_min = []
    for zn in all_znaniya:
        inner_rels_with_zn = Relation.objects.filter(bz=zn).exclude(tr__name='Далее')
        if inner_rels_with_zn.count() < zn.tz.min_number_of_inner_rels:
            less_than_min.append(f"{zn.tz.name} «{zn.name}»")
    if not less_than_min:
        return None
    return {'less_than_min': less_than_min}


@require_http_methods(['GET'])
def check_course_correctness_from_request(request):
    """Проверка курса с данными из GET-запроса"""
    course_id = request.GET.get('id')
    check_course = check_course_correctness(course_id)
    if check_course is None:
        return JsonResponse({}, status=200)
    return JsonResponse(check_course, status=200)
