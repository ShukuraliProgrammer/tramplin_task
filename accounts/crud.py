from accounts.models import Profile


def get_profile(username):
    profiles = Profile.objects.filter(username=username)
    if profiles.exists():
        return profiles.first()
    else:
        return False
