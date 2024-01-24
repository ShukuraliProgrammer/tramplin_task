from accounts.models import Profile


def get_profile(username):
    """This function returns profile object by username if profile exists or False"""

    profiles = Profile.objects.filter(username=username, is_active=False)
    if profiles.exists():
        return profiles.first()
    else:
        return False


def create_profile(username, phone, user_id):
    """This function creates profile object and returns it"""

    return Profile.objects.create(username=username, phone=phone, user_id=user_id)
