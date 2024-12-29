import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Simulation parameters
time_step = 0.1
simulation_time = 30
num_drones = 20  #number of drones

# Defense zone (circle)
defense_center = np.array([50, 50])
defense_radius = 20

# Drones' initial positions and speeds
drone_positions = np.random.rand(num_drones, 2) * 100  # Random positions in 100x100 area
drone_speeds = np.random.rand(num_drones, 2) * 2 - 1  # Random directions and speeds

# Defense system
defense_system_active = [False] * num_drones  # Whether the defense is activated for a drone
drones_eliminated = [False] * num_drones  # Whether a drone has been eliminated
drones_escaped = [False] * num_drones  # Whether a drone has escaped successfully

# Performance metrics
eliminated_count = 0
escaped_count = 0

# Visualization setup
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

defense_circle = plt.Circle(defense_center, defense_radius, color='blue', fill=False, label="Defense Zone")
ax.add_artist(defense_circle)

drone_scatter = ax.scatter(drone_positions[:, 0], drone_positions[:, 1], color='red', label="Drones")
eliminated_scatter = ax.scatter([], [], color='black', label="Eliminated Drones")
escaped_scatter = ax.scatter([], [], color='orange', label="Escaped Drones")

# Update function for animation
def update(frame):
    global drone_positions, drone_speeds, defense_system_active, drones_eliminated, drones_escaped
    global eliminated_count, escaped_count

    # Update drone positions
    drone_positions += drone_speeds

    # Reflect drones off walls
    for i in range(num_drones):
        if drones_eliminated[i] or drones_escaped[i]:
            continue  # Skip eliminated or escaped drones
        if drone_positions[i, 0] < 0 or drone_positions[i, 0] > 100:
            drone_speeds[i, 0] *= -1
        if drone_positions[i, 1] < 0 or drone_positions[i, 1] > 100:
            drone_speeds[i, 1] *= -1

        # Check if drones escape the defense zone
        distance_to_center = np.linalg.norm(drone_positions[i] - defense_center)
        if distance_to_center < defense_radius:
            defense_system_active[i] = True
            drones_eliminated[i] = True
            eliminated_count += 1
            drone_positions[i] = [-10, -10]  # Move eliminated drones out of the area
        elif frame * time_step >= simulation_time - 5:  # Escape condition: Drone survives until the end
            drones_escaped[i] = True
            escaped_count += 1

    # Update visualization
    active_positions = drone_positions[~np.logical_or(drones_eliminated, drones_escaped)]
    eliminated_positions = drone_positions[drones_eliminated]
    escaped_positions = drone_positions[drones_escaped]

    drone_scatter.set_offsets(active_positions)
    eliminated_scatter.set_offsets(eliminated_positions)
    escaped_scatter.set_offsets(escaped_positions)

    return drone_scatter, eliminated_scatter, escaped_scatter

ani = FuncAnimation(fig, update, frames=int(simulation_time / time_step), interval=50, blit=True)

plt.legend()
plt.title("Anti-Drone Defense System with Performance Metrics")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.grid()

# Display animation as HTML in Colab
HTML(ani.to_jshtml())

# Print performance metrics after the simulation
def print_performance():
    total_drones = num_drones
    success_rate = (eliminated_count / total_drones) * 100
    escape_rate = (escaped_count / total_drones) * 100

    print("Performance Metrics:")
    print(f"Total Drones: {total_drones}")
    print(f"Eliminated Drones: {eliminated_count}")
    print(f"Escaped Drones: {escaped_count}")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Escape Rate: {escape_rate:.2f}%")

# Run performance calculation after the animation
print_performance()
