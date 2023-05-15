import os
import re
import pandas as pd
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from Lproducts import *

class App(ttk.Frame):

    # CONSTANTS
    db               = dict()
    temp_product     = producto()
    temp_product.img = None
    db_keys          = ["description", "price", "benefits", "duration", "img"]
    df_products      = pd.read_csv("products.csv")

    for index, row in df_products.iterrows():
        product = producto()
        product.code        = row["code"]
        product.description = row["description"]
        product.price       = row["price"]
        product.benefits    = row["benefits"].split(",")
        product.duration    = row["duration"]
        product.img         = row["img"]
        db[product.code]    = product


    CODE, DESCRIPTION, PRICE, BENEFITS, DURATION, IMG = 0, 1, 2, 3, 4, 5
    P_DES, P_EXA = 0, 1
    PARAMETERS = {
        CODE        : ["Código del producto",      "000000"                       ], 
        DESCRIPTION : ["Descripción del producto", "Descripción..."               ],
        PRICE       : ["Precio del producto",      "0.00"                         ],
        BENEFITS    : ["Beneficios del producto",  "Beneficio 1, Beneficio 2, ..."],
        DURATION    : ["Duración del producto",    "0"                            ],
        IMG         : ["Seleccionar Imagen",       ""                             ]
    }
    PATTERNS = {
        CODE        : [r"^\d{6}$",                           6], 
        DESCRIPTION : [r"^[a-zA-Z\s]+$",                      20], 
        PRICE       : [r"^\d{1,4}(\.\d{1,2})?$",             7], 
        BENEFITS    : [r"^[a-zA-Z0-9 ]+(,[a-zA-Z0-9 ]+)*$", 20], 
        DURATION    : [r"^\d{1,3}$",                         6] 
    }
##########################################################################################

    def __init__(self, master):
        
        super().__init__(master)
        self.pack(fill = BOTH, expand= YES)

        # Sidebar __init__
        self.sidebar_f = ttk.Frame(self, width = 200)
        self.sidebar_f.pack(side = LEFT, fill = Y, expand = YES, anchor="nw")
        self.sidebar_btns = {}
        self.create_sidebar_btns()

        # Main container __init__
        main_container = ttk.Frame(self)
        main_container.pack(side = LEFT, expand = YES, anchor="nw", padx=10, pady=5)
        main_container.grid_rowconfigure(0, weight = 1)
        main_container.grid_columnconfigure(0, weight = 1)


        # LabelFrames __init__
        self.frames ={}

        # Register frame
        register_text = 'Complete los campos para registrar un producto'
        register_lf = ttk.Labelframe(main_container, text = register_text, padding=(15,10,15,10))
        register_lf.configure(style="info.TLabelframe")
        self.frames["register"] = register_lf
        register_lf.grid(row = 0, column = 0, sticky = "nsew")

        # Modify frame
        modify_text = 'Complete los campos para modificar un producto'
        modify_lf = ttk.Labelframe(main_container, text = modify_text, padding=(15,10,15,10))
        modify_lf.configure(style="info.TLabelframe")
        self.frames["modify"] = modify_lf
        modify_lf.grid(row = 0, column = 0, sticky = "nsew")

        # Show register frame
        self.show_lf("register")
        self.register_entries ={}
        self.register_fields()
        self.modify_entries ={}
        self.modify_fields()
        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())
        master.maxsize(master.winfo_width(), master.winfo_height())
##########################################################################################

    def create_sidebar_btns(self):

        register_btn = ttk.Button(
            master=self.sidebar_f,
            text='Registrar producto',
            bootstyle = PRIMARY,
            command=lambda: self.show_lf("register")
        )
        self.sidebar_btns["register"] = register_btn
        register_btn.pack(fill = X,  pady = (15,0), padx = (5,0)) 

        modify_btn = ttk.Button(
            master=self.sidebar_f,
            text='Modificar producto',
            bootstyle = PRIMARY,
            command=lambda: self.show_lf("modify")
        )
        self.sidebar_btns["modify"] = modify_btn
        modify_btn.pack(fill = X, pady = (10,0), padx = (5,0))
##########################################################################################

    def register_fields(self):

        register_frame = ttk.Frame(self.frames["register"])
        register_frame.pack(fill = X, expand = YES, anchor="nw")

        for P in App.PARAMETERS:
            entry = None

            # Prepare label
            label_text = App.PARAMETERS[P][App.P_DES].split()[0]
            label = ttk.Label(register_frame, text = label_text)

            # Handle image entry
            if P == App.IMG:
                label.configure(text = "")
                label.grid(row=0, column=P, sticky="w", padx=5)
                entry = ttk.Button(register_frame,
                    text=App.PARAMETERS[P][App.P_DES], 
                    command=lambda label = label: self.get_img(label)
                )
                entry.grid(row=1, column=P, padx=5)
                entry.configure(style="info.TButton")
                self.register_entries[P] = entry
                continue

            # Handle other entries
            label.grid(row=0, column=P, sticky="w", padx=5)
            entry = ttk.Entry(register_frame,
                    font       = ("DM Sans", 10),
                    foreground = "#ababab",
                    width      = App.PATTERNS[P][1]
            )
            entry.insert(0, App.PARAMETERS[P][App.P_EXA])
            entry.bind("<FocusIn>",  
                lambda event, entry = entry, default_text = App.PARAMETERS[P][App.P_EXA]: 
                self.entry_focus(event, entry, default_text)
            )
            entry.bind("<FocusOut>", 
                lambda event, entry = entry, default_text = App.PARAMETERS[P][App.P_EXA]: 
                self.entry_focus(event, entry, default_text)
            )
            entry.configure(style="info.TEntry")
            entry.grid(row=1, column=P, padx=5)
            
            self.register_entries[P] = entry

            register_btn = ttk.Button(register_frame, 
                text="Registrar", 
                command=lambda: self.get_values(self.register_entries)
            )
            register_btn.configure(style="success.TButton")
            register_btn.grid(row=2, column=0, padx=5, pady=(15,0), sticky="w", columnspan=2)
##########################################################################################

    def modify_fields(self):
        modify_frame = ttk.Frame(self.frames["modify"])
        modify_frame.pack(fill = X, expand = YES, anchor="nw")

        for P in App.PARAMETERS:
            entry = None

            # Prepare label
            label_text = App.PARAMETERS[P][App.P_DES].split()[0]
            label = ttk.Label(modify_frame, text = label_text)

            # Handle image entry
            if P == App.IMG:
                label.configure(text = "")
                label.grid(row=2, column=P-1, sticky="w", padx=5)
                entry = ttk.Button(modify_frame,
                    text=App.PARAMETERS[P][App.P_DES], 
                    command=lambda label = label: self.get_img(label)
                )
                entry.grid(row=3, column=P, padx=5)
                entry.configure(style="info.TButton")
                self.modify_entries[P] = entry
                continue

            # Handle other entries
            entry = ttk.Entry(modify_frame,
                    font       = ("DM Sans", 10),
                    foreground = "#ababab",
                    width      = App.PATTERNS[P][1]
            )
            entry.insert(0, App.PARAMETERS[P][App.P_EXA])
            entry.bind("<FocusIn>",  
                lambda event, entry = entry, default_text = App.PARAMETERS[P][App.P_EXA]: 
                self.entry_focus(event, entry, default_text)
            )
            
            entry.bind("<FocusOut>", 
                lambda event, entry = entry, default_text = App.PARAMETERS[P][App.P_EXA]: 
                self.entry_focus(event, entry, default_text)
            )
            entry.configure(style="info.TEntry")
            if P == App.CODE:
                label.grid(row=0, column=0, sticky="w", padx=5)
                entry.grid(row=1, column=0, padx=5, sticky="w", pady=(0,15))
            else:
                label.grid(row=2, column=P-1, sticky="w", padx=5)
                entry.grid(row=3, column=P-1, padx=5)
                
            self.modify_entries[P] = entry

            search_btn = ttk.Button(modify_frame,
                text="Buscar",
                command=lambda: self.get_values(self.modify_entries)
            )
            search_btn.configure(style="info.TButton")
            search_btn.grid(row=1, column=0, padx=(73, 5), pady=(0,15), sticky="w")

            modify_btn = ttk.Button(modify_frame, 
                text="Modificar", 
                command=lambda: self.get_values(self.modify_entries)
            )
            modify_btn.configure(style="success.TButton")
            modify_btn.grid(row=4, column=0, padx=5, pady=(15,0), sticky="w", columnspan=2)
##########################################################################################

    def show_lf(self, lf_name):

        frame = self.frames[lf_name]
        frame.tkraise()
        for btn in self.sidebar_btns.keys():
            if btn == lf_name:
                self.sidebar_btns[btn].configure(bootstyle = PRIMARY)
            else:
                self.sidebar_btns[btn].configure(bootstyle = OUTLINE)
##########################################################################################

    def entry_focus(self, event, entry, default_text):

        if entry.get() == default_text:
            entry.delete(0, "end")
            entry.config(foreground="#232323")
        elif entry.get() == "":
            entry.insert(0, default_text)
            entry.config(foreground="#ababab")
##########################################################################################

    def get_img(self, label):
        home_dir = os.path.expanduser("~")
        picture_dir = os.path.join(home_dir, "Pictures")
        image_path = filedialog.askopenfilename(
            initialdir = picture_dir, 
            title      ="Seleccione la imagen.", 
            filetypes  =[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        label.configure(text = image_path.split("/")[-1])
        if os.path.exists(image_path):
            App.temp_product.img = image_path
        else:
            App.temp_product.img = None
##########################################################################################

    def get_values(self, entries):
        error_index = None
        error_count = 0
        for P in entries.keys():
            if P == App.IMG:
                if App.temp_product.img == None:
                    error_index = P
                    error_count += 1
                    entries[P].configure(
                        bootstyle = DANGER)
                continue
            elif not re.match(App.PATTERNS[P][0], entries[P].get()) or entries[P].get() == "" or entries[P].get() == App.PARAMETERS[P][App.P_EXA]:
                error_index = P
                error_count += 1
                entries[P].configure(
                    bootstyle = DANGER)
            else:
                entries[P].configure(
                    bootstyle = PRIMARY)

        if error_count == 1:
            messagebox.showinfo(
                "Alert", 
                "El valor ingresado para el parámetro {} es inválido".format(
                    App.PARAMETERS[error_index][App.P_DES]
                )
            )
            return
        if error_count > 1:
            messagebox.showinfo(
                "Alert", 
                "Ingrese valores válidos para los parámetros marcados"
            )
            return
        App.temp_product.code        = int  (entries[App.CODE       ].get())
        App.temp_product.description =       entries[App.DESCRIPTION].get()
        App.temp_product.price       = float(entries[App.PRICE      ].get())
        App.temp_product.benefits    =       entries[App.BENEFITS   ].get().split(",")
        App.temp_product.duration    = int  (entries[App.DURATION   ].get())

        self.register_Product(App.temp_product, App.db)
##########################################################################################

    def modify_Product(self, product, db):

        pass
##########################################################################################

    def register_Product(self, product, db):

        if product.code in db.keys():
            response =messagebox.askyesnocancel("Alert", "El producto {} ya existe, ¿Desea modificarlo?".format(product.code))
            if response:
                self.modify_Product(product, db)
            return
        else:
            db[product.code] = [
                product.description,
                product.price,
                product.benefits,
                product.duration,
                product.img
            ]
            #write db to csv with pandas, each column is a parameter of the product
            df = pd.DataFrame.from_dict(db, orient='index')
            df.to_csv("products.csv", header=App.db_keys, index_label="code")




        messagebox.showinfo("Alert", "Producto registrado con éxito")
##########################################################################################



if __name__ == '__main__':
    app = ttk.Window(themename = "minty")
    app.title("Aromaterapia")
    app.minsize()
    custom_style = ttk.Style(theme="minty")
    custom_style.configure('.', font = ('DM Sans', 10))
    App(app)
    app.mainloop()
