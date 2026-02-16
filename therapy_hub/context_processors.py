def user_profile(request):
    if request.user.is_authenticated:
        # Safely get profile, or None
        profile = getattr(request.user, 'profile', None)
        return {'user_profile': profile}
    return {'user_profile': None}