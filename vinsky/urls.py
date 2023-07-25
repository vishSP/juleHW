from vinsky.apps import VinskyConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from vinsky.views import СourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView,  PaymentsListAPIView, \
    PaymentIntentCreateView, PaymentMethodCreateView, PaymentIntentConfirmView ,SubscriptionCreateView, SubscriptionDeleteView

app_name = VinskyConfig.name

router = DefaultRouter()

router.register(r'course', СourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/detail/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_one'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    #Payments
    path('payment/', PaymentsListAPIView.as_view(), name='payment_list'),
    path('payment-intent/create/', PaymentIntentCreateView.as_view(), name='payment_intent_create'),
    path('payment-method/create/', PaymentMethodCreateView.as_view(), name='payment_method_create'),
    path('payment-confirm/', PaymentIntentConfirmView.as_view(), name='payments_confirm'),

    #Subscription
    path('subscriptions/create/', SubscriptionCreateView.as_view(), name='subscription_create'),
    path('subscriptions/delete/<int:pk>/', SubscriptionDeleteView.as_view(), name='subscription_delete'),



              ] + router.urls
