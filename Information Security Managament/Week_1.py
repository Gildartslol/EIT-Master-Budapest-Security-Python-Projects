# empty list
def convert(s):
    new = ""
    # traverse in the string
    for x in s:
        new += x
        # return string
    return new


if __name__ == '__main__':

    my_list = [88, 85, 84, 71, 66, 72, 65, 82, 74, 70, 87, 70, 85, 68, 74, 84, 81, 87, 79, 82]
    print(my_list)
    characters = [chr(n) for n in my_list]
    print(characters)
    str = convert(characters)
    print(str)
    str = str.lower()
    print(str)
    if len(str) > 10:
        twoToTen = str[2:10]
    else:
        twoToTen = str[2:]

    twoToTen = twoToTen + twoToTen
    print(twoToTen)
