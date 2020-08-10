from PIL import ImageDraw, Image

BLUE = (0, 0, 255)
RED = (255, 0, 0)

def initialize_draw(image=None, file_path=None):
    if file_path is None and image is not None:
        pil_image = Image.fromarray(image)
    elif file_path is not None and image is None:
        pil_image = Image.open(file_path)
    else:
        raise Exception
    return ImageDraw.Draw(pil_image), pil_image

def show_draw(draw, pil_image):
    del draw
    pil_image.show()

def draw_face(draw, name, color, top, right, bottom, left):
    draw.rectangle(((left, top), (right, bottom)), outline=color)
    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=color, outline=color)
    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

def save_face(pil_image, timestamp):
    pil_image.save(f'faces/{timestamp}.jpg')