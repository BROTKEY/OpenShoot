import cv2
import socket
import tkinter
import threading
import time

shot = []
shots =[[]]
tk=tkinter.Tk()

canvas = tkinter.Canvas(tk, width=796, height=796, bg="white")
target = tkinter.PhotoImage(file="Luftgewehrscheibe.png")

def server():
    ip = "127.0.0.1"
    port = 5005
    address = (ip, port)

    datasocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    datasocket.bind(address)

    while True:
        data, addr = datasocket.recvfrom(1024)

        data = data.decode("utf-8")
        data = data.split(";")
        pixel = (int((float(data[0])*-1)/3*271), int((float(data[1])*-1)/3*271))

        shot.append((pixel[0], pixel[1], time.time()))



def clear():
    global shot
    global shots
    global canvas
    global tk

    canvas.create_image(800/2, 800/2, image=target)
    shots.append(shot)
    shot = []
        
    canvas.update_idletasks()
    tk.update()

def ui():
    canvas.pack()

    tk.title("OpenShoot")
    tk.geometry("1200x1200")
    tk.resizable(False, False)

    button = tkinter.Button(tk, text="Clear", command=clear, bg="white", fg="black", height=5, width=10)
    button.pack(side="bottom")

    while True:
        if thread.is_alive() == False:
            exit()

        canvas.create_image(800/2, 800/2, image=target)
        if len(shot) > 1:
            for i, point in enumerate(shot):
                if i == 0:
                    continue
                x,y,_ = point
                x2,y2,_ = shot[i-1]
                canvas.create_line(int(x)+400, int(y)+400, int(x2)+400, int(y2)+400, fill="#F00", width=1)

        canvas.update_idletasks()
        tk.update()
        time.sleep(0.05)


thread = threading.Thread(target=server)
thread.start()
ui()