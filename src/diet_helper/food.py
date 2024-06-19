from .calculator import * 

class Food:
    def __init__(self, name, p, f, c, variants=None):
        self.name = str(name)
        self.proteins = int(p)
        self.fats = int(f)
        self.carbs = int(c)
        self.variants = variants

    def update_info(self, name=str, p=int, f=int, c=int, variants=None) -> str:
        if name is not None:
            self.name = name
        if p is not None:
            self.proteins = p
        if f is not None:
            self.fats = f
        if c is not None:
            self.carbs = c
        if variants is not None:
            self.variants = {}
        return f'{self.name} updated'
    

    def add_variant(self, new_variant):
        if self.variants is None:
            self.variants = {}
        self.variants.update(new_variant)
        return f"{', '.join(new_variant.keys())} added to {self.name}"


    def update_variant(self, variant_name, new_weight):
        if self.variants is None or variant_name not in list(self.variants.keys()):
            print( f"{self.name} has no variant with name {variant_name}\nPlease choose out of the following: {', '.join(self.variants.keys())}")
            return '404'
        self.variants[variant_name] = new_weight
        return f"variant {self.name} now has {new_weight}"
    

    def delete_variant(self, variant_name):
        if self.variants is None:
            return f"food `{self.name}` has no variants"
        del self.variants[variant_name]
        if len(self.variants) == 0:
            self.variants = None
            return f"food `{self.name}` has no variants"
        return f"variant {self.name} now has {self.variants}"


    def get_name(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Food(name={self.name}, proteins={self.proteins}, fats={self.fats}, carbs={self.carbs}, variants={self.variants})"
    
    def __str__(self) -> str:
        return f'{self.name} per 100g: {self.proteins}g of proteins, {self.fats}g of fats, {self.carbs}g of carbs'