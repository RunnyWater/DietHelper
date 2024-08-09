from diet_helper import Days, DaysMenu, FoodsMenu
# from voice_assistant import VoiceAssistant


def main_function():
    # test = Days(db_type='json')
    test = DaysMenu() if input('d/f?') == 'd' else FoodsMenu()
    


if __name__ == "__main__":
    main_function()
