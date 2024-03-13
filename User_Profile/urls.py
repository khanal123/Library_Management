from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'User',UserRegisteredView,basename='Userlist')
# router.register(r'Login',LoginViewSet,basename='Userlist')
router.register(r'Login',LoginViewSet,basename='UserLoginList')


urlpatterns=[
    # path('', api_root, name = 'api-root'),
    path('api/',include(router.urls)),
    # path('profile/',UserProfileListCreateView.as_view(),name='profile-list-create'),
    # path('profile/<int:pk>/',UserProfileDetailView.as_view(),name='profile-detail'),  
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('signup/', SignUpView.as_view(), name='signup'),
    # path('login/', LoginViewSet.as_view({'post':'add'}), name='login'),
]
