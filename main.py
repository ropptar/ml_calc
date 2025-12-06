import tkinter as tk
import numpy as np
import pickle

class PixelEditor:
    def __init__(self, model_path: str):
        self.root = tk.Tk()
        self.root.title("28x28 Pixel Editor")
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)

        # Инициализация массива пикселей (28x28)
        self.pixels = np.zeros((28, 28), dtype=np.uint8)

        # Создание холста с масштабированием 8x
        self.scale = 8
        canvas_size = 28 * self.scale
        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size, bg='white')
        self.canvas.pack()

        # Кнопки управления
        tk.Button(self.root, text="Clear", command=self.clear).pack(side=tk.LEFT)
        tk.Button(self.root, text="Print", command=self.print_pixels).pack(side=tk.RIGHT)
        tk.Button(self.root, text="Predict", command=self.predict).pack(side=tk.RIGHT)

        # Привязка событий мыши
        self.canvas.bind("<B1-Motion>", self.draw)

    def draw(self, event):
        """Обработчик рисования пикселей"""
        x, y = event.x // self.scale, event.y // self.scale  # Масштабирование координат
        if 0 <= x < 28 and 0 <= y < 28:  # Проверка границ
            self.pixels[y][x] = 1  # Установка пикселя
            # Отрисовка квадрата на холсте
            self.canvas.create_rectangle(
                x * self.scale, y * self.scale,
                (x + 1) * self.scale, (y + 1) * self.scale,
                fill='black', outline=''
            )

    def clear(self):
        """Очистка холста и массива"""
        self.pixels.fill(0)
        self.canvas.delete("all")

    def print_pixels(self):
        """Вывод массива в консоль"""
        for row in self.pixels:
            print(" ".join(f"{val:1d}" for val in row))

    def predict(self):
        print(self.model.predict(self.pixels.reshape(1,-1)))

app = PixelEditor('number_recognition_model.pkl')
app.root.mainloop()