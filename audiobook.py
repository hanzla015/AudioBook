from tkinter.filedialog import * # To import tkinter filedialog functions
from tkinter.font import BOLD # import tkinter' Font property BOLD
import PyPDF2 # Main for opening pdf
from tkinter import * # Import of all tkinter widgets
from tkinter.constants import * # import of all tkinter CONSTANTS
import pyttsx3 # module for Saying the text # pip install
from threading import *# for threading
import os

# ------------ Creating Engine for Speaking __________
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
engine.setProperty('rate',120)

# -------------- List of consonats and symbols for validating user input of page
letter = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','!','@','#','$','%','^','&','*','(',')','_','+','=','-','`','~','|','}','{','[',']',';',':',"'",'"','/','?','.','>','<']

#---------------- main function to read the user given text 
def read():
    try:
        page = int(page_number_by_user.get())
        page_number_by_user.config(state=DISABLED)
    
        if  int(page) > pages:# configure error label if page number are greater than total pages of book
            error_file_label.config(text="Page number cannot exceed total pages")
            error_file_label.pack(side=BOTTOM,pady=10)
            page_number_by_user.config(state=NORMAL)

        elif int(page) < 0:# configure error label if page number is lower than 0
            error_file_label.config(text="Page number cannot be less then total pages")
            error_file_label.pack(side=BOTTOM,pady=10)
            page_number_by_user.config(state=NORMAL)

        else:# if no error in page number then extract the page number to read
            error_file_label.pack_forget()
            read_btn.config(text="Reading....")
            read_btn.config(state=DISABLED)
            read_full_btn.pack_forget()
            file_chose_btn.pack_forget()
            main.geometry("400x340")
            pdfReader = PyPDF2.PdfFileReader(book)
            num = int(page)# num is page nuber entered by user
            if (num == 1) or (num == 0) :
                page = 0
            else:
                page = num - 1
            page_open = pdfReader.getPage(page)# open page entered by user
            opened_page_text = page_open.extractText()# extract the page text
            # opened_page_text = opened_page_text.replace("\n","")
            # print(opened_page_text)
            engine.say(text=opened_page_text)# say the opened page text
            engine.runAndWait()# engine runs and stops
            page_number_by_user.config(state=NORMAL)
            read_btn.config(text="Start Reading")
            read_btn.config(state=ACTIVE)
            read_full_btn.pack(side=TOP,pady=5)
            file_chose_btn.config(text="Change PDF")
            file_chose_btn.pack(side=TOP,pady=5)
            exit_btn.pack_forget()
            exit_btn.pack(side=TOP,pady=5)
            main.geometry("400x500")

    except Exception as e:# if error during getting the page input then except block statement execute
        if "invalid literal for int() with base 10" in str(e):
            error_file_label.config(justify=CENTER,text="Make sure the page number is not empty.\npage number is Integers only.")
            error_file_label.pack(side=BOTTOM,pady=10)
            page_number_by_user.config(state=NORMAL)

def read_full():
    # pages = int(pages)
    try:
        error_file_label.pack_forget()
        read_btn.config(text="Reading....")
        read_btn.config(state=DISABLED)
        page_number_by_user.config(state=DISABLED)
        read_full_btn.pack_forget()
        file_chose_btn.pack_forget()
        main.geometry("400x340")
        pdfReader = PyPDF2.PdfFileReader(book)
        for i in range(0,pages):
            page_open = pdfReader.getPage(i)# open page entered by user
            opened_page_text = page_open.extractText()# extract the page text
            # opened_page_text = opened_page_text.replace("\n","")
            # print(opened_page_text)
            engine.say(text=opened_page_text)# say the opened page text
            engine.runAndWait()# engine runs and stops
        page_number_by_user.config(state=NORMAL)
        read_btn.config(text="Start Reading")
        read_btn.config(state=ACTIVE)
        read_full_btn.pack(side=TOP,pady=5)
        file_chose_btn.config(text="Change PDF")
        file_chose_btn.pack(side=TOP,pady=5)
        exit_btn.pack_forget()
        exit_btn.pack(side=TOP,pady=5)
        main.geometry("400x500")
    except:
        print("HI")

# ---------------- fucntion to get pdf file path and validate path or file
def path_to_file():
    path = askopenfile()
    if path is None:# if path is none then return to start
        return
    else:# split the path by .
        path_splited = path.name.split(".")

    if not "pdf" in path_splited:# check that if not "pdf" exist in path and raise error file_label 
        error_file_label.pack_forget()
        error_file_label.config(text="Choose a pdf file only")
        error_file_label.pack(side=BOTTOM,pady=5)
    else:# executed only if ".pdf" in path
        try:
            error_file_label.pack_forget()# to remove the previous error_file_label
            path_of_file = path.name# the path of file on secondary storage
            global book # global variable of book to use in read fuction
            global pages# global variable of pages to get total number of pages in read function
            book = open(f'{path_of_file}','rb')# object to open pdf file in read binary mode
            pdfReader = PyPDF2.PdfFileReader(book)#pdf reader object to open book
            pages = pdfReader.numPages# total number of 
            file_chose_btn.pack_forget()# to unpack forget pack of file_chose_btn
            exit_btn.pack_forget()# to unpack forget pack of exit_btn
            main.geometry("400x500")#change geometry of main
            label_file_chosed.config(text=f"File Choosed\n{path_of_file}",font=("Times New Roman",16))#show the file path selected 
            label_file_chosed.pack(side=TOP,pady=5)# pack the label file chosed path on main window
            total_pages.config(text=f"Total number of pages in this book is {pages}.\nEnter page number for start reading.")
            total_pages.pack(side=TOP,pady=4)
            page_number_by_user.pack(side=TOP)
            read_btn.pack(side=TOP,pady=5)
            read_full_btn.pack(side=TOP,pady=5)
            file_chose_btn.config(text="Change PDF")
            file_chose_btn.pack(side=TOP,pady=5)
        except Exception as e:
            error_file_label.config(text=f'{e}')
            error_file_label.pack(side=BOTTOM,pady=3)
        exit_btn.pack(side=TOP,pady=5)

# Threads for window proper working
def start_reading():
    thread = Thread(target=read)
    thread.start()

def read_full_Thread():
    thread = Thread(target=read_full)
    thread.start()

def exit():
    os.system("taskkill /f /im audiobook.exe")
    main.destroy()

# gui setup starts here
main = Tk()#main class packed in main variable
main.title("Audio Book")# title of main window
main.geometry("350x200")# geometry of main window
# main.config(bg="yellow")# background color of main window
main.iconbitmap('audiobook.ico')# icon of the main window

#    labels  of main windows
error_file_label = Label(main,foreground="red",text='',font=("Times New Roman",14))
heading = Label(main,text="AudioBook",font=("Times New Roman",18,BOLD))
author = Label(main,text="@Hanzla",font=("Times New Roman",18,BOLD))
total_pages = Label(main,font=("Times New Roman",14))
label_file_chosed = Label(main,font=("Times New Roman",14),wraplength=400)
file = PhotoImage(
    file='D:\\Karen\\assets\\img\\photo.png')
headingIcon = Label(main, image=file)

# Buttons of main windows
file_chose_btn = Button(main,text="Choose PDF",activeforeground="green",font=("Times New Roman",14),relief=RIDGE,command=path_to_file)
read_btn = Button(main,text="Start Reading",activeforeground="green",font=("Times New Roman",14),command=start_reading,relief=RIDGE)
exit_btn = Button(main,activeforeground="green",font=("Times New Roman",14),text="Exit",relief=RIDGE,command=exit)
read_full_btn = Button(main,activeforeground="green",font=("Times New Roman",14),text="Read Full book",relief=RIDGE,command=read_full_Thread)
# ENTRY FOR PAGE NUMBER
page_number_by_user = Entry(main,font=('Times New Roman',18),foreground="white",background="black",justify=CENTER,relief=RIDGE)

# # Packing
heading.pack(side=TOP)
file_chose_btn.pack(side=TOP,pady=10)
exit_btn.pack(side=TOP,pady=5)

author.pack(side=BOTTOM)

main.mainloop()# main loop to run main window
