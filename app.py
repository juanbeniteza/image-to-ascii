import sys
import os
from PIL import Image


ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255
MAX_HEIGHT = 100  # Higher values dont fit well in the console


def build_pixel_matrix(image):

    if image.height > MAX_HEIGHT:
        half_height = image.height // 2
        new_height = half_height if half_height <= MAX_HEIGHT else MAX_HEIGHT
        new_width = int(new_height * image.width / image.height)  # Conserving ratio

        image = image.resize((new_width, new_height), Image.ANTIALIAS)  # We resize the image

    # To build the pixel matriz we get the average of the pixel, each pixel in the image has the format (R, G, B)
    pixel_matrix = [[(sum(image.getpixel((x, y))) / 3) for x in range(image.width)] for y in range(image.height)]
    return pixel_matrix


def convert_to_ascii(pixel_matrix):

    # We try to map our pixels in the matrix to the ascii list
    # for this we do a cross-multiplication
    # P -->  MAX_PIXEL_VALUE
    # ? ---> len(ASCII_CHARS)
    # We rest 1 at the end so we dont get an index out of range when ? is the last element in the ASCII_CHARS
    ascii_matrix = []
    for row in pixel_matrix:
        ascii_row = []
        for pixel in row:
            ascii_row.append(ASCII_CHARS[int(len(ASCII_CHARS)*(pixel/MAX_PIXEL_VALUE)-1)])
        ascii_matrix.append(ascii_row)

    return ascii_matrix


def ascii_art(ascii_matrix, filename=None):

    if filename:
        filename = f'{filename}.txt'
        with open(filename, 'w') as f:
            for row in ascii_matrix:
                line = [p for p in row]
                f.write("".join(line)+'\n')

    else:
        for row in ascii_matrix:
            line = [p for p in row]
            print("".join(line))


if __name__ == "__main__":

    filepath = sys.argv[1]
    options = [opt for opt in sys.argv[1:] if opt.startswith("-")]

    filename = None

    if '-f' in options:
        filename = os.path.splitext(filepath)[0]

    try:
        image = Image.open(filepath)
    except:
        raise SystemExit(f"File was not found.")

    pixel_matrix = build_pixel_matrix(image)

    ascii_matrix = convert_to_ascii(pixel_matrix)
    ascii_art(ascii_matrix, filename)
