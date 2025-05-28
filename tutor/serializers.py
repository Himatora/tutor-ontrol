from rest_framework import serializers
from .models import Teacher, LearningGoal, LearningCategory, Student, LessonType, Topic, Lesson, Homework, JournalEntry

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'subject']

class LearningGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningGoal
        fields = ['id', 'name']

class LearningCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCategory
        fields = ['id', 'name', 'slug']

class StudentSerializer(serializers.ModelSerializer):
    learning_category = LearningCategorySerializer()
    learning_goal = LearningGoalSerializer()
    teacher = TeacherSerializer()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'grade', 'learning_goal', 'teacher', 'learning_category']

class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ['id', 'name']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']

class LessonSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    lesson_type = LessonTypeSerializer()
    topic = TopicSerializer()

    class Meta:
        model = Lesson
        fields = ['id', 'student', 'lesson_type', 'topic', 'date', 'comment']

class HomeworkSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)

    class Meta:
        model = Homework
        fields = ['id', 'lesson', 'topics', 'status', 'difficulty', 'result']

class JournalEntrySerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = JournalEntry
        fields = ['id', 'student', 'created_at', 'good_results', 'bad_results', 'covered_topics', 'working_on', 'recommended_lessons', 'recommendation_reason']