import json
import random
import os
import csv

def deprecate_space(str):
    if len(str) > 0:
        while str[0] == " ":
            str = str[1:]
        while str[-1] == " ":
            str = str[:-1]
    return str

def deprecate_duplication(str):
    for i in range(len(str)):
        try:
            while str[i] == " " and str[i+1] == " ":
                str = str[:i+1] + str[i+2:]
        except IndexError:
            continue
    return str

def data_default():
    return "Here is the default text.", "D.B.Lofen", None

def data_json():
    with open(os.path.join(os.path.dirname(__file__), "quotes.json"), "r", encoding= "utf-8") as file:
        data = json.load(file)
    quotes = data["quotes"]
    quote = random.choice(quotes)
    context = quote['quote']
    author = quote['author']
    return context, author, None

def data_csv():
    with open('Quotes.csv', 'r') as csvfile:
        stream = csv.reader(csvfile, delimiter=";")
        quote = random.choice(list(stream)[1:])
    context = quote[0]
    author = quote[1]
    catagory = quote[2]
    return context, author, catagory

def data_qrwe():
    skill_list = ["q", "r", "w", "e"]
    str = ""
    for _ in range(random.randrange(10, 110)):
        str += random.choice(skill_list)
    return str, "qrwe", None

def get_quote():
    LINECHAR = 50
    data_function = [data_default, data_json, data_csv, data_qrwe]
    context, author, catagory = data_function[2]()
    res = []
    chars = 0
    while len(context) > chars:
        forward = LINECHAR
        if chars + LINECHAR < len(context):
            while context[chars + forward] != " ":
                forward -= 1
                if forward == 0:
                    forward = LINECHAR
                    break
        res.append(deprecate_space(context[chars: min(chars + forward + 1, len(context))]))
        chars += forward
    res.append(author)
    return res, catagory

if __name__ == "__main__":
    import datetime
    print("{:03d}".format(datetime.datetime.now()))