import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Step 2: Load and Explore the Dataset
df = pd.read_csv('C:\Tugas\Tugas Nana\SEM 6\PEMODELAN, SIMULASI\simulated_call_centre.csv')
print("Dataset Head:")
print(df.head())
print("\nDataset Info:")
print(df.info())

# Step 3: Implement the Queueing Simulation
class QueueSimulation:
    def __init__(self, arrival_rate, service_rate, num_agents, simulation_time):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.num_agents = num_agents
        self.simulation_time = simulation_time
        self.queue = []
        self.wait_times = []
    
    def simulate(self):
        current_time = 0
        servers = [0] * self.num_agents  # Waktu kapan agen akan bebas lagi
        while current_time < self.simulation_time:
            arrival_time = np.random.exponential(1/self.arrival_rate)
            service_time = np.random.exponential(1/self.service_rate)
            current_time += arrival_time
            available_agent = min(range(self.num_agents), key=lambda x: servers[x])
            
            if servers[available_agent] <= current_time:
                servers[available_agent] = current_time + service_time
                self.wait_times.append(0)  # Tidak menunggu jika ada agen tersedia
            else:
                wait_time = servers[available_agent] - current_time
                self.wait_times.append(wait_time)
                servers[available_agent] += service_time
    
    def get_average_wait_time(self):
        return np.mean(self.wait_times)

# Parameter simulasi
arrival_rate = 5  # rata-rata kedatangan per menit
service_rate = 6   # rata-rata layanan per menit
num_agents = 3     # jumlah agen
simulation_time = 120  # waktu simulasi dalam menit

sim = QueueSimulation(arrival_rate, service_rate, num_agents, simulation_time)
sim.simulate()

# Step 4: Performance Analysis & Visualization
sns.histplot(sim.wait_times, bins=20, kde=True)
plt.xlabel("Wait Time (minutes)")
plt.ylabel("Frequency")
plt.title("Distribution of Wait Times in Call Centre")
plt.show()

# Step 5: Modify Parameters and Optimize
optimized_agents = 5  # coba meningkatkan jumlah agen
sim_opt = QueueSimulation(arrival_rate, service_rate, optimized_agents, simulation_time)
sim_opt.simulate()

print(f"Average Wait Time (Original): {sim.get_average_wait_time():.2f} minutes")
print(f"Average Wait Time (Optimized): {sim_opt.get_average_wait_time():.2f} minutes")

# Step 6: Plot Additional Insights
agents_range = range(1, 11)  # Mencoba dari 1 hingga 10 agen
wait_times_avg = []

for agents in agents_range:
    sim_test = QueueSimulation(arrival_rate, service_rate, agents, simulation_time)
    sim_test.simulate()
    wait_times_avg.append(sim_test.get_average_wait_time())

plt.plot(agents_range, wait_times_avg, marker='o', linestyle='-')
plt.xlabel("Number of Agents")
plt.ylabel("Average Wait Time (minutes)")
plt.title("Effect of Increasing Agents on Wait Time")
plt.show()
