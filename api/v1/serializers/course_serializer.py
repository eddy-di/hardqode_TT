from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers

from courses.models import Course, Group, Lesson
from users.models import Subscription

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    # TODO Доп. задание

    class Meta:
        model = Group
        fields = (
            'title',
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj) -> int:
        """Количество уроков в курсе."""
        return obj.lessons.all().count()

    def get_students_count(self, obj) -> int:
        """Общее количество студентов на курсе."""
        return obj.subscription.all().count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел.."""
        groups = obj.groups.all()
        group_counts = [(group.users.count() / 30) * 100 for group in groups]
        average = sum(group_counts) // len(group_counts)
        return average * 100

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        # TODO Доп. задание

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = '__all__'
    
    def create(self, validated_data):
        course = super().create(validated_data)
        
        for i in range(10):
            Group.objects.create(
                title=f'{course.title[:3].upper()}_{course.id}_G{i + 1}',
                course=course
            )
        return course
