import requests
from glob import glob
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
    has_face = False
    for face in payload['faces']:
        has_face = True
        print(payload)
        top = face['rect']['top']
        left = face['rect']['left']
        right = left + face['rect']['width']
        bottem = top + face['rect']['height']
        if face['matched']:
            color = BLUE
            name = face['name']
        else:
            color = RED
            name = 'Unknown'
        draw_face(draw, name, color, top, right, bottem, left)
    if has_face:
        show_draw(draw, pil_image)
    return payload

def train_faces(person):
    headers = {"Accept" : "application/json; charset=utf-8"}
    for picture_path in glob(f"train/{person}/*.jpg"):
        params = {'name' : person, 'id' : picture_path.split('/')[-1]}
        files = {'file': open(picture_path,'rb')}
        response = requests.post("http://localhost:8080/facebox/teach", params=params, headers=headers, files=files)
        print(response)
        assert response.status_code == 200, f"Response: {response.json()}, {picture_path}"
        print(response.json())