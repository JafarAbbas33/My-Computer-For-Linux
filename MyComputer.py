
from tkinter.ttk import *
from tkinter import *
from PIL import Image, ImageTk

import subprocess
import sys
import os
import re

MAX_DRIVES_IN_A_ROW = 2

def extract_details_from_line(line):
    file_system, total_size, used_size, available_size, percentage_used, mount_location = line.split()
    percentage_used = percentage_used.replace('%', '')
    drive_name = mount_location.split('/')[-1]
    if drive_name == '':
        drive_name = 'Root'
    return drive_name, percentage_used, available_size, total_size, mount_location
    


def binder(obj, path):
    obj.bind('<Double-Button-1>', lambda event: os.system('pcmanfm "' + path + '"'))

class GridHandler:
    row = 0
    column = 0
    def get_row_and_column():
        if GridHandler.column < MAX_DRIVES_IN_A_ROW:
            return GridHandler.column, GridHandler.row
        else:
            GridHandler.row += 1
            GridHandler.column = 0
            return GridHandler.column, GridHandler.row


def get_drive_frame(root, line):
    drive_name, percentage_used, available_size, total_size, mount_location = extract_details_from_line(line)

##    image = Image.open("drive_icon.png")
##    image = image.resize((86, 44))
##    photo = ImageTk.PhotoImage(image)
##    photo_list.append(photo)

    main_frame = Frame(root, highlightthickness=2)
        
    drive_icon = Label(main_frame, image=photo)
    drive_icon.pack(side = LEFT, pady=14, padx=6)
    binder(drive_icon, mount_location)

    # Details frame
    details_frame = Frame(main_frame)

    drive_name_label = Label(details_frame, text=drive_name)
    drive_name_label.pack()
    binder(drive_name_label, mount_location)

    progress_bar = Progressbar(details_frame, orient = HORIZONTAL, length = 200,
                                mode = 'determinate')
    progress_bar['value'] = percentage_used
    binder(progress_bar, mount_location)
    progress_bar.pack()

    space_label = Label(details_frame, text=available_size + ' free of ' + total_size)
    space_label.pack()
    binder(space_label, mount_location)
    
    details_frame.pack(side = LEFT, padx=8)
    
    # main_frame.pack(side = LEFT, padx=10)
    column, row = GridHandler.get_row_and_column()
    # print(column, row)
    main_frame.grid(column=column, row=row, pady = 10, padx = 20)
    GridHandler.column += 1
    
    binder(main_frame, mount_location)
    binder(details_frame, mount_location)
    
    main_frame.config(highlightbackground = "steel blue")
    
    






def main():
    script_location = sys.argv[0].split('/')
    script_location.pop(-1)
    cwd = '/'.join(script_location)
    os.chdir(cwd)
    
    call = subprocess.Popen(['df', '-h'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output = call.communicate()[0].decode().splitlines()
    #return output[-3]
    #print(output)
    #print()

    # creating tkinter window 
    root = Tk()
    root.title('My Computer')

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    
    global photo
    image = Image.open("drive_icon.png")
    image = image.resize((86, 44))
    photo = ImageTk.PhotoImage(image)
    
    #root.geometry(str(w) + 'x' + str(h))
      
    for line in output:
        if 'sda' in line:
            get_drive_frame(root, line)
            #break

    root.update_idletasks()
    root.update()

    print('---End---')
    root.mainloop()



if __name__ == '__main__':
    main()
    



