from diet_helper import Days



def main_function():
    test = Days(db_type='mongo')
    # print(test.days)
    for day in test.days.values():
        print(day)

    # print(test.get_meal_by_id(0).get_macros())
    # test.get_days_mongo()

if __name__ == "__main__":
    main_function()

