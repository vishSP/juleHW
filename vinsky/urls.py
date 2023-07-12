from vinsky.apps import VinskyConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from vinsky.views import СourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentsCreateAPIView, PaymentsListAPIView, \
    PaymentsDetailAPIView, PaymentsUpdateAPIView, PaymentsDeleteAPIView

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
    path('payment/create/', PaymentsCreateAPIView.as_view(), name='payment_create'),
    path('paymentv/detail/<int:pk>/', PaymentsDetailAPIView.as_view(), name='payment_detail'),
    path('payment/update/<int:pk>/', PaymentsUpdateAPIView.as_view(), name='payment_update'),
    path('payment/delete/<int:pk>/', PaymentsDeleteAPIView.as_view(), name='payment_delete'),

              ] + router.urls
