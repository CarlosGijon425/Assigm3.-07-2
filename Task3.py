import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button, Scale
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Tool")
        
        self.image_label = Label(root)
        self.image_label.pack()
        
        self.load_button = Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()
        
        self.crop_button = Button(root, text="Crop Image", command=self.start_crop)
        self.crop_button.pack()
        
        self.resize_slider = Scale(root, from_=1, to=100, orient="horizontal", command=self.resize_preview)
        self.resize_slider.pack()
        
        self.save_button = Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack()
        
        self.image = None
        self.processed_image = None
        self.thumbnail = None
        self.crop_coords = None
        
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.thumbnail = cv2.resize(self.image, (200, 200))
            self.display_image(self.thumbnail)
    
    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img
    
    def start_crop(self):
        if self.image is not None:
            self.crop_coords = (50, 50, 200, 200)  # Fixed crop for now
            mask = np.ones_like(self.image) * 255
            cv2.rectangle(mask, (self.crop_coords[0], self.crop_coords[1]), (self.crop_coords[2], self.crop_coords[3]), (0, 0, 0), -1)
            self.processed_image = cv2.bitwise_and(self.image, mask)
            self.display_image(self.processed_image)
    
    def resize_preview(self, val):
        if self.processed_image is not None:
            factor = int(val) / 100.0
            degraded = cv2.GaussianBlur(self.processed_image, (int(5 * factor) * 2 + 1, int(5 * factor) * 2 + 1), 0)
            self.display_image(degraded)
    
    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
