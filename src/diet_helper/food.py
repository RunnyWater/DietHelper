class Food:
    def __init__(self, name=str, p=str, f=str, c=str, variants=dict):
        self.name = name
        self.proteins = p
        self.fats = f
        self.carbs = c
        self.variants = variants

    def __repr__(self) -> str:
        return f"Food(name={self.name}, proteins={self.proteins}, fats={self.fats}, carbs={self.carbs}, variants={self.variants})"
    
    def __str__(self) -> str:
        return self.name