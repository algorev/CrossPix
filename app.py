from tkinter import *
import tkinter.filedialog
from imagedata import *
from PIL import ImageTk
from PIL import Image
from svgwrite import utils
from pattern import *
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM, renderPDF
import copy
import threading #can you tell this is gonna be a mess?

class App (Frame):
    file = None
    image = None
    optionContainer = None
    options = None
    paletteSelect = None
    bgcolor = None
    exportFormat = None
    black_white = None
    legend = None
    completion = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.bgcolor = IntVar()
        self.exportFormat = StringVar()
        self.black_white = IntVar()
        self.legend = IntVar()
        self.create_widgets()
    
    def create_widgets(self):
        self.openButton = Button(self)
        self.openButton["text"] = "Open an image..."
        self.openButton["command"] = self.openImage
        self.openButton.pack(pady=5)

        self.imagePreview = Label(self, text="Open an image to create a pattern.")
        self.imagePreview.pack()

        self.optionContainer = Label(self)
        self.optionContainer.pack()

        Label(self, text="Choose export format:").pack()
        self.exportFormat.set("PDF")
        self.exportOptions = OptionMenu(self, self.exportFormat, "PDF", "PNG")
        self.exportOptions.pack()

        Checkbutton(self, text="Remove Colors from Pattern", variable = self.black_white, onvalue=1, offvalue=0).pack(anchor=W)
        Checkbutton(self, text="Add Legend to Pattern", variable = self.legend, onvalue=1, offvalue=0).pack(anchor=W)

        self.confirm = Button(self, state="disabled")
        self.confirm["text"] = "Convert into Pattern"
        self.confirm["command"] = self.convert
        self.confirm.pack(pady=5)
    
    def openImage(self):
        self.file = tkinter.filedialog.askopenfile("rb")
        if self.options:
                self.options.destroy()
        if self.file:
            try:
                self.image = ImageData(self.file)
            except:
                self.confirm["state"] = "disabled"
                self.imagePreview["image"] = ""
                self.imagePreview["text"] = "Image could not be processed."
                return None
            self.options = Label(self.optionContainer)
            self.options.pack()
            photo = ImageTk.PhotoImage(image=self.image.image)
            self.imagePreview.photo = photo
            self.imagePreview["image"] = photo
            self.addPaletteButtons()
            self.confirm["state"] = "normal"
        else:
            self.confirm["state"] = "disabled"
            self.imagePreview["image"] = ""
            self.imagePreview["text"] = "Image could not be opened."
    
    def addPaletteButtons(self):
        bgcolor = IntVar()
        def colorChosen():
            pass
        if self.paletteSelect:
            for element in self.paletteSelect:
                element.destroy()
            self.paletteSelect = None
        palette = self.image.palette
        self.paletteSelect = []
        self.paletteSelect.append(Label(self.options, text=f"{len(palette)} colors detected.\nChoose background color:"))
        for color in range(0, len(palette)):
            shade = palette[color]
            self.paletteSelect.append(Radiobutton(self.options, text=f"Color {color}", variable=self.bgcolor, value=color, command=colorChosen, bg='#{:02x}{:02x}{:02x}'.format(shade[0], shade[1], shade[2])))
        for element in self.paletteSelect:
            element.pack()
        colorChosen()
    
    def convert(self):
        bg = self.bgcolor.get()
        export = self.exportFormat.get()
        filename = tkinter.filedialog.asksaveasfilename()
        if self.completion:
            self.completion.destroy()
        self.completion = Label(self, text="Processing...", wraplength=120)
        self.completion.pack()
        self.confirm["state"] = "disabled"
        def process_image(filename):
            initialPalette = copy.deepcopy(self.image.palette)
            self.image.set_background(self.image.palette[bg])
            self.image.compute_pixels()
            legend = False
            black_white = False
            if self.legend.get() == 1:
                legend = True
            else:
                legend = False
            if self.black_white.get() == 1:
                black_white = True
            else:
                black_white = False
            pattern = Pattern("_temp.svg", self.image, black_white, legend, 10)
            pattern.make_pattern()
            pattern.write()
            drawing = svg2rlg('_temp.svg')
            if export == "PDF":
                if not (filename[-4:] == ".pdf"):
                    filename += ".pdf"
                renderPDF.drawToFile(drawing, filename, " ")
            if export == "PNG":
                if not (filename[-4:] == ".png"):
                    filename += ".png"
                renderPM.drawToFile(drawing, filename, fmt='PNG')
            os.remove("_temp.svg")
            self.completion["text"] = f"Saved pattern as {filename}"
            self.confirm["state"] = "normal"
            self.image.palette = initialPalette
        self.worker = threading.Thread(target=process_image, args=(filename,))
        self.worker.start()

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    app.mainloop()