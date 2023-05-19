import re
import os
import pandas as pd
import ttkbootstrap as ttk
from Producto import Product
from tkinter import filedialog
from tkinter import messagebox
from ttkbootstrap.constants import *
import control_registro_producto as crp

class Pantalla(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill = BOTH, expand = YES)
        self.parameters_keys = crp.get_Keys()
        self.aux_product = Product()

        # Sidebar frame __init__
        self.sidebar_f = ttk.Frame(self, width = 200)
        self.sidebar_f.pack(side = LEFT, fill = Y, expand = YES, anchor="nw")
        self.sidebar_btns = {}
        self.create_sidebar_btns()
        
        # Main container frame __init__
        main_container = ttk.Frame(self)
        main_container.pack(side = LEFT, expand = YES, anchor="nw", padx=10, pady=5)
        main_container.grid_rowconfigure(0, weight = 1)
        main_container.grid_columnconfigure(0, weight = 1)

        # Main container frame content __init__
        self.frames = {}

        # Register product frame __init__
        register_text = 'Complete los campos para registrar un producto nuevo'
        register_lf = ttk.Labelframe(main_container, text = register_text, padding=(15,10,10,10))
        register_lf.configure(style="info.TLabelframe")
        register_lf.grid(row = 0, column = 0, sticky = "nsew")
        self.frames["REGISTER"] = register_lf
        self.register_entries = {}
        self.register_img_btn = None
        self.register_img_label = None
        self.create_register_fields()

        # Modify product frame __init__
        modify_text = 'Complete los campos para modificar un producto'
        modify_lf = ttk.Labelframe(main_container, text = modify_text, padding=(15,10,10,10))
        modify_lf.configure(style="info.TLabelframe")
        modify_lf.grid(row = 0, column = 0, sticky = "nsew")
        self.frames["MODIFY"] = modify_lf
        self.modify_entries = {}
        self.modify_control_btns = {}
        self.modify_img_btn = None
        self.modify_img_label = None
        self.create_modify_fields()

        # Show register frame
        self.show_lf("REGISTER")
        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())
    # end __init__


    def create_sidebar_btns(self):
        register_btn = ttk.Button(
            master=self.sidebar_f,
            text='Registrar producto',
            bootstyle = PRIMARY,
            command=lambda: self.show_lf("REGISTER")
        )
        self.sidebar_btns["REGISTER"] = register_btn
        register_btn.pack(fill = X,  pady = (15,0), padx = (5,0)) 

        modify_btn = ttk.Button(
            master=self.sidebar_f,
            text='Modificar producto',
            bootstyle = PRIMARY,
            command=lambda: self.show_lf("MODIFY")
        )
        self.sidebar_btns["MODIFY"] = modify_btn
        modify_btn.pack(fill = X, pady = (10,0), padx = (5,0))
    # end create_sidebar_btns

    def create_register_fields(self):
        register_frame = ttk.Frame(self.frames["REGISTER"])
        register_frame.pack(fill = X, expand = YES, anchor="nw")
        register_btn = ttk.Button(register_frame, 
            text="Registrar", 
            command=lambda: self.register_product()
        )
        register_btn.configure(style="success.TButton")
        register_btn.grid(row=2, column=0, padx=5, pady=(15,0), sticky="w", columnspan=2)
        label_text = ''

        for index, P in enumerate(self.parameters_keys):
            entry = None
            label_text = crp.get_Parameter_Description(P)
            label = ttk.Label(register_frame, text = label_text)
            label.grid(row=0, column=index, sticky="w", padx=5)
            entry = ttk.Entry(register_frame,
                    font       = ("DM Sans", 10),
                    foreground = "#ababab",
                    width      = crp.get_Parameter_Width(P)
            )
            entry.insert(0, crp.get_Parameter_Default_Value(P))
            entry.bind("<FocusIn>",  
                lambda event, entry = entry, default_text = crp.get_Parameter_Default_Value(P):
                self.entry_focus(event, entry, default_text)
            )
            entry.bind("<FocusOut>", 
                lambda event, entry = entry, default_text = crp.get_Parameter_Default_Value(P): 
                self.entry_focus(event, entry, default_text)
            )
            entry.configure(style="info.TEntry")
            entry.grid(row=1, column=index, padx=5)
            self.register_entries[P] = entry

        label = ttk.Label(register_frame)
        label.grid(row=0, column=index+1, sticky="w", padx=5)
        self.register_img_label = label
        btn = ttk.Button(register_frame,
            text="Seleccionar imagen",
            command=lambda label = label: self.get_img(label)
        )
        btn.grid(row=1, column=index+1, padx=5)
        btn.configure(style="info.TButton")
        self.register_img_btn = btn
    # end create_register_fields

    def create_modify_fields(self):
        modify_frame = ttk.Frame(self.frames["MODIFY"])
        modify_frame.pack(fill = X, expand = YES, anchor="nw")

        search_btn = ttk.Button(modify_frame,
            text="Buscar",
            command=lambda: self.search_product()
        )
        search_btn.configure(bootstyle = INFO)
        search_btn.grid(row=1, column=0, padx=(73, 5), pady=(0,15), sticky="w")
        self.modify_control_btns["SEARCH"] = search_btn

        modify_btn = ttk.Button(modify_frame, 
            text="Modificar", 
            command=lambda: self.modify_product()
        )
        modify_btn.configure(bootstyle = SUCCESS)
        modify_btn.configure(state = DISABLED)
        modify_btn.grid(row=3, column=6, padx=5)
        self.modify_control_btns["MODIFY"] = modify_btn
        
        cancel_btn = ttk.Button(modify_frame,
            text="Cancelar",
            command=lambda: self.cancel_modify
        )
        cancel_btn.configure(bootstyle = DANGER)
        cancel_btn.configure(state = DISABLED)
        cancel_btn.grid(row=3, column=7, padx=5)
        self.modify_control_btns["CANCEL"] = cancel_btn
        
        label_text = ''

        for index, P in enumerate(self.parameters_keys):
            entry = None
            label_text = crp.get_Parameter_Description(P)
            label = ttk.Label(modify_frame, text = label_text)
            
            entry = ttk.Entry(modify_frame,
                font       = ("DM Sans", 10),
                foreground = "#ababab",
                width      = crp.get_Parameter_Width(P)
            )
            entry.insert(0, crp.get_Parameter_Default_Value(P))
            entry.bind("<FocusIn>",
                lambda event, entry = entry, default_text = crp.get_Parameter_Default_Value(P):
                self.entry_focus(event, entry, default_text)
            )
            entry.bind("<FocusOut>",
                lambda event, entry = entry, default_text = crp.get_Parameter_Default_Value(P):
                self.entry_focus(event, entry, default_text)
            )

            if P == self.parameters_keys[0]: # P == "CODE"
                label.grid(row=0, column=0, sticky="w", padx=5)
                entry.configure(bootstyle= INFO)
                entry.grid(row=1, column=0, padx=5, sticky="w", pady=(0,15))
            else:
                label.grid(row=2, column=index - 1, sticky="w", padx=5)
                entry.configure(bootstyle= DISABLED)
                entry.configure(state = "disabled")
                entry.grid(row=3, column=index - 1, padx=5)
            
            self.modify_entries[P] = entry

        label = ttk.Label(modify_frame)
        label.grid(row=2, column=index, sticky="w", padx=5)
        self.modify_img_label = label
        btn = ttk.Button(modify_frame,
            text="Seleccionar imagen",
            command=lambda label = label: self.get_img(label)
        )
        btn.grid(row=3, column=index, padx=5)
        btn.configure(style="info.TButton", state=DISABLED)
        self.modify_img_btn = btn
    # end create_modify_fields

    def show_lf(self, lf_name):
        frame = self.frames[lf_name]
        frame.tkraise()
        self.sidebar_btns[lf_name].configure(bootstyle = PRIMARY)
        for key in self.sidebar_btns.keys():
            if key != lf_name:
                self.sidebar_btns[key].configure(bootstyle = OUTLINE)
    # end show_lf

    def entry_focus(self, event, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, END)
            entry.configure(foreground = "#232323")
        elif entry.get() == '':
            entry.insert(0, default_text)
            entry.configure(foreground = "#ababab")
    # end entry_focus

    def get_img(self, label):
        home_dir = os.path.expanduser("~")
        pic_dir = os.path.join(home_dir, "Pictures")
        img_path = filedialog.askopenfilename(
            initialdir = pic_dir,
            title = "Seleccionar imagen",
            filetypes = (("Archivos de imagen", "*.png *.jpg *.jpeg *.gif"), ("Todos los archivos", "*.*"))
        )
        if os.path.isfile(img_path):
            label.configure(text = img_path.split("/")[-1])
            self.aux_product.IMG = img_path
        else:
            label.configure(text = '')
            self.aux_product.IMG = ''
    # end get_img
        
    def search_product(self):
        code = self.modify_entries[self.parameters_keys[0]].get()
        if code == crp.get_Parameter_Default_Value(self.parameters_keys[0]) or code == '' or not crp.isValidCode(code):
            messagebox.showerror("Error", "Ingrese un código de producto válido")
            return
        if not crp.is_Registered(code):
            messagebox.showerror("Error", "El producto no está registrado")
            return
        
        self.aux_product = crp.get_Product(code)
        
        self.modify_entries["CODE"].configure(state = DISABLED)
        for P in self.parameters_keys[1:]:
            self.modify_entries[P].configure(state = ACTIVE)
            self.modify_entries[P].configure(bootstyle = INFO)
            self.modify_entries[P].configure(cursor = 'xterm')
            self.modify_entries[P].delete(0, "end")
            self.modify_entries[P].insert(0, getattr(self.aux_product, P))
            self.modify_entries[P].configure(foreground = "#232323")

        self.modify_img_label.configure(text = getattr(self.aux_product, "IMG").split("/")[-1])
        self.modify_img_btn.configure(state = ACTIVE)
        self.modify_control_btns["MODIFY"].configure(state = ACTIVE)
        self.modify_control_btns["CANCEL"].configure(state = ACTIVE)
        self.modify_control_btns["SEARCH"].configure(state = DISABLED)
    # end search_product

    def register_product(self):
        is_valid, errors_in = crp.Verify_Data(self.register_entries, self.aux_product.IMG)
        if not is_valid:
            if len(errors_in) == 1:
                messagebox.showerror("Error", 
                    "El valor ingresado para el parámetro {} no es válido".format(crp.get_Parameter_Description(errors_in[0]))
                )	
            if len(errors_in) > 1:
                messagebox.showerror("Error", "Ingrese valores válidos en los campos marcados")
            self.invalid_data(self.register_entries, errors_in, "REGISTER")
            return
        
        self.aux_product.CODE        = self.register_entries["CODE"].get()
        self.aux_product.DESCRIPTION = self.register_entries["DESCRIPTION"].get()
        self.aux_product.PRICE       = float(self.register_entries["PRICE"].get())
        self.aux_product.BENEFITS    = self.register_entries["BENEFITS"].get()
        self.aux_product.DURATION    = int(self.register_entries["DURATION"].get())
    
        if crp.is_Registered(self.aux_product.CODE):
            response = messagebox.askyesnocancel("Alert", "El producto {} ya existe. ¿Desea modificarlo?".format(self.aux_product.CODE))
            if response:
                crp.Modify_Product(self.aux_product)
                self.clear_entries(self.register_entries, "REGISTER")
                messagebox.showinfo("Éxito", "El producto se ha modificado correctamente")
            return

        response = messagebox.askyesnocancel("Alert", "¿Desea registrar el producto {}?".format(self.aux_product.CODE))
        if response:
            crp.Register_Product(self.aux_product)
            self.valid_data(self.register_entries, self.parameters_keys[1:], "REGISTER")
            self.clear_entries(self.register_entries, "REGISTER")
            messagebox.showinfo("Éxito", "El producto se ha registrado correctamente")
    # end register_product

    def modify_product(self):
        is_valid, errors_in = crp.Verify_Data(self.modify_entries, self.aux_product.IMG)
        if not is_valid:
            if len(errors_in) == 1:
                messagebox.showerror("Error", 
                    "El valor ingresado para el parámetro {} no es válido".format(crp.get_Parameter_Description(errors_in[0]))
                )	
            if len(errors_in) > 1:
                messagebox.showerror("Error", "Ingrese valores válidos en los campos marcados")
            self.invalid_data(self.modify_entries, errors_in, "MODIFY")
            return
        
        self.aux_product.DESCRIPTION = self.modify_entries["DESCRIPTION"].get()
        self.aux_product.PRICE       = float(self.modify_entries["PRICE"].get())
        self.aux_product.BENEFITS    = self.modify_entries["BENEFITS"].get()
        self.aux_product.DURATION    = int(self.modify_entries["DURATION"].get())
    
        if not crp.is_Registered(self.aux_product.CODE):
            response = messagebox.askyesnocancel("Alert", "El producto {} no esta registrado. ¿Desea registrarlo?".format(self.aux_product.CODE))
            if response:
                crp.Register_Product(self.aux_product)
                self.clear_entries(self.register_entries, "MODIFY")
                messagebox.showinfo("Éxito", "El producto se ha registrado correctamente")
            return
        
        response = messagebox.askyesnocancel("Alert", "¿Desea modificar el producto {}?".format(self.aux_product.CODE))
        if response:
            crp.Modify_Product(self.aux_product)
            self.valid_data(self.modify_entries, self.parameters_keys[1:], "MODIFY")
            self.clear_entries(self.modify_entries, "MODIFY")
            messagebox.showinfo("Éxito", "El producto se ha modificado correctamente")

    def invalid_data(self, entries : dict, keys : list, from_f : str):
        for key in keys:
            if key == "IMG" and from_f == "MODIFY":
                self.modify_img_btn.configure(bootstyle = DANGER)
                continue
            if key == "IMG" and from_f == "REGISTER":
                self.register_img_btn.configure(bootstyle = DANGER)
                continue
            entries[key].configure(bootstyle = DANGER)
        valid_keys = [value for value in self.parameters_keys + ["IMG"] if value not in keys]
        print("valid keys {}".format(valid_keys))
        self.valid_data(entries, valid_keys, from_f)
    # end invalid_data

    def valid_data(self, entries : dict, keys : list, from_f : str):
        for key in keys:
            if key == "IMG" and from_f == "MODIFY":
                self.modify_img_btn.configure(bootstyle = INFO)
                continue
            if key == "IMG" and from_f == "REGISTER":
                self.register_img_btn.configure(bootstyle = INFO)
                continue
            entries[key].configure(bootstyle = INFO)
    # end valid_data

    def clear_entries(self, entries : dict, from_f : str):
        if from_f == "MODIFY":
            self.modify_img_label.configure(text = '')
            entries["CODE"].configure(state = ACTIVE)
            for key in entries.keys():
                entries[key].delete(0, END)
                entries[key].insert(0, crp.get_Parameter_Default_Value(key))
                entries[key].configure(foreground = "#ababab")
                entries[key].configure(bootstyle = DISABLED)
                entries[key].configure(state = DISABLED)
            entries["CODE"].configure(state = ACTIVE)
            entries["CODE"].configure(bootstyle = INFO)
            self.modify_img_btn.configure(state = DISABLED)
            self.modify_control_btns["MODIFY"].configure(state = DISABLED)
            self.modify_control_btns["CANCEL"].configure(state = DISABLED)
            self.modify_control_btns["SEARCH"].configure(state = ACTIVE)

        if from_f == "REGISTER":
            for key in entries.keys():
                entries[key].delete(0, END)
                entries[key].insert(0, crp.get_Parameter_Default_Value(key))
                entries[key].configure(foreground = "#ababab")
                entries[key].configure(bootstyle = INFO)
            self.register_img_label.configure(text = '')
    # end clear_entries