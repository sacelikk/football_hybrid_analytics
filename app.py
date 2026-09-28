import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Austrian Bundesliga - Pro Tactical KPI Platform",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Austrian Bundesliga: Tactical Hybrid KPI Platform")
st.markdown("Fiziksel yük (HSR) ile taktiksel pres ve top kazanım verimini harmanlayan **Kulüp Düzeyi Karar Destek Paneli**.")

# 1. Veri Okuma ve Genişletilmiş KPI Motoru
@st.cache_data
def load_and_calculate_data():
    csv_file = "austrian_bundesliga_data.csv"
    if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
        default_data = [
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
        df = pd.DataFrame(default_data)
        df.to_csv(csv_file, index=False)
    else:
        df = pd.read_csv(csv_file)

    # Gelişmiş Taktik Çıktı ve HPE
    df["Tactical_Output"] = (df["Att_3rd"] * 1.8) + (df["Mid_3rd"] * 1.0) + (df["Turnovers"] * 3.0)
    df["Advanced_HPE"] = ((df["Tactical_Output"] / df["HIR_Index"]) * (df["Succ_Rate"] / 100.0) * 10).round(2)
    
    # Otomatik Taktik Profil Ataması
    def assign_profile(row):
        if row["Advanced_HPE"] >= 15.0 and row["HIR_Index"] >= 7.5:
            return "Elit Presçi (Yüksek Yoğunluk)"
        elif row["Advanced_HPE"] >= 15.0 and row["HIR_Index"] < 7.5:
            return "Pozisyonel Pres Ustası (Akıllı Efor)"
        elif row["Advanced_HPE"] < 12.0 and row["HIR_Index"] >= 7.0:
            return "Verimsiz Koşucu (Düşük Taktik Çıktı)"
        else:
            return "Standart / Destekleyici Profil"

    df["Tactical_Archetype"] = df.apply(assign_profile, axis=1)
    return df.sort_values(by="Advanced_HPE", ascending=False).reset_index(drop=True)

df = load_and_calculate_data()

# 2. Yan Panel Filtreleri
st.sidebar.header("🔍 Taktik Filtreler")

# Takım Filtresi
available_teams = list(df["Team"].unique())
selected_teams = st.sidebar.multiselect("Takım", available_teams, default=available_teams)

# Pozisyon Filtresi
available_positions = list(df["Pos"].unique())
selected_positions = st.sidebar.multiselect("Pozisyon", available_positions, default=available_positions)

# Min Skor
min_hpe = st.sidebar.slider(
    "Minimum Hibrit Verimlilik Skoru (HPE)", 
    float(df["Advanced_HPE"].min()), 
    float(df["Advanced_HPE"].max()), 
    float(df["Advanced_HPE"].min())
)

filtered_df = df[
    (df["Team"].isin(selected_teams)) & 
    (df["Pos"].isin(selected_positions)) & 
    (df["Advanced_HPE"] >= min_hpe)
]

# 3. Özet Metrik Kartları
st.markdown("### 📌 Lig Genel Görünümü")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Analiz Edilen Oyuncu", len(filtered_df))
m2.metric("En Yüksek HPE Skoru", f"{filtered_df['Advanced_HPE'].max()} ({filtered_df.iloc[0]['Player'] if len(filtered_df) > 0 else '-'})")
m3.metric("Ortalama Pres Başarısı", f"%{filtered_df['Succ_Rate'].mean():.1f}" if len(filtered_df) > 0 else "-")
m4.metric("Ort. Fiziksel Yük (HIR)", f"{filtered_df['HIR_Index'].mean():.1f}" if len(filtered_df) > 0 else "-")

st.divider()

# 4. Görseller: Karar Matrisi ve Karşılaştırma Radarı
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📊 Hibrit Karar Matrisi")
    fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
    ax.set_facecolor("#121212")
    fig.patch.set_facecolor("#121212")
    
    color_map = {
        "SK Rapid Wien": "#008837", "Sturm Graz": "#ffffff", "RB Salzburg": "#d90429",
        "Austria Wien": "#7b2cbf", "LASK": "#ffb703", "Wolfsberger AC": "#48cae4"
    }

    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            ax.scatter(
                row["HIR_Index"], 
                row["Tactical_Output"], 
                s=row["Advanced_HPE"] * 35,
                color=color_map.get(row["Team"], "#aaaaaa"), 
                alpha=0.85, 
                edgecolors="#ffffff"
            )
            ax.annotate(
                f"{row['Player']}\n({row['Advanced_HPE']})", 
                (row["HIR_Index"], row["Tactical_Output"]),
                textcoords="offset points", 
                xytext=(0, 6), 
                ha="center", 
                fontsize=7.5, 
                color="#ffffff"
            )

    ax.set_xlabel("Fiziksel Yük (High-Intensity Running Index)", color="#cccccc", fontsize=8)
    ax.set_ylabel("Ağırlıklı Taktik Çıktı (Pres & Top Kazanımı)", color="#cccccc", fontsize=8)
    ax.tick_params(colors="#888888", labelsize=8)
    ax.grid(True, linestyle=":", alpha=0.3, color="#555555")
    st.pyplot(fig)

with col2:
    st.subheader("🎯 Oyuncu Kıyaslama Radarı")
    player_list = list(df["Player"])
    p1 = st.selectbox("1. Oyuncu:", player_list, index=0)
    p2 = st.selectbox("2. Oyuncu:", player_list, index=1)

    categories = ['Att_3rd Press', 'Midfield Press', 'Turnovers', 'Success Rate', 'HIR Index']
    max_vals = [15.0, 15.0, 4.0, 40.0, 10.0]
    
    r1 = df[df["Player"] == p1].iloc[0]
    r2 = df[df["Player"] == p2].iloc[0]
    
    vals1 = [r1["Att_3rd"], r1["Mid_3rd"], r1["Turnovers"], r1["Succ_Rate"], r1["HIR_Index"]]
    vals2 = [r2["Att_3rd"], r2["Mid_3rd"], r2["Turnovers"], r2["Succ_Rate"], r2["HIR_Index"]]
    
    s1 = [v / m * 100 for v, m in zip(vals1, max_vals)] + [vals1[0] / max_vals[0] * 100]
    s2 = [v / m * 100 for v, m in zip(vals2, max_vals)] + [vals2[0] / max_vals[0] * 100]
    
    angles = [n / float(len(categories)) * 2 * np.pi for n in range(len(categories))] + [0]

    fig_r, ax_r = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True), dpi=150)
    fig_r.patch.set_facecolor('#121212')
    ax_r.set_facecolor('#1a1a1a')
    
    ax_r.plot(angles, s1, linewidth=1.5, color='#00ff88', label=p1)
    ax_r.fill(angles, s1, color='#00ff88', alpha=0.2)
    ax_r.plot(angles, s2, linewidth=1.5, color='#ffaa00', label=p2)
    ax_r.fill(angles, s2, color='#ffaa00', alpha=0.2)
    
    plt.xticks(angles[:-1], categories, color='#ffffff', size=7)
    ax_r.tick_params(colors='#666666')
    ax_r.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), facecolor='#222222', edgecolor='none', labelcolor='#ffffff', fontsize=7)
    st.pyplot(fig_r)

# 5. Oyuncu Detay Kartı (Scout Raporu)
st.subheader(f"🔍 Scout Raporu: {p1}")
c_info1, c_info2 = st.columns([1, 2])
with c_info1:
    st.info(f"**Takım:** {r1['Team']}\n\n**Mevki:** {r1['Pos']}\n\n**Taktiksel Rol:** {r1['Tactical_Archetype']}")
with c_info2:
    st.write(f"- **Hibrit Verimlilik (HPE):** `{r1['Advanced_HPE']}` (Ligde üst sıralarda)")
    st.write(f"- **Top Kazanımı / 90 dk:** `{r1['Turnovers']}` kez doğrudan topu takıma kazandırdı.")
    st.write(f"- **Pres Başarısı:** %`{r1['Succ_Rate']}` pres aksiyonu sonrasında takım 5 sn içinde topa sahip oldu.")

# 6. Tablo ve Dışa Aktarma
st.subheader("📋 Sıralanmış Hibrit Performans Tablosu")
st.dataframe(
    filtered_df[["Player", "Team", "Pos", "Tactical_Archetype", "Advanced_HPE", "Att_3rd", "Mid_3rd", "Turnovers", "Succ_Rate", "HIR_Index"]], 
    use_container_width=True
)

# CSV İndirme Butonu
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Filtrelenmiş Raporu CSV Olarak İndir",
    data=csv_data,
    file_name="bundesliga_hybrid_kpi_report.csv",
    mime="text/csv"
)

st.caption("Veri Altyapısı: Austrian Bundesliga Match Event Data | Metodoloji: Physical-Technical Hybrid Metric Engine")