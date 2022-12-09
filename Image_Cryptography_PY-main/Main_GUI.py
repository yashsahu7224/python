from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk,Image

root=Tk()
root.geometry("300x240")

def encrypt_image():
    file1=filedialog.askopenfile(mode='r',filetype=[('jpg file','*.jpg')])
    if file1 is not None:
        print(file1)
        file_name=file1.name
        key=entry1.get(1.0,END)
        print("The path of the file is :",file_name)
        print("The key entered is :",key)
        fin=open(file_name,'rb')
        image=fin.read()
        fin.close()
        image=bytearray(image)
        for index, values in enumerate(image):
            image[index]=values ^ int(key)
        fin=open(file_name,'wb')
        fin.write(image)
        fin.close()
        b = Label(root, text="Encryption Completed",bg="red",fg="black")
        b.place(x=85,y=10)
        print("Encryption Completed!!")
        popup()

def popup():
    messagebox.showinfo("Status","Task Completed!")

# try:
#     path = input(r'Enter path of Image : ')
#     key = int(input('Enter Key for encryption of Image : '))
#     print('The path of file : ', path)
#     print('Key for encryption : ', key)
#     fin = open(path, 'rb')
#     image = fin.read()
#     fin.close()
#     image = bytearray(image)
#     for index, values in enumerate(image):
# 	    image[index] = values ^ key
#     fin = open(path, 'wb')
#     fin.write(image)
#     fin.close()
#     print('Encryption Done...')
# except Exception:
# 	print('Error caught : ', Exception.__name__)      

def decrypt_image():
    file1=filedialog.askopenfile(mode='r',filetype=[('jpg file','*.jpg')])
    if file1 is not None:
        print(file1)
        file_name=file1.name
        key=entry1.get(1.0,END)
        print("The path of the file to be decrypted is :",file_name)
        print("The key entered is :",key)
        fin=open(file_name,'rb')
        image=fin.read()
        fin.close()
        image=bytearray(image)
        for index, values in enumerate(image):
            image[index]=values ^ int(key)
        fin=open(file_name,'wb')
        fin.write(image)
        fin.close()
        b = Label(root, text="Decryption Done!                ",bg="green",fg="white")
        b.place(x=85,y=10)
        print("Decryption Completed!!")
        popup()

my_img = ImageTk.PhotoImage(Image.open("Background.jpg"),size="300x240")
my_bg = Label(image=my_img)
my_bg.pack()

b1= Button(root,text="Encrypt",command=encrypt_image)

b1.place(x=80,y=50)

b2= Button(root,text="Decrypt",command=decrypt_image)
b2.place(x=160,y=50)

label=Label(root,text="Enter key :")
label.place(x=30,y=100)
entry1=Text(root,height=1,width=10)
entry1.place(x=106,y=100)

w = Label(root, text='*Note You use the same key as you did before!')
w.place(x=32,y=130)


button_exit= Button(root,text="Exit App",command=root.quit)
button_exit.place(x=125,y=160)



root.mainloop()