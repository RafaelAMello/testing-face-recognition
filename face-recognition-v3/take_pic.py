from datetime import datetime

def take_picture():
    picture_time = datetime.now()
    picture_location = f"{picture_time}.jpg".replace(' ', '')
    # https://lbhtran.github.io/Camera-setting-and-photo-taking-schedule-to-get-the-best-result/
    # fswebcam -D 2 -S 20 --set Focus, Auto=False --set brightness=30% --set contrast=0%  -F 10 -r  640x480 --no-banner /home/pi/camera/$DATE.jpg
    os.system(f'fswebcam -S 20 -r 1280x730 --set "Zoom, Absolute"=500 --no-banner {picture_location}')
    return picture_location, picture_time
