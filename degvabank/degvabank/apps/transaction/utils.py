def is_our_card(number):
    return number.startswith("1337")

def is_our_account(number):
    return number.startswith("00691337")

def is_our_number(number):
    return is_our_card(number) or is_our_account(number)

def is_card(number):
    return len(number) == 16

def is_account(number):
    return len(number) == 20
