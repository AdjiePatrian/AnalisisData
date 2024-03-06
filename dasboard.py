import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_weather_rentals(df):
    Weather_rentals=df.groupby("weather").agg({
        "casual": "sum",
        "registered": "sum",
        "RealTemp": "mean",
        "cnt": "sum"
    }).sort_values(by="cnt", ascending=False)
    return Weather_rentals

def create_season_rentals(df):
    season_rentals=df.groupby("seasonName").agg({
    "casual": "sum",
    "registered": "sum",
    "RealTemp": "mean",
    "cnt": "sum"
    }).sort_values(by='cnt', ascending=False)
    return season_rentals

def create_rentals_by_month(dataframe):
    # Memilih data berdasarkan rentang tahun
    #filtered_df = dataframe[(dataframe['dteday'].dt.year >= start_year) & (dataframe['dteday'].dt.year <= end_year)]
    day_df_2011 = dataframe[dataframe['dteday'].dt.year == 2011]
    day_df_2012 = dataframe[dataframe['dteday'].dt.year == 2012]
    # Menghitung jumlah penggunaan sepeda per bulan
    monthly_orders_df_2011 = day_df_2011.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
    })
    monthly_orders_df_2012 = day_df_2012.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
    })

    # Mengubah format index menjadi string '%B' (nama bulan)
    monthly_orders_df_2011.index = monthly_orders_df_2011.index.strftime('%B')

    return monthly_orders_df_2011, monthly_orders_df_2012

def weather_and_cnt(dataframe,rental):
    hour_df_2011 = dataframe[dataframe['dteday'].dt.year == 2011]
    hour_df_2012 = dataframe[dataframe['dteday'].dt.year == 2012]

    # Menghitung jumlah penggunaan sepeda per kategori cuaca untuk tahun 2011 dan 2012
    monthly_orders_weather_df_2011 = hour_df_2011.groupby(['weather'])[rental].sum()
    monthly_orders_weather_df_2012 = hour_df_2012.groupby(['weather'])[rental].sum()

    # Menggabungkan data ke dalam satu dataframe
    monthly_orders_weather_df = pd.concat([monthly_orders_weather_df_2011, monthly_orders_weather_df_2012], axis=1)
    monthly_orders_weather_df.columns = ['2011', '2012']  # Mengubah nama kolom
    return monthly_orders_weather_df

def season_and_cnt(dataframe,rental):
    hour_df_2011 = dataframe[dataframe['dteday'].dt.year == 2011]
    hour_df_2012 = dataframe[dataframe['dteday'].dt.year == 2012]

    # Menghitung jumlah penggunaan sepeda per kategori cuaca untuk tahun 2011 dan 2012
    monthly_orders_weather_df_2011 = hour_df_2011.groupby(['seasonName'])[rental].sum()
    monthly_orders_weather_df_2012 = hour_df_2012.groupby(['seasonName'])[rental].sum()

    # Menggabungkan data ke dalam satu dataframe
    monthly_orders_weather_df = pd.concat([monthly_orders_weather_df_2011, monthly_orders_weather_df_2012], axis=1)
    monthly_orders_weather_df.columns = ['2011', '2012']  # Mengubah nama kolom
    return monthly_orders_weather_df

day_df = pd.read_csv("day_clean.csv")
hour_df = pd.read_csv("hour_clean.csv")   


datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])


min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("1.png")
    
    # Mengambil start_date & end_date dari date_input
    #start_date, end_date = st.date_input(
        #label='Rentang Waktu',min_value=min_date,
        #max_value=max_date,
        #value=[min_date, max_date]
    #)
mainDay_df =day_df
mainHour_df = hour_df


rentals_by_month_2011, rentals_by_month_2012 = create_rentals_by_month(mainDay_df)
weather_cnt_casual=weather_and_cnt(mainHour_df,'casual')
weather_cnt_registered=weather_and_cnt(mainHour_df,'registered')
weather_cnt=weather_and_cnt(mainHour_df,'cnt')
season_cnt_casual=season_and_cnt(mainDay_df,'casual')
season_cnt_registered=season_and_cnt(mainDay_df,'registered')


st.header('Adjie: Bike Sharing Dasboard')

st.subheader('Rental Data')

col1, col2 = st.columns(2)

with col1:
    total_orders_2011 = mainDay_df[mainDay_df['dteday'].dt.year == 2011]['cnt'].sum()
    st.metric("Total rentals 2011", value=total_orders_2011)
 
with col2:
    total_orders_2011 = mainDay_df[mainDay_df['dteday'].dt.year == 2012]['cnt'].sum()
    st.metric("Total rentals 2012", value=total_orders_2011)

fig, ax=plt.subplots(figsize=(30,20))

ax.plot(
    rentals_by_month_2011.index,
    rentals_by_month_2011["cnt"],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax.plot(
    rentals_by_month_2011.index,
    rentals_by_month_2012["cnt"],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=20)
 
st.pyplot(fig)

st.subheader("Hubungan Weather dengan Banyak Rental")

fig, ax=plt.subplots(figsize=(30,20))
ax.set_title("Total Rental dan Weather", loc="center", fontsize=50)
ax.plot(
    weather_cnt.index,
    weather_cnt["2011"],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax.plot(
    weather_cnt.index,
    weather_cnt["2012"],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 20))

# Grafik untuk weather_cnt_casual
ax[0].plot(
    weather_cnt_casual.index,
    weather_cnt_casual['2011'],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax[0].set_title('Casual Rentals', fontsize=25)
ax[0].tick_params(axis='y', labelsize=25)
ax[0].tick_params(axis='x', labelsize=20)
ax[0].legend()
ax[0].set_ylim(0,700000)

# Grafik untuk weather_cnt_registered
ax[1].plot(
    weather_cnt_registered.index,
    weather_cnt_registered['2011'],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax[1].set_title('Registered Rentals', fontsize=25)
ax[1].tick_params(axis='y', labelsize=25)
ax[1].tick_params(axis='x', labelsize=20)
ax[1].legend()
ax[1].set_ylim(0,700000)

# Menampilkan subplot menggunakan Streamlit
st.pyplot(fig)

st.subheader("Hubungan Seaason dengan Banyak Rental")

fig, ax=plt.subplots(figsize=(30,20))
ax.set_title("Total Rental(Casual) dan Season", loc="center", fontsize=50)
ax.plot(
    season_cnt_casual.index,
    season_cnt_casual["2011"],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax.plot(
    season_cnt_casual.index,
    season_cnt_casual["2012"],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)
fig, ax=plt.subplots(figsize=(30,20))
ax.set_title("Total Rental(Registered) dan Season", loc="center", fontsize=50)
ax.plot(
    season_cnt_registered.index,
    season_cnt_registered["2011"],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax.plot(
    season_cnt_registered.index,
    season_cnt_registered["2012"],
    marker='o',
    linewidth=2,
    color="#72BCD4",
    label="2011"
)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)