from tkinter import *
import random
from tkinter import messagebox
import sqlite3
import os

root = Tk()
root.title('Billing')
root.geometry('1280x720')
bg_color = 'black'

conn = sqlite3.connect('Billing.db')
c=conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS bills (
                bill_no TEXT PRIMARY KEY,
                customer_name TEXT,
                customer_phone TEXT,
                total_amount REAL
            )''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS bill_items (
                bill_no TEXT,
                product_name TEXT,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY (bill_no) REFERENCES bills (bill_no)
            )''')
conn.commit()





c_name=StringVar()
c_phone=StringVar()
item = StringVar()
Rate = IntVar()
Quantity = IntVar()
bill_no=StringVar()
x = random.randint(1000,9999)
bill_no.set(str(x))
global l
l=[]
def welcome():
    textarea.delete(1.0,END)
    textarea.insert(END,"\t Welcome Textiles")
    textarea.insert(END, f'\n\nBill Number:\t\t{bill_no.get()}')
    textarea.insert(END,f'\nCustomer Name:\t\t{c_name.get()}')
    textarea.insert(END,f'\nCustomer Phone No.:\t\t{c_phone.get()}')
    textarea.insert(END,f'\n\t==================================')
    textarea.insert(END,'\n Product\t\t\tQuantity\t\t     Price')
    textarea.insert(END,f'\n\t==================================\n')
    textarea.configure(font='arial 12 bold')

def clear_item_fields():
    item.set('')
    Rate.set(0)
    Quantity.set(0)


def additm():
    n=Rate.get()
    m = Quantity.get()*n
    l.append(m)
    if item.get()=='':
        messagebox.showerror('Error','Please enter the item')
    else:
        textarea.insert((10.0+float(len(l)-1)),f'{item.get()}\t\t\t{Quantity.get()}\t\t{m}\n')
        clear_item_fields()

def gbill():
        if c_name.get()=='' or c_phone.get=='':
            messagebox.showerror('Error','Customer Details are must')
        else:
            tex=textarea.get(10.0,(10.0+float(len(l))))
            welcome()
            textarea.insert(END,tex)
            textarea.insert(END,f'\n\t==================================')
            textarea.insert(END,f'\n\t\t\tTotal Paybill Amount : \t\t\t{sum(l)}')
            textarea.insert(END,f'\n\t==================================')
            savebill()
            clear_bill_area()

def savebill():
    op = messagebox.askyesno('Save bill','Do you want to save the bill')
    if op>0:
        try:
            # Insert the bill data into the bills table
            c.execute("INSERT INTO bills (bill_no, customer_name, customer_phone, total_amount) VALUES (?, ?, ?, ?)", 
                      (bill_no.get(), c_name.get(), c_phone.get(), sum(l)))
            
            # Insert the product details into the bill_items table
            for i in range(len(l)):
                product_name = item.get()
                quantity = Quantity.get()
                price = l[i]
                c.execute("INSERT INTO bill_items (bill_no, product_name, quantity, price) VALUES (?, ?, ?, ?)", 
                          (bill_no.get(), product_name, quantity, price))
                
            conn.commit()
            messagebox.showinfo('Saved', f'Bill no.: {bill_no.get()} Saved successfully in database')
        
        except Exception as e:
            conn.rollback()  # Rollback in case of error
            messagebox.showerror("Database Error", f"Error: {str(e)}")

    else:
        return


def print_bill():
    op = messagebox.askyesno('Print bill', 'Do you want to print the bill?')
    if op > 0:
        bill_details = textarea.get(1.0, END)
        with open(f"{bill_no.get()}.txt", "w") as bill_file:
            bill_file.write(bill_details)
        os.startfile(f"{bill_no.get()}.txt", "print")  # Use subprocess for more control



def clear():
    c_name.set('')
    c_phone.set('')
    item.set('')
    Rate.set(0)
    Quantity.set(0)

def clear_bill_area():
    textarea.delete(1.0, END)
    l.clear() 

def exit():
    op = messagebox.askyesno('Exit','Do you want to exit?')
    if op>0:
        conn.close()
        root.destroy()
    

title = Label(root,text='Billing Software',bg=bg_color,fg='white',font=('Lucida',25,'bold'),relief=GROOVE,bd=12)
title.pack(fill=X)


F1 = LabelFrame(root,text='Customer Details',font=('Lucida',18,'bold'),relief=GROOVE,bd=10,bg=bg_color,fg='gold')
F1.place(x=0,y=80,relwidth=1)

cname_label = Label(F1,text='Customer Name:',font=('Lucida',18,'bold'),bg=bg_color,fg='white')
cname_label.grid(row=0,column=0,padx=10,pady=5)

cname_txt = Entry(F1,width=15,font='arial 15 bold',relief = SUNKEN,textvariable=c_name)
cname_txt.grid(row=0,column=1,padx=10,pady=5)

cno_label = Label(F1,text='Phone No.:',font=('Lucida',18,'bold'),bg=bg_color,fg='white')
cno_label.grid(row=0,column=2,padx=10,pady=5)


def validate_phone_number(action, value_if_allowed):
    if action == '1':  # 1 -> Insert, so validate the input
        if value_if_allowed.isdigit() and len(value_if_allowed)<=10:  # Only allow digits
            return True
        elif not value_if_allowed.isdigit():
            messagebox.showerror('Error','Please enter digits in phone number')
            return False
        elif len(value_if_allowed)>10:
            messagebox.showerror('Invalid input','Phone number cannot exceed 10 digits.')
            return False

    else:
        return True  # Allow deletion of characters

# Registering the validation function with the Tkinter root
vcmd = (root.register(validate_phone_number), '%d', '%P')

cno_txt = Entry(F1,width=15,font='arial 15 bold',relief = SUNKEN,textvariable=c_phone,validate='key',validatecommand=vcmd)
cno_txt.grid(row=0,column=3,padx=10,pady=5)

F2 = LabelFrame(root,text='Product Details',font=('Lucida',18,'bold'),relief=GROOVE,bd=10,bg=bg_color,fg='gold')
F2.place(x=20,y=180,width=630,height=500)

itm=Label(F2,text='Product Name',font=('Lucida',18,'bold'),bg=bg_color,fg='lightgreen')
itm.grid(row=0,column=0,padx=30,pady=20)
itm_txt = Entry(F2,width=20,font='arial 15 bold',textvariable=item)
itm_txt.grid(row=0,column=1,padx=30,pady=20)

rate=Label(F2,text='Product Rate',font=('Lucida',18,'bold'),bg=bg_color,fg='lightgreen')
rate.grid(row=1,column=0,padx=30,pady=20)
rate_txt = Entry(F2,width=20,font='arial 15 bold',textvariable=Rate)
rate_txt.grid(row=1,column=1,padx=30,pady=20)

quantity=Label(F2,text='Product Quantity',font=('Lucida',18,'bold'),bg=bg_color,fg='lightgreen')
quantity.grid(row=2,column=0,padx=30,pady=20)
quantity_txt = Entry(F2,width=20,font='arial 15 bold',textvariable=Quantity)
quantity_txt.grid(row=2,column=1,padx=30,pady=20)

btn1 = Button(F2,text='Add Item', font='arial 15 bold',padx=5,pady=10,bg='green',width=15,command=additm)
btn1.grid(row=3,column=0,padx=10,pady=30)

btn2 = Button(F2,text='Generate Bill', font='arial 15 bold',padx=5,pady=10,bg='green',width=15,command=gbill)
btn2.grid(row=3,column=1,padx=10,pady=30)

btn3 = Button(F2,text='Clear', font='arial 15 bold',padx=5,pady=10,bg='green',width=15,command=clear)
btn3.grid(row=4,column=0,padx=10,pady=30)

btn4 = Button(F2, text='Print', font='arial 15 bold', padx=5, pady=10, bg='green', width=15, command=print_bill)
btn4.grid(row=4, column=1, padx=10, pady=30)

btn5 = Button(F2, text='Exit', font='arial 15 bold', padx=5, pady=10, bg='green', width=15, command=exit)
btn5.grid(row=5, column=0, padx=10, pady=30)


F3 = Frame(root,relief=GROOVE,bd=10)
F3.place(x=700,y=180,width=500,height=500)

bill_title=Label(F3,text='Bill Area',font='arial 15 bold',relief=GROOVE,bd=7).pack(fill=X)
scroll_y=Scrollbar(F3,orient=VERTICAL)
textarea = Text(F3,yscrollcommand=scroll_y)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_y.config(command=textarea.yview)
textarea.pack()
welcome()


root.mainloop()
