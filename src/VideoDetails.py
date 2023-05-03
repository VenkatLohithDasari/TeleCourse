import cv2
from PIL import Image
import random


def videoDetails(file):
    vidcap = cv2.VideoCapture(file)
    # get total number of frames
    totalFrames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    duration_in_seconds = int(totalFrames / fps)
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    ffr = int(0.3*totalFrames)
    randomFrameNumber = random.randint(
        ffr, int(totalFrames-ffr))
    # set frame position
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, randomFrameNumber)
    success, image = vidcap.read()
    if success:
        if not cv2.imwrite("./temp/screenshot.jpg", image):
            raise Exception("Failed to write Image!")
        im = Image.open("./temp/screenshot.jpg")
        reso = (320, 180)
        im = im.resize(reso)
        im.save("./temp/screenshot.jpg")
        vidcap.release()
        cv2.destroyAllWindows()
    return {"thumb": "./temp/screenshot.jpg",
            "duration": duration_in_seconds,
            "width": width,
            "height": height
            }
