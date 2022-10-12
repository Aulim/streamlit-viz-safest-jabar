import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="Kota/Kabupaten Rawan Bencana Alam di Jawa Barat")
st.title("Kota/Kabupaten Jawa Barat Manakah yang Paling Rawan dari Bencana Alam?")

st.markdown("""
Saat ini beberapa wilayah di Indonesia sedang dilanda [cuaca yang tidak menentu dan ekstrem](https://www.bmkg.go.id/press-release/?p=bmkg-waspada-potensi-cuaca-ekstrem-masih-berlanjut-untuk-sepekan-ke-depan-09-15-oktober-2022&tag=&lang=ID). 
Bahkan, himbauan telah diberikan [hampir satu bulan yang lalu](https://bandung.kompas.com/read/2022/09/09/121547578/cuaca-ekstrem-warga-jawa-barat-diminta-waspadai-potensi-hujan-es?page=all).
Hingga saat ini, tercatat beberapa kabupaten dan kota di Jawa Barat telah mengalami kejadian bencana alam, seperti [banjir dan longsor di Puncak Bogor](https://jabar.antaranews.com/berita/409185/14-lokasi-wilayah-puncak-bogor-diterjang-banjir-dan-longsor) dan 
[banjir di Bandung](https://regional.kompas.com/read/2022/10/09/093050678/semalaman-diguyur-hujan-kabupaten-bandung-kembali-terendam-banjir?page=all).

Berdasarkan data kejadian-kejadian sebelumnya, daerah mana sajakah yang cenderung terkena bencana alam?
""")

df_banjir = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRC1OK4ZmIdRHdA9LdF4Jb3KBUFWkdLcsbcqfQT0ZdYdHjUOOR4hr06MSksyoy8PY983mLlmqQrzdLq/pub?gid=1278603687&single=true&output=csv")
df_longsor = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTAucK0NVY4-8SXYooJhuussL018QUJaIEETMW1YeJlEGXjO7TtEryHBOUIPECx-6092RAolqHZVsEa/pub?gid=1045559606&single=true&output=csv")
df_gempa = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRtnQMnqpauJ4_HynZvDQigwwP6s_nWyHIGaa47rssRTw5uHj2n0yPEsuGDvwh56U9zQvUh99mqKW1p/pub?gid=1250106213&single=true&output=csv")
df_topan = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSaddbfoWtCGTmrZmz07VJiVw87dG5oWVi2dGYzPl_F_EeJgqkPhz7a5US8NKR17wZ19aFsUxG7l24R/pub?gid=918492154&single=true&output=csv")

df_bencana = pd.merge(df_banjir, df_longsor)
df_bencana = pd.merge(df_bencana, df_gempa)
df_bencana = pd.merge(df_bencana, df_topan)

tab1, tab2 = st.tabs(['Bencana per Kota/Kabupaten Tahun 2012-2021', 'Kota/Kabupaten dengan Bencana Terbanyak'])

with tab1:
    kotakab = st.selectbox(
        "Pilih kota/kabupaten yang ingin ditampilkan:",
        df_bencana['nama_kabupaten_kota'].unique()
    )

    target_cols = ['jumlah_banjir', 'jumlah_tanah_longsor', 'jumlah_gempa_bumi', 'jumlah_puting_beliung']

    max_banjir = df_bencana['jumlah_banjir'].max()
    max_beliung = df_bencana['jumlah_puting_beliung'].max()
    max_longsor = df_bencana['jumlah_tanah_longsor'].max()
    max_gempa = df_bencana['jumlah_gempa_bumi'].max()
    max_bencana = max([max_banjir, max_beliung, max_longsor, max_gempa])

    # Plot banyak bencana dari tahun ke tahun

    df_tsChart = df_bencana[df_bencana['nama_kabupaten_kota'] == kotakab]

    ts_bencana = plt.figure()
    plt.plot(df_tsChart['tahun'], df_tsChart['jumlah_banjir'], label='Banjir', linestyle='-')
    plt.plot(df_tsChart['tahun'], df_tsChart['jumlah_puting_beliung'], label='Puting Beliung', linestyle='--')
    plt.plot(df_tsChart['tahun'], df_tsChart['jumlah_tanah_longsor'], label='Longsor', linestyle='-.')
    plt.plot(df_tsChart['tahun'], df_tsChart['jumlah_gempa_bumi'], label='Gempa', linestyle=':')
    plt.legend(loc='best')
    plt.ylabel('Jumlah Kejadian')
    plt.ylim([0,max_bencana])
    plt.xlabel('Tahun')
    plt.title(f'Bencana Alam {kotakab.title()} 2012-2021')

    st.pyplot(ts_bencana)

    # st.line_chart(
    #     df_bencana[df_bencana['nama_kabupaten_kota'] == kotakab], 
    #     x='tahun', 
    #     y=['jumlah_banjir','jumlah_puting_beliung','jumlah_tanah_longsor','jumlah_gempa_bumi'],
    #     width=10
    # )

with tab2:
    bencana = st.selectbox(
        "Pilih ranking bencana yang ingin ditampilkan:",
        ['Banjir','Tanah Longsor','Gempa Bumi','Puting Beliung']
    )

    aggregasi = st.radio(
        "Pilih jenis agregasi: ",
        ["Tahunan tanpa agregasi",'Rerata','Total'],
        horizontal=True
    )

    if aggregasi == "Tahunan tanpa agregasi":
        tahun = st.selectbox(
            "Pilih jangka waktu: ",
            df_bencana['tahun'].unique()
        )
        xlab = f"Kejadian Bencana {bencana} pada Tahun {tahun}"
        df_tahun = df_bencana[df_bencana['tahun'] == tahun]
    else:
        if aggregasi == "Rerata":
            df_tahun = df_bencana.groupby(['nama_kabupaten_kota']).agg("mean").reset_index()
            xlab = f"Rata-rata Kejadian Bencana {bencana} per Tahun"
        else:
            df_tahun = df_bencana.groupby(['nama_kabupaten_kota']).agg("sum").reset_index()
            xlab = f"Total Kejadian Bencana {bencana} Tahun 2012-2021"


    ambil_n = st.slider(
        "Lihat berapa kota/kabupaten?",
        min_value=1,
        max_value=df_bencana['nama_kabupaten_kota'].nunique(),
        value=3,
        step=1
    )

    shown_columns = ['nama_kabupaten_kota'] + target_cols

    if bencana == 'Banjir':
        selected_metric = 'jumlah_banjir'
    elif bencana == 'Tanah Longsor':
        selected_metric = 'jumlah_tanah_longsor'
    elif bencana == 'Gempa Bumi':
        selected_metric = 'jumlah_gempa_bumi'
    else:
        selected_metric = 'jumlah_puting_beliung'

    df_sorted = df_tahun.sort_values(by=selected_metric, ascending=False)
    df_sorted = df_sorted[shown_columns]
    x = df_sorted[selected_metric].head(ambil_n)
    y = df_sorted['nama_kabupaten_kota'].head(ambil_n)

    bar_bencana, ax = plt.subplots()
    ax.barh(y,x)
    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)

    # Add x, y gridlines
    ax.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)
    
    # Show top values
    ax.invert_yaxis()

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
                str(round((i.get_width()), 2)),
                fontsize = 10, fontweight ='bold',
                color ='grey')
    
    ax.set_xlabel(xlab)

    st.pyplot(bar_bencana)

    with st.expander("Tabel Data"):
        st.dataframe(df_sorted.head(ambil_n).reset_index(drop=True))