from PIL import Image
import sys

ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255


def get_pixel_matrix(img):
    img.thumbnail((100, 100))
    pixels = list(img.getdata())
    return [pixels[i:i+img.width] for i in range(0, len(pixels), img.width)]


def get_intensity_matrix(pixels_matrix):
    intensity_matrix = []
    for row in pixels_matrix:
        intensity_row = []
        for p in row:
            intensity = (p[0] + p[1] + p[2] / 3.0)
            intensity_row.append(intensity)
        intensity_matrix.append(intensity_row)

    return intensity_matrix


def normalize_intensity_matrix(intensity_matrix):
    normalized_intensity_matrix = []
    max_pixel = max(map(max, intensity_matrix))
    min_pixel = min(map(min, intensity_matrix))
    for row in intensity_matrix:
        rescaled_row = []
        for p in row:
            r = MAX_PIXEL_VALUE * (p - min_pixel) / float(max_pixel - min_pixel)
            rescaled_row.append(r)
        normalized_intensity_matrix.append(rescaled_row)

    return normalized_intensity_matrix


def convert_to_ascii(intensity_matrix, ascii_chars):
    ascii_matrix = []
    for row in intensity_matrix:
        ascii_row = []
        for p in row:
            ascii_row.append(ascii_chars[int(p/MAX_PIXEL_VALUE * len(ascii_chars)) - 1])
        ascii_matrix.append(ascii_row)

    return ascii_matrix


def print_ascii_matrix(ascii_matrix):
    for row in ascii_matrix:
        line = [p for p in row]
        print("".join(line))


filepath = sys.argv[1]

img = Image.open(filepath)
pixels = get_pixel_matrix(img)

intensity_matrix = get_intensity_matrix(pixels)
intensity_matrix = normalize_intensity_matrix(intensity_matrix)

ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
print_ascii_matrix(ascii_matrix)