# -*- coding: utf-8 -*-
"""clean_OMR.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XDqkbp5CAqBwv8IxitoT93DfIwDp39X2

Libraries to install and pip install
"""

#!pip install lilypond
#!sudo apt install -y fluidsynth
#!pip install fluidsynth

#to load Model
from transformers import AutoProcessor, AutoTokenizer, AutoModelForImageTextToText

from PIL import Image
import torch

import subprocess
import lilypond

import os
import fluidsynth
import platform

tokenizer = AutoTokenizer.from_pretrained("Flova/omr_transformer")
processor = AutoProcessor.from_pretrained("Flova/omr_transformer")
model = AutoModelForImageTextToText.from_pretrained("Flova/omr_transformer")

image_path = "test7.png"
image = Image.open(image_path)
image = image.convert("RGB")
inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
  outputs = model.generate(**inputs)

caption = processor.decode(outputs[0], skip_special_tokens=True)

#print(f"Generated Caption: {caption}")

with open("test7.ly", "w") as f:
    f.write("\score { \midi{} \layout{} {" + caption + "}}")


subprocess.run([lilypond.executable(), "test7.ly"])

command = [
    "fluidsynth",
    "-ni",
    "sound.sf2",
    "test7.midi",
    "-F", "ouptut.wav",
    "-r", "48000"
]
subprocess.run(command, check=True)


#fluidsynth -ni sound.sf2 test7.midi -F output.wav -r 48000
