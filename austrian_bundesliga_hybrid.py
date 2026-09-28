import pandas as pd
import matplotlib.pyplot as plt

# 1. Avusturya Bundesliga Hücum/Kanat/Ofansif Orta Saha Veri Seti
# Metrikler: 90 dk başına pres hacmi, top kazanımı ve yüksek şiddetli efor yükü
data = [
    {"Player": "Guido Burgstaller", "Team": "SK Rapid Wien", "Pos": "FW", "Pressures_P90": 18.4, "Turnovers_P90": 2.8, "High_Intensity_Load": 7.2},
    {"Player": "Dion Beljo", "Team": "SK Rapid Wien", "Pos": "FW", "Pressures_P90": 14.1, "Turnovers_P90": 1.6, "High_Intensity_Load": 6.1},
    {"Player": "Matthias Seidl", "Team": "SK Rapid Wien", "Pos": "AM", "Pressures_P90": 22.6, "Turnovers_P90": 3.4, "High_Intensity_Load": 8.5},
    {"Player": "Oscar Gloukh", "Team": "RB Salzburg", "Pos": "AM", "Pressures_P90": 16.8, "Turnovers_P90": 2.2, "High_Intensity_Load": 7.0},
    {"Player": "Karim Konate", "Team": "RB Salzburg", "Pos": "FW", "Pressures_P90": 19.5, "Turnovers_P90": 2.9, "High_Intensity_Load": 8.1},
    {"Player": "Mika Biereth", "Team": "Sturm Graz", "Pos": "FW", "Pressures_P90": 21.0, "Turnovers_P90": 3.1, "High_Intensity_Load": 8.0},
    {"Player": "William Böving", "Team": "Sturm Graz", "Pos": "LW", "Pressures_P90": 17.9, "Turnovers_P90": 2.4, "High_Intensity_Load": 7.4},
    {"Player": "Dominik Fitz", "Team": "Austria Wien", "Pos": "AM", "Pressures_P90": 13.5, "Turnovers_P90": 1.5, "High_Intensity_Load": 5.8},
    {"Player": "Andreas Gruber", "Team": "Austria Wien", "Pos": "RW", "Pressures_P90": 15.2, "Turnovers_P90": 1.9, "High_Intensity_Load": 6.5},
    {"Player": "Robert Zulj", "Team": "LASK", "Pos": "AM", "Pressures_P90": 12.8, "Turnovers_P90": 1.4, "High_Intensity_Load": 5.2},
    {"Player": "Marin Ljubicic", "Team": "LASK", "Pos": "FW", "Pressures_P90": 16.5, "Turnovers_P90": 2.1, "High_Intensity_Load": 7.3},
    {"Player": "Thierno Ballo", "Team": "Wolfsberger AC", "Pos": "LW", "Pressures_P90": 18.8, "Turnovers_P90": 2.7, "High_Intensity_Load": 7.6}
]

df = pd.DataFrame(data)

# 2. Daniel Schmitt Hibrit KPI Hesaplaması
# (Pres Hacmi + Kazanılan Top Değeri) / Fiziksel Yük Endeksi
df["Hybrid_Press_Index"] = (
    (df["Pressures_P90"] * 1.0 + df["Turnovers_P90"] * 2.5) / df["High_Intensity_Load"]
).round(2)

# Sıralama
df = df.sort_values(by="Hybrid_Press_Index", ascending=False).reset_index(drop=True)

# 3. Görselleştirme: Kulüp Analiz Paneli
plt.figure(figsize=(11, 6), dpi=300)
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

colors = []
for team in df["Team"]:
    if "Rapid" in team:
        colors.append("#1b5e20")  # Yeşil (Rapid Wien)
    elif "Salzburg" in team:
        colors.append("#d32f2f")  # Kırmızı (RB Salzburg)
    elif "Sturm" in team:
        colors.append("#212121")  # Siyah (Sturm Graz)
    elif "Austria Wien" in team:
        colors.append("#4a148c")  # Mor (Austria Wien)
    else:
        colors.append("#757575")

bars = plt.barh(df["Player"] + " (" + df["Team"] + ")", df["Hybrid_Press_Index"], color=colors, edgecolor="black", alpha=0.85)

# Çubukların üstüne değerleri yazdır
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.05, bar.get_y() + bar.get_height() / 2, f"{width:.2f}",
             va="center", ha="left", fontsize=9, fontweight="bold")

plt.title("Austrian Bundesliga: Hybrid Pressing Efficiency Index (Physical vs. Defensive Action)", 
          fontsize=12, fontweight="bold", pad=15)
plt.xlabel("Hybrid Score = (Pressures + 2.5 * Turnovers) / Physical Load", fontsize=10, fontweight="bold")
plt.xlim(0, max(df["Hybrid_Press_Index"]) + 0.6)
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig("austrian_bundesliga_hybrid_kpi.png")
print("Analiz tamamlandı. 'austrian_bundesliga_hybrid_kpi.png' oluşturuldu.")

# Terminal Çıktısı Tablosu
print("\n" + "="*70)
print(f"{'Oyuncu':<20} {'Takım':<18} {'Pres/90':<10} {'Fiziksel Yük':<14} {'Hibrit Skor':<10}")
print("="*70)
for _, r in df.iterrows():
    print(f"{r['Player']:<20} {r['Team']:<18} {r['Pressures_P90']:<10} {r['High_Intensity_Load']:<14} {r['Hybrid_Press_Index']:<10}")
print("="*70)