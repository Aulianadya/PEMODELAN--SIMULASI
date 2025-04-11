import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import poisson

# 1. Parameter distribusi
lambda_defect = 4  # Rata-rata jumlah cacat per hari

# 2. Simulasi selama 30 hari
np.random.seed(42)
simulasi_cacat = np.random.poisson(lam=lambda_defect, size=30)

# 3. Statistik hasil simulasi
rata2_simulasi = np.mean(simulasi_cacat)
maks_cacat = np.max(simulasi_cacat)
min_cacat = np.min(simulasi_cacat)

print("===== HASIL SIMULASI =====")
print(f"Jumlah Hari Simulasi     : {len(simulasi_cacat)}")
print(f"Rata-rata Jumlah Cacat   : {rata2_simulasi:.2f}")
print(f"Jumlah Cacat Maksimum    : {maks_cacat}")
print(f"Jumlah Cacat Minimum     : {min_cacat}")
print(f"Nilai Teoritis (λ)       : {lambda_defect}")

# 4. Tampilkan data simulasi
tabel_simulasi = pd.DataFrame({
    "Hari ke-": np.arange(1, 31),
    "Jumlah Cacat": simulasi_cacat
})
print("\nData Simulasi:")
print(tabel_simulasi.to_string(index=False))

# 5. Visualisasi histogram hasil
plt.figure(figsize=(10, 6))
sns.histplot(simulasi_cacat, bins=range(0, max(simulasi_cacat)+2), kde=False, color='skyblue', edgecolor='black')
plt.axvline(lambda_defect, color='red', linestyle='--', label=f'λ Teoritis = {lambda_defect}')
plt.axvline(rata2_simulasi, color='green', linestyle='--', label=f'Rata-rata Simulasi = {rata2_simulasi:.2f}')
plt.title('Histogram Jumlah Barang Cacat per Hari (Distribusi Poisson)')
plt.xlabel('Jumlah Cacat')
plt.ylabel('Frekuensi')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
