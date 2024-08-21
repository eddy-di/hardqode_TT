from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, GroupCustomUsers
from users.models import Balance, Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk=None):
        """Покупка доступа к курсу (подписка на курс)."""

        user = self.request.user
        balance_inst = get_object_or_404(Balance, user=user)
        course = get_object_or_404(Course, pk=pk)
        price = course.price
        if balance_inst.bonus < price:
            return Response(
                {'detail':'Low balance.'},
                status=status.HTTP_418_IM_A_TEAPOT
            )
        balance_inst.bonus -= price
        balance_inst.save()

        subscription = Subscription.objects.create(
            user=user,
            course=course,
            amount_paid=price
        )
        subscription.save()

        groups = course.groups.all()
        valid_groups = [
            {'group': group, 'users_count': group.users.count()}
            for group in groups
            if 0 <= group.users.count() < 30
        ]
        if valid_groups:
            min_group = min(valid_groups, key=lambda x: x['users_count'])

            GroupCustomUsers.objects.create(group=min_group['group'], user=user)

            serializer = SubscriptionSerializer(instance=subscription)
            data = serializer.data
            return Response(
                data=data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'detail': 'All groups are full for this course.'},
            status=status.HTTP_400_BAD_REQUEST
        )
