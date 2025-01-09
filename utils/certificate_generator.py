from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime

def generate_certificate(student_name, course_name):
    MEDIA_PATH = Path(__file__).parent.parent / 'media'
    MODEL_PATH = MEDIA_PATH / 'model_certificate' / 'modelo_certificado.jpg'
    SAVE_IN = MEDIA_PATH / 'certificates'
    font = 'arial.ttf'
    font_size = 50

    certificate = Image.open(MODEL_PATH)
    draw = ImageDraw.Draw(certificate)

    font_name = ImageFont.truetype(font, font_size)
    font_outhers = ImageFont.truetype(font, int(font_size * 0.6))

    name_pos = (400, 300)
    draw.text(name_pos, student_name, font=font_name, fill='black')

    course_pos = (400, 400)
    draw.text(course_pos, course_name, font=font_outhers, fill='black')

    date_pos = (400, 500)
    date = datetime.now()
    draw.text(date_pos, f"{date}", font=font_outhers, fill='black')
    
    certificate_path = SAVE_IN / f'certificado_{student_name}_{course_name}.jpg'
    certificate.save(certificate_path)
    return certificate_path
    