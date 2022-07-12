# feed from camera to ascii generator live
import numpy as np
import math
import cv2
import os

#=======================================
# Settings
is_inverted_color = False
will_show_camera = False
#=======================================
# optimization: only update frames that actually change their gs value

# open ASCII chars into ASCII array for later use
def getASCII(invert=False):
    ASCII = []
    with open("ascii_grayscale.txt", 'r') as ascii_txt:
        for line in ascii_txt:
            for char in line:
                ASCII+=char
    if invert == True:
        ASCII = ASCII[::-1]
    return ASCII

# convert each pixel data of each frame to grayscale for a light value,
# then to ASCII using that light value and num of ASCII chars as an index
def frameToASCII(frame, ASCII):
    height, width, num_channels = frame.shape
    frame_ASCII = [[0 for i in range(width)] for j in range(height)]
    for i in range(height):
        for j in range(width):
            # get pixel data from individual frame
            # NOTE that cv2 uses bgr convention instead of rgb,
            # values are uint8 so must be converted later to avoid overflow
            b, g, r, *kwarg = frame[i][j]
            # average color vals for grayscale
            gs = math.floor((int(r) + int(g) + int(b)) / 3)
            frame[i][j] = [gs, gs, gs]
            frame_ASCII[i][j] = ASCII[math.floor(gs * len(ASCII) / 256)]
    return frame_ASCII

# prints ASCII to terminal
def print_ASCII(frame_ASCII):
    # clearing screen on each print SIGNIFICANTLY reduces framerate
    os.system("clear")
    print('\n'.join((''.join(row) for row in frame_ASCII)), end='')

# cv2.CAP_DSHOW will show image with default proportion without black borders
cap = cv2.VideoCapture(0)

ASCII = getASCII(is_inverted_color)

while 1:
    # ret says if working properly, frame is the actually image data
    ret, frame = cap.read()

    # resize to much lower res since ascii doesn't need higher res
    screen_height, screen_width = os.popen('stty size', 'r').read().split()
    frame_reduced = cv2.resize(frame, (int(screen_width),int(screen_height)), interpolation = cv2.INTER_LINEAR)

    frame_ASCII = frameToASCII(frame_reduced, ASCII)
    print_ASCII(frame_ASCII)

    #cv2.imshow("frame", frame_ASCII)

    # ends script when 'q' is pressed (while cam window selected)
    if cv2.waitKey(1) == ord('q'):
        break

# release capture so another program could use
cap.release()
cv2.destroyAllWindows()