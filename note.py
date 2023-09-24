import os
import re

def note(targets, catagory = None):
    if not catagory:
        catagory = "default"

    id = 1
    path = os.path.join(os.path.dirname(__file__), "quotes_book", f"{catagory}.txt")

    if not os.path.exists(path):
        open(path, "x")

    with open(path, "r") as f:
        quotes = f.readlines()

    for quote in quotes:
        if re.match(r"\d+\.", quote):
            id += 1
        if quote.split("\n")[0] == targets[0]:
            return

    with open(path, "a") as f:
        print("", file = f)
        print(f"{id}.", file = f)
        for i in targets:
            print(i, file = f)

if __name__ == "__main__":
    note(["q"])
    note(["w"])