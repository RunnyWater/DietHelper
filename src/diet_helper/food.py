from typing import Any


class Food:
    def __init__(self, name=str, p=str, f=str, c=str, variants=None):
        self.name = name
        self.proteins = p
        self.fats = f
        self.carbs = c
        self.variants = variants

    def updateInfo(self, name=None, p=None, f=None, c=None, variants=None) -> str:
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

    def __repr__(self) -> str:
        return f"Food(name={self.name}, proteins={self.proteins}, fats={self.fats}, carbs={self.carbs}, variants={self.variants})"
    
    def __str__(self) -> str:
        return self.name