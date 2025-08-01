from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size = 10 * 1024 * 1024  # 10 MB
    if file.size > max_size:
        raise ValidationError(f"File size must be less than {max_size} bytes.")