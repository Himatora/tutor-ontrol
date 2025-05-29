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
    learning_category = LearningCategorySerializer(read_only=True)
    learning_goal = LearningGoalSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    
    learning_category_id = serializers.PrimaryKeyRelatedField(
        queryset=LearningCategory.objects.all(), source='learning_category', write_only=True
    )
    learning_goal_id = serializers.PrimaryKeyRelatedField(
        queryset=LearningGoal.objects.all(), source='learning_goal', write_only=True
    )
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source='teacher', write_only=True
    )

    class Meta:
        model = Student
        fields = [
            'id', 'full_name', 'grade',
            'learning_goal', 'learning_goal_id',
            'teacher', 'teacher_id',
            'learning_category', 'learning_category_id'
        ]

    def validate(self, data):
        print(f"Валидация данных студента: {data}")
        return data

class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ['id', 'name']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']

class LessonSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    lesson_type = LessonTypeSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True
    )
    lesson_type_id = serializers.PrimaryKeyRelatedField(
        queryset=LessonType.objects.all(), source='lesson_type', write_only=True
    )
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), source='topic', write_only=True
    )

    class Meta:
        model = Lesson
        fields = ['id', 'student', 'student_id', 'lesson_type', 'lesson_type_id', 'topic', 'topic_id', 'date', 'comment']

class HomeworkSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    topic_ids = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), source='topics', many=True, write_only=True
    )

    class Meta:
        model = Homework
        fields = ['id', 'lesson', 'topics', 'topic_ids', 'status', 'difficulty', 'result']

class JournalEntrySerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True
    )

    class Meta:
        model = JournalEntry
        fields = ['id', 'student', 'student_id', 'created_at', 'good_results', 'bad_results', 'covered_topics', 'working_on', 'recommended_lessons', 'recommendation_reason']