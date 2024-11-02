import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QFileDialog, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class CubeVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cube Visualizer")

        self.setFixedSize(1000, 700)

        self.cube_states = []
        self.current_index = 0
        self.is_playing = False
        self.playback_speed = 1.0
        self.angle_x = 20  
        self.angle_y = 0    

        main_layout = QHBoxLayout()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(main_layout)

        # Control panel 
        control_layout = QVBoxLayout()
        main_layout.addLayout(control_layout)

        # Load button
        self.load_button = QPushButton('Load Experiment File', self)
        control_layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.load_experiment_file)
        self.load_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px")

        # Play/Pause button
        self.play_button = QPushButton('Play', self)
        control_layout.addWidget(self.play_button)
        self.play_button.clicked.connect(self.toggle_play)
        self.play_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 5px")

        # Progress slider 
        progress_layout = QHBoxLayout()
        self.progress_slider = QSlider(Qt.Horizontal, self)
        self.progress_slider.sliderReleased.connect(self.update_state)
        self.progress_slider.setMinimum(0)
        progress_layout.addWidget(self.progress_slider)
        
        self.frame_label = QLabel("Frame: 0", self)
        progress_layout.addWidget(self.frame_label)
        
        control_layout.addLayout(progress_layout)

        # Playback speed 
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(5)
        control_layout.addWidget(self.speed_slider)
        self.speed_slider.sliderReleased.connect(self.update_speed)

        # Rotation and tilt buttons
        self.rotate_left_button = QPushButton('Rotate Left', self)
        control_layout.addWidget(self.rotate_left_button)
        self.rotate_left_button.clicked.connect(self.rotate_left)
        self.rotate_left_button.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 5px")

        self.rotate_right_button = QPushButton('Rotate Right', self)
        control_layout.addWidget(self.rotate_right_button)
        self.rotate_right_button.clicked.connect(self.rotate_right)
        self.rotate_right_button.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 5px")

        self.tilt_up_button = QPushButton('Tilt Up', self)
        control_layout.addWidget(self.tilt_up_button)
        self.tilt_up_button.clicked.connect(self.tilt_up)
        self.tilt_up_button.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 5px")

        self.tilt_down_button = QPushButton('Tilt Down', self)
        control_layout.addWidget(self.tilt_down_button)
        self.tilt_down_button.clicked.connect(self.tilt_down)
        self.tilt_down_button.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 5px")

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas)

        # Setup timer 
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

        plt.ion()  
        self.update_cube_plot() 

    def load_experiment_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Experiment File', '', 'JSON Files (*.json)')
        if filename:
            with open(filename, 'r') as f:
                self.cube_states = json.load(f)
            self.current_index = 0
            self.progress_slider.setMaximum(len(self.cube_states) - 1)
            self.update_cube_plot()

    def toggle_play(self):
        self.is_playing = not self.is_playing
        self.play_button.setText('Pause' if self.is_playing else 'Play')
        if self.is_playing:
            self.timer.start(int(1000 / self.playback_speed))
        else:
            self.timer.stop()

    def update_state(self):
        self.current_index = self.progress_slider.value()
        self.update_cube_plot()

    def update_speed(self):
        self.playback_speed = self.speed_slider.value()
        if self.is_playing:
            self.timer.setInterval(int(1000 / self.playback_speed))

    def next_frame(self):
        if self.current_index < len(self.cube_states) - 1:
            self.current_index += 1
        else:
            self.current_index = 0  
        self.progress_slider.setValue(self.current_index)
        self.update_cube_plot()

    def rotate_left(self):
        self.angle_y -= 5 
        self.update_view()

    def rotate_right(self):
        self.angle_y += 5  
        self.update_view()

    def tilt_up(self):
        self.angle_x += 5  
        self.update_view()

    def tilt_down(self):
        self.angle_x -= 5  
        self.update_view()

    def update_view(self):
        self.ax.view_init(elev=self.angle_x, azim=self.angle_y)  
        self.canvas.draw_idle()  

    def update_cube_plot(self):
        self.ax.clear() 
        if self.cube_states:
            cube_state = self.cube_states[self.current_index]['cube']
            self.plot_cube(cube_state)
            self.frame_label.setText(f"Frame: {self.current_index}")
        self.update_view()  
        self.canvas.draw_idle()  

    def plot_cube(self, cube_state):
        n = len(cube_state)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    self.ax.text(i + 0.5, j + 0.5, k + 0.5, str(cube_state[i][j][k]), color='black', ha='center', va='center', fontsize=8, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

        self.ax.set_xlim(0, n)
        self.ax.set_ylim(0, n)
        self.ax.set_zlim(0, n)
        self.ax.set_xticks(range(n))
        self.ax.set_yticks(range(n))
        self.ax.set_zticks(range(n))
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_zlabel('Z-axis')
        self.ax.set_title('Cube State')


# app = QApplication(sys.argv)
# window = CubeVisualizer()
# window.show()
# sys.exit(app.exec_())
