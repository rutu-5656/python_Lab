"""Simple Snake game using Tkinter.

Run:
    python snake_game.py

Controls:
    Arrow keys to move, Space to pause/resume, R to restart.
"""

from __future__ import annotations

import random
import tkinter as tk


class SnakeGame:
    def __init__(self, root: tk.Tk, rows: int = 20, cols: int = 20, cell_size: int = 24) -> None:
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size

        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#111")
        self.canvas.pack()

        self.score_var = tk.StringVar(value="Score: 0")
        self.score_label = tk.Label(root, textvariable=self.score_var, font=("Arial", 12))
        self.score_label.pack(pady=6)

        self.direction = "Right"
        self.next_direction = "Right"
        self.speed_ms = 120
        self.game_running = True
        self.paused = False

        self.root.bind("<Key>", self.on_key)
        self.reset_game()
        self.loop()

    def reset_game(self) -> None:
        self.canvas.delete("all")
        self.score = 0
        self.score_var.set("Score: 0")
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_running = True
        self.paused = False

        start_row = self.rows // 2
        start_col = self.cols // 2
        self.snake = [
            (start_row, start_col - 1),
            (start_row, start_col),
            (start_row, start_col + 1),
        ]
        self.spawn_food()
        self.draw()

    def spawn_food(self) -> None:
        available = {
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in self.snake
        }
        self.food = random.choice(list(available)) if available else None

    def on_key(self, event: tk.Event) -> None:
        key = event.keysym
        if key in {"Up", "Down", "Left", "Right"}:
            self.update_direction(key)
        elif key == "space":
            self.toggle_pause()
        elif key in {"r", "R"}:
            self.reset_game()

    def update_direction(self, key: str) -> None:
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if key != opposites.get(self.direction):
            self.next_direction = key

    def toggle_pause(self) -> None:
        if not self.game_running:
            return
        self.paused = not self.paused

    def loop(self) -> None:
        if self.game_running and not self.paused:
            self.step()
        self.root.after(self.speed_ms, self.loop)

    def step(self) -> None:
        self.direction = self.next_direction
        head_row, head_col = self.snake[-1]
        delta = {
            "Up": (-1, 0),
            "Down": (1, 0),
            "Left": (0, -1),
            "Right": (0, 1),
        }[self.direction]
        new_head = (head_row + delta[0], head_col + delta[1])

        if self.hit_wall(new_head) or new_head in self.snake:
            self.game_over()
            return

        self.snake.append(new_head)

        if self.food and new_head == self.food:
            self.score += 1
            self.score_var.set(f"Score: {self.score}")
            self.spawn_food()
        else:
            self.snake.pop(0)

        self.draw()

    def hit_wall(self, position: tuple[int, int]) -> bool:
        row, col = position
        return row < 0 or row >= self.rows or col < 0 or col >= self.cols

    def draw_cell(self, position: tuple[int, int], color: str, outline: str = "") -> None:
        row, col = position
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline)

    def draw(self) -> None:
        self.canvas.delete("all")
        for segment in self.snake[:-1]:
            self.draw_cell(segment, "#2ecc71")
        self.draw_cell(self.snake[-1], "#27ae60", outline="#0b6623")

        if self.food:
            self.draw_cell(self.food, "#e74c3c", outline="#b03a2e")

        if self.paused:
            self.draw_overlay("Paused")
        if not self.game_running:
            self.draw_overlay("Game Over")

    def draw_overlay(self, text: str) -> None:
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#000", stipple="gray50")
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text=text,
            fill="white",
            font=("Arial", 24, "bold"),
        )

    def game_over(self) -> None:
        self.game_running = False
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
