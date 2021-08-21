import sys

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

from random import *
from time import *

from player import Player
from ball import Ball
from tone import Tone

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

p1 = Player(SCREEN_HEIGHT / 2)
p2 = Player(SCREEN_HEIGHT / 2, True)
P_HEIGHT = 80
P_HEIGHT_HALF = P_HEIGHT / 2
P_WIDTH = 10
P_WIDTH_HALF = P_WIDTH / 2
P_SPEED = 0.25

ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
BALL_WIDTH = 30
BALL_WIDTH_HALF = BALL_WIDTH / 2
BALL_SPEED = 0.1

is_resetting = False
game_over = False
single_player = True

NUMBERS = {
  '0': [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
    ],
  '1': [
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1]
  ],
  '2': [
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 1, 1, 1]
  ],
  '3': [
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 1, 1, 1],
    [0, 0, 0, 1],
    [1, 1, 1, 1]
  ],
  '4': [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1]
  ],
  '5': [
    [1, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [1, 1, 1, 1]
  ],
  '6': [
    [1, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
  ],
  '7': [
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1]
  ],
  '8': [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
  ],
  '9': [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1]
  ]
}

def clear_window():
  glClear(GL_COLOR_BUFFER_BIT)

  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

  glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
  gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

  glClearColor(0.1, 0.1, 0.1, 1)

def draw_board():
  # Center solid line
  # glLineWidth(10)
  # glColor3f(.9, .9, .9)
  # glBegin(GL_LINES)
  # glVertex2f(SCREEN_WIDTH / 2, 0)
  # glVertex2f(SCREEN_WIDTH / 2, SCREEN_HEIGHT)
  # glEnd()

  # Center dotted line
  for i in range(5, SCREEN_HEIGHT, 20):
    glRectf((SCREEN_WIDTH / 2) - 5, i, (SCREEN_WIDTH / 2) + 5, i + 10)

  # Player 1
  glRectf(25 - P_WIDTH_HALF, p1.y - P_HEIGHT_HALF, \
          25 + P_WIDTH_HALF, p1.y + P_HEIGHT_HALF)
  # Player 2
  glRectf(SCREEN_WIDTH - (25 + P_WIDTH_HALF), p2.y - P_HEIGHT_HALF, \
          SCREEN_WIDTH - (25 - P_WIDTH_HALF), p2.y + P_HEIGHT_HALF)

  # Ball
  glRectf(ball.x - BALL_WIDTH_HALF, ball.y - BALL_WIDTH_HALF, \
          ball.x + BALL_WIDTH_HALF, ball.y + BALL_WIDTH_HALF)  # Ball
  
  # Score
  ## Player 1
  for char in str(p1.score):
    p1_score_y = SCREEN_HEIGHT - 40
    for num in NUMBERS[char]:
      p1_score_x = 300
      for bit in num:
        if bit:
          glRectf(p1_score_x, p1_score_y, p1_score_x + 15, p1_score_y - 15)
        p1_score_x += 15
      p1_score_y -= 15
  ## Player 2
  for char in str(p2.score):
    p2_score_y = SCREEN_HEIGHT - 40
    for num in NUMBERS[char]:
      p2_score_x = 440
      for bit in num:
        if bit:
          glRectf(p2_score_x, p2_score_y, p2_score_x + 15, p2_score_y - 15)
        p2_score_x += 15
      p2_score_y -= 15

def reset():
  global is_resetting
  center_h = SCREEN_HEIGHT / 2
  center_w = SCREEN_WIDTH / 2

  ball.x = center_w
  ball.y = center_h

  p1.y = center_h
  p2.y = center_h

  ball.is_outside = False

def play_bounce():
  Tone(288).play(24)

def play_score():
  Tone(72).play(32)

def init_game():
  pygame.mixer.pre_init(44100, -16, 1, 1024)
  pygame.init()
  pygame.display.init()
  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF|OPENGL)
  pygame.display.set_caption("PYPONG")
  pygame.mouse.set_visible(False)

  draw_board()
  ball.going_left = True

def update():
  global is_resetting, game_over
  if game_over and not is_resetting:
    pass
  elif ball.is_outside and is_resetting:
    reset()
  elif not ball.is_outside and is_resetting:
    is_resetting = False
    sleep(1)
  else:
    if p1.going_up and p1.y + P_HEIGHT_HALF < SCREEN_HEIGHT:
      p1.y += P_SPEED
    elif p1.going_down and p1.y - P_HEIGHT_HALF > 0:
      p1.y -= P_SPEED
    
    if not single_player:
      if p2.going_up and p2.y + P_HEIGHT_HALF < SCREEN_HEIGHT:
        p2.y += P_SPEED
      elif p2.going_down and p2.y - P_HEIGHT_HALF > 0:
        p2.y -= P_SPEED

    if ball.going_left:
      if ball.x - BALL_WIDTH_HALF <= 30 and \
        (ball.y + BALL_WIDTH_HALF > p1.y - P_HEIGHT_HALF - 0.5 and \
        ball.y - BALL_WIDTH_HALF < p1.y + P_HEIGHT_HALF - 0.5):
        play_bounce()
        ball.going_left = False
        ball.going_right = True

        if ball.y < p1.y - P_HEIGHT_HALF / 2:
          ball.going_up = False
          ball.going_down = True
        elif ball.y > p1.y + P_HEIGHT_HALF / 2:
          ball.going_down = False
          ball.going_up = True
      else:
        ball.x -= 0.1
      
      if ball.x < 0:
        play_score()
        p2.score += 1
        ball.is_outside = True
        is_resetting = True
        if p2.score >= 9:
          game_over = True
    elif ball.going_right:
      if ball.x + BALL_WIDTH_HALF >= SCREEN_WIDTH - 30 and \
        (ball.y + BALL_WIDTH_HALF > p2.y - P_HEIGHT_HALF - 0.5 and \
        ball.y - BALL_WIDTH_HALF < p2.y + P_HEIGHT_HALF - 0.5):
        play_bounce()
        ball.going_right = False
        ball.going_left = True

        if ball.y < p2.y - P_HEIGHT_HALF / 2:
          ball.going_up = False
          ball.going_down = True
        elif ball.y > p2.y + P_HEIGHT_HALF / 2:
          ball.going_down = False
          ball.going_up = True
      else:
        ball.x += 0.1

      if ball.x > SCREEN_WIDTH:
        play_score()
        p1.score += 1
        ball.is_outside = True
        is_resetting = True
        if p1.score >= 9:
          game_over = True

    if ball.going_up:
      if ball.y >= SCREEN_HEIGHT:
        play_bounce()
        ball.going_up = False
        ball.going_down = True
      else:
        ball.y += 0.1
    elif ball.going_down:
      if ball.y <= 0:
        play_bounce()
        ball.going_down = False
        ball.going_up = True
      else:
        ball.y -= 0.1
    
    if single_player:
      if ball.y >= p2.y:
        p2.y += 0.0866
      else:
        p2.y -= 0.0866

def display():
  clear_window()
  draw_board()

  pygame.display.flip()

def game_loop():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
    if event.type == pygame.KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.quit()
        quit()
      if single_player:
        if event.key == pygame.K_UP:
          p1.going_up = True
        elif event.key == pygame.K_DOWN:
          p1.going_down = True
      else:
        if event.key == pygame.K_w:
          p1.going_up = True
        elif event.key == pygame.K_s:
          p1.going_down = True

        if event.key == pygame.K_UP:
          p2.going_up = True
        elif event.key == pygame.K_DOWN:
          p2.going_down = True
    elif event.type == pygame.KEYUP:
      if single_player:
        if event.key == pygame.K_UP:
          p1.going_up = False
        elif event.key == pygame.K_DOWN:
          p1.going_down = False
      else:
        if event.key == pygame.K_w:
          p1.going_up = False
        elif event.key == pygame.K_s:
          p1.going_down = False

        if event.key == pygame.K_UP:
          p2.going_up = False
        elif event.key == pygame.K_DOWN:
          p2.going_down = False
    if single_player and event.type == pygame.MOUSEMOTION:
      p1.y = SCREEN_HEIGHT - event.pos[1]
  update()
  display()

def main():
  global single_player
  init_game()
  if len(sys.argv) > 1:
    if sys.argv[1].upper() == '2P':
      single_player = False
  while True:
    game_loop()

if __name__ == '__main__':
  main()