import json
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from datetime import datetime
from django.views.generic.edit import ProcessFormView

from .course_check_correctness_view import check_course_correctness
from ..models import Znanie, IP, Visits, BrowsingHistory, Relation, Tr
from loguru import logger

from ..models.courses_data import CourseWork, CourseData
from ..models.users_course_elements import CourseAdditionalElements
from ..relations_tree import get_children_by_relation_type_for_knowledge, get_children_for_knowledge

logger.add('logs/main.log',
           format="{time} {level} {message}", rotation='100Kb', level="ERROR")


class CourseDetailView(DetailView):
    model = Znanie
    context_object_name = 'znanie'
    template_name = "drevo/course_detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Передает в шаблон данные через контекст
        """
        context = super().get_context_data(**kwargs)

        # первичный ключ текущей записи
        pk = self.object.pk

        # сохранение ip пользователя
        knowledge = Znanie.objects.get(pk=pk)
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        ip_obj, created = IP.objects.get_or_create(ip=ip)
        if knowledge not in ip_obj.visits.all() and self.request.user.is_anonymous:
            ip_obj.visits.add(knowledge)

        # добавление просмотра
        if self.request.user.is_authenticated:
            Visits.objects.create(znanie=knowledge, user=self.request.user)

        # добавление историю просмотра
        if self.request.user.is_authenticated:
            browsing_history_obj, created = BrowsingHistory.objects.get_or_create(znanie=knowledge,
                                                                                  user=self.request.user)
            if not created:
                browsing_history_obj.date = datetime.now()
                browsing_history_obj.save()

            context['previous_works'] = CourseWork.objects.filter(user=self.request.user, course=knowledge) \
                .values_list('work_name', flat=True)

            if previous_works := self.request.GET.get('previous_works'):
                context['progress'] = list(CourseData.objects.filter(user=self.request.user, course=knowledge,
                                                                     work__work_name=previous_works).values(
                    'element', 'element_type'))
                if self.request.GET.get('previous_works'):
                    context['current_work'] = self.request.GET.get('previous_works')

            elif len(context['previous_works']) == 1:
                context['progress'] = list(CourseData.objects.filter(user=self.request.user, course=knowledge,
                                                                     work__work_name=context[
                                                                         'previous_works'].first()).values(
                    'element', 'element_type'))
                context['current_work'] = context['previous_works'].first()

            if self.request.GET.get('mode'):
                context['modification'] = 'on'

            # В случае, если у знания может быть лишь одна работа - сразу загружаем пользовательский прогресс
            if not knowledge.several_works:
                context['progress'] = list(CourseData.objects.filter(user=self.request.user, course=knowledge,
                                                                     work__work_name='Данные по курсу').values(
                    'element', 'element_type'))

        # Создание словаря со всеми элементами обучения
        try:
            next_relation = Tr.objects.get(name='Далее')
        except Tr.DoesNotExist:
            next_relation = None
        try:
            start_of_course = Relation.objects.get(bz=knowledge, tr__name='Начало курса').rz
            context['course_data'] = make_complicated_dict1(
                {'previous_key': []},
                start_of_course,
                'previous_key',
                next_relation=next_relation
            )['previous_key']
        except Relation.DoesNotExist:
            context['course_data'] = []
        if check_course_correctness(knowledge.id):
            context['warning_text'] = 'Данный курс на данный момент находится в разработке'

        return context


def make_complicated_dict1(course_dict, queryset, previous_key, level=1, next_relation=None):
    """
    Рекурсивно ищет потомков текущего знания до тех пор,
    пока функция get_children_by_relation_type_for_knowledge не вернет None
    """

    children = get_children_for_knowledge(queryset)

    if not children:
        relations = None
    else:
        relations = {}
        for child in children:
            relation = Relation.objects.filter(bz=queryset, rz=child).first()
            relations.setdefault(relation.tr, []).append(child)
        relations = dict(sorted(relations.items(), key=lambda x: x[0].name, reverse=True))

    if relations:
        if next_relation in relations.keys() and len(relations) == 1:
            if level == 0:
                course_dict.append(queryset)
                for relation, elem in relations.items():
                    make_complicated_dict1(course_dict, elem[0], elem[0], level=0)
            else:
                course_dict[previous_key].append(queryset)
                for relation, elem in relations.items():
                    make_complicated_dict1(course_dict[previous_key], elem[0], elem[0], level=0)
        else:
            if level == 0:
                course_dict.append({queryset: []})
                last_direction = None
                for relation, elem in relations.items():
                    if relation.name == 'Далее':
                        last_direction = elem[0]
                    else:
                        for el in elem:
                            make_complicated_dict1(course_dict[len(course_dict) - 1], el, queryset, level=1,
                                                   next_relation=next_relation)
                if last_direction:
                    make_complicated_dict1(course_dict, last_direction, previous_key, level=0,
                                           next_relation=next_relation)
            else:
                course_dict[previous_key].append({queryset: []})
                last_direction = None
                for relation, elem in relations.items():
                    if relation.name == 'Далее':
                        last_direction = elem[0]
                    else:
                        for el in elem:
                            make_complicated_dict1(course_dict[previous_key][len(course_dict[previous_key]) - 1],
                                                   el, queryset, level=1, next_relation=next_relation)
                if last_direction:
                    make_complicated_dict1(course_dict[previous_key], last_direction, previous_key, level=0,
                                           next_relation=next_relation)
    else:
        if level == 0:
            course_dict.append(queryset)
        else:
            course_dict[previous_key].append(queryset)

    return course_dict


class CourseResultAdd(ProcessFormView):
    def get(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            user = self.request.user

            if not user.is_authenticated:
                return JsonResponse({}, status=403)

            if pk:
                course = get_object_or_404(Znanie, id=pk)
                saved_progress = json.loads(request.GET.get('values'))
                elements_for_deletion = json.loads(request.GET.get('for_deletion'))
                work_name = request.GET.get('work')
                previous_work = CourseWork.objects.filter(course=course, user=user,
                                                          work_name=str(work_name)).first()

                if elements_for_deletion and elements_for_deletion == 'delete old results':
                    results_for_delete = CourseData.objects.filter(work=previous_work)
                    results_for_delete.delete()
                else:
                    if not previous_work:
                        previous_work = CourseWork.objects.create(
                            course=course,
                            user=user,
                            work_name=work_name,
                        )

                    for deleted_element in elements_for_deletion:
                        elem = get_object_or_404(CourseData, user=user, course=course,
                                                 work=previous_work, element=str(deleted_element))
                        elem.delete()

                    for course_element, course_element_type in saved_progress.items():
                        try:
                            next_relation = CourseData.objects.get(course=course,
                                                                   user=user,
                                                                   element=str(course_element), work=previous_work)
                            next_relation.element_type = course_element_type
                            next_relation.save()
                        except CourseData.DoesNotExist:
                            CourseData.objects.create(
                                course=course,
                                user=user,
                                element=str(course_element),
                                element_type=course_element_type,
                                work=previous_work,
                            )

                return JsonResponse({}, status=200)

        raise Http404


class EditCourse(ProcessFormView):
    def get(self, request, pk, *args, **kwargs):
        try:
            if request.is_ajax():
                user = self.request.user

                if not user.is_authenticated:
                    return JsonResponse({}, status=403)

                if pk:
                    course = get_object_or_404(Znanie, id=pk)
                    work_name = request.GET.get('work')
                    previous_work, created = CourseWork.objects.get_or_create(
                        course=course,
                        user=user,
                        work_name=str(work_name),
                    )

                    if request.GET.get('new_element'):
                        new_element = json.loads(request.GET.get('new_element'))
                        CourseAdditionalElements.objects.create(
                            user=user,
                            course=course,
                            work=previous_work,
                            parent_element=get_object_or_404(Znanie, name=str(new_element['parent_element'])),
                            element_name=new_element['element_name'],
                            relation_type=new_element['relation_type'],
                            insertion_type=new_element['insertion_type'],
                        )
                    elif request.GET.get('deleted'):
                        deleted_element = request.GET.get('deleted')
                        elem = get_object_or_404(CourseAdditionalElements, user=user, course=course,
                                                 work=previous_work, element_name=str(deleted_element))
                        elem.delete()
                        results_for_delete = CourseData.objects.filter(work=previous_work,
                                                                       element=str(deleted_element))
                        results_for_delete.delete()
                    elif request.GET.get('redacted'):
                        redacted_element = json.loads(request.GET.get('redacted'))
                        elem = get_object_or_404(CourseAdditionalElements, user=user, course=course,
                                                 work=previous_work, element_name=str(redacted_element[0]))
                        elem.element_name = redacted_element[1]
                        elem.save()
                        results_for_redaction = CourseData.objects.filter(work=previous_work,
                                                                          element=str(redacted_element[0]))
                        for saved_item in results_for_redaction:
                            saved_item.element = redacted_element[1]
                            saved_item.save()

                    return JsonResponse({}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
