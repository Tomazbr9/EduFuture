from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime
import os

MEDIA_PATH = Path(__file__).parent.parent / 'media'
print(os.path.exists(MEDIA_PATH / 'logo'/ 'logo edufuture.png'))

def generate_certificate(student_name, course_name):
    MEDIA_PATH = Path(__file__).parent.parent / 'media'
    MODEL_PATH = MEDIA_PATH / 'model_certificate' / 'modelo_certificado.jpg'
    SAVE_IN = MEDIA_PATH / 'certificates'
    FONT_PATH = MEDIA_PATH / 'fonts' / 'GreatVibes-Regular.ttf'
    font_size_name = 100
    font_size_course = 60
    font_size_date = 50

    certificate = Image.open(MODEL_PATH)
    draw = ImageDraw.Draw(certificate)

    font_name = ImageFont.truetype(str(FONT_PATH), font_size_name)
    font_course = ImageFont.truetype(str(FONT_PATH), font_size_course)
    font_date = ImageFont.truetype(str(FONT_PATH), font_size_date)

    name_pos = (certificate.width // 2, 450)
    course_pos = (certificate.width // 2, 600)
    date_pos = (certificate.width // 2, 750)

    draw.text(name_pos, student_name, font=font_name, fill='black', anchor='mm')
    draw.text(course_pos, course_name, font=font_course, fill='black', anchor='mm')
    draw.text(date_pos, datetime.now().strftime("%d/%m/%Y"), font=font_date, fill='black', anchor='mm')

    certificate_path = SAVE_IN / f'certificado_{student_name}_{course_name}.jpg'
    certificate.save(certificate_path)
    return certificate_path