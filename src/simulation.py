import numpy as np
import matplotlib.pyplot as plt
from tracker import HandTracker

class RobotArmSimulation:
    def __init__(self, arm_length=44, max_x=176, max_y=88):
        self.tracker = HandTracker()
        self.arm_length = arm_length
        self.max_x = max_x
        self.max_y = max_y
        self.x0 = 0
        self.y0 = 0

    def getTracker(self):
        return self.tracker

    def simulate(self, iterations=1000):
        i = 0
        while i < iterations:
            stuff = self.tracker.getPalmCoords()
            scaled_coords = stuff[0]
            coords = self.tracker.getReal(scaled_coords[0], scaled_coords[1], self.max_x, self.max_y)

            dist = stuff[1]
            maxDist = dist[1] * 2
            currentDist = (dist[0] / maxDist ) - 0.1
            if currentDist < 0:
                currentDist = 0

            print(f"opening : {currentDist * 100}%")

            if coords:
                theta1, theta2 = self.tracker.calculateAnglesRad(coords[0], coords[1], self.y0, self.arm_length, self.arm_length)

                x1 = self.x0 + self.arm_length * np.cos(theta1)
                y1 = self.y0 + self.arm_length * np.sin(theta1)
                
                x2 = x1 + self.arm_length * np.cos(theta1 + theta2)
                y2 = y1 + self.arm_length * np.sin(theta1 + theta2)

                plt.figure()
                plt.plot([0, x1], [0, y1], 'b-o')  # First link
                plt.plot([x1, x2], [y1, y2], 'r-o')  # Second link
                plt.plot([0, 10 * currentDist], [-10, -10], 'g-o')
                plt.plot(0, 0, 'ko')  # Base
                plt.axis('equal')
                plt.xlim(-100, 100)
                plt.ylim(-20, 100)
                plt.xlabel('X-axis')
                plt.ylabel('Y-axis')
                plt.title('Robot Arm Simulation')
                plt.grid(True)
                plt.show()

            i += 1

    def captureInitialCoords(self, iterations=100):
        i = 0
        while i < iterations:
            coords = self.tracker.getPalmCoords()
            if coords:
                print(f"Original: {coords}")
                real_x = (coords[0] * self.max_x) - (self.max_x / 2)
                real_y = (coords[1] * self.max_y)
                real_pair = (real_x, real_y)
                print(f"Converted: {real_pair}")
            else:
                pair = (0, self.max_y)
                print(pair)

if __name__ == "__main__":
    robot_arm = RobotArmSimulation()
    robot_arm.simulate(iterations=1000)
    robot_arm.captureInitialCoords()