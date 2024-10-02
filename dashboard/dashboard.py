import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk membuat plot dari tren PM10 di setiap wilayah
def plot_pm10_trend(df, wilayah):
    monthly_pm10 = df.groupby([df['datetime'].dt.to_period('M'), 'station'])['PM10'].mean().unstack()
    plt.figure(figsize=(10, 6))
    if wilayah == 'Keseluruhan Wilayah':
        monthly_pm10.plot(marker='o')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        monthly_pm10[wilayah].plot(marker='o', label=wilayah)
        plt.legend(loc='upper left')
    plt.title(f'Tren Rata-rata PM10 di {wilayah}')
    plt.xlabel('Waktu')
    plt.ylabel('Rata-rata PM10 (µg/m³)')
    plt.grid(True)
    st.pyplot(plt)

# Fungsi untuk membuat plot dari konsentrasi PM10 berdasarkan jam
def plot_pm10_hourly(df, wilayah):
    hourly_pm10 = df.groupby(['hour', 'station'])['PM10'].mean().unstack()
    plt.figure(figsize=(10, 6))
    if wilayah == 'Keseluruhan Wilayah':
        hourly_pm10.plot(marker='o')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        hourly_pm10[wilayah].plot(marker='o', label=wilayah)
        plt.legend(loc='upper left')
    plt.title(f'Rata-rata Konsentrasi PM10 Berdasarkan Jam di {wilayah}')
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Rata-rata PM10 (µg/m³)')
    plt.grid(True)
    st.pyplot(plt)

# Load data yang sudah dibersihkan
df = pd.read_csv("dashboard/main_data.csv")
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

# Judul untuk dashboard
st.title("Dashboard Polusi Udara PM10")

# Membuat dua bagian untuk masing-masing pertanyaan
option = st.selectbox(
    'Pilih Bagian:',
    ('Tren PM10 Berdasarkan Wilayah (2013-2017)', 'Konsentrasi PM10 Berdasarkan Jam di Setiap Wilayah')
)

# List nama wilayah untuk tabs
wilayah_list = ['Keseluruhan Wilayah', 'Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 
                'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 
                'Wanliu', 'Wanshouxigong']

# Menampilkan tabs untuk setiap wilayah
if option == 'Tren PM10 Berdasarkan Wilayah (2013-2017)':
    tabs = st.tabs(wilayah_list)
    for i, wilayah in enumerate(wilayah_list):
        with tabs[i]:
            st.header(f'Tren PM10 di {wilayah}')
            plot_pm10_trend(df, wilayah)
            
elif option == 'Konsentrasi PM10 Berdasarkan Jam di Setiap Wilayah':
    tabs = st.tabs(wilayah_list)
    for i, wilayah in enumerate(wilayah_list):
        with tabs[i]:
            st.header(f'Konsentrasi PM10 di {wilayah} Berdasarkan Jam')
            plot_pm10_hourly(df, wilayah)
