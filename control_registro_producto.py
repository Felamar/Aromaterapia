import re
import os
import pandas as pd
from Producto import Product

KEYS = ["CODE", "DESCRIPTION", "PRICE", "BENEFITS", "DURATION"]

PATTERNS = [
    r"^\d{6}$",                          # CODE
    r"^[a-zA-Z0-9\s]+$",                 # DESCRIPTION
    r"^\d{1,4}(\.\d{1,2})?$",            # PRICE
    r"^[a-zA-Z0-9 ]+(,[a-zA-Z0-9 ]+)*$", # BENEFITS
    r"^\d{1,3}$"                         # DURATION
]


DEFAULT_VALUES = [
    "000000",                        # CODE
    "Descripción...",                # DESCRIPTION
    "0.00",                          # PRICE
    "Beneficio 1, Beneficio 2, ...", # BENEFITS
    "0"                              # DURATION
]

DESCRIPTIONS = [
    "Código",
    "Descripción",
    "Precio",
    "Beneficios",
    "Duración"
]

WIDTHS = [6, 20, 8, 20, 6]


def get_Keys() -> list:
    return KEYS

def get_Parameter_Default_Value(Parameter : str) -> str:
    return dict(zip(KEYS, DEFAULT_VALUES))[Parameter]

def get_Parameter_Description(Parameter : str) -> str:
    if Parameter != "IMG":
        return dict(zip(KEYS, DESCRIPTIONS))[Parameter]
    return "Imagen"

def get_Parameter_Width(Parameter : str) -> int:
    return dict(zip(KEYS, WIDTHS))[Parameter]

def is_Registered(code: str) -> bool:
    df = pd.read_csv("products.csv", dtype={"CODE": str})
    return code in df["CODE"].values

def isValidCode(code : int) -> bool:
    return re.match(PATTERNS[0], str(code))

def get_Product(code : int) -> Product:
    return Product.get_product(code)

def Verify_Data(fields: dict, image_path : str) -> tuple:
    default_patterns = dict(zip(KEYS, PATTERNS))
    default_field_values = dict(zip(KEYS, DEFAULT_VALUES))
    errors_in_fields = []
    aux_keys = KEYS

    for field in aux_keys:
        if fields[field].get() == default_field_values[field] or fields[field].get() == "" or not (re.match(default_patterns[field], fields[field].get())) :
            errors_in_fields.append(field)
    if image_path == None or not os.path.isfile(image_path):
        errors_in_fields.append("IMG")

    return len(errors_in_fields) == 0, errors_in_fields

def Register_Product(product : Product):
    df = pd.read_csv("products.csv", dtype={"CODE": str})
    print(df)
    df = pd.concat([df, pd.DataFrame(product.__dict__, index=[0])], ignore_index=False)
    df.to_csv('products.csv', index=False)

def Modify_Product(product : Product):
    df = pd.read_csv("products.csv", dtype={"CODE": str})
    df.loc[df["CODE"] == product.CODE, ["DESCRIPTION", "PRICE", "BENEFITS", "DURATION", "IMG"]] = [product.DESCRIPTION, product.PRICE, product.BENEFITS, product.DURATION, product.IMG]
    df.to_csv('products.csv', index=False)
