from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser

from users.serializers import PaymentSerializer
from vinsky.models import Сourse, Lesson, Payments, Subscription
from vinsky.pagination import MaterialsPagination
from vinsky.permissions import IsModerator, IsOwner

from vinsky.serializers import СourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer


class СourseViewSet(viewsets.ModelViewSet):
    pagination_class = MaterialsPagination
    serializer_class = СourseSerializer
    queryset = Сourse.objects.all()
    permission_classes = [IsAdminUser | IsModerator | IsOwner]


class LessonListAPIView(generics.ListAPIView):
    pagination_class = MaterialsPagination
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'method_payment']
    ordering_fields = ['payment_date']
    permission_classes = [IsModerator | IsOwner]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAdminUser]


class PaymentsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAdminUser]


class PaymentsDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsModerator | IsOwner]


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsModerator | IsOwner]


class SubscriptionCreateView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAdminUser]


class SubscriptionDeleteView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAdminUser]


class SubscriptionUpdateView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAdminUser]
