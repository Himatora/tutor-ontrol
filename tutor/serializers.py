from rest_framework import serializers
from .models import *

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class LearningGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningGoal
        fields = '__all__'

class LearningCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningCategory
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = '__all__'
    
    def get_lessons_count(self, obj):
        return obj.lessons_count

class HomeworkSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)
    
    class Meta:
        model = Homework
        fields = '__all__'

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'