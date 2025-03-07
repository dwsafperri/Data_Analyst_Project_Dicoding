import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# load dataset
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  
data_path = os.path.join(base_path, "data")

# path lengkap ke file CSV
path_day = os.path.join(data_path, "day.csv")
path_hour = os.path.join(data_path, "hour.csv")

day_df = pd.read_csv(path_day)
hour_df = pd.read_csv(path_hour)

# konversi tanggal ke format datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# menghitung total peminjaman per hari
daily_rentals = day_df[["dteday", "cnt"]]

# menghitung rata-rata peminjaman per jam
hourly_avg = hour_df.groupby("hr")["cnt"].mean().reset_index()

# menghitung rata-rata penyewaan berdasarkan hari kerja dan hari libur
workday_avg = day_df.groupby("workingday")["cnt"].mean()
holiday_avg = day_df.groupby("holiday")["cnt"].mean()

# menghitung ringkasan data hourly untuk dibandingkan dengan data harian
hourly_summary = hour_df.groupby("dteday").agg({
    "cnt": "sum",
    "casual": "sum",
    "registered": "sum",
    "temp": "mean",
    "atemp": "mean",
    "hum": "mean",
    "windspeed": "mean"
}).reset_index()

# menggabungkan dataset day.csv dengan ringkasan data dari hour.csv berdasarkan dteday
merged_df = pd.merge(day_df, hourly_summary, on="dteday", suffixes=("_day", "_hour"))

def main():
    st.title("🚲 Dashboard Peminjaman Sepeda")
    st.markdown("### Analisis Data Peminjaman Sepeda 🚲")
    st.write("Dashboard ini menyajikan berbagai visualisasi untuk memahami pola peminjaman sepeda berdasarkan waktu dan kondisi lingkungan.")
    
    # ringkasan Data
    st.subheader("📊 Ringkasan Peminjaman Sepeda")
    col1, col2 = st.columns(2)
    col1.metric("Total Hari", f"{daily_rentals.shape[0]} hari")
    col2.metric("Total Peminjaman", f"{daily_rentals['cnt'].sum()} sepeda")
        
    # tren Peminjaman Sepeda Bulanan
    st.subheader("📆 Tren Peminjaman Sepeda per Bulan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x="mnth", y="cnt", data=hour_df, marker="o")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax.set_title("Tren Rental Sepeda per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Rental Sepeda")
    st.pyplot(fig)

    # perbandingan penyewaan sepeda pada hari kerja dan hari libur
    st.subheader("📆 Perbandingan Penyewaan Sepeda: Hari Kerja vs Hari Libur")
    workday_avg = day_df.groupby("workingday")["cnt"].mean()
    holiday_avg = day_df.groupby("holiday")["cnt"].mean()
    
    st.write(f"Rata-rata penyewaan sepeda pada hari kerja: {workday_avg[1]:.2f}")
    st.write(f"Rata-rata penyewaan sepeda pada hari libur: {holiday_avg[1]:.2f}")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x="workingday", y="cnt", data=day_df, hue="workingday", palette="coolwarm")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Hari libur", "Hari kerja"])
    ax.set_title("Perbandingan Jumlah Penyewaan Sepeda antara Hari Kerja dan Hari Libur")
    ax.set_xlabel("Kategori hari")
    ax.set_ylabel("Jumlah penyewaan sepeda")
    st.pyplot(fig)
    
    # hubungan antara suhu dan jumlah rental
    st.subheader("🌡️ Hubungan Suhu dan Jumlah Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(x="temp", y="cnt", data=day_df, scatter_kws={"alpha": 0.5, "color": "royalblue"}, line_kws={"color": "red"})
    ax.set_title("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda")
    ax.set_xlabel("Suhu (Normalized)")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(fig)
    
    # peminjaman berdasarkan musim
    st.subheader("🌦️ Peminjaman Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(x=day_df["season"], y=day_df["cnt"], palette="Set2")
    ax.set_title("Distribusi Peminjaman Sepeda Berdasarkan Musim")
    ax.set_xlabel("Musim (1: Semi, 2: Panas, 3: Gugur, 4: Dingin)")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)

    # visualisasi rata-rata rental sepeda per jam
    st.subheader("⏰ Rata-rata Rental Sepeda per Jam dalam Sehari")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x="hr", y="cnt", data=hour_df, estimator="mean", errorbar=None, marker="o")
    ax.set_title("Rata-rata Rental Sepeda Per Jam dalam Sehari")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah rental sepeda")
    st.pyplot(fig)
    
    # scatter plot hubungan faktor lingkungan dan peminjaman sepeda
    st.subheader("🌍 Hubungan faktor lingkungan dengan peminjaman sepeda")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    sns.regplot(ax=axes[0, 0], x=merged_df["temp_day"], y=merged_df["cnt_day"], scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
    axes[0, 0].set_title("pengaruh suhu terhadap peminjaman sepeda")
    
    sns.regplot(ax=axes[0, 1], x=merged_df["atemp_day"], y=merged_df["cnt_day"], scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
    axes[0, 1].set_title("pengaruh suhu terasa terhadap peminjaman sepeda")
    
    sns.regplot(ax=axes[1, 0], x=merged_df["hum_day"], y=merged_df["cnt_day"], scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
    axes[1, 0].set_title("pengaruh kelembaban terhadap peminjaman sepeda")
    
    sns.regplot(ax=axes[1, 1], x=merged_df["windspeed_day"], y=merged_df["cnt_day"], scatter_kws={"alpha": 0.5}, line_kws={"color": "red"})
    axes[1, 1].set_title("pengaruh kecepatan angin terhadap peminjaman sepeda")
    
    for ax in axes.flat:
        ax.set_xlabel("Nilai faktor lingkungan")
        ax.set_ylabel("Jumlah peminjaman sepeda")
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("Terima kasih sudah menggunakan dashboard ini! 🚴‍♂️💨")
    st.markdown("© Made by Dewi Safira Permata Sari")
    
if __name__ == "__main__":
    main()