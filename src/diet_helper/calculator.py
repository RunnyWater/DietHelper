def get_calories(weight:float, p:float, f:float, c:float) -> float:
        return round((p * 4 + f * 9 + c * 4)*weight, 2)


def get_proteins(weight:float, p:float) -> float:
    return round(p*weight, 2)


def get_fats(weight:float,f:float) -> float:
   return round(f*weight, 2)


def get_carbs(weight:float, c:float) -> float:
    return round(c*weight, 2)