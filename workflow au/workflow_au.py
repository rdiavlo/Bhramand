
""" This offers you two plates, the first which lets you select a SQL query from your rucksack and the second which
runs your python scripts sire"""
import os
from tkinter import *
import subprocess
from datetime import datetime

base_dir_path = r"C:\Users\rnayakm\OneDrive - Cisco\Desktop\Projects\LTI\RTW\\"


def read_files(file_path):
    acc = ""
    with open(file_path, "r") as file_object:
        line_list = file_object.readlines()
        for line in line_list:
            acc += line
    return acc


root = Tk()

def remove_previous_widgets(parent_obj):
    object_to_remove_list = parent_obj.winfo_children()[2:]
    for object_v in object_to_remove_list:
        object_v.destroy()

def SQLWindow(parent_obj):
    remove_previous_widgets(parent_obj)

    query_dir_path = base_dir_path + r"queries - Copy\\"
    query_file_list = os.listdir(query_dir_path)

    listbox_1= Listbox(parent_obj)
    listbox_1.pack(side=LEFT, fill=BOTH)
    scrollbar = Scrollbar(parent_obj)
    scrollbar.pack(side=RIGHT, fill=BOTH)

    # Insert elements into the listbox
    for file_name in query_file_list:
        listbox_1.insert(END, file_name)
    def openNewSQLdisplayWindow():
        user_selected_file = listbox_1.get(listbox_1.curselection())
        user_selected_file_path = query_dir_path + user_selected_file
        file_text = read_files(user_selected_file_path)

        newWindow = Toplevel(parent_obj)
        newWindow.title("New Window")
        width, height = "800", "600"
        newWindow.geometry(f"{width}x{height}")
        text_widget = Text(newWindow, height=int(width), width=int(400))
        text_widget.insert(END, file_text)
        text_widget.pack()


    b1 = Button(parent_obj, text='print selection', width=15, height=2, command=lambda: openNewSQLdisplayWindow())
    b1.pack()


def CodeRunWindow(parent_obj):
    remove_previous_widgets(parent_obj)

    code_dir_path = base_dir_path + r"code\\"
    code_file_list = os.listdir(code_dir_path)


    listbox_1= Listbox(parent_obj)
    listbox_1.pack(side=LEFT, fill=BOTH)
    scrollbar = Scrollbar(parent_obj)
    scrollbar.pack(side=RIGHT, fill=BOTH)

    # Insert elements into the listbox
    for file_name in code_file_list:
        listbox_1.insert(END, file_name)

    b1 = Button(parent_obj, text='Open code interface', width=15, height=2, command=lambda: openCodeRunWindow())
    b1.pack()


    def openCodeRunWindow():
        script_file_name = listbox_1.get(listbox_1.curselection())
        user_selected_file_path = code_dir_path + script_file_name

        newWindow = Toplevel(root)
        newWindow.title(script_file_name)
        width, height = "800", "600"
        newWindow.geometry(f"{width}x{height}")

        inputtxt = Text(newWindow, height=20, width=int(width))
        inputtxt.pack()

        b1 = Button(newWindow, text="Run code", width=15, height=2, command=lambda: get_code_output())
        b1.pack()

        text_widget = Text(newWindow, height=20, width=int(width))
        text_widget.pack()

        def get_code_output():
            python_path = r"C:\Users\rnayakm\AppData\Local\Programs\Python\Python39\python.exe"

            script_input = inputtxt.get(1.0, "end-1c")
            code_result = subprocess.run([python_path, user_selected_file_path, "--input_arguments", script_input], stdout=subprocess.PIPE)
            code_result = code_result.stdout.decode("utf-8")
            text_widget.insert(END, code_result)
            text_widget.insert(END, "Last output on: " + str(datetime.now()) + "\n" + "="*80 + "\n")


# SQLWindow()

b1 = Button(root, text='Open SQL interface', width=15, height=2, command=lambda: SQLWindow(root))
b1.pack()
b2 = Button(root, text='Open Code interface', width=15, height=2, command=lambda: CodeRunWindow(root))
b2.pack()



root.mainloop()
