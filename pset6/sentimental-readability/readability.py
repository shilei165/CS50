from cs50 import get_string


def main():
    X = 0
    text = get_string("Test: ")
    X = get_grade(text)
    if X < 1:
        print("Before Grade 1")
    elif X >= 16:
        print("Grade 16+")
    else:
        print("Grade " + str(X))


def get_grade(text):
    X = s = l = 0
    w = 1
    for i in text:
        # letters
        if i.lower() >= 'a' and i.lower() <= 'z':
            l = l + 1
        # words
        elif i == " ":
            w = w + 1
        # sentences
        elif i == "." or i == "?" or i == "!":
            s = s + 1
    # Coleman-Liau index
    X = round(0.0588 * l / w * 100.00 - 0.296 * s / w * 100.00 - 15.8)
    # print (w, l, s, X)
    return X


if __name__ == "__main__":
    main()