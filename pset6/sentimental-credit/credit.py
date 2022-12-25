import sys


def main():
    credit_card = get_card_num()

    validate_card(credit_card)
    

def get_card_num():
    while True:
        cardnumber = input("Number: ")
        try:
            if len(cardnumber) > 0 and int(cardnumber):
                break
        except ValueError:
            continue
    return cardnumber


def validate_card(credit_card):
    digits = [13, 15, 16]
    card_len = len(credit_card)
    total = div = mod = 0
    left = []
    underline = []

    # print(card_len)

    if card_len not in digits:
        print("INVALID")
        sys.exit(0)

    if (card_len % 2 == 0):
        for i in range(0, card_len, 2):
            if int(credit_card[i]) * 2 < 10:
                underline.append(int(credit_card[i]) * 2)
            else:
                div = int(credit_card[i]) * 2 // 10
                mod = int(credit_card[i]) * 2 % 10
                underline.append(div)
                underline.append(mod)
        # print("underline: " + str(underline))
        for j in range(1, card_len, 2):
            left.append(int(credit_card[j]))
        # print("left digits: " + str(left))
        total = int(sum(underline)) + int(sum(left))
        # print("even digits")
        # print("total: " + str(total))
    else:
        for i in range(1, card_len, 2):
            if int(credit_card[i]) * 2 < 10:
                underline.append(int(credit_card[i]) * 2)
            else:
                div = int(credit_card[i]) * 2 // 10
                mod = int(credit_card[i]) * 2 % 10
                underline.append(div)
                underline.append(mod)
        for j in range(0, card_len, 2):
            left.append(int(credit_card[j]))
        total = int(sum(underline)) + int(sum(left))
        # print("odd digits")
        # print(total)

    if (total % 10 != 0):
        print("INVALID")

        sys.exit(0)

    # check card type
    # First two digits
    first = int(credit_card[0])
    second = int(credit_card[1])

    if first == 3 and (second == 4 or second == 7) and card_len == 15:
        print("AMEX")
    elif first == 5 and (second <= 5 and second > 0) and card_len == 16:
        print("MASTERCARD")
    elif first == 4 and (card_len == 13 or card_len == 16):
        print("VISA")
    else:
        print("INVALID")
        sys.exit(0)


if __name__ == "__main__":
    main()