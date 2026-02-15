import tkinter as tk
import random

# ==============================
# Einstellungen
# ==============================
CELL_SIZE = 20       # Größe jedes Segments
WIDTH = 500          # Fensterbreite
HEIGHT = 500         # Fensterhöhe
SPEED = 150          # Zeit zwischen Bewegungen in ms

# ==============================
# Fenster erstellen
# ==============================
root = tk.Tk()
root.title("Snake - Wrapping Edition")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# ==============================
# Score
# ==============================
score = 0
score_text = canvas.create_text(50, 20, text=f"Score: {score}", fill="white", font=("Arial", 16))

# ==============================
# Snake starten
# ==============================
snake = [(5, 5), (4, 5), (3, 5)]  # Liste von Segmenten (x, y) in Zellen
direction = "Right"                # Start-Richtung

# ==============================
# Food
# ==============================
food = None

def create_food():
    global food
    while True:
        x = random.randint(0, (WIDTH//CELL_SIZE)-1)
        y = random.randint(0, (HEIGHT//CELL_SIZE)-1)
        if (x, y) not in snake:   # Nicht auf der Schlange
            food = (x, y)
            break

create_food()

# ==============================
# Zeichnen
# ==============================
def draw():
    canvas.delete("all")
    # Snake zeichnen
    for segment in snake:
        x, y = segment
        canvas.create_rectangle(
            x*CELL_SIZE, y*CELL_SIZE,
            x*CELL_SIZE+CELL_SIZE, y*CELL_SIZE+CELL_SIZE,
            fill="green"
        )
    # Food zeichnen
    fx, fy = food
    canvas.create_rectangle(
        fx*CELL_SIZE, fy*CELL_SIZE,
        fx*CELL_SIZE+CELL_SIZE, fy*CELL_SIZE+CELL_SIZE,
        fill="red"
    )
    # Score anzeigen
    canvas.create_text(50, 20, text=f"Score: {score}", fill="white", font=("Arial", 16))

# ==============================
# Snake bewegen
# ==============================
def move_snake():
    global snake, score

    head_x, head_y = snake[0]

    # Neue Kopfposition je nach Richtung
    if direction == "Right":
        head_x += 1
    elif direction == "Left":
        head_x -= 1
    elif direction == "Up":
        head_y -= 1
    elif direction == "Down":
        head_y += 1

    # Wrapping durch Wände
    head_x %= WIDTH//CELL_SIZE
    head_y %= HEIGHT//CELL_SIZE

    new_head = (head_x, head_y)

    # Selbst-Kollision prüfen
    if new_head in snake:
        game_over()
        return

    snake.insert(0, new_head)

    # Food gegessen?
    if new_head == food:
        score += 1
        create_food()
    else:
        snake.pop()  # Letztes Segment entfernen, wenn nicht gegessen

    draw()
    root.after(SPEED, move_snake)

# ==============================
# Steuerung
# ==============================
def change_direction(event):
    global direction
    if event.keysym == "Left" and direction != "Right":
        direction = "Left"
    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"
    elif event.keysym == "Up" and direction != "Down":
        direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"

root.bind("<Key>", change_direction)

# ==============================
# Game Over
# ==============================
def game_over():
    canvas.create_text(WIDTH//2, HEIGHT//2, text="GAME OVER", fill="yellow", font=("Arial", 30))

# ==============================
# Neustart-Button
# ==============================
def restart_game():
    global snake, direction, score
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = "Right"
    score = 0
    canvas.itemconfig(score_text, text=f"Score: {score}")
    create_food()
    move_snake()

restart_button = tk.Button(root, text="Restart", command=restart_game, font=("Arial", 14))
restart_button.pack(pady=10)

# ==============================
# Spiel starten
# ==============================
move_snake()
root.mainloop()
