import numpy as np

import matplotlib.pyplot as plt

# Constants and initial conditions
g = 9.81  # gravitational acceleration in m/s^2
#m = 15  # mass of the object in kg
Cd = 0.5  # drag coefficient of the object
rho = 1.2  # density of air in kg/m^3
A = 10  # cross-sectional area of the object in m^2
v0 = 50  # initial velocity in m/s
theta_deg = 45  # angle of launch in degrees
x0 = 0  # initial x position in m
y0 = 0  # initial y position in m
dt = 0.01  # time step in seconds
def plot(m,A,v0,theta_deg):
    m=round(m,-3)/10
    A=round(A,-2)
    v0=round(v0)

    # Convert launch angle to radians
    theta = np.radians(theta_deg)

    # Initialize arrays
    t = np.arange(0, 100, dt)
    x = np.zeros_like(t)
    y = np.zeros_like(t)
    vx = np.zeros_like(t)
    vy = np.zeros_like(t)
    ax = np.zeros_like(t)
    ay = np.zeros_like(t)

    # Set initial conditions
    x[0] = x0
    y[0] = y0
    vx[0] = v0 * np.cos(theta)
    vy[0] = v0 * np.sin(theta)

    # Initialize variables to store highest Y and furthest X
    Y_Max = 0
    X_Max = 0

        # Simulate the motion of the object
    for i in range(1, len(t)):
            # Calculate the drag force
        v = np.sqrt(vx[i-1]**2 + vy[i-1]**2)
        Fd = 0.5 * rho * A * Cd * v**2
            # Calculate the acceleration
        ax[i] = -Fd/m
        ay[i] = -g - Fd/m * vy[i-1] / v

            # Update the velocity and position
        vx[i] = vx[i-1] + ax[i] * dt
        vy[i] = vy[i-1] + ay[i] * dt
        x[i] = x[i-1] + vx[i] * dt
        y[i] = y[i-1] + vy[i] * dt

            # Check if the projectile has hit the ground
        if y[i] < 0:
            y[i] = 0
            Air_Time=t[i]
            break
        # Update highest_y and furthest_x if needed
        if y[i] > Y_Max:
            Y_Max = y[i]
        if x[i] > X_Max:
            X_Max = x[i]

        # Store the coordinates in a list
        cords = list(zip(np.round(abs(x),2), np.round(abs(y),2)))
        #clean up array
    clean = False
    while clean == False:
        if cords[-1][0]==0:
            cords.pop(-1)
        else:
            clean = True
    plt.figure(figsize=(5,3))
    plt.plot(x, y)
    name=f"{Y_Max}.png"
    plt.savefig(f"{Y_Max}.png")
    X_Final=cords[-1][0]
    return cords,Y_Max,X_Max,X_Final,Air_Time,name


