from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser
from vinsky.tasks import notify_course_updates, notify_lesson_updates
from users.serializers import PaymentSerializer
from vinsky.models import Сourse, Lesson, Payments, Subscription
from vinsky.pagination import MaterialsPagination
from vinsky.permissions import IsModerator, IsOwner

from vinsky.serializers import СourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer, \
    PaymentIntentCreateSerializer, PaymentMethodCreateSerializer, PaymentIntentConfirmSerializer
from vinsky.services import StripeService, StripeServiceError


class СourseViewSet(viewsets.ModelViewSet):
    pagination_class = MaterialsPagination
    serializer_class = СourseSerializer
    queryset = Сourse.objects.all()
    permission_classes = [IsAdminUser | IsModerator | IsOwner]

    def perform_update(self, serializer):
        self.object = serializer.save()
        notify_course_updates.delay(self.object.pk)


class LessonListAPIView(generics.ListAPIView):
    pagination_class = MaterialsPagination
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]

    def perform_update(self, serializer):
         self.object = serializer.save()
         notify_lesson_updates.delay(self.object.pk)

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
    ordering_fields = ['payday']
    permission_classes = [IsModerator | IsOwner]

    class StripeServiceError(APIException):
        status_code = 400
        default_detail = 'Ошибка сервиса Stripe'
        default_code = 'stripe_error'


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
        serializer.is_valid(raise_exception=True)
        try:
            course = serializer.validated_data['course']
            user_id = request.user

            payment_intent = StripeService.create_payment_intent(course, user_id)
            payment = Payments.objects.get(payment_intent_id=payment_intent['id'])
        except StripeServiceError as e:
            raise StripeServiceError(detail=str(e))

        except Payments.DoesNotExist:
            raise APIException(detail='Платеж не найден')
        else:
            data = PaymentSerializer(payment).data
            status_code = status.HTTP_201_CREATED

            return Response(data, status=status_code)


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
