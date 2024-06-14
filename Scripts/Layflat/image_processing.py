from PIL import Image, ExifTags
from datetime import datetime

def get_scaled_dimensions(image, max_width, max_height):
    width, height = image.size
    ratio = min(max_width / width, max_height / height)
    return int(width * ratio), int(height * ratio)

def correct_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            exif = dict(exif.items())
            orientation = exif.get(orientation, None)

            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return image

def convert_to_rgb(image):
    if image.mode == 'RGBA':
        return image.convert('RGB')
    return image

def get_image_date(image_path):
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if exif is not None:
            exif = dict(exif.items())
            for tag, value in exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                if decoded == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        return None
    except Exception as e:
        print(f"Fehler beim Lesen des Aufnahmedatums für {image_path}: {e}")
        return None
