from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
# router.register('auth/signup', SignUpViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls.jwt')),
    # path('auth/token/', TokenViewSet.as_view(), name='token'),
]