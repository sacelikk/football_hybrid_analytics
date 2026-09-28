import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Genişletilmiş ve Bölge Ağırlıklı Avusturya Bundesliga Veri Seti
# Att_3rd: Hücum bölgesi presi, Mid_3rd: Orta saha presi, Turnovers: Top kazanımı,
# Succ_Rate: Presin başarı yüzdesi (%), HIR_Index: Yüksek şiddetli koşu yükü (1-10)
players_data = [
    {"Player": "Matthias Seidl", "Team": "SK Rapid Wien", "Pos": "Attacking Mid", "Att_3rd": 11.2, "Mid_3rd": 11.4, "Turnovers": 3.4, "Succ_Rate": 34.5, "HIR_Index": 8.5},
    {"Player": "Guido Burgstaller", "Team": "SK Rapid Wien", "Pos": "Striker", "Att_3rd": 13.8, "Mid_3rd": 4.6, "Turnovers": 2.8, "Succ_Rate": 32.0, "HIR_Index": 7.2},
    {"Player": "Dion Beljo", "Team": "SK Rapid Wien", "Pos": "Striker", "Att_3rd": 9.5, "Mid_3rd": 4.6, "Turnovers": 1.6, "Succ_Rate": 26.5, "HIR_Index": 6.1},
    {"Player": "Mika Biereth", "Team": "Sturm Graz", "Pos": "Striker", "Att_3rd": 14.2, "Mid_3rd": 6.8, "Turnovers": 3.1, "Succ_Rate": 33.2, "HIR_Index": 8.0},
    {"Player": "William Böving", "Team": "Sturm Graz", "Pos": "Winger", "Att_3rd": 10.1, "Mid_3rd": 7.8, "Turnovers": 2.4, "Succ_Rate": 29.8, "HIR_Index": 7.4},
    {"Player": "Karim Konate", "Team": "RB Salzburg", "Pos": "Striker", "Att_3rd": 13.0, "Mid_3rd": 6.5, "Turnovers": 2.9, "Succ_Rate": 31.5, "HIR_Index": 8.1},
    {"Player": "Oscar Gloukh", "Team": "RB Salzburg", "Pos": "Attacking Mid", "Att_3rd": 8.4, "Mid_3rd": 8.4, "Turnovers": 2.2, "Succ_Rate": 30.1, "HIR_Index": 7.0},
    {"Player": "Dominik Fitz", "Team": "Austria Wien", "Pos": "Playmaker", "Att_3rd": 5.2, "Mid_3rd": 8.3, "Turnovers": 1.5, "Succ_Rate": 24.0, "HIR_Index": 5.8},
    {"Player": "Andreas Gruber", "Team": "Austria Wien", "Pos": "Winger", "Att_3rd": 8.6, "Mid_3rd": 6.6, "Turnovers": 1.9, "Succ_Rate": 27.5, "HIR_Index": 6.5},
    {"Player": "Marin Ljubicic", "Team": "LASK", "Pos": "Striker", "Att_3rd": 10.8, "Mid_3rd": 5.7, "Turnovers": 2.1, "Succ_Rate": 28.0, "HIR_Index": 7.3},
    {"Player": "Thierno Ballo", "Team": "Wolfsberger AC", "Pos": "Winger", "Att_3rd": 9.9, "Mid_3rd": 8.9, "Turnovers": 2.7, "Succ_Rate": 31.0, "HIR_Index": 7.6}
]

df = pd.DataFrame(players_data)

# 2. Gelişmiş Taktik Hibrit Formülü
# Rakip 3. bölge presine x1.8 ağırlık, kazanılan toplara x3.0 ağırlık, başarı yüzdesi çarpanı
df["Tactical_Output"] = (df["Att_3rd"] * 1.8) + (df["Mid_3rd"] * 1.0) + (df["Turnovers"] * 3.0)
df["Advanced_HPE"] = ((df["Tactical_Output"] / df["HIR_Index"]) * (df["Succ_Rate"] / 100.0) * 10).round(2)

df = df.sort_values(by="Advanced_HPE", ascending=False).reset_index(drop=True)

# 3. İki Boyutlu Taktik Karar Matrisi Grafiği
fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
ax.set_facecolor("#121212")
fig.patch.set_facecolor("#121212")

# Takım Renk Kodlaması
color_map = {
    "SK Rapid Wien": "#008837",
    "Sturm Graz": "#ffffff",
    "RB Salzburg": "#d90429",
    "Austria Wien": "#7b2cbf",
    "LASK": "#ffb703",
    "Wolfsberger AC": "#48cae4"
}

for _, row in df.iterrows():
    ax.scatter(
        row["HIR_Index"], 
        row["Tactical_Output"],
        s=row["Advanced_HPE"] * 180,
        color=color_map.get(row["Team"], "#aaaaaa"),
        alpha=0.85,
        edgecolors="#ffffff",
        linewidth=1.2
    )
    # Oyuncu İsimleri ve HPE Skoru
    ax.annotate(
        f"{row['Player']}\n({row['Advanced_HPE']})",
        (row["HIR_Index"], row["Tactical_Output"]),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=8.5,
        fontweight="bold",
        color="#ffffff"
    )

# Kadran Çizgileri (Ortalama Ayırıcılar)
mean_hir = df["HIR_Index"].mean()
mean_tactical = df["Tactical_Output"].mean()

ax.axvline(mean_hir, color="#555555", linestyle="--", linewidth=1)
ax.axhline(mean_tactical, color="#555555", linestyle="--", linewidth=1)

# Kadran Açıklamaları
ax.text(9.0, mean_tactical + 6, "YÜKSEK FİZİKSEL EFOR &\nYÜKSEK TAKTİK TEHLİKE\n(Elit Presçiler)", 
        color="#00ff88", fontsize=8.5, fontweight="bold", ha="center")
ax.text(5.8, mean_tactical + 6, "DÜŞÜK EFOR &\nYÜKSEK TAKTİK VERİM\n(Akıllı / Pozisyonel)", 
        color="#00e5ff", fontsize=8.5, fontweight="bold", ha="center")
ax.text(9.0, mean_tactical - 8, "VERİMSİZ KOŞUCULAR\n(Yüksek Efor / Düşük Çıktı)", 
        color="#ff595e", fontsize=8.5, fontweight="bold", ha="center")

ax.set_title("Austrian Bundesliga: Advanced Hybrid Pressing Matrix", fontsize=13, fontweight="bold", color="#ffffff", pad=15)
ax.set_xlabel("High-Intensity Running Index (Physical Load)", fontsize=10, fontweight="bold", color="#dddddd")
ax.set_ylabel("Weighted Tactical Output (Attacking 3rd Pressures & Turnovers)", fontsize=10, fontweight="bold", color="#dddddd")
ax.tick_params(colors="#cccccc")
ax.grid(True, linestyle=":", alpha=0.3, color="#777777")

plt.tight_layout()
plt.savefig("austrian_bundesliga_advanced_matrix.png")
print("Gelişmiş analiz tamamlandı: 'austrian_bundesliga_advanced_matrix.png'")