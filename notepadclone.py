from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mg
r=Tk()
global userinput,maintext,redoinput,redoid,copytext,cuttext
inputid=0
redoid=0
userinput={}
redoinput={}
#Function to adjust textbox size to always match the window size
def text_adjust(event):
    global textarea
    main_geometry=r.geometry()
    main_geometry=main_geometry.split('+')
    main_geometry=main_geometry[0]
    main_geometry=main_geometry.split('x')
    textarea.config(width=main_geometry[0],height=main_geometry[1])
#Function to open the file and replace textbox text
def openfile():
    global filename
    f=fd.askopenfile(mode='r+',filetypes=[('Text File','.txt')],initialdir='/')
    if f != None:
        maintext=f.read()
        textarea.delete(1.0,END)
        textarea.insert(1.0,maintext)
        filename=f.name
        f.close()
#Function to save the text to a file
def savefile():
    maintext=textarea.get(1.0,END)
    maintext=maintext.rstrip()
    try:
        filename
        f=open(filename,'w')
        f.write(maintext)
        f.close()
    except:
        try:
            file_name=fd.asksaveasfilename(defaultextension='.txt',filetypes=[('Text File','.txt'),('HTML','.html'),('All Files','.*')])
            f=open(file_name,'w')
            f.write(maintext)
            f.close()
        except:
            pass
def saveasfile():
    maintext=textarea.get(1.0,END)
    maintext=maintext.rstrip()
    filename=fd.asksaveasfilename(defaultextension='.txt',filetypes=[('Text File','.txt'),('HTML','.html'),('All Files','.*')])
    f=open(filename,'w')
    f.write(maintext)
    f.close()
def customquit():
    maintext=textarea.get(1.0,END)
    try:
        global filename
        filename
        f=open(filename,'r')
        filetext=f.read()
        f.close()
        maintext=maintext.rstrip("\n")
        filetext=filetext.rstrip("\n")
        if(filetext==maintext):
            r.destroy()
        else:
            confirm_save=Tk()
            def confirmdontsave():
                confirm_save.destroy()
                r.destroy()
            def confirmsave():
                f=open(filename,'w')
                f.write(maintext)
                f.close()
                confirm_save.destroy()
                r.destroy()
            ce_text=Label(confirm_save,text="Would you like to save your changes?",font=('Segoe UI',12))
            ce_yes=Button(confirm_save,text='Save',width=15,borderwidth=0.5,command=confirmsave)
            ce_no=Button(confirm_save,text="Don't Save",width=15,borderwidth=0.5,command=confirmdontsave)
            ce_cancel=Button(confirm_save,text="Cancel",width=15,borderwidth=0.5,command=confirm_save.destroy)
            ce_text.place(relx=0.5,rely=0.2,anchor=CENTER)
            ce_yes.place(relx=0.2,rely=0.6,anchor=CENTER)
            ce_no.place(relx=0.5,rely=0.6,anchor=CENTER)
            ce_cancel.place(relx=0.8,rely=0.6,anchor=CENTER)
            height=str(round(confirm_save.winfo_screenheight()/2-200))
            width=str(round(confirm_save.winfo_screenwidth()/2-450))
            confirm_save.geometry("600x125+"+width+"+"+height)
            confirm_save.resizable(False,False)
            confirm_save.title("Confirm Exit")
            confirm_save.mainloop()
    except:
        alt_maintext=maintext.strip()
        if(alt_maintext==''):
            r.destroy()
        else:
            confirm_save=Tk()
            def confirmdontsave():
                confirm_save.destroy()
                r.destroy()
            def confirmsave():
                filename=fd.asksaveasfilename(defaultextension='.txt',filetypes=[('Text File','.txt'),('HTML','.html'),('All Files','.*')])
                if(filename!=''):
                    f=open(filename,'w')
                    f.write(maintext)
                    f.close()
                    confirm_save.destroy()
                    r.destroy()
                else:
                    confirm_save.destroy()
            ce_text=Label(confirm_save,text="Would you like to save your changes?",font=('Segoe UI',12))
            ce_yes=Button(confirm_save,text='Save',width=15,borderwidth=0.5,command=confirmsave)
            ce_no=Button(confirm_save,text="Don't Save",width=15,borderwidth=0.5,command=confirmdontsave)
            ce_cancel=Button(confirm_save,text="Cancel",width=15,borderwidth=0.5,command=confirm_save.destroy)
            ce_text.place(relx=0.5,rely=0.2,anchor=CENTER)
            ce_yes.place(relx=0.2,rely=0.6,anchor=CENTER)
            ce_no.place(relx=0.5,rely=0.6,anchor=CENTER)
            ce_cancel.place(relx=0.8,rely=0.6,anchor=CENTER)
            height=str(round(confirm_save.winfo_screenheight()/2-200))
            width=str(round(confirm_save.winfo_screenwidth()/2-450))
            confirm_save.geometry("600x125+"+width+"+"+height)
            confirm_save.resizable(False,False)
            confirm_save.title("Confirm Exit")
            confirm_save.mainloop()
def storekey(event):
    textarea.tag_delete("found")
    if(event.state!=12):
        if(event.char!='' or event.keysym in ['BackSpace','Delete']):
            global inputid
            inputid+=1
            undotext=textarea.get(1.0,END)
            undotext=undotext.rstrip("\n")
            userinput[inputid]=undotext
            redoinput.clear()
        if(len(userinput)>150):
            del userinput[min(userinput)]
def undo():
    global redoid
    redoid+=1
    if(userinput!={}):
        undochar=userinput[max(userinput)]
        textarea.delete(1.0,END)
        textarea.insert(1.0,undochar.rstrip("\n"))
        redoinput[redoid]=undochar
        del userinput[max(userinput)]
        if(len(redoinput)>150):
            del redoinput[min(redoinput)]
def undoevent(event):
    undo()
def redo():
    global inputid
    if(redoinput!={}):
        redochar=redoinput[max(redoinput)]
        textarea.delete(1.0,END)
        textarea.insert(1.0,redochar)
        inputid+=1
        userinput[inputid]=redochar
        del redoinput[max(redoinput)]
def redoevent(event):
    redo()
def cut():
    cuttext=textarea.get(SEL_FIRST,SEL_LAST)
    cuttext=cuttext.rstrip("\n")
    textarea.delete(SEL_FIRST,SEL_LAST)
    r.clipboard_append(cuttext)
    r.update()
def copy():
    copytext=textarea.get(SEL_FIRST,SEL_LAST)
    copytext=copytext.rstrip("\n")
    r.clipboard_append(copytext)
    r.update()
def paste():
    clipboard=r.clipboard_get()
    clipboard=clipboard.rstrip("\n")
    textarea.insert(INSERT,clipboard)
def delete():
    textarea.delete(SEL_FIRST,SEL_LAST)
def findwindow():
    findbox=Tk()
    def find():
        global index_start
        global index_end
        find_text=find_entry.get()
        index_start=textarea.search(find_text,1.0,END)
        if(index_start!=''):
            try:
                textarea.tag_delete("found")
            except:
                pass
            textarea.focus_force()
            textarea.mark_set("insert",index_start)
            index_end='%s+%dc'%(index_start,len(find_text))
            textarea.tag_add("found",index_start,index_end)
            textarea.tag_configure("found",background="#D9E310",foreground="black")
            print("Find")
        else:
            mg.showerror("Error","Text not found")
    def findnext():
        global index_start
        global index_end
        find_text=find_entry.get()
        try:
            index_start
            index_start=textarea.search(find_text,index_end,END)
            if(index_start!=''):
                try:
                    textarea.tag_delete("found")
                except:
                    pass
                textarea.focus_force()
                textarea.mark_set("insert",index_start)
                index_end='%s+%dc'%(index_start,len(find_text))
                print(index_end)
                textarea.tag_add("found",index_start,index_end)
                textarea.tag_configure("found",background="#D9E310",foreground="black")
                print("FindNext")
            else:
                mg.showerror("Error","Text not found")
        except:
            find()
    find_entry=Entry(findbox,width=40)
    find_submit=Button(findbox,text="Find",width=5,command=find)
    find_next=Button(findbox,text="Find next",command=findnext)
    find_entry.place(relx=0.3,rely=0.5,anchor=CENTER)
    find_submit.place(relx=0.65,rely=0.5,anchor=CENTER)
    find_next.place(relx=0.8,rely=0.5,anchor=CENTER)
    findbox.geometry("500x50")
    findbox.resizable(False,False)
    findbox.mainloop()
def find_short(event):
    findwindow()
def replace():
    repwin=Tk()
    repwin.geometry("500x50")
    repwin.resizable(False,False)
    repwin.mainloop()
menubar=Menu(r)
filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="Open",command=openfile)
filemenu.add_command(label="Save",command=savefile)
filemenu.add_command(label="Save As",command=saveasfile)
filemenu.add_separator()
filemenu.add_command(label="Exit",command=customquit)
editmenu=Menu(menubar,tearoff=0)
editmenu.add_command(label="Undo",command=undo)
editmenu.add_command(label="Redo",command=redo)
editmenu.add_separator()
editmenu.add_command(label="Cut",command=cut)
editmenu.add_command(label="Copy",command=copy)
editmenu.add_command(label="Paste",command=paste)
editmenu.add_command(label="Delete",command=delete)
editmenu.add_separator()
editmenu.add_command(label="Find",command=findwindow)
editmenu.add_command(label="Replace",command=replace)
infomenu=Menu(menubar,tearoff=0)
infomenu.add_command(label="Source Code")
infomenu.add_command(label="About")
menubar.add_cascade(label='File',menu=filemenu)
menubar.add_cascade(label="Edit",menu=editmenu)
menubar.add_cascade(label="Info",menu=infomenu)
r.config(menu=menubar)
r.bind('<Configure>',text_adjust)
textarea=Text(r,borderwidth=0)
textarea.pack()
textarea.bind("<Key>",storekey)
textarea.bind("<Control-z>",undoevent)
textarea.bind("<Control-y>",redoevent)
textarea.bind("<Control-f>",find_short)
r.title("Notepad Clone")
r.geometry('900x500')
r.mainloop()