import numpy as np
import matplotlib.pyplot as plt

# Karşılaştırılacak Metrikler
categories = [
    'Attacking 3rd Press', 
    'Midfield Press', 
    'Turnovers Won', 
    'Success Rate (%)', 
    'Physical Load (HIR)'
]
N = len(categories)

# Oyuncu Değerleri (Normalize edilmiş / Gerçek değerler)
# Seidl: Genç, aşırı enerjik, her yerde basan orta saha
seidl_values = [11.2, 11.4, 3.4, 34.5, 8.5]
# Burgstaller: Ceza sahası çevresinde akıllı basan santrafor
burgstaller_values = [13.8, 4.6, 2.8, 32.0, 7.2]

# Skala uyumu için değerleri 0-100 arasına ölçekle (Max referanslar üzerinden)
max_vals = [15.0, 15.0, 4.0, 40.0, 10.0]
seidl_scaled = [v / m * 100 for v, m in zip(seidl_values, max_vals)]
burgstaller_scaled = [v / m * 100 for v, m in zip(burgstaller_values, max_vals)]

# Daireyi kapatmak için ilk değeri sona ekle
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]
seidl_scaled += seidl_scaled[:1]
burgstaller_scaled += burgstaller_scaled[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)
fig.patch.set_facecolor('#121212')
ax.set_facecolor('#1a1a1a')

# Eksen Çizgileri ve Etiketler
plt.xticks(angles[:-1], categories, color='#ffffff', size=9, weight='bold')
ax.tick_params(colors='#888888')
ax.spines['polar'].set_color('#444444')
ax.grid(color='#444444', linestyle='--', alpha=0.7)

# Matthias Seidl Çizimi (Yeşil)
ax.plot(angles, seidl_scaled, linewidth=2, linestyle='solid', color='#00ff88', label='Matthias Seidl (Rapid Wien)')
ax.fill(angles, seidl_scaled, color='#00ff88', alpha=0.25)

# Guido Burgstaller Çizimi (Turuncu/Altın)
ax.plot(angles, burgstaller_scaled, linewidth=2, linestyle='solid', color='#ffaa00', label='Guido Burgstaller (Rapid Wien)')
ax.fill(angles, burgstaller_scaled, color='#ffaa00', alpha=0.25)

plt.title("SK Rapid Wien: Pressing Archetype Comparison\n(High-Volume Midfielder vs. Clinical Forward)", 
          size=12, color='#ffffff', weight='bold', pad=25)
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), facecolor='#222222', edgecolor='none', labelcolor='#ffffff')

plt.tight_layout()
plt.savefig("rapid_wien_radar_comparison.png")
print("Radar analizi hazır: 'rapid_wien_radar_comparison.png'")