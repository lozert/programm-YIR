import sys
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("График функции")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.function_label = QLabel("Введите функцию:", self)
        self.layout.addWidget(self.function_label)

        self.function_input = QLineEdit(self)
        self.function_input.setText("np.sin(x)")  # Пример: По умолчанию установлен график синуса
        self.layout.addWidget(self.function_input)

        self.range_label = QLabel("Введите диапазон значений (через запятую):", self)
        self.layout.addWidget(self.range_label)

        self.range_input = QLineEdit(self)
        self.range_input.setText("-10, 10, 1")  
        self.layout.addWidget(self.range_input)

        self.plot_button = QPushButton("Построить график", self)
        self.plot_button.clicked.connect(self.plot)
        self.layout.addWidget(self.plot_button)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def plot(self):
        try:
            function_text = self.function_input.text()
            range_text = self.range_input.text()

            function = lambda x: eval(f"{function_text}")
            range_start, range_end, step_text = map(float, range_text.split(','))
            
            step = float(step_text) if step_text else (range_end - range_start) / 200  # Используем введенный шаг или рассчитываем автоматически

            x_values = np.linspace(range_start,range_end, 200)
            y_values = function(x_values)
            range_step = np.arange(range_start, range_end+0.1, step)
            self.ax.clear()
            self.ax.plot(x_values, y_values)
            
            self.ax.set_title("График функции")
            self.ax.set_xlabel("X-ось")
            self.ax.set_ylabel("Y-ось")

            # Используем xticks для установки делений по оси X
            self.ax.set_xticks(range_step)

            self.canvas.draw()
            self.writeInFile(function_text,x_values, y_values)

        except Exception as e:
            print(f"Ошибка при построении графика: {e}")

    def writeInFile(self, function_text, x_values, y_values):
        with open("data.txt", "w") as file:
            file.write(f" Функция: {function_text}\n")
            file.write(f" X {'-' * 10} Y\n")
            for i in range(len(x_values)):
                file.write(f"{x_values[i]:.5f}  {y_values[i]:.5f}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
