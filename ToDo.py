import tkinter.messagebox as mb
from tkinter import *
from tkinter import ttk
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)
# Connecting to the Database where all information will be stored
connector = sqlite3.connect('TodoList.db')
cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS TASK_DTLS (TASK_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, TASK_NAME TEXT, TASK_DTLS TEXT)"
)

class Todo:

    def remove_record(self):
        if not self.tree.selection():
            mb.showerror('Error!', 'Please select an item from the database')
        else:
            current_item = self.tree.focus()
            values = self.tree.item(current_item)
            selection = values["values"]
            self.tree.delete(current_item)
            connector.execute('DELETE FROM TASK_DTLS WHERE TASK_ID=%d' % selection[0])
            connector.commit()
            mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
            self.display_records()

    def view_record(self):
        if not self.tree.selection():
            mb.showerror('Error!', 'Please select a record to view')
        else:
            current_item = self.tree.focus()
            values = self.tree.item(current_item)
            selection = values["values"]
            self.taskdtlstr.delete("1.0", "end")
            self.name_strvar.set(selection[1]);
            self.taskdtlstr.insert("end", selection[2])

    def reset_form(self):
        global tree
        self.tree.delete(*self.tree.get_children())
        self.reset_fields()

    def reset_fields(self):
        self.name_strvar.set(' ')
        self.taskdtlstr.delete("1.0", "end")

    def add_record(self):
        self.name = self.name_strvar.get()
        self.taskdtls = self.taskdtlstr.get('1.0', 'end')
        if not self.name or not self.taskdtls:
            mb.showerror('Error!', "Please fill all the missing fields!!")
        else:
            #try:
            connector.execute(
                    'INSERT INTO TASK_DTLS (TASK_NAME, TASK_DTLS) VALUES (?,?)', (self.name, self.taskdtls)
            )
            connector.commit()
            mb.showinfo('Record added', f"Record of {self.name} was successfully added")
            self.reset_fields()
            self.display_records()
            #except:
                #mb.showerror('Wrong type',
                 #            'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')

    def display_records(self):
        connector = sqlite3.connect('TodoList.db')
        self.tree.delete(*self.tree.get_children())
        curr = connector.execute('SELECT TASK_ID,TASK_NAME,TASK_DTLS FROM TASK_DTLS')
        data = curr.fetchall()
        for records in data:
            self.tree.insert('', END, values=records)

    def OnDoubleClick(self):
        item = self.tree.focus()
        values = self.tree.item(item)
        selection = values["values"]
        main.clipboard_clear()
        main.clipboard_append(selection[2])

    def __init__(self,main):
        main.title('ToDo Task')

        main.geometry('1000x600')
        main.resizable(0, 0)

    # Creating the background and foreground color variables
        lab_bg = 'Azure2'
        lf_bg = 'Azure1' # bg color for the left_frame
        cf_bg = 'Azure3' # bg color for the center_frame
        rt_bg = 'Azure4'

    # Creating the StringVar or IntVar variables
        self.taskdtlstr = StringVar()
        self.name_strvar = StringVar()

    # Placing the components in the main window
        lable_frame = Frame(main, bg=lab_bg)
        lable_frame.place(relx=0.4, rely=0, relheight=0.05, relwidth=0.6)
        Label(lable_frame, text="ToDo Task", font=headlabelfont, bg=lab_bg).pack(side=TOP, fill=X)

        left_frame = Frame(main, bg=lf_bg)
        left_frame.place(relx=0, rely=0, relheight=0.8, relwidth=0.4)

        button_frame = Frame(main, bg=cf_bg)
        button_frame.place(relx=0, rely=0.8, relheight=0.2, relwidth=0.4)

        right_frame = Frame(main, bg=rt_bg)
        right_frame.place(relx=0.4, rely=0.05, relheight=0.95, relwidth=0.6)

        Label(left_frame, text="Task Name:", font=labelfont, bg=lf_bg).place(relx=0.1, rely=0.05)
        Label(left_frame, text="Task Details:", font=labelfont, bg=lf_bg).place(relx=0.1, rely=0.2)

        Entry(left_frame, width=19, textvariable=self.name_strvar, font=entryfont).place(relx=0.5, rely=0.05)
        self.taskdtlstr = Text(left_frame, width=19, height=19,font=entryfont)
        self.taskdtlstr.place(relx=0.5, rely=0.2)

        Button(button_frame, text='Submit', font=labelfont, command=self.add_record, width=12).place(relx=0.1, rely=0.05)
        Button(button_frame, text='Delete Record', font=labelfont, command=self.remove_record, width=12).place(relx=0.6, rely=0.05)
        Button(button_frame, text='View Record', font=labelfont, command=self.view_record, width=12).place(relx=0.1, rely=0.38)
        Button(button_frame, text='Reset Fields', font=labelfont, command=self.reset_fields, width=12).place(relx=0.6, rely=0.38)
        Button(button_frame, text='Reset Form', font=labelfont, command=self.reset_form, width=12).place(relx=0.35, rely=0.7)

        Label(right_frame, text='Task List', font=headlabelfont, bg='white', fg='LightCyan').pack(side=TOP, fill=X)
        self.tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,columns=('ID', 'Task Name', "Task Details"))
        X_scroller = Scrollbar(self.tree, orient=HORIZONTAL, command=self.tree.xview)
        Y_scroller = Scrollbar(self.tree, orient=VERTICAL, command=self.tree.yview)
        X_scroller.pack(side=BOTTOM, fill=X)
        Y_scroller.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
        self.tree.heading('ID', text='ID', anchor=CENTER)
        self.tree.heading('Task Name', text='Task Name', anchor=CENTER)
        self.tree.heading('Task Details', text='Task Details', anchor=CENTER)
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('#1', width=40, stretch=NO)
        self.tree.column('#2', width=80, stretch=NO)
        self.tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

        self.display_records();

        self.tree.bind('<Double-1>', lambda e:self.OnDoubleClick() )

main = Tk()
todo = Todo(main)
main.update()
main.mainloop()