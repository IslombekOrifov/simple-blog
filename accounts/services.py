

def upload_avatar_path(instance, avatar):
    return f"users/{instance.USERNAME_FIELD}/avatar/{avatar}"
