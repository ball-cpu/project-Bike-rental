import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# set style seaborn
sns.set(style="dark")


# Membuat Helper function
def create_daily_df(df):
    daily_df = df.groupby(by="dteday").agg({"cnt": "sum"}).reset_index()
    return daily_df


def create_users_df(df):
    total_casual_users = df["casual"].sum()
    total_registered_users = df["registered"].sum()

    user_type_df = {
        "Type of Users": ["Casual Users", "Registered Users"],
        "Users Total": [total_casual_users, total_registered_users],
    }
    return user_type_df


def create_year_df(df):
    year_df = df.groupby(by="yr").agg({"cnt": "sum"}).reset_index()
    return year_df


def create_season_df(df):
    season_df = df.groupby(by="season").agg({"cnt": "sum"}).reset_index()
    return season_df


def create_monthly_df(df):
    monthly_df = df.groupby(by="mnth").agg({"cnt": "sum"}).reset_index()
    return monthly_df


def create_weather_df(df):
    weather_df = df.groupby(by="weathersit").agg({"cnt": "sum"}).reset_index()
    return weather_df


# Nah, setelah menyiapkan beberapa helper function tersebut, tahap berikutnya ialah load berkas
all_df = pd.read_csv("days_df.csv")

# membuat komponen date
min_date = pd.to_datetime(all_df["dteday"]).dt.date.min()
max_date = pd.to_datetime(all_df["dteday"]).dt.date.max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image(
        "https://www.shutterstock.com/image-vector/bike-rental-vintage-logo-design-600w-1391655131.jpg"
    )

    # Mengambil start_date & end_date dari date_input

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

# Nah, start_date dan end_date di atas akan digunakan untuk memfilter all_df. Data yang telah difilter ini selanjutnya akan disimpan dalam main_df. Proses ini dijalankan menggunakan kode berikut.
main_df = all_df[
    (all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))
]


# DataFrame yang telah difilter (main_df) inilah yang digunakan untuk menghasilkan berbagai DataFrame yang dibutuhkan untuk membuat visualisasi data. Proses ini tentunya dilakukan dengan memanggil helper function yang telah kita buat sebelumnya.
daily_df = create_daily_df(main_df)
user_type_df = create_users_df(main_df)
year_df = create_year_df(main_df)
season_df = create_season_df(main_df)
monthly_df = create_monthly_df(main_df)
weather_df = create_weather_df(main_df)

# Oke, setelah membuat filter dan menyiapkan seluruh DataFrame yang dibutuhkan, kini saatnya kita melengkapi dashboard tersebut dengan berbagai visualisasi data. Pada bagian awal, kita perlu menambahkan header pada dashboard tersebut. Berikut merupakan kode untuk melakukannya
st.header("Bike Rental Company 🚲")


st.subheader("Daily rentals")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Casual Users", value=int(main_df["casual"].sum()))
with col2:
    st.metric("Registered Users", value=int(main_df["registered"].sum()))
with col3:
    st.metric("Total Users", value=int(main_df["cnt"].sum()))


st.subheader("Rental Analysis")
# Berdasarkan cuaca
st.subheader("Based on weather")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="weathersit", y="cnt", data=weather_df, palette="viridis", ax=ax)
ax.set_title("Total Bike Rentals by Weather Condition")
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# berdasarkan season
st.subheader("Based on season")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="season", y="cnt", data=season_df, palette="viridis", ax=ax)
ax.set_title("Total Bike Rentals by Season")
ax.set_xlabel("Season")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# berdasarkan suhu dan kelembapan
st.subheader("Based on temperature and humidity")
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 15))

# berdasarkan suhu
sns.scatterplot(x="temp", y="cnt", data=main_df, ax=axes[0])
axes[0].set_title("Bike Rentals Distribution by Temperature")
axes[0].set_xlabel("Temperature")
axes[0].set_ylabel("Total Rentals")

# berdasarkan kelembapan
sns.scatterplot(x="hum", y="cnt", data=main_df, ax=axes[1])
axes[1].set_title("Bike Rentals Distribution by Humidity")
axes[1].set_xlabel("Humidity")
axes[1].set_ylabel("Total Rentals")

# pengelompokkan suhu dan kelembapan
main_df["temp_group"] = pd.cut(
    main_df["temp"],
    bins=5,
    labels=["sangat dingin", "dingin", "sedang", "panas", "sangat panas"],
)
main_df["hum_group"] = pd.cut(
    main_df["hum"],
    bins=5,
    labels=["sangat rendah", "rendah", "sedang", "tinggi", "sangat tinggi"],
)

sns.barplot(x="temp_group", y="cnt", hue="hum_group", data=main_df, ax=axes[2])
axes[2].set_title("Bike Rentals Distribution by Temperature and Humidity")
axes[2].set_xlabel("Temperature Category")
axes[2].set_ylabel("Total Rentals")
axes[2].legend(title="Humidity Category")

plt.tight_layout()
st.pyplot(fig)

st.caption("Copyright 2024 ©️ 2024 Ball-cpu")
