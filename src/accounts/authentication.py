from .models import CustomUser, Profile


class EmailAuthBackend:
    """
        authenticate by email
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (CustomUser.DoesNotExist, CustomUser.MultipleObjectsReturned):
            return None
        
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
        

def create_profile(backend, user, *args, **kwargs):
    """
    Создать профиль пользователя для социальной аутентификации
    """
    Profile.objects.get_or_create(user=user)