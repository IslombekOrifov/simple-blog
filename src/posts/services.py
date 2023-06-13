def upload_image_path(instance, image):
    return f"users/{instance.USERNAME_FIELD}/{instance.username}/posts/{image}"