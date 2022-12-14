import tkinter as tk

import keyboard
import maze_maker as mm

RED=(255,0,0)
BULE=(0,0,255)


def key_down(event):
    global key
    key = event.keysym

def key_up(event):
    global key
    key = ""
   
def main_proc():
    global cx, cy
    global mx,my
    if key == "w":
        my -= 1
    if key == "s":
        my += 1
    if key == "a":
        mx -= 1
    if key == "d":
        mx += 1
    if maze_lst[my][mx]==0:
        cx,cy=mx*100+50,my*100+50
    else:
        if key == "w":
            my += 1
        if key == "s":
            my -= 1
        if key == "a":
            mx += 1
        if key == "d":
            mx -= 1
    

    canv.coords("tori", cx, cy)
    root.after(100, main_proc)

    
    
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん") # 練習1

    # 練習2
    canv = tk.Canvas(root, width=1500, height=900, bg="black")
    canv.pack()

    maze_lst = mm.make_maze(15, 9)
    # print(maze_lst) # 1:壁／0:床
    mm.show_maze(canv, maze_lst)

    # 練習3
    tori = tk.PhotoImage(file="fig/5.png") 
    mx,my=1,1
    cx, cy = mx*100+50, my*100+50#スタート位置

    canv.create_image(cx, cy, image=tori, tag="tori")

    # 練習4
    key = "" # 現在押されているキーを表す

    # 練習5,6
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)    

    # 練習7
    main_proc()

#while True:
    #if keyboard.read_key() == "j":
        #print("j")
        #break
    #elif keyboard.is_pressed("j"):
        #print("j")
        #break


       
    root.mainloop()