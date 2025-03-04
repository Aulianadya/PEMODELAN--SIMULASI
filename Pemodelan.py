import simpy
import random
import pandas as pd
from datetime import datetime, timedelta

# Parameter simulasi
RANDOM_SEED = 42  # Seed untuk hasil yang reproducible
NUM_BOOTH = 2  # Jumlah booth yang tersedia
ARRIVAL_RATE = 3  # Rata-rata kedatangan pelanggan (per menit)
SERVICE_TIME = (5, 10)  # Waktu layanan dalam rentang (min, max) menit
NUM_CUSTOMERS = 100  # Jumlah pelanggan maksimum

data = []  # List untuk menyimpan data pelanggan
waiting_times = []  # List untuk menyimpan waktu tunggu pelanggan
booth_status = {i: 'Idle' for i in range(1, NUM_BOOTH + 1)}  # Status booth
START_TIME = datetime.strptime("08:00", "%H:%M")  # Simulasi dimulai pukul 08:00

def customer(env, name, booth, booth_id):
    """Proses pelanggan yang tiba di studio."""
    arrival_time = START_TIME + timedelta(minutes=env.now)
    arrival_time_str = arrival_time.strftime("%H:%M")
    
    with booth.request() as request:
        queue_enter_time = env.now  # Waktu pelanggan mulai menunggu di antrian
        yield request  # Menunggu giliran
        wait_time = round(env.now - queue_enter_time, 1)  # Hitung waktu tunggu dengan benar
        
        # Simpan waktu tunggu ke list
        waiting_times.append(wait_time)
        
        # Booth menjadi busy
        booth_status[booth_id] = 'Busy'
        
        service_duration = random.randint(*SERVICE_TIME)
        yield env.timeout(service_duration)  # Proses foto berlangsung
        departure_time = START_TIME + timedelta(minutes=env.now)
        departure_time_str = departure_time.strftime("%H:%M")
        
        # Simpan data ke dalam list sebelum mengubah status booth kembali ke Idle
        data.append([name, arrival_time_str, f"{wait_time} min", departure_time_str, f"{service_duration} min", booth_id, booth_status[booth_id]])
        
        # Booth menjadi idle kembali setelah layanan selesai
        booth_status[booth_id] = 'Idle'

def customer_generator(env, booths):
    """Generator pelanggan yang datang secara acak."""
    customer_id = 0
    while customer_id < NUM_CUSTOMERS:
        yield env.timeout(random.expovariate(1.0 / ARRIVAL_RATE))  # Kedatangan random
        customer_id += 1
        booth_id = (customer_id % NUM_BOOTH) + 1  # Menentukan booth berdasarkan ID pelanggan
        env.process(customer(env, f'Customer {customer_id}', booths[booth_id - 1], booth_id))

def main():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    booths = [simpy.Resource(env, capacity=1) for _ in range(NUM_BOOTH)]  # Membuat beberapa booth
    env.process(customer_generator(env, booths))
    env.run()
    
    # Buat dataframe dari hasil simulasi
    df = pd.DataFrame(data, columns=['Customer', 'Arrival Time', 'Wait Time', 'Departure Time', 'Service Duration', 'Booth', 'Booth Status'])
    print(df.to_string(index=False))
    
    # Hitung dan tampilkan rata-rata waktu tunggu
    if waiting_times:
        avg_waiting_time = sum(waiting_times) / len(waiting_times)
        print(f"\nRata-rata waktu tunggu pelanggan: {avg_waiting_time:.2f} menit")
    else:
        print("\nTidak ada data waktu tunggu yang tersedia.")

if __name__ == '__main__':
    main()
