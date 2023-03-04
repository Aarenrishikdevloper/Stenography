import random
import string
from argparse import FileType
from cProfile import label
from cgitb import text
from fileinput import filename
from logging import root
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import sys
from tkinter.tix import IMAGETEXT
import numpy as np
import hashlib

from PIL import*
import os
from tkinter import filedialog 
from PIL import Image, ImageTk, ImageDraw, ImageFont
from stegano import  lsb
from stegano.lsb import  generators
#designate height and width of the app
root=Tk()

width = 780
height = 500
x = (root.winfo_screenwidth()//2)-(width//2)
y = (root.winfo_screenheight()//2)-(height//2)

root.title("Steganography")
root.geometry(f'{width}x{height}+{x}+{y}'.format(width, height, x, y))
root.resizable(False,False)
root.configure(bg="#000033")


#defining background image
bg=ImageTk.PhotoImage(Image.open("bg2.png"))
my_label = Label(root, image=bg)
my_label.pack()
def open_image():
    filepath = filedialog.askopenfilename() 
    if filepath: 
        image = Image.open(filepath) 
        image = image.resize((340, 280), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image) 
        lbl.configure(image = photo) 
        lbl.image_names = photo 
        file_path.delete(0, tk.END) 
        file_path.insert(0, filepath)
    return filepath

#defining the commands in buttons


image_icon=PhotoImage(file="icon.png")
root.iconphoto(False,image_icon)
def show_dialogencrypt():
  
    password_dialog = tk.Toplevel(root) 
    password_dialog.title("Password for Encryption") 
    password_dialog.geometry("300x150") 
    password_dialog.resizable(False, False)
    password_label = tk.Label(password_dialog, text="Please Enter the password") 
    password_label.pack(pady=10) 
    password_entry = tk.Entry(password_dialog, show="*") 
    password_entry.pack()

    def encode_message():
        filename = file_path.get()
        im = Image.open(filename)
        width, height = im.size
        # check if  the image has alpha channel
        has_alpha = im.mode.endswith("A")
        password = password_entry.get()
        message = str(text1.get("1.0", END))
        # create a new image to hold the encrypted data
        enc_im = Image.new(im.mode, (width, height))
        draw = ImageDraw.Draw(enc_im)
        # set the font and message color
        font = ImageFont.truetype("arial.ttf", 16)
        color = (255, 255, 255, 255) if has_alpha else (255, 255, 255)
        # encrypting the image by Xoring it with password
        if message:
            message_byte = [ord(c) for c in message]
            encrypted_message = [message_byte[i] ^ ord(password[i % len(password)]) for i in range(len(message_byte))]
        else:
            messagebox.showerror("Error", "PLease Insert a message")
        # draw the pixels on encrypted image
        index = 0
        for x in range(width):
            for y in range(height):
                # get the pixel data
                pixel = im.getpixel((x, y))
                # check if the pixel is transparent
                if has_alpha and pixel[-1] == 0:
                    # if the pixel is transparent  copy it to encrypted image
                    enc_im.putpixel((x, y), pixel)
                else:
                    if index < len(encrypted_message):
                        encrypted_byte = encrypted_message[index]
                        index += 1

                    encrypted_byte = max(min(encrypted_byte, 255), 0)
                    # draw the pixel on the encrypted image
                    if has_alpha:
                        pixel = pixel[:-1] + (encrypted_byte,)
                    else:
                        pixel = pixel[:1] + (encrypted_byte,)
                    draw.point((x, y), pixel)
        password_dialog.destroy()
        enc_im.save("encode.png")






    submit_buttom = tk.Button( password_dialog, text="Encrypt", font="arial 14", command=encode_message )
    submit_buttom.pack(pady=10)












root.iconphoto(False, image_icon)


def show_dialogdecrypt():
    password_dialog = tk.Toplevel(root)
    password_dialog.resizable(False, False)
    password_dialog.title("Password for decryption")
    password_dialog.geometry("300x150")
    password_label = tk.Label(password_dialog, text="Please Enter the password")
    password_label.pack(pady=10)
    password_entry = tk.Entry(password_dialog, show="*")
    password_entry.pack()

    def decode_message():
        filename = file_path.get()
        im = Image.open(filename)
        width, height = im.size
        has_alpha = im.mode.endswith("A")
        password = password_entry.get()
        decrypted_message = []
        index = 0
        # loop through each pixel in the image
        for x in range(width):
            for y in range(height):
                # get the pixel data
                pixel = im.getpixel((x, y))
                # check if the pixel is transparent
                if has_alpha and pixel[-1] == 0:
                    # if the pixel is transparent, ignore it
                    pass
                else:
                    # get the encrypted byte from the pixel
                    if has_alpha:
                        encrypted_byte = pixel[-1]
                    else:
                        encrypted_byte = pixel[1]
                    # decrypt the byte using the password
                    decrypted_byte = encrypted_byte ^ ord(password[index % len(password)])
                    decrypted_message.append(chr(decrypted_byte))
                    index += 1
        # filter out non-printable characters from the decrypted message
        printable_chars = set(string.printable)
        decrypted_message = ''.join(filter(lambda c: c in printable_chars, decrypted_message))
        # display the decrypted message
        text1.delete(1.0, END)
        text1.insert(END, decrypted_message)





    # Show the decoded message
    submit_buttom = tk.Button(password_dialog, text="decrypt", font="arial 14", command=decode_message)
    submit_buttom.pack(pady=10)

    # Convert the binary message to ASCII








Label(root, text="STEGANOGRAPHY", bg="black", fg="white", font="arial 25 bold").place(x=40, y=20)

# first frame
frame1 = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
frame1.place(x=40, y=80)

lbl = Label(frame1, bg="black")
lbl.place(x=40, y=10)
file_path = Entry(frame1)

# second frame
frame2 = Frame(root, bd=3, bg="white", width=340, height=280, relief=GROOVE)
frame2.place(x=380, y=80)

text1 = Text(frame2, font="Robote 20", bg="white", fg="black", relief=GROOVE, )
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# third frame
frame3 = Frame(root, bd=3, bg="black", width=330, height=100, relief=GROOVE)
frame3.place(x=40, y=370)

Button(frame3, text="open Image", width=10, height=2, font="arial 14", command=open_image).place(x=40, y=30)
Button(frame3, text="save Image", width=10, height=2, font="arial 14", ).place(x=200, y=30)
Label(frame3, text="Picture, Image, Photo File", bg="black", fg="yellow").place(x=40, y=5)

# fourth frame
frame4 = Frame(root, bd=3, bg="black", width=330, height=100, relief=GROOVE)
frame4.place(x=380, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14", command=show_dialogencrypt).place(x=40, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14", command=show_dialogdecrypt).place(x=200, y=30)
Label(frame4, text="Picture, Image, Photo File", bg="black", fg="yellow").place(x=40, y=5)

root.mainloop()















































