from django.urls import path
from .views import SignInView, SignOutView, SignUpView, ProfileEditView, ProfileEditPassword, ProfileAvatar

app_name = "myauth"

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name="sign-up"),
    path('sign-out/', SignOutView.as_view(), name="sign-out"),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('profile/', ProfileEditView.as_view(), name="profile_edit"),
    path('profile/password/', ProfileEditPassword.as_view(), name="profile_pass"),
    path('profile/avatar/', ProfileAvatar.as_view(), name="profile_avatar"),

    ]

