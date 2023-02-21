from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

validate_phone = RegexValidator(
    regex=r'^[+]998\d{9}$',
    message="""
        Telefon raqam: 13 ta belgidan iborat bolishi kerak. P.s: +998912345678
    """
)



def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
