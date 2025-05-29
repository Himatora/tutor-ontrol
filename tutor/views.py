from rest_framework import viewsets, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *
import logging

logger = logging.getLogger(__name__)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"Создание учителя: {request.data}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Обновление учителя: {request.data}")
        return super().update(request, *args, **kwargs)

class LearningGoalViewSet(viewsets.ModelViewSet):
    queryset = LearningGoal.objects.all()
    serializer_class = LearningGoalSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"Создание цели обучения: {request.data}")
        return super().create(request, *args, **kwargs)

class LearningCategoriesViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = LearningCategory.objects.all()
    serializer_class = LearningCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"Создание категории обучения: {request.data}")
        return super().create(request, *args, **kwargs)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['learning_category']
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Создание ученика: {request.data}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Обновление ученика: {request.data}")
        return super().update(request, *args, **kwargs)

class LessonTypeViewSet(viewsets.ModelViewSet):
    queryset = LessonType.objects.all()
    serializer_class = LessonTypeSerializer
    permission_classes = [AllowAny]

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student']
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        logger.info(f"Запрос уроков: {request.query_params}")
        return super().list(request, *args, **kwargs)

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [AllowAny]

class JournalViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def generate(self, request):
        student_id = request.data.get('student_id')
        lessons_count = int(request.data.get('lessons_count', 5))

        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            logger.error(f"Студент с ID {student_id} не найден")
            return Response({"error": "Student not found"}, status=404)

        lessons = Lesson.objects.filter(student=student).order_by('-date')[:lessons_count]
        covered_topics = ", ".join(set(lesson.topic.name for lesson in lessons)) if lessons else "Нет данных"

        good_results = []
        bad_results = []
        problem_topics = []
        for lesson in lessons:
            try:
                homework = Homework.objects.get(lesson=lesson)
                if homework.result is not None:
                    if homework.result >= 50:
                        good_results.append(f"Тема '{lesson.topic.name}': {homework.result}%")
                    else:
                        bad_results.append(f"Тема '{lesson.topic.name}': {homework.result}%")
                        problem_topics.append(lesson.topic.name)
            except Homework.DoesNotExist:
                continue

        good_results_str = "; ".join(good_results) if good_results else "Нет данных"
        bad_results_str = "; ".join(bad_results) if bad_results else "Нет данных"
        working_on = ", ".join(set(problem_topics)) if problem_topics else "Нет данных"
        recommended_lessons = 5 if len(problem_topics) >= 3 else 3
        recommendation_reason = (
            f"Рекомендуется {recommended_lessons} занятий, так как есть темы с низким процентом выполнения: {working_on}"
            if problem_topics
            else "Рекомендуется стандартный объем занятий"
        )

        journal_entry = JournalEntry.objects.create(
            student=student,
            good_results=good_results_str,
            bad_results=bad_results_str,
            covered_topics=covered_topics,
            working_on=working_on,
            recommended_lessons=recommended_lessons,
            recommendation_reason=recommendation_reason
        )

        serializer = self.get_serializer(journal_entry)
        logger.info(f"Создана запись в журнале: {serializer.data}")
        return Response(serializer.data, status=201)