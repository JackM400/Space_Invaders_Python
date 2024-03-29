# Space Invaders [Basic]
# Space Invaders - 1978 original created by Tomohiro Nishikado
# JackM400
# jack.millar400@gmail.com
import math
import random
import keyboard
import turtle

isRunning = True
playerLives = 3
game_limit = 275

# game screen
game_window = turtle.Screen()
game_window.screensize(300, 300)
game_window.title("Space Invaders - JackM400")
# game_window.setup(width=600, height=600)
game_window.bgcolor("black")

# game visual elements
game_window.bgpic("game_background.png")
game_window.register_shape("tank_player.gif")
game_window.register_shape("enemy_invader.gif")

# game attributes
# -score
GameScore: int = 0

score_builder = turtle.Turtle()
score_builder.hideturtle()
score_builder.speed()
score_builder.color("white")
score_builder.penup()
score_builder.setposition(-290, 275)
printed_score = "Game Score : " + str(GameScore)
score_builder.clear()
score_builder.write(printed_score, False, align="left", font=("Arial", 14, "normal"))
score_builder.hideturtle()


def life_counter():
    lives_builder = turtle.Turtle()
    lives_builder.hideturtle()
    lives_builder.speed()
    lives_builder.color("white")
    lives_builder.penup()
    lives_builder.setposition(165, 275)
    printed_player_lives = "Player Lives : " + str(playerLives)
    lives_builder.clear()
    lives_builder.write(printed_player_lives, False, align="left", font=("Arial", 14, "normal"))
    lives_builder.hideturtle()


def end_screen():
    end_game_builder = turtle.Turtle()
    end_game_builder.hideturtle()
    end_game_builder.speed()
    end_game_builder.color("white")
    end_game_builder.penup()
    printed_end = "Game Over\nScore : " + str(GameScore)
    end_game_builder.write(printed_end, False, align="left", font=("Arial", 14, "normal"))
    end_game_builder.clear()
    end_game_builder.hideturtle()


# screen attributes
# -border
border_builder = turtle.Turtle()
border_builder.speed(0)  # 0 == fastest speed
border_builder.color("white")
border_builder.pensize(3)
border_builder.penup()
border_builder.setposition(-300, -300)
border_builder.pendown()

for side in range(4):
    border_builder.fd(600)
    border_builder.lt(90)
border_builder.hideturtle()

# Tank [Player]
# Player attributes
player = turtle.Turtle()
player.penup()
player.speed(0)
player.setposition(-20, -230)
player.shape("tank_player.gif")
player.setheading(90)
player.color("green")

# -Movement
player_speed = 20
enemy_speed = 5
projectile_Speed = 25

# projectiles
projectile = turtle.Turtle()
projectile.color("white")
projectile.shape("triangle")
projectile.penup()
projectile.speed()
projectile.setheading(90)
projectile.shapesize(.45, .45)
projectile.hideturtle()

canFire = True
firing = False

# Enemies
enemy_count = 5
enemies = []

# add enemy entities to list
for i in range(enemy_count):
    enemies.append(turtle.Turtle())
# add attributes to each enemy in enemies
for enemy in enemies:
    # enemy starts at random location
    x = random.randint(-200, 200)
    y = random.randint(175, 250)
    enemy.color("red")
    enemy.shape("enemy_invader.gif")
    enemy.penup()
    enemy.speed()
    enemy.setheading(270)
    enemy.setposition(x, y)


def enemy_start_pos():
    enemy.hideturtle()
    enemy.setposition(-200, 250)
    global enemy_speed
    enemy_speed += 5
    enemy.showturtle()


def player_start_pos():
    player.hideturtle()
    player.setposition(-20, -230)
    player.showturtle()


def fire():
    # set projectile to nose of player
    global canFire
    global firing
    if canFire:
        if not firing:
            firing = True
            # start location of projectiles , @player
            positionx = player.xcor()
            positiony = player.ycor() + 15
            projectile.setposition(positionx, positiony)
            projectile.showturtle()
    else:
        print("Gun Disabled")


# check if projectile and enemy area overlap -> hit , enemy kill
def isHit(projectile, enemy):
    # distance equation between points P ,Q
    # d(P, Q) = sqrt(p(x2 − x1)2 + (y2 − y1)2)
    rel_distance = 100
    rel_distance = math.sqrt(math.pow(projectile.xcor() - enemy.xcor(), 2) +
                             math.pow(projectile.ycor() - enemy.ycor(), 2))
    if rel_distance < 25:
        return True
    else:
        return False


# @start position is 0, if move L(-) or R(+) selected ,  player speed acts on position
# -Right
def move_right():
    position = player.xcor()
    position += player_speed
    if position > 250:
        position = 250
    player.setx(position)


# -Left
def move_left():
    position = player.xcor()
    position -= player_speed
    if position < -250:
        position = -250
    player.setx(position)


life_counter()
while isRunning:
    # keyboard Input
    game_window.listen()
    if keyboard.is_pressed("d"):  # move player left
        move_right()
    else:
        pass
    if keyboard.is_pressed("a"):  # move player right
        move_left()
    else:
        pass
    if keyboard.is_pressed("space"):  # fire player weapon
        fire()
    else:
        pass

    # projectile movement
    projectile_y = projectile.ycor()
    projectile_y += projectile_Speed
    projectile.sety(projectile_y)

    # if projectile in flight , cannot fire again until complete
    if projectile.ycor() > 295:
        firing = False
        projectile.hideturtle()

    for enemy in enemies:
        # boot
        # populate enemies
        # set enemy speed
        # move enemy
        enemy.showturtle()
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # enemy progression , R -> D -> L -> D -> R ....
        # Left ,Right + Down movement
        if enemy.xcor() > game_limit or enemy.xcor() < (game_limit * -1):  # if enemy hit left side or right side
            for entity in enemies:
                y = entity.ycor()
                y -= 20
                entity.sety(y)
            enemy_speed *= -1

        # if projectile hits enemy
        # (point objects as standard , low chance of direct hit ,
        # hit counts if projected shapes of projectile  + enemy overlap)

        if isHit(projectile, enemy):
            projectile.hideturtle()
            canFire = True
            enemy_start_pos()  # temp check to make sure collision works
            GameScore += 10
            printed_score = "Game Score : " + str(GameScore)
            score_builder.clear()
            score_builder.write(printed_score, False, align="left", font=("Arial", 14, "normal"))

        # if player enemy collision
        if isHit(player, enemy):
            playerLives -= 1
            print("Player Lives :" + str(playerLives))
            player_start_pos()
            enemy_start_pos()  # temp check to make sure collision works
            GameScore += 10
            canFire = True

        # lose checks
        # enemy "lands" [reaches bottom of screen]
        if enemy.ycor() < -250:
            print("Game Over")
            end_screen()
            isRunning = False
    # if player no of lives runs out
    if playerLives == 0:
        print("Game Over")
        end_screen()
        isRunning = False
    # isRunning = False

game_window.mainloop()

