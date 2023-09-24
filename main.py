import pygame
from pygame.locals import *
import time
import random
from get_quote import get_quote
import datetime
from timer import Timer
from note import note



RED = (255, 0, 0)
GREEN = (50, 205, 50)
YELLOW = (0, 255, 255)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)
LIGHT_BLUE = (117, 187, 220)
LIGHT_YELLOW = (255,255,0)
DEEP_GRAY = (100, 100, 100)
PLUM = (201, 140, 201)
FPS = 60

# targets = ["I have not failed.","I've just found 10,000 ways that won't work.","Thomas Edison"]
pygame.init()

WIDTH, HEIGHT = 1000, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SK Telecom Stapler')

clock = pygame.time.Clock()
cache = []
catache = []
current_pos = 0

def staple(targets, catagory):
    global current_pos
    waiting = False
    saving = False
    cong = False
    word_count = 0
    word_total = 0
    word_all = 0
    timer = Timer()
    TOPLEFT = (50, 50)
    TIMEPOS = (50, 700)
    WORDPOS = (290, 700)
    WPMPOS = (540, 700)
    ACCPOS = (760, 700)
    # print(pygame.font.get_fonts())
    bgcolor = random.choice([PINK, LIGHT_BLUE, LIGHT_YELLOW, PLUM])
    text = ""
    font = pygame.font.SysFont("mvboli", 30)
    text_warning = font.render(" *ERROR*", True, RED)
    save_info = font.render(" *SAVE*", True, GREEN)
    cong_info = font.render(" *SUCCESS*", True, GREEN)
    img = font.render(text, True, BLUE)
    background_lines = []
    for target in targets:
        word_total += len(target)
        background_line = font.render(target, True, bgcolor)
        background_lines.append([background_line, None])
    rect = img.get_rect()
    rect.topleft = TOPLEFT
    lines = []
    texts = []
    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(GRAY)
        background_topleft = TOPLEFT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_BACKSPACE:
                    if len(text) > 0:
                        text = text[:-1]
                        word_count -= 1
                    elif len(lines) > 0:
                        text = texts[-1]
                        rect = lines[-1][1]
                        lines = lines[:-1]
                        texts = texts[:-1]
                elif event.key == K_RETURN:
                    lines.append((img.copy(), rect.copy()))
                    texts.append(text)
                    text = ""
                    rect.topleft = rect.bottomleft
                    if texts == targets:
                        print("CONGRATULATIONS")
                        with open("logging.txt", "a") as file:
                            print("{} - {:02f} - {} - {} - {}".format(datetime.datetime.now(), float(timer.__str__()), 12 * word_count / float(timer.__str__()), int(100 * (word_count+1) / (word_all+1)), targets), file = file)
                        waiting = True
                        run = False
                        cong = True                  
                elif event.key == K_LEFT and current_pos > 0:
                    current_pos -= 1
                    timer.flesh()
                    staple(cache[current_pos], catache[current_pos])
                    timer.reflesh()
                elif event.key == K_RIGHT:
                    run = False
                elif event.key == K_TAB:
                    saving = True
                else:
                    if str(event.unicode) not in "":
                        word_count += 1
                        word_all += 1
                    text += event.unicode
        timeline = font.render("Time: {:.2f}s".format(float(timer.__str__())), True, DEEP_GRAY)
        wordline = font.render("Word: {}/{}".format(word_count, word_total), True, DEEP_GRAY)
        wpsline = font.render("WPM: ", True, DEEP_GRAY)
        hotper = min(1, max(0, (12 * word_count / float(timer.__str__()) - 10) * 0.02))
        hotcolor = [int((1 - hotper) * DEEP_GRAY[i] + hotper * RED[i]) for i in range(3)]
        wpsvalue = font.render("{:.1f}".format(12 * word_count / float(timer.__str__())), True, hotcolor)
        accline = font.render("ACC: {}%".format(int(100 * (word_count+1) / (word_all+1))), True, DEEP_GRAY)
        WIN.blit(timeline, TIMEPOS)
        WIN.blit(wordline, WORDPOS)
        WIN.blit(wpsline, WPMPOS)
        wpsrect = wpsline.get_rect()
        wpsrect.topleft = WPMPOS
        WIN.blit(wpsvalue, wpsrect.topright)
        WIN.blit(accline, ACCPOS)
        for ind, [background_img, _] in enumerate(background_lines):
            br = background_img.get_rect()
            br.topleft = background_topleft
            background_lines[ind][1] = br
            WIN.blit(background_img, br)
            background_rect = background_img.get_rect()
            background_rect.topleft = background_topleft
            background_topleft = background_rect.bottomleft

        if text != targets[min(len(targets)-1, len(texts))][:len(text)]:
            try:
                # WIN.blit(text_warning, background_lines[len(texts)][1].topright)
                # print(background_lines[len(texts)][1].topright[0],rect.topright[0])
                WIN.blit(text_warning, (max(background_lines[len(texts)][1].topright[0],rect.topright[0]), rect.topright[1]))
            except IndexError:
                WIN.blit(text_warning,rect.topright)
        for ind, t in enumerate(texts):
            try:
                if t != targets[ind]:
                    WIN.blit(text_warning, lines[ind][1].topright)
            except IndexError:
                WIN.blit(text_warning, lines[ind][1].topright)
        img = font.render(text, True, BLACK)
        rect.size = img.get_size()
        cursor = Rect(rect.topright, (2, rect.height))
        cursor.topleft = rect.topright
        for (i, r) in lines:
            WIN.blit(i, r)
        WIN.blit(img, rect)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(WIN, BLACK, cursor)
        pygame.display.update()
        while waiting:
            
            WIN.blit(cong_info, (400, 300))
            clock.tick(FPS)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    if event.key == K_TAB:
                        saving = True
        if cong:
            WIN.blit(cong_info, (400, 300))
            for _ in range(30):
                clock.tick(FPS)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        break
            cong = False
        if saving:
            note(targets, catagory)
            WIN.blit(save_info, (400, 300))
            for _ in range(30):
                clock.tick(FPS)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        break
                saving = False
    current_pos += 1        

print("Welcome to Lofen's stapler! build in 2023.9.20")

if __name__ == "__main__":
    while True:
        targets, catagory = get_quote()
        staple(targets, catagory)
        cache.append(targets)
        catache.append(catagory)