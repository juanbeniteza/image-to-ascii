from PIL import Image
import sys

ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255


def get_pixel_matrix(img):
    img.thumbnail((100, 100))
    p = list(img.getdata())
    return [p[i:i+img.width] for i in range(0, len(p), img.width)]


def get_intensity_matrix(pixels_matrix):
    im = []
    for row in pixels_matrix:
        intensity_row = []
        for p in row:
            intensity = (p[0] + p[1] + p[2] / 3.0)
            intensity_row.append(intensity)
        im.append(intensity_row)

    return im


def normalize_intensity_matrix(im):
    normalized_intensity_matrix = []
    max_pixel = max(map(max, im))
    min_pixel = min(map(min, im))
    for row in im:
        rescaled_row = []
        for p in row:
            r = MAX_PIXEL_VALUE * (p - min_pixel) / float(max_pixel - min_pixel)
            rescaled_row.append(r)
        normalized_intensity_matrix.append(rescaled_row)

    return normalized_intensity_matrix


def convert_to_ascii(im, ascii_chars):
    am = []
    for row in im:
        ascii_row = []
        for p in row:
            ascii_row.append(ascii_chars[int(p/MAX_PIXEL_VALUE * len(ascii_chars)) - 1])
        am.append(ascii_row)

    return am


def print_ascii_matrix(am):
    for row in am:
        line = [p for p in row]
        print("".join(line))


filepath = sys.argv[1]

image = Image.open(filepath)
pixels = get_pixel_matrix(image)

intensity_matrix = get_intensity_matrix(pixels)
intensity_matrix = normalize_intensity_matrix(intensity_matrix)

ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
print_ascii_matrix(ascii_matrix)