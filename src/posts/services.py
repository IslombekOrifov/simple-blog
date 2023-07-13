def upload_image_path(instance, image):
    return f"users/{instance.author.username}/posts/image/{image}"

def upload_video_path(instance, video):
    return f"users/{instance.author.username}/posts/video/{video}"