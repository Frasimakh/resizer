import os
from configparser import ConfigParser

from PIL import Image, ImageEnhance

if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('data.ini')
    Data = cfg["Data"]
    new_width = int(Data["width"])
    new_height = int(Data["height"])
    watermark = Image.open(Data["path_of_watermark"]).convert("RGBA")

    for image in os.listdir(Data["first_folder"]):
        instance = Image.open(os.path.join(Data["first_folder"], image)).convert("RGBA")
        instance = instance.resize((new_width, new_height))

        new_width_of_watermark = round(instance.width * 0.3)
        new_height_of_watermark = round(instance.width * 0.3 * watermark.height / watermark.width)
        watermark = watermark.resize((new_width_of_watermark, new_height_of_watermark))

        instance.paste(watermark, (0, instance.height - watermark.height), watermark)
        instance = instance.save(os.path.join(Data["second_folder"], "new " + image))
