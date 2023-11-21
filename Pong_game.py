import tkinter as Tkinter
import time
import random
import sys
from copy import copy


window = Tkinter.Tk()

window_dimensions = [800, 625]
window.geometry(str(window_dimensions[0]) + "x" + str(window_dimensions[1]))
window.resizable(0, 0)

window.title("Simple Pong Game")

window.protocol("WM_DELETE_WINDOW", sys.exit)

frames_per_second = 30

game_canvas = Tkinter.Canvas(window, width=window_dimensions[0], height=window_dimensions[1], bd=0, highlightthickness=0)
game_canvas.pack()

#Game variables
paddle_size = [15, 125]

initial_y_position = (window_dimensions[1] - paddle_size[1]) / 2

player_y_position = initial_y_position
player_y_velocity = 0

ai_y_position = initial_y_position
ai_y_velocity = 0

ball_diameter = 15

initial_ball_position = [(window_dimensions[0] - 35 - paddle_size[0]) - (int(window_dimensions[1] / 2)),
                         ((window_dimensions[1] - ball_diameter) / 2) - (int(window_dimensions[1] / 2))]
initial_ball_velocity = [12, 12]

ball_position = copy(initial_ball_position)
ball_velocity = copy(initial_ball_velocity)

score = [0, 0]

del initial_y_position

display_instructions = True

optimal_position = False

# create new variable to track the winning player
winning_player = None
game_paused = False

reset_game_after = None 


# define the reset_game function
def reset_game():
    global score
    global ball_position
    global ball_velocity
    global optimal_position
    global winning_player
    global game_paused
    
    score = [0, 0]

 # Reset ball position and velocity
    ball_position[0] = (window_dimensions[0] - 35 - paddle_size[0]) - (int(window_dimensions[1] / 2))
    ball_position[1] = ((window_dimensions[1] - ball_diameter) / 2) - (int(window_dimensions[1] / 2))
    ball_velocity[0] = 12
    ball_velocity[1] = 12

    optimal_position = optimalPaddlePosition(ball_velocity, ball_position, ball_diameter, paddle_size)

    winning_player = None

    congrat_label.place_forget()
    play_again_button.place_forget()

    # Resume the game
    game_paused = False
    
    gameloop()


    window.after_cancel(reset_game_after)
    
congrat_label = Tkinter.Label(window, text="", font="Monaco 20 bold", fg="#ffffff", bg="#001F3F")

play_again_button = Tkinter.Button(window, text="Play Again", font="Monaco 16 bold", fg="#ffffff", bg="#001F3F",
                                     command=lambda: reset_game())

game_paused = False  



# gameloop
def gameloop():
    global frames_per_second
    global game_canvas
    global window_dimensions
    global player_y_position
    global paddle_size
    global ai_y_position
    global ball_diameter
    global ball_position
    global ball_velocity
    global player_y_velocity
    global ai_y_velocity
    global display_instructions
    global optimal_position
    global score
    global winning_player
    global game_paused
    global reset_game_after

    if game_paused:
        return

    # Check if any player has reached 5 points
    if score[0] == 5 or score[1] == 5:
        # Stop the game for 5 seconds for celebration
        if winning_player is None:
            winning_player = 0 if score[0] == 2 else 1
            message = f"Player {winning_player + 1} Wins! 🎉"
            congrat_label.config(text=message)
            congrat_label.place(x=window_dimensions[0] // 2, y=window_dimensions[1] // 2 - 50, anchor="center")

            # Display "Play Again" button
            play_again_button.place(x=window_dimensions[0] // 2, y=window_dimensions[1] // 2 + 50, anchor="center")

            # Pause the game
            game_paused = True

            reset_game_after = window.after(5000, reset_game)
    # call gameloop again in 100 milliseconds (gameloops is called every 100 MS)
    window.after(int(1000 / frames_per_second), gameloop)

    

    game_canvas.delete("all")

    game_canvas.create_rectangle(0, 0, window_dimensions[0], window_dimensions[1], fill="#001F3F", outline="#001F3F")

    game_canvas.create_rectangle(35, player_y_position, 35 + paddle_size[0], player_y_position + paddle_size[1],
                                 fill="#0008ff", outline="#0008ff")

    game_canvas.create_rectangle(window_dimensions[0] - 35, ai_y_position,
                                 (window_dimensions[0] - 35) - paddle_size[0], ai_y_position + paddle_size[1],
                                 fill="#FF0000", outline="#FF0000")

    game_canvas.create_oval(ball_position[0], ball_position[1], ball_position[0] + ball_diameter,
                            ball_position[1] + ball_diameter, fill="#00FF00", outline="#00FF00")

    game_canvas.create_text(window_dimensions[0] / 2, 35, anchor="center", font="Monaco 28 bold", fill="#ffffff",
                             text=str(score[0]) + "   " + str(score[1]))

    game_canvas.create_line((window_dimensions[0] / 2), 0, (window_dimensions[0] / 2), window_dimensions[1],
                            fill="#ffffff", dash=(6, 10), width=3)

    if display_instructions:
        game_canvas.create_text((window_dimensions[0] / 2) - 30, window_dimensions[1] - 40, anchor="ne",
                                 font="Monaco 16 bold", fill="#ffffff", text="Move with W/S")
    player_y_position += player_y_velocity

    ai_y_position += ai_y_velocity

    # set window boundaries for max and min position for paddles

    if player_y_position + paddle_size[1] > window_dimensions[1]:
        player_y_position = window_dimensions[1] - paddle_size[1]
    elif player_y_position < 0:
        player_y_position = 0

    if ai_y_position + paddle_size[1] > window_dimensions[1]:
        ai_y_position = window_dimensions[1] - paddle_size[1]
    elif ai_y_position < 0:
        ai_y_position = 0

    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]


    if ball_position[1] >= window_dimensions[1] - ball_diameter or ball_position[1] <= 0:
        ball_velocity[1] = -ball_velocity[1]

    # left side and right side of screen --> update score accordingly and reset ball vars
    if ball_position[0] <= 0:
        score[1] += 1

        ball_position = copy(initial_ball_position)
        ball_velocity = copy(initial_ball_velocity)

        optimal_position = optimalPaddlePosition(ball_velocity, ball_position, ball_diameter, paddle_size)

    if ball_position[0] >= window_dimensions[0] - ball_diameter:
        score[0] += 1

        ball_position = copy(initial_ball_position)
        ball_velocity = copy(initial_ball_velocity)

        optimal_position = optimalPaddlePosition(ball_velocity, ball_position, ball_diameter, paddle_size)

    if (
        ((ball_position[0] >= 35 and ball_position[0] <= 35 + paddle_size[0]) and
         (ball_position[1] + ball_diameter >= player_y_position and
          ball_position[1] <= player_y_position + paddle_size[1]) and ball_velocity[0] <= 0) or
        ((ball_position[0] + ball_diameter <= window_dimensions[0] - 35 and
          ball_position[0] + ball_diameter >= (window_dimensions[0] - 35) - paddle_size[0]) and
         (ball_position[1] + ball_diameter >= ai_y_position and
          ball_position[1] <= ai_y_position + paddle_size[1]) and ball_velocity[0] >= 0)
    ):
        ball_velocity[0] = -ball_velocity[0]


        if ball_velocity[0] >= 0:
            if (ball_position[1] + ball_diameter <= player_y_position + paddle_size[0] and ball_velocity[1] >= 0) or \
                    (ball_position[1] >= player_y_position + paddle_size[1] - paddle_size[0] and ball_velocity[1] <= 0):
                ball_velocity[1] = -ball_velocity[1]

        if ball_velocity[0] <= 0:
            if (ball_position[1] + ball_diameter <= ai_y_position + paddle_size[0] and ball_velocity[1] >= 0) or \
                    (ball_position[1] >= ai_y_position + paddle_size[1] - paddle_size[0] and ball_velocity[1] <= 0):
                ball_velocity[1] = -ball_velocity[1]


        if ball_velocity[0] <= 0:
            optimal_position = False
        else:
            optimal_position = optimalPaddlePosition(ball_velocity, ball_position, ball_diameter, paddle_size)


    if ball_position[0] > window_dimensions[0] * 0.65:
        if optimal_position is not False and (ai_y_position < optimal_position and
                                              ai_y_position + paddle_size[1] > optimal_position):
            ai_y_velocity = 0
        elif optimal_position is not False:
            if ai_y_position > optimal_position:
                ai_y_velocity = -15
            if ai_y_position < optimal_position:
                ai_y_velocity = 15



def optimalPaddlePosition(local_ball_velocity, local_ball_position, local_ball_diameter, local_paddle_size):

    global window_dimensions


    local_ball_velocity = copy(local_ball_velocity)
    local_ball_position = copy(local_ball_position)
    local_paddle_size = copy(local_paddle_size)


    while local_ball_position[0] < window_dimensions[0] - 35 - local_paddle_size[0]:

        local_ball_position[0] += local_ball_velocity[0]
        local_ball_position[1] += local_ball_velocity[1]


        if local_ball_position[1] >= window_dimensions[1] - local_ball_diameter or local_ball_position[1] <= 0:
            local_ball_velocity[1] = -local_ball_velocity[1]

    # with a random number added 55% of the time to make computer player imperfect
    local_optimal_position = local_ball_position[1]

    if random.randint(0, 100) <= 55:
        # add either -20 or 20 (randomly chosen) to optimal position variable
        local_optimal_position += [-20, 20][random.randint(0, 1)]


    if local_optimal_position + local_ball_diameter > window_dimensions[1]:
        local_optimal_position = window_dimensions[1] - local_ball_diameter

    if local_optimal_position < 0:
        local_optimal_position = 0

    return local_optimal_position


def onKeyDown(e):
    
    global player_y_velocity
    global ai_y_velocity
    global display_instructions

    player_y_velocity_current = player_y_velocity
    ai_y_velocity_current = ai_y_velocity

    if e.keysym == "w":
        player_y_velocity = -15
    elif e.keysym == "s":
        player_y_velocity = 15

    if player_y_velocity_current != player_y_velocity or ai_y_velocity_current != ai_y_velocity:
        display_instructions = False


def onKeyUp(e):
    global player_y_velocity
    global ai_y_velocity

    if e.keysym == "w" or e.keysym == "s":
        player_y_velocity = 0


window.bind("<KeyPress>", onKeyDown)

window.bind("<KeyRelease>", onKeyUp)

reset_game_after = None  
gameloop()
window.mainloop()
