from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class LearningGoalViewSet(viewsets.ModelViewSet):
    queryset = LearningGoal.objects.all()
    serializer_class = LearningGoalSerializer


class LearningCategoriesViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = LearningCategory.objects.all()
    serializer_class = LearningCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class LessonTypeViewSet(viewsets.ModelViewSet):
    queryset = LessonType.objects.all()
    serializer_class = LessonTypeSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class JournalViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalSerializer
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        student_id = request.data.get('student_id')
        lessons_count = request.data.get('lessons_count', 5)
        
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)
        
        # Получаем последние N уроков
        lessons = Lesson.objects.filter(student=student).order_by('-date')[:lessons_count]
        
        # Собираем данные для журнала
        goals = student.learning_goal.name
        covered_topics = ", ".join(set(lesson.topic.name for lesson in lessons))
        
        # Анализируем домашние задания
        problem_topics = []
        for lesson in lessons:
            try:
                homework = Homework.objects.get(lesson=lesson)
                if homework.result and homework.result < 50:
                    problem_topics.append(lesson.topic.name)
            except Homework.DoesNotExist:
                continue
        
        working_on = ", ".join(set(problem_topics)) if problem_topics else "нет данных"
        
        # Рассчитываем рекомендуемый объем занятий
        recommended_lessons = 5 if len(problem_topics) >= 3 else 3
        recommendation_reason = f"Рекомендуется {recommended_lessons} занятий, так как есть темы с низким процентом выполнения: {working_on}" if problem_topics else "Рекомендуется стандартный объем занятий"
        
        # Создаем запись в журнале
        JournalEntry = JournalEntry.objects.create(
            student=student,
            goals=goals,
            covered_topics=covered_topics,
            working_on=working_on,
            recommended_lessons=recommended_lessons,
            recommendation_reason=recommendation_reason
        )
        
        serializer = self.get_serializer(JournalEntry)
        return Response(serializer.data)