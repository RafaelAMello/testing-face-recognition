import requests
from draw_face import initialize_draw, show_draw, draw_face, BLUE, RED

def upload_picture(url, file_path):
    headers = {"Accept" : "application/json; charset=utf-8"}
    files = {'file': open(file_path,'rb')}
    response = requests.post("http://localhost:8080/facebox/check", headers=headers, files=files)
    print(f"Response: {response.json()}")
    assert response.json()['success']
    return response.json()

def process_faces(file_path):
    payload = upload_picture("http://localhost:8080/facebox/check", file_path)
    draw, pil_image = initialize_draw(file_path=file_path)
    for face in payload['faces']:
        print(payload)
        top = face['rect']['top']
        left = face['rect']['left']
        right = left + face['rect']['width']
        bottem = top + face['rect']['height']
        color = BLUE if face['matched'] else RED
        draw_face(draw, "rafael", color, top, right, bottem, left)
    show_draw(draw, pil_image)

def process_image_tags(file_path):
    payload = upload_picture("http://localhost:8080/facebox/check", file_path)


