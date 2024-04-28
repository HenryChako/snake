import tkinter
import random
import os

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self, head):
        self.head = head
        self.body = []
        self.velocityX = 0
        self.velocityY = 0

class Game:
    def __init__(self, window, canvas, snake, food):
        self.window = window
        self.canvas = canvas
        self.snake = snake
        self.food = food
        self.game_over = False
        self.score = 0

    def reset_game(self):
        self.snake = Snake(Tile(TILE_SIZE * 5, TILE_SIZE * 5))
        self.food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
        self.snake.velocityX = 0
        self.snake.velocityY = 0
        self.snake.body = []
        self.game_over = False
        self.score = 0

    def change_direction(self, e): #e = event
        if (self.game_over):
            if (e.keysym == 'r'):
                self.reset_game()
                self.draw()  # Start the game loop again
            return

        if (e.keysym == "Up" and self.snake.velocityY != 1):
            self.snake.velocityX = 0
            self.snake.velocityY = -1
            
        elif (e.keysym == "Down" and self.snake.velocityY != -1):
            self.snake.velocityX = 0
            self.snake.velocityY = 1

        elif (e.keysym == "Left" and self.snake.velocityX != 1):
            self.snake.velocityX = -1
            self.snake.velocityY = 0

        elif (e.keysym == "Right" and self.snake.velocityX != -1):
            self.snake.velocityX = 1
            self.snake.velocityY = 0

    def move(self):
        if (self.game_over):
            return
        
        if (self.snake.head.x < 0 or self.snake.head.x >= WINDOW_WIDTH or self.snake.head.y < 0 or self.snake.head.y >= WINDOW_HEIGHT):
            self.game_over = True
            return
        
        for tile in self.snake.body:
            if (self.snake.head.x == tile.x and self.snake.head.y == tile.y):
                self.game_over = True
                return
        
        #collision
        if (self.snake.head.x == self.food.x and self.snake.head.y == self.food.y): 
            self.snake.body.append(Tile(self.food.x, self.food.y))
            self.food.x = random.randint(0, COLS-1) * TILE_SIZE
            self.food.y = random.randint(0, ROWS-1) * TILE_SIZE
            self.score += 1

        #update snake body
        for i in range(len(self.snake.body)-1, -1, -1):
            tile = self.snake.body[i]
            if (i == 0):
                tile.x = self.snake.head.x
                tile.y = self.snake.head.y
            else:
                prev_tile = self.snake.body[i-1]
                tile.x = prev_tile.x
                tile.y = prev_tile.y
        
        self.snake.head.x += self.snake.velocityX * TILE_SIZE
        self.snake.head.y += self.snake.velocityY * TILE_SIZE

    def draw(self):
        if self.game_over:
            self.canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {self.score}", fill = "white")
            self.canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 30, font = "Arial 20", text = "Press 'r' to restart", fill = "white")
            save_high_scores(self.score)  # Save the high score when the game ends
        else:
            self.move()
            self.canvas.delete("all")
            self.canvas.create_rectangle(self.food.x, self.food.y, self.food.x + TILE_SIZE, self.food.y + TILE_SIZE, fill = 'red')
            self.canvas.create_rectangle(self.snake.head.x, self.snake.head.y, self.snake.head.x + TILE_SIZE, self.snake.head.y + TILE_SIZE, fill = 'lime green')
            for tile in self.snake.body:
                self.canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'lime green')
            self.canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {self.score}", fill = "white")
            self.window.after(100, self.draw) #call draw again every 100ms (1/10 of a second) = 10 frames per second

def save_high_scores(score, filename='high_scores.txt'):
    # Read the existing high scores
    high_scores = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            high_scores = [int(line.strip()) for line in f.readlines()]

    # Add the new score
    high_scores.append(score)

    # Sort and keep the top 10 scores
    high_scores = sorted(high_scores, reverse=True)[:10]

    # Write the high scores back to the file
    with open(filename, 'w') as f:
        for score in high_scores:
            f.write(str(score) + '\n')

# Initialize game
snake = Snake(Tile(TILE_SIZE * 5, TILE_SIZE * 5))
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)

# Game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

# Format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

game = Game(window, canvas, snake, food)
game.draw()
window.bind("<KeyRelease>", game.change_direction) #when you press on any key and then let go
window.mainloop()  # Used for listening to window events like key presses
