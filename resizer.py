import os
from configparser import ConfigParser

from PIL import Image, ImageEnhance

if __name__ == '__main__':

    # parsing of data
    cfg = ConfigParser()
    cfg.read('data.ini')
    data = cfg["data"]
    new_width = int(data["width"])
    new_height = int(data["height"])

    for image in os.listdir(data["folder_of_input_images"]):
        instance = Image.new('RGBA', (new_width, new_height),
                             (0, 0, 0, 0))  # make a transparent background of output image
        img = Image.open(os.path.join(data["folder_of_input_images"], image)).convert("RGBA")
        watermark = Image.open(data["path_of_watermark"]).convert("RGBA")

        # the calculation of the proportional size
        if img.width / new_width > img.height / new_height:
            img = img.resize((new_width, round(img.height * new_width / img.width)))
        else:
            img = img.resize((round(img.width * new_height / img.height), new_height))
        instance.paste(img, (0, 0), img)

        # the calculation of the watermark size
        new_width_of_watermark = round(img.width * 0.3)
        new_height_of_watermark = round(img.width * 0.3 * watermark.height / watermark.width)
        watermark = watermark.resize((new_width_of_watermark, new_height_of_watermark))
        instance.paste(watermark, (0, img.height - watermark.height), watermark)

        instance = instance.save(os.path.join(data["folder_of_output_images"], image[:-4] + ".png"))
