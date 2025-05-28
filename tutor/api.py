from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from tutor.models import Teacher,Student, LearningGoal, LearningCategory, Lesson, LessonType, Topic, Homework, JournalEntry
from tutor.serializers import TeacherSerializer, StudentSerializer, LearningGoalSerializer, LearningCategorySerializer,LessonSerializer, LessonTypeSerializer, TopicSerializer, HomeworkSerializer, JournalEntrySerializer
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class TeachersViewset(mixins.CreateModelMixin,mixins.ListModelMixin,GenericViewSet):
    queryset=Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentsViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['learning_category']

class LearningGoalsViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset=LearningGoal.objects.all()
    serializer_class = LearningGoalSerializer


class LearningCategoriesViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = LearningCategory.objects.all()
    serializer_class = LearningCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']

    def list(self, request, *args, **kwargs):
        slug = request.query_params.get('slug')
        logger.info(f"Запрос категории с slug: {slug}")
        if slug:
            try:
                category = self.queryset.get(slug=slug)
                serializer = self.get_serializer(category)
                logger.info(f"Найдена категория: {serializer.data}")
                return Response(serializer.data)
            except LearningCategory.DoesNotExist:
                logger.warning(f"Категория с slug {slug} не найдена")
                return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        # Применяем фильтры из django-filter
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"Возвращено {len(serializer.data)} категорий")
        return Response(serializer.data)


class LessonsViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset=Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonTypesViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset=LessonType.objects.all()
    serializer_class = LessonTypeSerializer


class TopicsViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset=Topic.objects.all()
    serializer_class = TopicSerializer

class HomeworksViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset=Homework.objects.all()
    serializer_class = HomeworkSerializer

class JournalViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset=JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer