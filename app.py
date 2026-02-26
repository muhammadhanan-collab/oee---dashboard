import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Analisis Kinerja Produksi lini Spinning Continuous PT Indonesia Toray Synthetics Berbasis OEE")

tab1, tab2 = st.tabs(["📊 Simulasi perhitungan OEE", "📈 Analisis Historis Lini Spinning Continuous PT ITS Tahun 2025"])


# KALKULATOR OEE

with tab1:
    st.header("Input Data Produksi")

    loading_time = st.number_input("Loading Time (menit)", min_value=0.0)
    downtime = st.number_input("Downtime (menit)", min_value=0.0)
    ideal_output = st.number_input("Output Ideal", min_value=0.0)
    actual_output = st.number_input("Output Aktual", min_value=0.0)
    defect = st.number_input("Jumlah Defect", min_value=0.0)

    if st.button("Hitung OEE"):
        if loading_time > 0 and actual_output > 0:
            availability = (loading_time - downtime) / loading_time
            performance = actual_output / ideal_output if ideal_output > 0 else 0
            quality = (actual_output - defect) / actual_output

            oee = availability * performance * quality

            st.subheader("Hasil Perhitungan OEE")
            st.write(f"Availability: {availability:.2%}")
            st.write(f"Performance: {performance:.2%}")
            st.write(f"Quality: {quality:.2%}")
            st.write(f"OEE: {oee:.2%}")

            # Interpretasi otomatis
            st.subheader("Interpretasi Kondisi Perusahaan")

            if oee < 0.6:
                st.error("Kondisi KRITIS - Perlu perbaikan menyeluruh pada sistem produksi.")
            elif oee < 0.75:
                st.warning("Kondisi CUKUP - Sudah cukup baik namun perlu banyak peningkatan agar menjadi lebih baik.")
            elif oee < 0.85:
                st.info("Kondisi BAIK - Operasi relatif stabil dan sudah memenuhi standard internasional.")
            else:
                st.success("WORLD CLASS - Kinerja sudah sangat optimal.")


# 2️⃣ ANALISIS DATA HISTORIS

with tab2:
    st.header("Data Historis Lini Spinning Continuous PT Indonesia Toray Synthetics Tahun 2025")

    df = pd.read_csv("DataHistoris2025.csv")
    st.write("Data Historis:", df)

        # Perhitungan OEE dari csv
    df["Availability"] = (df["LoadingTime"] - df["Downtime"]) / df["LoadingTime"]
    df["Performance"] = (df["Theoryticalcycletime"] * df["ActualOutput"]) / df["OperatingTime"]
    df["Quality"] = (df["ActualOutput"] - df["Defect"]) / df["ActualOutput"]
    df["OEE"] = df["Availability"] * df["Performance"] * df["Quality"]

    st.subheader("Grafik Tren OEE Lini Spinning continuous PT Indonesia Toray Synthetics Tahun 2025")
    plt.figure()
    plt.plot(df["Bulan"], df["OEE"])
    plt.xlabel("Bulan")
    plt.ylabel("OEE")
    st.pyplot(plt)

    st.subheader("Analisis Bulan Tertinggi & Terendah")
    max_month = df.loc[df["OEE"].idxmax()]
    min_month = df.loc[df["OEE"].idxmin()]

    st.write(f"Bulan Tertinggi: {max_month['Bulan']} ({max_month['OEE']:.2%})")
    st.write(f"Bulan Terendah: {min_month['Bulan']} ({min_month['OEE']:.2%})")

    st.subheader("Dampak Nilai OEE terhadap perusahaan")

    st.write("""
    - Bulan dengan OEE rendah yaitu pada bulan Oktober menunjukkan downtime yang sangat tinggi akibat penyesuaian after shutdown machine selama 1 bulan penuh di bulan september.
    - Dampak terhadap perusahaan: potensi penurunan output dan profit.
    - Dampak terhadap karyawan: peningkatan lembur dan beban kerja.
        """)








