import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

RANDOM_SEED = 42
NUM_TELLERS_2 = 2  
NUM_TELLERS_4 = 4  
ARRIVAL_RATE = 5  
SIM_TIME = 300  
VIP_PROB = 0.3  
TOTAL_CUSTOMERS = 100  

class Bank:
    def __init__(self, env, num_tellers):
        self.env = env
        self.teller = simpy.PriorityResource(env, capacity=num_tellers)
        self.wait_times = []
    
    def serve_customer(self, customer):
        arrival_time = self.env.now
        priority = 0 if customer['vip'] else 1  # VIP (0) dilayani lebih dulu
        with self.teller.request(priority=priority) as request:
            yield request
            service_time = random.randint(3, 8)
            yield self.env.timeout(service_time)
            self.wait_times.append(self.env.now - arrival_time)
            print(f"Customer {customer['id']} (VIP: {customer['vip']}) waited {self.env.now - arrival_time:.2f} seconds.")
            print(f"Customer {customer['id']} (VIP: {customer['vip']}) started service at {self.env.now:.2f} seconds.")

def customer_generator(env, bank):
    for customer_id in range(1, TOTAL_CUSTOMERS + 1):
        yield env.timeout(random.expovariate(1.0 / ARRIVAL_RATE))
        is_vip = random.random() < VIP_PROB
        env.process(bank.serve_customer({'id': customer_id, 'vip': is_vip}))

# Simulasi dengan 2 teller
random.seed(RANDOM_SEED)
env = simpy.Environment()
bank_2_tellers = Bank(env, NUM_TELLERS_2)
env.process(customer_generator(env, bank_2_tellers))
env.run()
wait_times_2_tellers = bank_2_tellers.wait_times

# Simulasi dengan 4 teller
random.seed(RANDOM_SEED)
env = simpy.Environment()
bank_4_tellers = Bank(env, NUM_TELLERS_4)
env.process(customer_generator(env, bank_4_tellers))
env.run()
wait_times_4_tellers = bank_4_tellers.wait_times

# Hitung rata-rata waktu tunggu
avg_wait_2_tellers = np.mean(wait_times_2_tellers) if wait_times_2_tellers else 0
avg_wait_4_tellers = np.mean(wait_times_4_tellers) if wait_times_4_tellers else 0
print(f"\nRata-rata waktu tunggu dengan 2 teller: {avg_wait_2_tellers:.2f} detik")
print(f"\nRata-rata waktu tunggu dengan 4 teller: {avg_wait_4_tellers:.2f} detik")

# Visualisasi perbandingan dalam grafik terpisah
plt.figure(figsize=(12, 5))

# Grafik untuk 2 teller
plt.subplot(1, 2, 1)
plt.hist(wait_times_2_tellers, bins=20, alpha=0.6, color='blue', edgecolor='black')
plt.axvline(avg_wait_2_tellers, color='red', linestyle='dashed', linewidth=2, label=f'Avg: {avg_wait_2_tellers:.2f}s')
plt.xlabel('Waktu Tunggu (detik)')
plt.ylabel('Jumlah Pelanggan')
plt.title('Waktu Tunggu dengan 2 Teller')
plt.legend()

# Grafik untuk 4 teller
plt.subplot(1, 2, 2)
plt.hist(wait_times_4_tellers, bins=20, alpha=0.6, color='orange', edgecolor='black')
plt.axvline(avg_wait_4_tellers, color='red', linestyle='dashed', linewidth=2, label=f'Avg: {avg_wait_4_tellers:.2f}s')
plt.xlabel('Waktu Tunggu (detik)')
plt.ylabel('Jumlah Pelanggan')
plt.title('Waktu Tunggu dengan 4 Teller')
plt.legend()

plt.tight_layout()
plt.show()
