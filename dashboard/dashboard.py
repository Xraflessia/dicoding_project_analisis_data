import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

day_df = pd.read_csv("https://raw.githubusercontent.com/Xraflessia/dicoding_project_analisis_data/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/Xraflessia/dicoding_project_analisis_data/refs/heads/main/data/hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.title("Dashboard Analisis Penyewaan Sepeda 🚲")

st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Pilih Tanggal Awal", day_df['dteday'].min().date())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", day_df['dteday'].max().date())

filtered_df = day_df[(day_df['dteday'].dt.date >= start_date) & (day_df['dteday'].dt.date <= end_date)]

st.subheader("Total Penyewaan Sepeda Berdasarkan Musim")
fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(data=filtered_df, x="season", y="cnt", estimator=np.sum, hue="season", palette="viridis", legend=False)
ax1.set_xlabel("Musim (1 = Semi, 2 = Panas, 3 = Gugur, 4 = Dingin)")
ax1.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig1)

st.subheader("Rata-rata Penyewaan Sepeda pada Hari Kerja vs Hari Libur")
avg_usage_by_holiday = filtered_df.groupby('holiday')[['cnt']].mean().reset_index()
avg_usage_by_holiday['holiday'] = avg_usage_by_holiday['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})

fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.barplot(x='holiday', y='cnt', data=avg_usage_by_holiday, palette='Set2', ax=ax2)
ax2.set_xlabel("Tipe Hari")
ax2.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig2)

st.subheader("Perbandingan Penyewa Casual vs Terdaftar")
fig3, ax3 = plt.subplots(figsize=(6, 4))
filtered_df[['casual', 'registered']].sum().plot(kind='bar', color=['orange', 'blue'], ax=ax3)
ax3.set_xlabel("Tipe Penyewa")
ax3.set_ylabel("Jumlah Penyewaan")
ax3.set_xticklabels(["Casual", "Registered"], rotation=0)
st.pyplot(fig3)

st.subheader("Tren Penyewaan Sepeda dari Waktu ke Waktu")
fig4, ax4 = plt.subplots(figsize=(12, 5))
sns.lineplot(data=filtered_df, x="dteday", y="cnt", color="purple", ax=ax4)
ax4.set_xlabel("Tanggal")
ax4.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig4)

st.subheader("Korelasi antara Cuaca dan Penyewaan Sepeda")
fig5, ax5 = plt.subplots(figsize=(8, 5))
sns.boxplot(data=filtered_df, x='weathersit', y='cnt', palette='coolwarm', ax=ax5)
ax5.set_xlabel("Kondisi Cuaca (1 = Cerah, 2 = Berawan, 3 = Hujan)")
ax5.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig5)

st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam")
avg_hourly = hour_df.groupby('hr')[['cnt']].mean().reset_index()

fig6, ax6 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=avg_hourly, x='hr', y='cnt', marker='o', color='red', ax=ax6)
ax6.set_xlabel("Jam")
ax6.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig6)

st.subheader("Kesimpulan")
st.markdown("""
- **Musim** memiliki pengaruh besar terhadap jumlah penyewaan sepeda, di mana musim semi memiliki jumlah penyewaan terendah.
- **Hari kerja** memiliki jumlah penyewaan lebih tinggi dibandingkan hari libur, menunjukkan bahwa sepeda sering digunakan untuk transportasi sehari-hari.
- **Penyewa terdaftar** jauh lebih banyak dibandingkan penyewa casual, menandakan pengguna loyal lebih mendominasi.
- **Tren penyewaan** meningkat dari awal 2011 hingga pertengahan 2012, lalu mengalami penurunan pada akhir 2012.
- **Cuaca** yang buruk seperti hujan mengurangi jumlah penyewaan sepeda secara signifikan.
- **Pola penyewaan berdasarkan jam** menunjukkan lonjakan pada pagi dan sore hari, menandakan sepeda banyak digunakan untuk perjalanan kerja.
""")
