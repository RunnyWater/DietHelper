def get_user_input_date() -> list[int]:
    print("Please provide the information in numbers: year, month, day ( for quit)")
    try:    
        year = int(input("Year: "))
        month = int(input("Month: "))
        day = int(input("Day: "))
    except ValueError:
        if year == 'q' or month == 'q' or day == 'q':
            print("Exiting...")
            return [False, False, False]
        else: 
            print("Invalid input")
            return get_user_input_date()
    
    return [year, month, day]


def get_choice_date(days:dict) -> str:
    while True:
        dates = {i+1:day for i, day in enumerate(list(days.keys()))}
        print(dates)
        user_input= input("Please choose one of the dates (q for quit): ")
        if user_input == 'q':
            break
        elif user_input.isdigit() and int(user_input) in dates.keys():
            break
        else:
            print("Invalid input")
    return dates[user_input]