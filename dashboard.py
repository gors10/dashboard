import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st 
from babel.numbers import format_currency
sns.set(style='dark')

def create_monthly_price_df(df):
    monthly_price_df = df.resample(rule='M', on='order_approved_at').agg({
        "price_y": ["min", "max"]
    })
    monthly_price_df = monthly_price_df.reset_index()
    monthly_price_df.columns = ['order_approved_at', 'min_price', 'max_price']
    
    return monthly_price_df

def summarize_transactions_by_state(df):
    result = df.groupby("customer_state").agg({
        "order_id": "nunique",
        "order_approved_at": "count"
    })
    result.columns = ['unique_orders', 'total_transactions']
    return result

all_df = pd.read_csv("all_data.csv")

all_df["order_approved_at"] = pd.to_datetime(all_df["order_approved_at"])


datetime_columns = ["order_approved_at"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("bike.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                (all_df["order_approved_at"] <= str(end_date))]
st.header('Bike Collection Dashboard: ')

monthly_price_df = create_monthly_price_df(main_df)

# Plot harga bulanan menggunakan matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_price_df['order_approved_at'], monthly_price_df['min_price'], marker='o', label='Harga Minimum')
ax.plot(monthly_price_df['order_approved_at'], monthly_price_df['max_price'], marker='o', label='Harga Maksimum')
ax.set_xlabel('Bulan')
ax.set_ylabel('Harga')
ax.set_title('Ringkasan Harga Bulanan')
ax.legend()
ax.tick_params(axis='x', rotation=45)

# Menampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

# Memanggil fungsi summarize_transactions_by_state untuk membuat ringkasan transaksi berdasarkan negara bagian
transaction_summary_df = summarize_transactions_by_state(main_df)

# Membuat plot menggunakan matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
transaction_summary_df.plot(kind='bar', ax=ax)
ax.set_xlabel('Negara Bagian')
ax.set_ylabel('Jumlah')
ax.set_title('Ringkasan Transaksi per Negara Bagian')
ax.legend(["Jumlah Pesanan", "Jumlah Transaksi"], loc='upper right')
ax.tick_params(axis='x', rotation=45)

# Menampilkan plot menggunakan st.pyplot()
st.pyplot(fig)