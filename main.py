import tkinter as tk
from tkinter import Button, Label, PhotoImage, Text, Tk, filedialog, messagebox, simpledialog, WORD
from PIL import Image
import cv2
import wave
import os

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        root.title('Hide Secret Data in MultiMedia')
        root.geometry('700x580')
        root.config(bg='#2f4155')
        # Secret Key
        self.secret_key = "7620"
        # Icon
        try:
            image_icon = PhotoImage(file='logo.png')
            root.iconphoto(False, image_icon)
            logo = PhotoImage(file='logo.png')
            Label(root, image=logo, bg='#2f4155').place(x=10, y=0)
            self.logo = logo  # prevent garbage collection
        except Exception as e:
            print("Icon error:", e)
        Label(root, text=' Indira Cyber Security', font='impack 30 bold', bg='#2f4155', fg='white').place(x=85, y=17)
        
        # Interface layout
        tk.Label(root, text="Choose Mode:", font='impack 17 bold', bg='#2f4155', fg='white').place(x=27, y=120)
        self.mode = tk.StringVar(value="image")
        tk.Radiobutton(root, text="Image", variable=self.mode, value="image", font='impack 14 bold', bg='#2f4155', fg='green').place(x=160, y=160)
        tk.Radiobutton(root, text="Audio", variable=self.mode, value="audio", font='impack 12 bold', bg='#2f4155', fg='green').place(x=160, y=200)
        tk.Radiobutton(root, text="Video", variable=self.mode, value="video", font='impack 12 bold', bg='#2f4155', fg='green').place(x=160, y=240)
        
        # Secret Key Entry
        tk.Label(root, text='Secret Key:', font='impack 15 bold', bg='#2f4155', fg='white').place(x=21, y=350)
        self.key_entry = tk.Entry(root, font='impack 12', show='*')
        self.key_entry.place(x=158, y=355, width=110)
        # Forgot Key Button
        tk.Button(root, text="Forgot Key", font='impack 12 bold', bg='#2f4155', fg='white', command=self.forgot_key).place(x=160, y=380)

        # Text area for data input
        tk.Label(root, text="Enter Data:", font='impack 15 bold', bg='#2f4155', fg='white').place(x=360, y=125)
        self.data_entry = Text(root, font='impack 12', wrap=WORD)
        self.data_entry.place(x=360, y=170, width=300, height=200)
        
        # Choose file button
        tk.Button(root, text="Choose File", font='impack 12 bold', bg='#2f4155', fg='white', command=self.choose_file).place(x=160, y=290)
         
        # Hide data button
        tk.Button(root, text="Hide Data", font='impack 12 bold', bg='#2f4155', fg='white', command=self.hide_data).place(x=65, y=450)
        
        # Show data button
        tk.Button(root, text="Show Data", font='impack 12 bold', bg='#2f4155', fg='white', command=self.extract_data).place(x=260, y=450)

        # Label to display chosen file name
        self.file_label = Label(root, text="No file selected", font='impack 12', bg='#2f4155', fg='white')
        self.file_label.place(x=160, y=320)

        # This will hold the path of the file we work on
        self.file_path = ""
        # This variable keeps track of the output file name after hiding data.
        self.output_file = ""



    def check_key(self):
        entered_key = self.key_entry.get()
        if entered_key != self.secret_key:
            messagebox.showerror("Error", "Wrong Secret Key")
            return False
        return True   



    def forgot_key(self):
        new_key = simpledialog.askstring("Forgot Key", "Enter your new secret key:")
        if new_key:
            self.secret_key = new_key
            messagebox.showinfo("Success", "Your secret key has been updated!")
        else:
            messagebox.showwarning("Warning", "No key entered!")

    def choose_file(self):
        if not self.check_key():
            return 
        mode = self.mode.get()
        if mode == "image":
            filetypes = [('Image files', '*.png;*.bmp;*.jpg;*.jpeg')]
        elif mode == "audio":
            filetypes = [('Wav files', '*.wav')]
        elif mode == "video":
            filetypes = [('Video files', '*.avi;*.mp4')]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            self.file_path = path
            self.file_label.config(text=os.path.basename(path))




    def hide_data(self):
        if not self.check_key():
            return
        if not self.file_path:
            messagebox.showwarning("Warning", "No file selected!")
            return
        data = self.data_entry.get("1.0", tk.END).strip()
        if not data:
            messagebox.showwarning("Warning", "No data entered!")
            return

        mode = self.mode.get()
        if mode == "image":
            self.hide_in_image(self.file_path, data)
        elif mode == "audio":
            self.hide_in_audio(self.file_path, data)
        elif mode == "video":
            self.hide_in_video(self.file_path, data)




    def extract_data(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "No file selected!")
            return
        mode = self.mode.get()
        if mode == "image":
            self.extract_from_image(self.file_path)
        elif mode == "audio":
            self.extract_from_audio(self.file_path)
        elif mode == "video":
            self.extract_from_video(self.file_path)

    
    

    
    
    def hide_in_image(self, image_path, data):
        try:
            # Convert image to RGB to ensure we have three channels.
            image = Image.open(image_path).convert('RGB')
            encoded = image.copy()
            data += "***END***"
            data_bin = ''.join(format(ord(c), '08b') for c in data)
            (width, height) = image.size
            total_pixels = width * height

            if len(data_bin) > total_pixels:
                messagebox.showerror("Error", "Data too large to hide in image!")
                return

            pixels = encoded.load()
            idx = 0
            for y in range(height):
                for x in range(width):
                    if idx < len(data_bin):
                        r, g, b = pixels[x, y]
                        # Change only the red channel LSB for simplicity
                        r = (r & ~1) | int(data_bin[idx])
                        pixels[x, y] = (r, g, b)
                        idx += 1
                    else:
                        break
                if idx >= len(data_bin):
                    break

            self.output_file = "Secret.png"
            encoded.save(self.output_file)
            messagebox.showinfo("Success", f"Data hidden in image. Saved as '{self.output_file}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))





    def hide_in_audio(self, audio_path, data):
        try:
            audio = wave.open(audio_path, mode='rb')
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
            audio.close()

            data += "***END***"
            data_bits = ''.join(format(ord(c), '08b') for c in data)
            n_frames = len(frame_bytes)
            if len(data_bits) > n_frames:
                messagebox.showerror("Error", "Data too large to hide in audio!")
                return

            for i in range(len(data_bits)):
                frame_bytes[i] = (frame_bytes[i] & ~1) | int(data_bits[i])

            self.output_file = "Secret.wav"
            modified_audio = wave.open(self.output_file, 'wb')
            # Use same parameters as original if available; here we use defaults.
            modified_audio.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
            modified_audio.writeframes(frame_bytes)
            modified_audio.close()

            messagebox.showinfo("Success", f"Data hidden in audio. Saved as '{self.output_file}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))



    def hide_in_video(self, video_path, data):
        try:
            cap = cv2.VideoCapture(video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('Secret.avi', fourcc, cap.get(cv2.CAP_PROP_FPS), (width, height))

            data += '***END***'
            data_bin = ''.join(format(ord(i), '08b') for i in data)
            frame_idx = 0
            success, frame = cap.read()
            while success:
                if frame_idx < len(data_bin):
                    frame[0][0][0] = frame[0][0][0] & ~1 | int(data_bin[frame_idx])
                    frame_idx += 1
                out.write(frame)
                success, frame = cap.read()

            cap.release()
            out.release()
            messagebox.showinfo("Success", "Data hidden in video. Saved as 'Secret.avi'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_from_image(self, image_path):
        try:
            image = Image.open(image_path).convert('RGB')
            pixels = image.load()
            width, height = image.size
            data_bits = ""
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    data_bits += str(r & 1)
            data = ''.join(chr(int(data_bits[i:i+8], 2)) for i in range(0, len(data_bits), 8))
            extracted_data = data.split('***END***')[0]
            self.data_entry.delete("1.0", tk.END)
            self.data_entry.insert(tk.END, extracted_data)
            messagebox.showinfo("Extracted Data", extracted_data)
        except Exception as e:
            messagebox.showerror("Error", str(e))




    def extract_from_audio(self, audio_path):
        try:
            audio = wave.open(audio_path, mode='rb')
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
            audio.close()
            data_bits = ''.join(str(frame_bytes[i] & 1) for i in range(len(frame_bytes)))
            data = ''.join(chr(int(data_bits[i:i+8], 2)) for i in range(0, len(data_bits), 8))
            extracted_data = data.split('***END***')[0]
            self.data_entry.delete("1.0", tk.END)
            self.data_entry.insert(tk.END, extracted_data)
            messagebox.showinfo("Extracted Data", extracted_data)
        except Exception as e:
            messagebox.showerror("Error", str(e))





    def extract_from_video(self, video_path):
        try:
            cap = cv2.VideoCapture(video_path)
            data_bin = ""
            success, frame = cap.read()
            while success:
                data_bin += str(frame[0][0][0] & 1)
                success, frame = cap.read()

            data = ''.join(chr(int(data_bin[i:i+8], 2)) for i in range(0, len(data_bin), 8))
            extracted_data = data.split('***END***')[0]
            cap.release()
            messagebox.showinfo("Extracted Data", extracted_data)
        except Exception as e:
            messagebox.showerror("Error", str(e))





if __name__ == "__main__":
    root = Tk()
    app = SteganographyApp(root)
    root.mainloop()

