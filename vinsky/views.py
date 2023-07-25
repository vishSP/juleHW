from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser

from users.serializers import PaymentSerializer
from vinsky.models import Сourse, Lesson, Payments, Subscription
from vinsky.pagination import MaterialsPagination
from vinsky.permissions import IsModerator, IsOwner

from vinsky.serializers import СourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer, \
    PaymentIntentCreateSerializer, PaymentMethodCreateSerializer, PaymentIntentConfirmSerializer
from vinsky.services import StripeService


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
        serializer.save(user=self.request.user)


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
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_type']
    ordering_fields = ['payment_date']
    permission_classes = [IsModerator | IsOwner]


class PaymentsDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsModerator | IsOwner | IsAdminUser]


class SubscriptionCreateView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDeleteView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class PaymentIntentCreateView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentIntentCreateSerializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data['course_id']
            user_id = request.user.id
            try:
                payment_intent = StripeService.create_payment_intent(course_id, user_id)
                payment = Payments.objects.get(payment_intent_id=payment_intent['id'])
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentMethodCreateView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):

        serializer = PaymentMethodCreateSerializer(data=request.data)
        if serializer.is_valid():
            payment_intent_id = serializer.validated_data['payment_intent_id']
            payment_token = serializer.validated_data['payment_token']
            try:
                StripeService.connection(payment_intent_id, payment_token)
                payment = Payments.objects.get(payment_intent_id=payment_intent_id)
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentIntentConfirmView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):

        serializer = PaymentIntentConfirmSerializer(data=request.data)
        if serializer.is_valid():
            payment_intent_id = serializer.validated_data['payment_intent_id']
            try:
                StripeService.confirm_payment_intent(payment_intent_id)
                payment = Payments.objects.get(payment_intent_id=payment_intent_id)
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
