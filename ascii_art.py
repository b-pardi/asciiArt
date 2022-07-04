from PIL import Image
from PIL import ImageOps
import sys
import math
from pathlib import Path
import os
import time

# grab ascii chars from text file
ASCII = []
with open("ascii_grayscale.txt", 'r') as ascii_txt:
    for line in ascii_txt:
        for char in line:
            ASCII+=char

# open the images
path = Path.joinpath(Path.cwd(), "images")
imgs = [img for img in path.iterdir()]
for fp in imgs:
    start = time.time()
    try:
        img = Image.open(fp)
        img = ImageOps.exif_transpose(img)
        #img.save('tempZ.png')
    except:
        print(fp, "not a valid file name in the directory")
        sys.exit()
    
    result = open(f"results/ascii-{os.path.basename(fp)}.txt", "w")

    # PIL handles pngs and jpg differently
    isjpg = False
    ispng = False
    if img.format == "PNG":
        ispng = True
        ASCII.insert(0, ' ')
    elif img.format == "JPEG":
        isjpg == True

    # resize image using ratio and defined new height
    width, height = img.size
    # take into account the aspect ratio of an individual pixel
    pixel_ratio = 2.25
    ratio = width/height*pixel_ratio
    new_height = 200
    new_width = int(ratio*new_height)
    print(f"w: {new_width}; h: {new_height}")
    img = img.resize((int(new_width), new_height), Image.Resampling.NEAREST)

    # load pixels
    pxs = img.load()
    for i in range(new_height):
        for j in range(new_width):
            # convert image to grayscale
            r, g, b, *kwargs = pxs[j,i]
            gs = int((r + g + b) / 3)
            pxs[j,i] = (gs, gs, gs)
            # assign light value to a corresponding char in ASCII
            assg_ratio = len(ASCII) / 256
            assg_ind = math.floor(gs * assg_ratio)
            c = ASCII[assg_ind]
            result.write(c)
        result.write('\n')

    # close output file
    result.close()
    end = time.time()
    print(end-start)