import time
import logging
import argparse
import pygame
import os
import sys
import numpy as np
import subprocess

CONFIDENCE_THRESHOLD = 0.5
PERSISTANCE_THRESHOLD = 0.25

os.environ['SDL_FBDEV'] = "/dev/fb1"
os.environ['SDL_VIDEODRIVER'] = "fbcon"

# App
from rpi_vision.agent.capture import PiCameraStream
# Import the EfficientDet Model here

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# Initialize the display
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
capture_manager = PiCameraStream(resolution=(max(320, screen.get_width()), \
                max(240, screen.get_height())), rotation=180, preview=False)

def parse_args():
    # Add relevant arguments if needed.
    raise NotImplementedError

last_seen = [None] * 10
last_spoken = None

def main(args):
    global last_spoken

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.mouse.set_visible(False)
    screen.fill((0,0,0))

    try:
        splash = pygame.image.load(os.path.dirname(sys.argv[0]+'/passion-fruit.bmp'))
        screen.blit(splash, ((screen.get_width() / 2) - (splash.get_width() / 2),
                    (screen.get_height() / 2) - (splash.get_height() / 2)))

    except pygame.error:
        pass
    pygame.display.update()

    # Use the default font
    smallfont = pygame.font.Font(None, 24)
    medfont = pygame.font.Font(None, 36)
    bigfont = pygame.font.Font(None, 48)

    # Initialize model here
    model = None
    capture_manager.start()

    while not capture_manager.stopped:
        if capture_manager.frame is None:
            continue

        frame = capture_manager.read()
        # Get the raw data frame & swaop red & blud channels
        previewframe = np.ascontiguousarray(np.flip(np.array(capture_manager.frame), 2))

        # Make it an image
        img = pygame.image.frombuffer(np.flip(np.array(capture_manager.frame), 2))

        # Draw it
        screen.blit(img, (0,0))

        timestamp = time.monotic()

        # Model logic

        logging.info(prediction)
        delta = time.monotonic() - timestamp
        logging.info("%s inference took %d ms, %0.1f FPS" % ("TFLite" \
                    if arges.tflite else "TF", delta * 1000, 1 / delta))
        print(last_seen)

        # add FPS on top corner pf image
        fpstext = "%0.1f FPS" % (1/delta)
        fpstext_surface = smallfont.render(fpstext, True, (255, 0, 0))
        fpstext_position = (screen.get_width() - 10, 10) # Top right corner
        screen.blit(fpstext_surface, fpstext_surface.get_rect(topright=fpstext_position))

        # for p in prediction:
        #     label, name, conf = p
