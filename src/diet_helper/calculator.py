def get_calories(weight=1, p=int, f=int, c=int) -> int:
        return round((p * 4 + f * 9 + c * 4)*weight, 2)


def get_proteins(weight=1, p=int) -> int:
    return round(p*weight, 2)


def get_fats(weight=1,f=int) -> int:
   return round(f*weight, 2)


def get_carbs(weight=1, c=int) -> int:
    return round(c*weight, 2)