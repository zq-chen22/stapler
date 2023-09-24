import time

class Timer:
    def __init__(self):
        self.now = time.time()
        self.elapse = 0
    def flesh(self):
        history = self.now
        self.now = time.time()
        self.elapse += self.now - history
    def __str__(self):
        self.flesh()
        return str(self.elapse)
    def reflesh(self):
        self.now = time.time()

if __name__ == "__main__":
    print("a" in "asd")