import math
import time
import random
import pygame

pygame.init()

width, height = 800, 600  #pixels that we will use for the window

window = pygame.display.set_mode(
    (width, height))  #initialize a pygame window and display it on screen
pygame.display.set_caption("Aim Trainer")  #name of window

target_increment = 400  #400 milisecond per target
target_event = pygame.USEREVENT

bg_color = (0, 25, 40)  # rgb values

lives = 3

r = target_padding = 30  #30 pixels from the border

top_bar_height = 50

label_font = pygame.font.SysFont("comicsans", 24)


class target:
  max_size = 30
  growth_rate = 0.2
  color = "RED"
  second_color = "white"

  def __init__(self, x, y):  #x and y will be random positions for the target
    self.x = x
    self.y = y
    self.size = 0
    self.grow = True

  #the main idea is that we will start growing target until it reaches max size and the shrink it

  def update(self):  #update the size of target accordingly
    if self.size + self.growth_rate >= self.max_size:
      self.grow = False

    if self.grow:
      self.size += self.growth_rate
    else:
      self.size -= self.growth_rate

  def draw(self, win):
    #we are trying to make 1 circle with red-white-red-white ring like pattern so we make 4 overlapping circles in shrinking size
    pygame.draw.circle(win, self.color, (self.x, self.y), self.size)
    pygame.draw.circle(win, self.second_color, (self.x, self.y),
                       self.size * 0.8)
    pygame.draw.circle(win, self.color, (self.x, self.y), self.size * 0.6)
    pygame.draw.circle(win, self.second_color, (self.x, self.y),
                       self.size * 0.4)

  def collide(self, x, y):  #x and y are mouse position
    # our idea of succesfull click is that if distace between mouse coordinates and target'c center coordinates
    # are less then radius of circle then it its a successful hit
    #we will use simple math formula to calculate that
    distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
    return distance <= self.size


def Draw(win, targets):
  # in pygame the order in whih we draw things is important
  # if we draw something on top of something else its gonna overlap it
  # so we will clear the screen every single time we draw
  # so every frame we wipe everything previously was on it then we draw onto it

  win.fill(bg_color)

  for tarrget in targets:
    tarrget.draw(win)


def format_time(secs):
  milli = math.floor(int(secs * 1000 % 1000) / 100)
  seconds = int(round(secs % 60, 1))
  minutes = int(seconds // 60)

  return f"{minutes:02d}:{seconds:02d}:{milli}"


def draw_top_bar(win, elapsed_time, targets_pressed, misses):
  pygame.draw.rect(window, "grey", (0, 0, width, top_bar_height))
  time_label = label_font.render(f"Time: {format_time(elapsed_time)}", 1,
                                 "black")

  speed = round(targets_pressed / elapsed_time, 1)
  speed_label = label_font.render(f"speed:{speed}t/s", 1, "black")

  hits_label = label_font.render(f"hits:{targets_pressed}", 1, "black")

  lives_label = label_font.render(f"lives:{lives-misses}", 1, "black")

  win.blit(time_label, (5, 5))  #lets us display time label
  win.blit(speed_label, (200, 5))
  win.blit(hits_label, (400, 5))
  win.blit(lives_label, (600, 5))


def end_screen(win, elapsed_time, targets_pressed, clicks):
  win.fill(bg_color)  #stops everything and puts red on bf color

  time_label = label_font.render(f"Time: {format_time(elapsed_time)}", 1,
                                 "white")

  speed = round(targets_pressed / elapsed_time, 1)
  speed_label = label_font.render(f"speed:{speed}t/s", 1, "white")

  hits_label = label_font.render(f"hits:{targets_pressed}", 1, "white")

  accuracy = round(targets_pressed / clicks * 100, 1)
  accuracy_label = label_font.render(f"Accuracy:{accuracy}%", 1, "white")

  win.blit(time_label,
           (get_middle(time_label), 100))  #lets us display time label
  win.blit(speed_label, (get_middle(speed_label), 200))
  win.blit(hits_label, (get_middle(hits_label), 300))
  win.blit(accuracy_label, (get_middle(accuracy_label), 400))

  pygame.display.update()

  run = True
  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
        quit()


def get_middle(surface):  #returns middle coordinates of window
  return width / 2 - surface.get_width() / 2


def main():  #main loop
  run = True
  targets = []
  clock = pygame.time.Clock()
  pygame.time.set_timer(
      target_event,
      target_increment)  #triggers target event in each target increment time
  targets_pressed = 0
  total_clicks = 0
  misses = 0
  start_time = time.time()

  while run:
    clock.tick(60)  #this tick regulates the speed at which while loop runs
    click = False
    mouse_pos = pygame.mouse.get_pos()
    elapsed_time = time.time() - start_time

    for event in pygame.event.get(
    ):  #looping through all different events that are occuring
      if event.type == pygame.QUIT:  #in pygame when a user clicks X button we have to tell the program what to do so we are telling it to terminate here
        run = False
        break

      if event.type == target_event:
        x = random.randint(
            target_padding, width - target_padding
        )  #so the targets generate inside the window paddings because it also expands
        y = random.randint(target_padding + top_bar_height,
                           width - target_padding)

        Target = target(x, y)
        targets.append(Target)

      if event.type == pygame.MOUSEBUTTONDOWN:  #if mouse is clicked
        click = True
        total_clicks += 1

    for trgt in targets:
      trgt.update()

      if trgt.size <= 0:  #we remove the target that is shrunk so we keep control on size of list
        targets.remove(trgt)  #this prevents our game to get slow
        misses += 1

      if click and trgt.collide(
          *mouse_pos):  #  *mouse_pos breaks down tuple to individual component
        targets.remove(trgt)
        targets_pressed += 1

    if lives <= misses:
      end_screen(window, elapsed_time, targets_pressed, total_clicks)

    Draw(window, targets)
    draw_top_bar(window, elapsed_time, targets_pressed, misses)
    pygame.display.update()
    # the Draw function will only display all that we have rendered when the update function is called

  pygame.quit()


if __name__ == "__main__":  #if we import any function from another file it doesn't cause main to run
  main()
