from typing import Any


class Food:
    def __init__(self, name=str, p=str, f=str, c=str, variants=None):
        self.name = name
        self.proteins = p
        self.fats = f
        self.carbs = c
        self.variants = variants

    def update_info(self, name=None, p=None, f=None, c=None, variants=None) -> str:
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


    def get_calories(self, weight=1) -> int:
        return round((int(self.proteins) * 4 + int(self.fats) * 9 + int(self.carbs) * 4)*weight, 2)


    def get_proteins(self, weight=1) -> int:
        return round(int(self.proteins)*weight, 2)
    

    def get_fats(self, weight=1) -> int:
        return round(int(self.fats)*weight, 2)


    def get_carbs(self, weight=1) -> int:
        return round(int(self.carbs)*weight, 2)
    

    def add_variant(self, new_variant):
        if self.variants is None:
            self.variants = {}
        self.variants.update(new_variant)
        return f"{', '.join(new_variant.keys())} added to {self.name}"

    def get_name(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Food(name={self.name}, proteins={self.proteins}, fats={self.fats}, carbs={self.carbs}, variants={self.variants})"
    
    def __str__(self) -> str:
        return f'{self.name} per 100g: {self.proteins}g of proteins, {self.fats}g of fats, {self.carbs}g of carbs'