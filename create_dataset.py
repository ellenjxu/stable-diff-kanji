# convert svg images into raster (pixel) images indexed by character code

import lxml.etree as ET
import cairosvg
from PIL import Image
from io import BytesIO
import os

xml_file = 'kanjivg-20220427.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

images_dir = 'images/'
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

characters = root.findall('.//kanji')
print(f"{len(characters)} characters")

def char_to_image(character, directory):
    """Wraps character in svg tag, converts to png, and saves to directory"""
    svg = ET.tostring(character)
    svg_root = ET.fromstring(svg)
    for path in svg_root.iter('path'): # make sure closed shapes are not infilled
        path.set('fill', 'none')
        path.set('stroke', 'black')

    svg_str = ET.tostring(svg_root).decode('utf-8')
    svg_data = f"<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 100 100'>{svg_str}</svg>"
    image_data = cairosvg.svg2png(svg_data)
    image = Image.open(BytesIO(image_data))
    character_id = character.get('id').split(':')[-1].split('_')[1]
    image.save(os.path.join(directory, f"{character_id}.png"))

for char in characters:
    char_to_image(char, images_dir)

# open sample image
image = Image.open(os.path.join(images_dir, '091d6.png'))
image.show()