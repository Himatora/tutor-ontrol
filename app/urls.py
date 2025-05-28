"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from rest_framework.routers import DefaultRouter
from tutor.api import TeachersViewset,StudentsViewset, LearningGoalsViewset, LearningCategoriesViewset,LessonsViewset, LessonTypesViewset, TopicsViewset, HomeworksViewset, JournalViewset

router=DefaultRouter()
router.register(r'teachers', TeachersViewset)
router.register(r'learning-goals', LearningGoalsViewset)
router.register(r'learning-categories', LearningCategoriesViewset)
router.register(r'students', StudentsViewset)
router.register(r'lesson-types', LessonTypesViewset)
router.register(r'topics', TopicsViewset)
router.register(r'lessons', LessonsViewset)
router.register(r'homework', HomeworksViewset)
router.register(r'journal', JournalViewset)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
]
