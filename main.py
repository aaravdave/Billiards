import math
import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Billards')

balls = [[300, 300]]
new = [400, 300]

mouse = [0, 0]
prev_mouse = [0, 0]
clicked = 0
rotation = 0

dx = 0
dy = 0
x_vel = 0
y_vel = 0

scrollbar = (730, 200, 40, 200)
scrollbar_y = 0

powerbar = (30, 200, 40, 200)
powerbar_y = 0

field = (120, 120, 560, 360)
border = (110, 110, 580, 380)
border_x1 = (100, 110, 30, 360)   # top
border_x2 = (670, 110, 30, 360)  # bottom *
border_y1 = (110, 100, 580, 30)   # left
border_y2 = (110, 470, 580, 30)  # right  *

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = 1
            if pygame.Rect(powerbar).collidepoint(*mouse):
                prev_mouse = mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = 0
        elif event.type == pygame.MOUSEMOTION:
            mouse = event.pos
        elif event.type == pygame.MOUSEWHEEL:
            if pygame.Rect(scrollbar).collidepoint(*mouse) and abs(x_vel + y_vel) < 0.1:
                rotation += event.y * -1
                rotation %= 360
                scrollbar_y += math.copysign(1, event.y)
                if scrollbar_y > 8:
                    scrollbar_y = 0
                if scrollbar_y < 0:
                    scrollbar_y = 8

    screen.fill((150, 150, 255))
    pygame.draw.rect(screen, (255, 150, 50), (100, 100, 600, 400), 0, 10)   # Outer Border
    pygame.draw.rect(screen, (185, 100, 0), border, 0, 10)                  # Inner Border
    pygame.draw.rect(screen, (100, 200, 125), field, 0, 10)                 # Field

    pygame.draw.rect(screen, (150, 150, 150), scrollbar)                    # Scrollbar
    for i in range(200, 400, 10):
        pygame.draw.rect(screen, (100, 100, 100), (735, i + scrollbar_y, 30, 2))

    pygame.draw.rect(screen, (150, 150, 150), powerbar)                     # Powerbar
    pygame.draw.rect(screen, (255, 150, 50), (35, 205, 30, 100))  # Yellow
    pygame.draw.rect(screen, (255, 100, 50), (35, 305, 30, 55))   # Orange
    pygame.draw.rect(screen, (255, 50, 50), (35, 360, 30, 35))    # Red
    if clicked and pygame.Rect(powerbar).collidepoint(*mouse) and abs(x_vel + y_vel) < 0.1:
        dy = prev_mouse[1] - mouse[1]
        powerbar_y = dy
        if powerbar_y > 0:
            powerbar_y = 0
        elif powerbar_y < -175:
            powerbar_y = -175
    else:
        if powerbar_y:
            x_vel = (new[0] - balls[0][0]) / 50 * (-powerbar_y / 50)
            y_vel = (new[1] - balls[0][1]) / 50 * (-powerbar_y / 50)
            powerbar_y = 0
    pygame.draw.rect(screen, (255, 200, 100), (45, 210 - powerbar_y, 10, 185 + powerbar_y))

    for ball in balls:
        pygame.draw.circle(screen, (255, 255, 255), ball, 10)
    balls[0][0] += x_vel
    balls[0][1] += y_vel
    x_vel *= 0.99
    y_vel *= 0.99

    if pygame.Rect(border_x1).collidepoint(*balls[0]) or pygame.Rect(border_x2).collidepoint(*balls[0]):
        x_vel *= -1
    if pygame.Rect(border_y1).collidepoint(*balls[0]) or pygame.Rect(border_y2).collidepoint(*balls[0]):
        y_vel *= -1

    if clicked and pygame.Rect(field).collidepoint(*mouse) and abs(x_vel + y_vel) < 0.1:
        dx = (mouse[0] - balls[0][0])
        dy = (mouse[1] - balls[0][1])
        distance = math.sqrt(dx ** 2 + dy ** 2)
        rotation = math.degrees(math.asin(dy / distance))
    nx = 150 * math.copysign(1, dx) * math.cos(math.radians(rotation)) + balls[0][0]
    new = [nx, 150 * math.sin(math.radians(rotation)) + balls[0][1]]
    if abs(x_vel + y_vel) < 0.1:
        pygame.draw.line(screen, (255, 255, 255), balls[0], new, 3)
        pygame.draw.circle(screen, (255, 255, 255), new, 10, 3)

    pygame.display.update()
