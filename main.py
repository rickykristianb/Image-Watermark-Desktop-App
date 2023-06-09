
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageDraw, ImageFont, UnidentifiedImageError
import os


class ImageBehaviour(Frame):

    def __init__(self):
        super().__init__()

        self.__upload_image = LabelFrame(
            window,
            text='Upload Image',
            padx=100,
            pady=100
        )
        self.__upload_image.place(x=60, y=30)

        self.__water_mark_win = LabelFrame(
            window,
            text='Watermark',
            padx=40,
            pady=10
        )
        self.__water_mark_win.place(x=60, y=580)

        self.__button_display()

    def __delete_image(self):
        self.__image_display.destroy()
        self.__delete_img_button.destroy()
        self.__upload_button["state"] = "normal"

    def __display_image(self):
        self.image_selected = filedialog.askopenfilename(
            filetypes=(
                [("png files", "*.jpg"),
                 ("jpg files", "*.jpg")]
            ),
            title="Select image",
        )
        try:  # Check if user exit the upload image windows
            self.img = Image.open(self.image_selected)
            self.img_resize = self.img.resize((150, 150))
            self.img = ImageTk.PhotoImage(self.img_resize)
        except AttributeError:
            pass
        except UnidentifiedImageError:
            pass
        try:  # Check if the image is not broken
            if self.img:
                self.__image_display = Button(
                    self.__upload_image,
                    image=self.img
                )
                self.__image_display.pack(
                    pady=1,
                    padx=1
                )
                self.__delete_img_button = Button(
                    self.__upload_image,
                    text="Delete",
                    command=self.__delete_image
                )
                self.__delete_img_button.pack(
                    pady=2,
                    padx=2
                )
                self.__upload_button["state"] = "disabled"
        except AttributeError:
            messagebox.showerror(title="Error", message="There is something wrong with your picture, try another")

    def __add_watermark(self):
        text = self.__add_text_entry.get()
        try:
            self.img  # if image already uploaded
        except AttributeError:
            messagebox.showinfo("Error", message="You have not uploaded your image")
        else:
            if text:  # if watermark text is inserted
                # Add new window to preview watermarked image
                # User Toplevel() instead of Tk() because you open a new windows and
                # let the new windows as your new canvas
                self.window_image_preview = Toplevel()
                self.window_image_preview.title("Image Preview")
                self.window_image_preview.geometry("500x700")

                self.__preview_label = Label(
                    self.window_image_preview,
                    text="Image Preview",
                    font=('Arial', 25)
                )
                self.__preview_label.pack(
                    padx=20,
                    pady=20
                )

                # Start add text/draw on the picture
                self.image = Image.open(self.image_selected)
                image_draw = ImageDraw.Draw(self.image)
                image_font = ImageFont.truetype(r"C:\Users\System-Pc\Desktop\arial.ttf", 20)
                image_draw.text(
                    (28, 26),  # Coordinate to place the text
                    text=text,
                    fill=(255, 0, 0),  # RGB color
                    font=image_font
                )
                ph = ImageTk.PhotoImage(self.image.resize((300, 500)))

                label = Label(self.window_image_preview, image=ph, compound='center')
                label.pack(
                    padx=10,
                    pady=10
                )

                self.__download_image_button = Button(
                    self.window_image_preview,
                    width=50, text="Download",
                    command=self.__download_watermarked_image
                )
                self.__download_image_button.pack(
                    padx=20,
                    pady=20
                )
                self.window_image_preview.mainloop()
            else:
                messagebox.showinfo("Error", message="You have not inserted your watermark text")

    def __download_watermarked_image(self):
        file_type = [("png files", "*.png"),
                     ("jpg files", "*.jpg")]
        file = filedialog.asksaveasfile(
            filetypes=file_type,
            defaultextension=".png",
        )
        if self.image != 'RGBA':
            self.image = self.image.convert("RGBA")

        txt = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
        if file:
            abs_path = os.path.abspath(file.name)
            out = Image.alpha_composite(self.image, txt)
            out.save(abs_path)
            messagebox.showinfo(title="Saved Image", message="Your Image successfully saved")
        self.window_image_preview.destroy()

    def __button_display(self):
        self.__upload_button = Button(
            self.__upload_image,
            text="Upload",
            command=self.__display_image,
            width=25
        )
        self.__upload_button.pack(
            pady=10,
            padx=0
        )

        self.__add_text_label = Label(
            self.__water_mark_win,
            text="Add watermark text: "
        )
        self.__add_text_label.grid(
            column=0,
            row=2
        )
        self.__add_text_entry = Entry(
            self.__water_mark_win,
            width=50
        )
        self.__add_text_entry.grid(
            column=0,
            row=3
        )

        start_button = Button(
            self.__water_mark_win,
            text='Preview',
            command=self.__add_watermark,
            width=25
        )
        start_button.grid(
            columnspan=2,
            row=4
        )


if __name__ == '__main__':

    window = Tk()
    window.title("Image Watermarker")
    window.geometry("500x700")
    window.maxsize(height=700, width=500)
    window.minsize(height=700, width=500)

    app = ImageBehaviour()

    window.mainloop()
