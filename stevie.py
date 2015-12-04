import argparse
import io
import random
import time
import urllib.request

import PIL.Image


# This is the zoom level. Given an image of size 2500px x 1667px we
# usually use a viewer size of 525px x 350px. This results in each pixel
# of the viewer to represent 4.7619047619px x 4.7628571429px. The zoom level
# can now be used to decrease the ratio up to 1/8 resulting in a representation
# of 0.5952380952px x 0.5953571429px.
# The parameters x0 and y0 start at the top left of the image and
# represent the top left of the viewer. They can also be negative.
# The image returned by the API still contains a watermark. But we
# crop the returned viewer and only take the part below the watermark.
# The stepsize is not perfectly correct now but could be computed
# given the information presented above.
Z = 8


def open_fragment(prefix, id, x, y, width, height):
    """
    :type prefix: str
    :type id: int
    :type x: int
    :type y: int
    :type width: int
    :type height: int
    :rtype: Image
    """
    url = "{}?id={}&x1=0&x0={}&y1=0&y0={}&z={}&width={}&height={}".format(prefix, id, x, y, Z, width, height)
    req = urllib.request.urlopen(url)
    data = req.read()

    print(url)

    return PIL.Image.open(io.BytesIO(data))


def download_loop(prefix, id, width, height, x0_delta, x0_max, y0_delta, y0_max, crop_x_norm, crop_x_last, crop_y_norm,
                  crop_y_last):
    x0 = 0
    y0 = -y0_delta*3

    full_image = PIL.Image.new("RGB", (4100, 4100))
    full_x = 0
    full_y = 0

    while y0 < y0_max:
        x0 = 0
        full_x = 0

        if (y0 + y0_delta) < y0_max:
            crop_y = crop_y_norm
        else:
            crop_y = crop_y_last

        while x0 < x0_max:
            with open_fragment(prefix, id, x0, y0, width, height) as img:
                if (x0 + x0_delta) < x0_max:
                    crop_x = crop_x_norm
                else:
                    crop_x = crop_x_last

                img = img.crop((crop_x, crop_y, width, height))
                full_image.paste(img, (full_x, full_y))
                img.close()

            x0 += x0_delta
            full_x += width - crop_x

            time.sleep(.5 + random.uniform(0, .5))

        y0 += y0_delta
        full_y += height - crop_y

    return full_image.crop((0, 0, full_x, full_y))


def download_portrait(prefix, id):
    width = 350
    height = 525

    x0_delta = 40  # 64
    x0_max = 320 + 10

    y0_delta = 40  # 90 #128
    y0_max = 480 + 10

    crop_x = 30
    crop_x_last = 141

    crop_y = 204
    crop_y_last = 371

    img = download_loop(prefix, id, width, height, x0_delta, x0_max, y0_delta, y0_max, crop_x, crop_x_last, crop_y,
                        crop_y_last)

    # TODO: Figure out landscape crop
    return img


def download_landscape(prefix, id):
    width = 525
    height = 350

    x0_delta = 60  # 64
    x0_max = 480 + 10

    y0_delta = 14  # 90 #128
    y0_max = 306 + 10

    crop_x = 45
    crop_x_last = 211

    crop_y = 239
    crop_y_last = 253

    img = download_loop(prefix, id, width, height, x0_delta, x0_max, y0_delta, y0_max, crop_x, crop_x_last, crop_y,
                        crop_y_last)

    return img.crop((0, 98, img.width-62, img.height))


def download_id(prefix, id):
    if id < 0:
        id = -id
        img = download_landscape(prefix, id)
    else:
        img = download_portrait(prefix, id)

    print("=== SAVING {} ===".format(id))
    img.save("{}.jpg".format(id))
    img.close()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", dest="url_base", type=str, required=True)
    parser.add_argument("ids", metavar='N', type=int, nargs='+',
                        help='list of image integers, prepend "-" for landscape')

    args = parser.parse_args()

    for id in args.ids:
        download_id(args.url_base, id)


if __name__ == '__main__':
    main()
