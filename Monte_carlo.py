import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_pi(num_samples):
    inside_circle = 0
    x_inside = []
    y_inside = []
    x_outside = []
    y_outside = []
    
    for _ in range(num_samples):
        x, y = np.random.uniform(-1, 1, 2)  # Menghasilkan titik acak dalam rentang [-1, 1]
        if x**2 + y**2 <= 1:
            inside_circle += 1
            x_inside.append(x)
            y_inside.append(y)
        else:
            x_outside.append(x)
            y_outside.append(y)
    
    pi_estimate = (inside_circle / num_samples) * 4
    return pi_estimate, x_inside, y_inside, x_outside, y_outside

# Menjalankan simulasi
num_samples = 10000
pi_estimate, x_inside, y_inside, x_outside, y_outside = monte_carlo_pi(num_samples)

# Menampilkan hasil
print(f"Estimasi nilai π dengan {num_samples} sampel: {pi_estimate}")

# Membuat plot
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.set_title("Simulasi Monte Carlo untuk Estimasi Pi")

# Plot titik-titik
ax.scatter(x_inside, y_inside, color='blue', s=1, label="Inside Circle")
ax.scatter(x_outside, y_outside, color='red', s=1, label="Outside Circle")

# Plot lingkaran
circle = plt.Circle((0, 0), 1, color='black', fill=False)
ax.add_patch(circle)

# Plot persegi
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.legend()
plt.show()