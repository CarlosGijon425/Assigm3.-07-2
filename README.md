 def _init_(self, root):
        self.root = root
        self.root.title("Simple Image Editor")
        
        self.image = None
        self.display_image = None
        self.cropped_image = None
        self.rect_start = None
        self.rect_end = None
        self.is_drawing = False

        # Buttons
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.crop_button = tk.Button(self.root, text="Crop Image", command=self.start_crop)
        self.crop_button.pack()

        # Canvas to display image
        self.canvas = tk.Canvas(self.root, bg='gray', width=600, height=400)
        self.canvas.pack()

        # Mouse event bindings
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg;.png;*.jpeg")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image = self.image
            self.display_thumbnail(self.image)

    def display_thumbnail(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_thumbnail = img_pil.resize((200, 200))  # Resize to a thumbnail
        img_tk = ImageTk.PhotoImage(img_thumbnail)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk  # Keep reference

    def start_crop(self):
        if self.image is not None:
            self.is_drawing = True
            self.canvas.delete("all")
            self.display_thumbnail(self.image)

    def on_press(self, event):
        if self.is_drawing:
            self.rect_start = (event.x, event.y)

    def on_drag(self, event):
        if self.is_drawing and self.rect_start:
            self.canvas.delete("rectangle")
            self.rect_end = (event.x, event.y)
            self.canvas.create_rectangle(self.rect_start[0], self.rect_start[1], self.rect_end[0], self.rect_end[1], outline="red", tags="rectangle")

    def on_release(self, event):
        if self.is_drawing:
            self.is_drawing = False
            self.rect_end = (event.x, event.y)
            self.crop_image()

    def crop_image(self):
        if self.rect_start and self.rect_end:
            x1, y1 = self.rect_start
            x2, y2 = self.rect_end
            self.cropped_image = self.image[y1:y2, x1:x2]
            self.display_cropped_image()

    def display_cropped_image(self):
        if self.cropped_image is not None:
            img_rgb = cv2.cvtColor(self.cropped_image, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_resized = img_pil.resize((300, 300))  # Resize for display
            img_tk = ImageTk.PhotoImage(img_resized)
            self.canvas.create_image(400, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk  # Keep reference

    def save_image(self):
        if self.cropped_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if file_path:
                cv2.imwrite(file_path, self.cropped_image)
                messagebox.showinfo("Save", "Image saved successfully!")

# Initialize Tkinter window
root = tk.Tk()
app = SimpleImageEditor(root)
root.mainloop()
