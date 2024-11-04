from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from algorithm.restart import RandomRestart
from algorithm.stochastic import Stochastic
from algorithm.annealing import Annealing
from algorithm.geneticAlgorithm import GeneticAlgorithm
from algorithm.steepest import Steepest
from algorithm.sidewaysmove import SidewaysMove
from visualizer.visualizer import CubeVisualizer
import json
import matplotlib.pyplot as plt
import sys
import time

class CubeSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagonal Magic Cube Solver")
        
        self.solver = None
        self.history = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        self.setFixedSize(600, 650)

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
        self.algo_dropdown.addItems(["Random Restart Hill-Climbing", "Stochastic Hill-Climbing","Simulated Annealing", "Steepest Ascent Hill-Climbing","Sideways Move Hill-Climbing", "Genetic Algorithm"])
        self.algo_dropdown.setFont(QFont("Arial", 11))
        self.algo_dropdown.setStyleSheet("padding: 5px;")
        self.algo_dropdown.currentIndexChanged.connect(self.toggle_fields)
        self.layout.addWidget(self.algo_dropdown)

        self.restart_label = QLabel("Enter maximum restart:")
        self.restart_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.restart_label)
        
        self.restart_input = QLineEdit()
        self.restart_input.setFont(QFont("Arial", 11))
        self.restart_input.setPlaceholderText("Enter a number")
        self.restart_input.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.restart_input)

        # Fields for Random Restart, Annealing, SidewaysMove
        self.param_label = QLabel("Enter maximum iterations:")
        self.param_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.param_label)
        
        self.param_input = QLineEdit()
        self.param_input.setFont(QFont("Arial", 11))
        self.param_input.setPlaceholderText("Enter a number")
        self.param_input.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.param_input)
 
        self.temp_label = QLabel("Initial Temperature (Annealing):")
        self.temp_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.temp_label)
        
        self.temp_input = QLineEdit()
        self.temp_input.setFont(QFont("Arial", 11))
        self.temp_input.setPlaceholderText("Enter initial temperature")
        self.temp_input.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.temp_input)
        
        self.cooling_label = QLabel("Cooling Rate (Annealing):")
        self.cooling_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.cooling_label)
        
        self.cooling_input = QLineEdit()
        self.cooling_input.setFont(QFont("Arial", 11))
        self.cooling_input.setPlaceholderText("Enter cooling rate")
        self.cooling_input.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.cooling_input)
        
        self.schedule_label = QLabel("Select Cooling Schedule (Annealing):")
        self.schedule_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.schedule_label)
        
        self.schedule_dropdown = QComboBox()
        self.schedule_dropdown.addItems(["Linear", "Exponential", "Logarithmic", "Quadratic"])
        self.schedule_dropdown.setFont(QFont("Arial", 11))
        self.schedule_dropdown.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.schedule_dropdown)

        self.maxit_label = QLabel("Enter maximum iterations:")
        self.maxit_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.maxit_label)

        self.maxit_input = QLineEdit()
        self.maxit_input.setFont(QFont("Arial", 11))
        self.maxit_input.setPlaceholderText("Enter a number")
        self.maxit_input.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.maxit_input)

        self.population_total = QLabel("Population Total:")
        self.population_total.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.population_total)

        self.population_input = QLineEdit()
        self.population_input.setFont(QFont("Arial", 11))
        self.population_input.setPlaceholderText("Enter population total")
        self.population_input.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.population_input)

        self.sideways_label = QLabel("Enter maximum sideways moves:")
        self.sideways_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.sideways_label)

        self.sideways_input = QLineEdit()
        self.sideways_input.setFont(QFont("Arial", 11))
        self.sideways_input.setPlaceholderText("Enter maximum sideways moves")
        self.sideways_input.setStyleSheet("padding: 5px;")
        self.layout.addWidget(self.sideways_input)


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

        # Hide stochastic fields initially
        self.param_label.hide()
        self.param_input.hide()

        self.temp_label.hide()
        self.temp_input.hide()
        self.cooling_label.hide()
        self.cooling_input.hide()
        self.schedule_label.hide()
        self.schedule_dropdown.hide()
        self.population_input.hide()
        self.population_total.hide()
        self.maxit_label.hide()
        self.maxit_input.hide()
        self.sideways_label.hide()
        self.sideways_input.hide()

    def toggle_fields(self):
        algorithm = self.algo_dropdown.currentIndex()
        is_restart = (algorithm == 0)
        self.restart_label.setVisible(is_restart)
        self.restart_input.setVisible(is_restart)

        is_stochastic = (algorithm == 1)
        self.param_label.setVisible(is_stochastic)
        self.param_input.setVisible(is_stochastic)
        
        is_annealing = (algorithm == 2)
        self.temp_label.setVisible(is_annealing)
        self.temp_input.setVisible(is_annealing)
        self.cooling_label.setVisible(is_annealing)
        self.cooling_input.setVisible(is_annealing)
        self.schedule_label.setVisible(is_annealing)
        self.schedule_dropdown.setVisible(is_annealing)

        is_sideways_move = (algorithm == 3)
        self.sideways_label.setVisible(is_sideways_move)
        self.sideways_input.setVisible(is_sideways_move)

        is_sideways_move = (algorithm == 4)
        self.sideways_label.setVisible(is_sideways_move)
        self.sideways_input.setVisible(is_sideways_move)

        is_genetic = (algorithm == 5)
        self.maxit_label.setVisible(is_genetic)
        self.maxit_input.setVisible(is_genetic)
        self.population_total.setVisible(is_genetic)
        self.population_input.setVisible(is_genetic)

    def solve_cube(self):
        try:
            max_param = int(self.param_input.text()) if self.param_input.isVisible() else None
            restart_param = int(self.restart_input.text()) if self.restart_input.isVisible() else None
            max_sideways_moves = int(self.sideways_input.text()) if self.sideways_input.isVisible() else None
            algorithm = self.algo_dropdown.currentIndex()
            
            start_time = time.time()

            if algorithm == 0:
                self.solver = RandomRestart()
                self.solver.solveCube(restart_param)
            elif algorithm == 1:
                self.solver = Stochastic()
                self.solver.solveCube(max_param,num_workers=5)
            elif algorithm == 2:
                initial_temp = float(self.temp_input.text())
                cooling_rate = float(self.cooling_input.text())
                schedule_type = self.schedule_dropdown.currentText().lower()
                self.solver = Annealing(initial_temp, cooling_rate, schedule_type)
                self.solver.simulatedAnnealing()
            elif algorithm == 3:
                self.solver = Steepest()
                self.solver.solveCube()
            elif algorithm == 4:
                self.solver = SidewaysMove()
                self.solver.solveCube(max_sideways_moves)
            elif algorithm == 5:
                max_param = int(self.maxit_input.text())
                population_total = int(self.population_input.text())
                self.solver = GeneticAlgorithm(5, population_total, max_param)
                self.solver.solveGeneticAlgorithm()
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
        
        algorithm = self.algo_dropdown.currentIndex()
        if algorithm==0:
            plt.figure()
            for entry in self.history:
                frames = list(range(1, len(entry["objective_values"]) + 1))
                plt.plot(frames, entry["objective_values"], marker='o', label=f"Restart {entry['restart']}")

            plt.xlabel("Iteration")
            plt.ylabel("Objective Function Value")
            plt.title("Objective Function Value per Iteration for Each Restart")
            plt.legend()
            plt.grid(True)
            plt.show()
        else:
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
