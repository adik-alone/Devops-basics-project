from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ReminderViewSet

app_name = "reminders_api"

urlpatterns = [
    # login and register
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # reminder api
    path('reminders/', ReminderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('notes/<int:pk>', ReminderViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
]
