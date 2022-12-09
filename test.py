# Import the necessary modules!
import speedtest
from tkinter.ttk import *
from tkinter import *
import threading


root = Tk()
root.title("Test Internet Speed")
root.geometry('380x260')
root.resizable(False, False)
root.configure(bg="#ffffff")
root.iconbitmap('speed.ico')

# design Label
Label(root, text ='TEST INTERNET SPEED', bg='#ffffff', fg='#404042', font = 'arial 23 bold').pack()
Label(root, text ='by @milaan9', bg='#fff', fg='#404042', font = 'arial 15 bold').pack(side =BOTTOM)

# making label for show internet speed
down_label = Label(root, text="⏬ Download Speed - ", bg='#fff', font = 'arial 10 bold')
down_label.place(x = 90, y= 50)
up_label = Label(root, text="⏫ Upload Speed - ", bg='#fff', font = 'arial 10 bold')
up_label.place(x = 90, y= 80)
ping_label = Label(root, text="Your Ping - ", bg='#fff', font = 'arial 10 bold')
ping_label.place(x = 90, y= 110)

# function for check speed
def check_speed():
    global download_speed, upload_speed
    speed_test= speedtest.Speedtest()
    download= speed_test.download()
    upload = speed_test.upload()

    download_speed = round(download / (10 ** 6), 2)
    upload_speed = round(upload / (10 ** 6), 2)
    
# function for progress bar and update text
def update_text():
    thread=threading.Thread(target=check_speed, args=())
    thread.start()
    progress=Progressbar(root, orient=HORIZONTAL,
                         length=210, mode='indeterminate')
    progress.place(x = 85, y = 140)
    progress.start()
    while thread.is_alive():
        root.update()
        pass
    down_label.config(text="⏬ Download Speed - "+str(download_speed)+"Mbps")
    up_label.config(text="⏫ Upload Speed - "+str(upload_speed)+"Mbps")

    # Fetch the ping
    st.get_servers([])
    ping = st.results.ping
    
    ping_label.config(text="Your Ping is - "+str(ping))
    
    progress.stop()
    progress.destroy()

# button for call to function
button = Button(root, text="Check Speed ▶", width=30, bd = 0, bg = '#404042', fg='#fff', pady = 5, command=update_text)
button.place(x=85, y = 170)
root.mainloop()