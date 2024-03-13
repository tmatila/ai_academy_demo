import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans

class ImageColorChanger:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Color Changer')
        self.image_path = ''
        self.original_image = None
        self.processed_image = None
        self.colors = []
        
        # Load Button
        self.load_button = tk.Button(self.root, text='Load Image', command=self.load_image)
        self.load_button.pack()

        # Canvas for image
        #self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas = tk.Canvas(self.root, width=600, height=800)
        self.canvas.pack()
        #self.canvas = tk.Canvas(self.root)
        #self.canvas.pack(fill=tk.BOTH, expand=True)

        # Color change buttons will be stored in this list
        self.color_buttons = []

        # Save Button
        self.save_button = tk.Button(self.root, text='Save Image', command=self.save_image, state='disabled')
        self.save_button.pack()
        
        self.original_colors = [(255, 255, 255), (0, 0, 0), (0, 165, 255)]  # example colors
        self.labels = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.process_image()
            self.display_image(self.processed_image)


    def process_image(self):
        # Ensure the image is in RGB format
        if self.original_image.mode != 'RGB':
            self.original_image = self.original_image.convert('RGB')
        
        img = np.array(self.original_image)
        original_shape = img.shape[:2]  # Save the original shape
        img = img.reshape((-1, 3))
        
        # Find three most representative colors
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(img)
        self.colors = kmeans.cluster_centers_.astype(int)
        
        # Map each pixel to the nearest of the three colors
        self.labels = kmeans.predict(img)
        img_recolored = np.array([self.colors[label] for label in self.labels])
        
        # Reshape based on original image shape
        img_recolored = img_recolored.reshape(original_shape[0], original_shape[1], 3)
        self.processed_image = Image.fromarray(img_recolored.astype('uint8'), 'RGB')

        # Update GUI for color changing
        for btn in self.color_buttons:
            btn.destroy()
        self.color_buttons.clear()

        for i, color in enumerate(self.colors):
            btn = tk.Button(self.root, text=f'Change Color {i+1}', background='#%02x%02x%02x' % tuple(color), command=lambda c=color, idx=i: self.change_color(c, idx))
            btn.pack()
            self.color_buttons.append(btn)

        self.save_button['state'] = 'normal'

    # def change_color(self, color, index):
    #     rgb, hex = colorchooser.askcolor(color)
    #     if rgb:
    #         self.colors[index] = np.array(rgb, dtype=int)
    #         self.process_image()
    #         self.display_image(self.processed_image)

    def change_color(self, color, index):
        # Convert the NumPy array to a tuple for the color parameter
        initial_color = tuple(color)
        # Use the initial_color in the askcolor dialog
        rgb, hex = colorchooser.askcolor(color=initial_color)
        if rgb:
            self.colors[index] = np.array(rgb, dtype=int)
            #self.process_image()
            self.update_image_colors()
            self.display_image(self.processed_image)

        # Update GUI for color changing
        for btn in self.color_buttons:
            btn.destroy()
        self.color_buttons.clear()

        for i, color in enumerate(self.colors):
            btn = tk.Button(self.root, text=f'Change Color {i+1}', background='#%02x%02x%02x' % tuple(color), command=lambda c=color, idx=i: self.change_color(c, idx))
            btn.pack()
            self.color_buttons.append(btn)

        self.save_button['state'] = 'normal'


    def update_image_colors(self):
        # Convert the processed image to a NumPy array for efficient processing
        #img_array = np.array(self.processed_image)
        img = np.array(self.original_image)
        original_shape = img.shape[:2]  # Save the original shape

        img_recolored = np.array([self.colors[label] for label in self.labels])
        img_recolored = img_recolored.reshape(original_shape[0], original_shape[1], 3)
        self.processed_image = Image.fromarray(img_recolored.astype('uint8'), 'RGB')
        #print(self.original_colors, "=>", self.colors)

        # Assuming self.colors has been updated to the new colors,
        # and self.original_colors holds the original three colors from the k-means processing

        #CTOM# # Map each original color to the new color directly in the array
        #CTOM# for original_color, new_color in zip(self.original_colors, self.colors):
        #CTOM#     # Find where the image array matches the original color
        #CTOM#     mask = np.all(img_array == original_color, axis=-1)

        #CTOM#     # Update these locations with the new color
        #CTOM#     img_array[mask] = new_color

        # Convert back to PIL Image and store in self.processed_image
        #self.processed_image = Image.fromarray(img_array.astype('uint8'), 'RGB')

        # Now, self.processed_image has the updated colors and can be redrawn on the GUI and saved
        self.display_image(self.processed_image)

    def display_image(self, img):
        self.canvas.delete("all")
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(300, 400, image=img_tk)
        self.canvas.image = img_tk

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.processed_image.save(file_path)

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageColorChanger(root)
    root.mainloop()
    