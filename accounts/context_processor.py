from .models import UserProfile


def user_profiles(request):
    try:
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
        else:
            user_profile = None
    except UserProfile.DoesNotExist:
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.create(user=request.user)
        else:
            user_profile = None
    return dict(user_profile=user_profile)
