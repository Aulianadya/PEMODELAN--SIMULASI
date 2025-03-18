import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Load and Explore the Dataset
file_path = "C:\Tugas\Tugas Nana\SEM 6\PEMODELAN, SIMULASI\simulated_call_centre.csv"
df = pd.read_csv(file_path)

# Ambil hanya 100 data pertama
df = df.head(10000)

# Ubah tipe data agar sesuai
df['wait_length'] = df['wait_length'].astype(int)
df['service_length'] = df['service_length'].astype(int)

# Menampilkan informasi dataset
print("Dataset Head:")
print(df.head())
print("\nDataset Info:")
print(df.info())

# Step 3: Implement the Queueing Simulation
class QueueSimulation:
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.wait_times = []
    
    def simulate(self, wait_times, service_times):
        servers = [0] * self.num_agents  # Simpan waktu kapan agen tersedia
        for wait_time, service_time in zip(wait_times, service_times):
            available_agent = min(range(self.num_agents), key=lambda x: servers[x])
            
            if servers[available_agent] <= wait_time:
                servers[available_agent] = wait_time + service_time
                self.wait_times.append(0)  # Tidak menunggu jika ada agen tersedia
            else:
                wait_time = servers[available_agent] - wait_time
                self.wait_times.append(wait_time)
                servers[available_agent] += service_time
    
    def get_average_wait_time(self):
        return np.mean(self.wait_times)

# Step 4: Monte Carlo Simulation
def monte_carlo_simulation(runs=100, num_agents=3):
    results = []
    for _ in range(runs):  
        sim = QueueSimulation(num_agents)
        
        # Tambahkan variasi acak dalam waktu tunggu & layanan
        wait_times = np.random.normal(df['wait_length'], 5)
        service_times = np.random.normal(df['service_length'], 5)
        
        wait_times = np.clip(wait_times, 0, None)  # Pastikan tidak negatif
        service_times = np.clip(service_times, 1, None)

        sim.simulate(wait_times, service_times)
        results.append(sim.get_average_wait_time())  

    return results

# Jalankan simulasi Monte Carlo
mc_results = monte_carlo_simulation()

# Step 5: Performance Analysis & Visualization
plt.hist(mc_results, bins=20, alpha=0.7, label='Monte Carlo Wait Time')
plt.axvline(np.mean(mc_results), color='red', linestyle='dashed', linewidth=2, label='Mean Wait Time')
plt.xlabel('Average Wait Time (seconds)')
plt.ylabel('Frequency')
plt.legend()
plt.title('Monte Carlo Simulation of Wait Times')
plt.show()

# Step 6: Optimize Number of Agents
agents_range = range(1, 11)  # Coba dari 1 hingga 10 agen
wait_times_avg = []

for agents in agents_range:
    sim_test = QueueSimulation(agents)
    sim_test.simulate(df['wait_length'], df['service_length'])
    wait_times_avg.append(sim_test.get_average_wait_time())

plt.plot(agents_range, wait_times_avg, marker='o', linestyle='-')
plt.xlabel("Number of Agents")
plt.ylabel("Average Wait Time (seconds)")
plt.title("Effect of Increasing Agents on Wait Time")
plt.show()
