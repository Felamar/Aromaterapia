import os
import pandas as pd

class Product(object):
    def __init__(self, code = None, description = None, price = None, benefits = None, duration = None, img = None):
        self.CODE        = code
        self.DESCRIPTION = description
        self.PRICE       = price
        self.BENEFITS    = benefits
        self.DURATION    = duration
        self.IMG         = img
    
    
    @classmethod
    def get_products(self):
        db_keys = ["DESCRIPTION", "PRICE", "BENEFITS", "DURATION", "IMG"]
        db = {}
        if not os.path.isfile("products.csv"):
            df = pd.DataFrame(columns=["CODE"] + db_keys)
            df.to_csv('products.csv', index=False)
        else:
            df_products = pd.read_csv("products.csv", dtype={"CODE": str})
            for row in df_products.iterrows():
                code, description, price, benefits, duration, img = map(lambda x: row[1][x], ["CODE"] + db_keys)
                product = Product(code, description, price, benefits, duration, img)
                db[product.CODE] = product
        return db

    @classmethod
    def get_product(self, code):
        return self.get_products().get(code, None)