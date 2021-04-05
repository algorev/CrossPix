import svgwrite
from imagedata import ImageData

class Pattern:
    image = None
    size = (0, 0)
    canvas = None
    scale = 20
    gridcolor = svgwrite.rgb(200, 200, 200)
    textcolor = svgwrite.rgb(128, 128, 128)

    def __init__(self, filename, image):
        self.image = image
        self.size = image.size
        self.canvas = svgwrite.Drawing(filename, profile='tiny', size=((self.size[0]+1)*self.scale, (self.size[1]+1)*self.scale))
    
    def write(self):
        self.canvas.save()
    
    def grid(self): #what the fuck have i done
        def drawsquares():    
            for x in range(0, self.size[0]+1):
                xcoord = x * self.scale
                self.canvas.add(self.canvas.line((xcoord, 0), (xcoord, (self.size[1] + 1)*self.scale), stroke=self.gridcolor))
            for y in range(0, self.size[1]+1):
                ycoord = y * self.scale
                self.canvas.add(self.canvas.line((0, ycoord), ((self.size[0] + 1)*self.scale, ycoord), stroke=self.gridcolor))
            self.canvas.add(
                self.canvas.line(
                    ((self.size[0]+1)*self.scale, 0),
                    ((self.size[0]+1)*self.scale, (self.size[1])*self.scale),
                    stroke=self.gridcolor))
            self.canvas.add(
                self.canvas.line(
                    (0, (self.size[1]+1)*self.scale),
                    ((self.size[0])*self.scale, (self.size[1]+1)*self.scale),
                    stroke=self.gridcolor))
        def addnumbers(): #this is the most horrible thing i've written in my entire life
            for x in range(0, self.size[0]):
                if x <= 8:
                    self.canvas.add(
                    svgwrite.text.Text(str(x+1),
                        ((x*self.scale)+(self.scale/3),
                        ((self.size[1]+1)*self.scale)-(self.scale/4)),
                        fill=self.textcolor))
                else:
                    self.canvas.add(
                    svgwrite.text.Text(str(x+1),
                    ((x*self.scale)+(self.scale/10),
                    ((self.size[1]+1)*self.scale)-(self.scale/4)),
                    fill=self.textcolor))
            for y in range(0, self.size[1]):
                if y <= 8:
                    self.canvas.add(
                    svgwrite.text.Text(str(y+1),
                        ((((self.size[0]+1)*self.scale)-2*(self.scale/3)),
                        (y*self.scale)+4*(self.scale/5)),
                        fill=self.textcolor))
                else:
                    self.canvas.add(
                    svgwrite.text.Text(str(y+1),
                    (((self.size[0]+1)*self.scale)-9*(self.scale/10),
                    (y*self.scale)+4*(self.scale/5)),
                    fill=self.textcolor))
        drawsquares()
        addnumbers()
    
    def fill_squares(self):
        size = (self.scale, self.scale)
        def fill_color(coords, color):
            shade = image.palette[color] # didn't think i'd ever write this one
            shade = svgwrite.rgb(shade[0], shade[1], shade[2]) # neither this one
            self.canvas.add(
                svgwrite.shapes.Rect(
                    coords,
                    size,
                    fill=shade
                )
            )
        def fill_glyph(coords, color):
            filename = "Glyphs/" + str(color) + ".svg" # background color does not have a glyph, this is on purpose
            newcoords = (coords[0] + self.scale/4, coords[1] + self.scale/4)
            newsize = (self.scale / 2, self.scale / 2)
            glyph = svgwrite.image.Image(filename, newcoords, newsize)
            glyph.stretch()
            self.canvas.add(glyph)
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]): #i'm not making the same mistake as above LET'S TAKE IT SLOW
                coords = (x * self.scale, y * self.scale)
                color = image.pixels[x][y] # didn't think i'd ever write this one
                fill_color(coords, color)
                fill_glyph(coords, color)
                

if __name__ == "__main__":
    image = ImageData("image.png")
    image.set_background((172, 50, 50))
    image.compute_pixels()
    grille = Pattern('grid.svg', image)
    grille.fill_squares()
    grille.grid()
    grille.write()