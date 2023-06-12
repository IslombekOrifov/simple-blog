

def upload_avatar_path(instance, avatar):
    return f"users/{instance.USERNAME_FIELD}/{instance.username}/avatar/{avatar}"
