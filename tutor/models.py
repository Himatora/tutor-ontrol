from django.db import models

class Teacher(models.Model):
    full_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.full_name} ({self.subject})"

class LearningGoal(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name

class LearningCategory(models.Model):
    CATEGORY_CHOICES = [
        ('EGE', 'ЕГЭ'),
        ('OGE', 'ОГЭ'),
        ('SCHOOL', 'Школьная программа'),
        ('PROGRAMMING', 'Программирование'),
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()

class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    full_name = models.CharField(max_length=200)
    learning_goal = models.ForeignKey(LearningGoal, on_delete=models.PROTECT)
    learning_category = models.ForeignKey(LearningCategory, on_delete=models.PROTECT)
    grade = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.full_name

class LessonType(models.Model):
    TYPE_CHOICES = [
        ('VU', 'ВУ'),
        ('RU', 'РУ'),
    ]
    name = models.CharField(max_length=50, choices=TYPE_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()

class Lesson(models.Model):
    lesson_type = models.ForeignKey(LessonType, on_delete=models.PROTECT)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    
    @property
    def lessons_count(self):
        return Lesson.objects.filter(student=self.student).count()
    
    def __str__(self):
        return f"{self.student} - {self.topic} ({self.date})"

class Homework(models.Model):
    DIFFICULTY_CHOICES = [
        ('EASY', 'Легкий'),
        ('MEDIUM', 'Средний'),
        ('HARD', 'Сложный'),
    ]
    STATUS_CHOICES = [
        ('ASSIGNED', 'Задано'),
        ('NOT_ASSIGNED', 'Не задано'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    result = models.FloatField(null=True, blank=True)  # Процент выполнения
    
    def __str__(self):
        return f"ДЗ к уроку {self.lesson}"

class Journal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    goals = models.TextField()
    covered_topics = models.TextField()
    working_on = models.TextField()
    recommended_lessons = models.IntegerField()
    recommendation_reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Журнал для {self.student} от {self.created_at}"