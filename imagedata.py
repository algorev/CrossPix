from PIL import Image

class ImageData:
    "The processed image data that should be converted into a pattern"
    size = (0, 0) #pretty self-explanatory
    palette = [(255, 255, 255)] #a list containing, in order, the rgb tuples of every color in the image palette. the background color is always palette[0]
    pixels = [[]] #a 2d array containing the color of every pixel, as the number of their color on the palette.
    counts = [] # contains how many times every colour is used in the image. useful for computing thread lengths.
    image = None

    def __init__(self, filename):
        try:
            image = Image.open(filename)
        except:
            raise Exception("Image could not be processed.")
        image = image.convert("RGB")
        self.size = image.size
        self.palette = []
        self.counts = []
        for color in image.getcolors(2048):
            self.palette.append(color[1])
            self.counts.append(color[0])
        self.image = image
        
    def set_background(self, background_color):
        self.palette.remove(background_color)
        self.palette.insert(0, background_color)
        
    def compute_pixels(self):
        self.pixels = []
        for x in range(0, self.size[0]):
            currentRow = []
            for y in range(0, self.size[1]):
                color = self.image.getpixel((x, y))
                currentRow.append(self.palette.index(color))
            self.pixels.append(currentRow)