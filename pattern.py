import svgwrite

class Pattern:
    size = (0, 0)
    canvas = None
    scale = 20
    gridcolor = svgwrite.rgb(200,200, 200)
    textcolor = svgwrite.rgb(128, 128, 128)

    def __init__(self, filename, size):
        self.size = size
        self.canvas = svgwrite.Drawing(filename, profile='tiny', size=((size[0]+1)*self.scale, (size[1]+1)*self.scale))
    
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
                        stroke=self.textcolor))
                else:
                    self.canvas.add(
                    svgwrite.text.Text(str(x+1),
                    ((x*self.scale)+(self.scale/10),
                    ((self.size[1]+1)*self.scale)-(self.scale/4)),
                    stroke=self.textcolor))
            for y in range(0, self.size[1]):
                if y <= 8:
                    self.canvas.add(
                    svgwrite.text.Text(str(y+1),
                        ((((self.size[0]+1)*self.scale)-2*(self.scale/3)),
                        (y*self.scale)+4*(self.scale/5)),
                        stroke=self.textcolor))
                else:
                    self.canvas.add(
                    svgwrite.text.Text(str(y+1),
                    (((self.size[0]+1)*self.scale)-9*(self.scale/10),
                    (y*self.scale)+4*(self.scale/5)),
                    stroke=self.textcolor))
        drawsquares()
        addnumbers()

if __name__ == "__main__":
    grille = Pattern('grid.svg', (10, 10))
    grille.grid()
    grille.write()