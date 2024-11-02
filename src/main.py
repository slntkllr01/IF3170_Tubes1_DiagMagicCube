from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from algorithm.restart import RandomRestart
from algorithm.stochastic import Stochastic
from visualizer.visualizer import CubeVisualizer
import json
import matplotlib.pyplot as plt
import sys
import time

# cara cobanya donwload dulu library pyqt sm matplotlib dulu kalau gapunya, habis itu coba run file ini deh
# terus coba masukin file json
# sama teman-temanku yg jago design bolehlah dibagusin kalau sempat

class CubeSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagonal Magic Cube Solver")
        self.setFixedSize(800, 600)
        
        self.solver = None
        self.history = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        palette = self.central_widget.palette()
        palette.setColor(QPalette.Window, QColor("#f0f4f8"))
        self.central_widget.setPalette(palette)
        self.central_widget.setAutoFillBackground(True)
        
        self.title_label = QLabel("Diagonal Magic Cube Solver")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.algo_label = QLabel("Choose the algorithm:")
        self.algo_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.algo_label)
        
        self.algo_dropdown = QComboBox()
        self.algo_dropdown.addItems(["Random Restart Hill-Climbing", "Stochastic Hill-Climbing"])
        self.algo_dropdown.setFont(QFont("Arial", 11))
        self.algo_dropdown.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.algo_dropdown)
        
        self.param_label = QLabel("Enter maximum iterations:")
        self.param_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.param_label)
        
        self.param_input = QLineEdit()
        self.param_input.setFont(QFont("Arial", 11))
        self.param_input.setPlaceholderText("Enter a number")
        self.param_input.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.param_input)
 
        self.solve_button = QPushButton("Solve Cube")
        self.solve_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.solve_button.setStyleSheet("padding: 10px; background-color: #4CAF50; color: white;")
        self.solve_button.clicked.connect(self.solve_cube)
        self.layout.addWidget(self.solve_button)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
        self.plot_button = QPushButton("Show Objective Function Plot")
        self.plot_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.plot_button.setStyleSheet("padding: 10px; background-color: #2196F3; color: white;")
        self.plot_button.clicked.connect(self.show_plot)
        self.plot_button.setEnabled(False)
        self.layout.addWidget(self.plot_button)
        
        self.visualizer_button = QPushButton("Open Cube Visualizer")
        self.visualizer_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.visualizer_button.setStyleSheet("padding: 10px; background-color: #FF5722; color: white;")
        self.visualizer_button.clicked.connect(self.open_visualizer)
        self.visualizer_button.setEnabled(False)
        self.layout.addWidget(self.visualizer_button)
        
    def solve_cube(self):
        try:
            max_param = int(self.param_input.text())
            algorithm = self.algo_dropdown.currentIndex()
            
            start_time = time.time()

            if algorithm == 0:
                self.solver = RandomRestart()
                self.solver.solveCube(max_param)
            elif algorithm == 1:
                self.solver = Stochastic()
                self.solver.solveCube(max_param)
            else:
                raise ValueError("Invalid algorithm selection")
            
            end_time = time.time()  
            duration = end_time - start_time  

            self.history = self.solver.history
            self.plot_button.setEnabled(True)
            self.visualizer_button.setEnabled(True)
            
            # Save history to JSON
            with open("solver_history.json", "w") as f:
                json.dump(self.history, f, indent=4)
            QMessageBox.information(self, "Success", f"Solver history saved to solver_history.json \nDuration: {duration:.2f} seconds")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid integer for maximum iterations.")
    
    def show_plot(self):
        if self.history is None:
            QMessageBox.warning(self, "Error", "No solver history found.")
            return
        
        frames = [entry["frame"] for entry in self.history]
        objective_values = [entry["objective_value"] for entry in self.history]
        
   
        plt.figure()
        plt.plot(frames, objective_values, marker='o', color='#4CAF50')
        plt.xlabel("Iteration")
        plt.ylabel("Objective Function Value")
        plt.title("Objective Function Value over Iterations")
        plt.grid(True)
        plt.show()
    
    def open_visualizer(self):
        # Open the CubeVisualizer 
        self.visualizer_window = CubeVisualizer()
        self.visualizer_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CubeSolverApp()
    window.show()
    sys.exit(app.exec_())
