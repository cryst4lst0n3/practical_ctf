from PIL import Image
import random

img = Image.new('RGB', (21, 21))
pixels = img.load()

for y in range(21):
    for x in range(21):
        pixels[x, y] = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

img.save('data.png')
print(img.size)