import PIL.Image

# scale ascii chars for more detail. i.e. make chars smaller to fit more in same screen space
# for pngs, when grayscale value 0, make ascii char empty space, not max bright
# image getting flipped upside down?
# understand the list comprehension stuff

def getAscii():
    ASCII = []
    with open("ascii_grayscale.txt", 'r') as ascii_txt:
        for line in ascii_txt:
            for char in line:
                ASCII+=char

    return(ASCII)


def getImage():
    fn = input("enter image to convert: ")
    try:
        img = PIL.Image.open(fn)
    except:
        print(fn, "not a valid file name in the directory")

    # resize the image
    width, height = img.size
    ratio = height/width/1.65
    new_width = 1000
    new_height = int(new_width*ratio)
    resized_img = img.resize((new_width, new_height))

    # convert to grayscale
    gs_img = resized_img.convert("L")

    return (gs_img)

def convertAscii(gs_img, ASCII):
    pixels = gs_img.getdata()
    #wtf list comprehension
    chars = "".join([ASCII[pixel//25] for pixel in pixels])
    return(chars)

if __name__ == "__main__":
    # prepare image into raw data
    temp_ASCII = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
    img_data = convertAscii(getImage(), getAscii())

    num_pixels = len(img_data)
    new_width = 1000
    ascii_img = "\n".join(img_data[i:(i+new_width)] for i in range(0, num_pixels, new_width))
    
    with open("result.txt", "w") as result:
        result.write(ascii_img)