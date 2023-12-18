import tkinter as tk
from tkinter import messagebox
import numpy as np

matrix = np.array([
    [2, -1, -1, 1, -1, -1, 0],
    [-1, 2, -1, 1, -1, 2, -1],
    [-1, -1, 2, 2, 1, -1, -1],
    [1, 2, 2, -1, 0, 1, 1],
    [-1, -1, 1, 0, 0, -1, -1],
    [-1, 1, -1, 0, -1, 0, -1],
    [0, -1, -1, 0, -1, -1, 0]
])

class NineMensMorrisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nine Men's Morris")
        self.board = matrix
        self.canvas_size = 400
        self.cell_size = self.canvas_size // 7
        self.create_board_gui()

    def create_board_gui(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack()

        for i in range(7):
            for j in range(7):
                x, y = j * self.cell_size, i * self.cell_size
                cell_value = self.board[i, j]
                color = "white" if cell_value == 1 else "black" if cell_value == 2 else "gray"

                # Draw cell
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill=color)

                # Draw piece
                if cell_value == 1:
                    self.canvas.create_oval(x + 10, y + 10, x + self.cell_size - 10, y + self.cell_size - 10, fill="white")
                elif cell_value == 2:
                    self.canvas.create_oval(x + 10, y + 10, x + self.cell_size - 10, y + self.cell_size - 10, fill="black")

                # Bind click event
                self.canvas.tag_bind(f"cell_{i}_{j}", "<Button-1>", lambda event, row=i, col=j: self.on_cell_click(row, col))

    def on_cell_click(self, row, col):
        selected_value = self.board[row, col]
        if selected_value == 0:
            messagebox.showinfo("Info", "You clicked an empty cell.")
        elif selected_value == -1:
            messagebox.showinfo("Info", "You clicked a blocked cell.")
        elif selected_value == 1:
            messagebox.showinfo("Info", "You clicked a white piece.")
        elif selected_value == 2:
            messagebox.showinfo("Info", "You clicked a black piece.")


if __name__ == "__main__":
    root = tk.Tk()
    app = NineMensMorrisGUI(root)
    root.mainloop()
