from enum import Enum


class PostStatus(Enum):
    ac = 'Active'
    na = 'Not Active'
    ar = 'Archive'
    bn = 'Banned'

    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)
    

class CommentStatus(Enum):
    ac = 'Active'
    bn = 'Banned'

    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)