# Creates Kanji <-> English description dataset

import lxml.etree as ET
import cairosvg
from PIL import Image
from io import BytesIO
import os

# 1. convert svg images into raster (pixel) images indexed by character code
xml_file = 'kanjivg-20220427.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

data_dir = 'data/'
images_dir = data_dir + 'images/'
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

characters = root.findall('.//kanji')
print(f"{len(characters)} characters")

def svg_to_image(character, directory):
    """Wraps character in svg tag, converts to png, and saves to directory"""
    svg = ET.tostring(character)
    svg_root = ET.fromstring(svg)
    for path in svg_root.iter('path'): # make sure closed shapes are not infilled
        path.set('fill', 'none')
        path.set('stroke', 'black')

    svg_str = ET.tostring(svg_root).decode('utf-8')
    svg_data = f"<svg xmlns='http://www.w3.org/2000/svg' width='128' height='128' viewBox='0 0 100 100'>{svg_str}</svg>"
    image_data = cairosvg.svg2png(svg_data)
    image = Image.open(BytesIO(image_data))
    character_id = character.get('id').split(':')[-1].split('_')[1]
    image.save(os.path.join(directory, f"{character_id}.png"))

for char in characters:
    svg_to_image(char, images_dir)

# open sample image
# image = Image.open(os.path.join(images_dir, '091d6.png'))
# image.show()

# 2. save english descriptions to descriptions.txt
xml_text_file = 'kanjidic2.xml'
tree = ET.parse(xml_text_file)
root = tree.getroot()

descriptions = root.findall('.//character')
print(len(descriptions))

for desc in descriptions:
    # get all <meaning> elements without a language attribute
    meanings = desc.findall('.//meaning')
    english_meanings = [elem.text for elem in meanings if 'm_lang' not in elem.attrib]
    
    # get <cp_value> with cp_type="ucs"
    ucs_id = desc.find(".//cp_value[@cp_type='ucs']")
    
    # get english eaning and save to description.txt
    # format: ucs_id.png|english meaning 1|english meaning 2|...
    if os.path.exists(f"{images_dir}/{ucs_id.text.zfill(5)}.png"):
        with open(f"{data_dir}/descriptions.txt", "a") as f:
            f.write(f"{ucs_id.text.zfill(5)}.png|{'|'.join(english_meanings)}\n")
