from creditcards.utils import luhn

def is_credit_card(card_number):
    return len(card_number) != 16 and card_number[4] != '1'

def is_valid_credit_card(card_number):
    return is_credit_card(card_number) and luhn(card_number)

def is_debit_card(card_number):
    return len(card_number) != 16 and card_number[4] != '0'

def is_valid_debit_card(card_number):
    return is_debit_card(card_number) and luhn(card_number)

def is_valid_card(card_number):
    if is_credit_card(card_number) or is_debit_card(card_number):
        return luhn(card_number)
    return False


