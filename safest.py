from sklearn.cluster import AgglomerativeClustering
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="Kota/Kabupaten Rawan Bencana Alam di Jawa Barat", layout='wide')
st.title("Kota/Kabupaten Jawa Barat Manakah yang Paling Rawan dari Bencana Alam?")
st.caption("Ditulis dan diolah: Auliansa Muhammad (email: aulim.id@gmail.com)")

# st.markdown("""
# ![](https://cdn.pixabay.com/photo/2013/02/14/15/12/new-orleans-81669_960_720.jpg?raw=true)
# """)
# st.caption("Ilustrasi bencana alam. Gambar diambil dari pixabay.com")
st.markdown("""
Saat ini beberapa wilayah di Indonesia sedang dilanda [cuaca yang tidak menentu dan ekstrem](https://www.bmkg.go.id/press-release/?p=bmkg-waspada-potensi-cuaca-ekstrem-masih-berlanjut-untuk-sepekan-ke-depan-09-15-oktober-2022&tag=&lang=ID). 
Bahkan, himbauan telah diberikan [hampir satu bulan yang lalu](https://bandung.kompas.com/read/2022/09/09/121547578/cuaca-ekstrem-warga-jawa-barat-diminta-waspadai-potensi-hujan-es?page=all).
Hingga saat ini, tercatat beberapa kabupaten dan kota di Jawa Barat telah mengalami kejadian bencana alam, seperti [banjir dan longsor di Puncak Bogor](https://jabar.antaranews.com/berita/409185/14-lokasi-wilayah-puncak-bogor-diterjang-banjir-dan-longsor) dan 
[banjir di Bandung](https://regional.kompas.com/read/2022/10/09/093050678/semalaman-diguyur-hujan-kabupaten-bandung-kembali-terendam-banjir?page=all).

Berdasarkan data kejadian-kejadian bencana tahun 2012-2021 yang diperoleh dari [situs open data Jawa Barat](https://opendata.jabarprov.go.id/id/dataset), daerah mana sajakah yang cenderung terkena bencana alam? Apakah kejadian bencana alam sepuluh tahun terakhir di Jawa Barat cenderung meningkat?
""")

df_banjir = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRC1OK4ZmIdRHdA9LdF4Jb3KBUFWkdLcsbcqfQT0ZdYdHjUOOR4hr06MSksyoy8PY983mLlmqQrzdLq/pub?gid=1278603687&single=true&output=csv")
df_longsor = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTAucK0NVY4-8SXYooJhuussL018QUJaIEETMW1YeJlEGXjO7TtEryHBOUIPECx-6092RAolqHZVsEa/pub?gid=1045559606&single=true&output=csv")
df_gempa = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRtnQMnqpauJ4_HynZvDQigwwP6s_nWyHIGaa47rssRTw5uHj2n0yPEsuGDvwh56U9zQvUh99mqKW1p/pub?gid=1250106213&single=true&output=csv")
df_topan = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSaddbfoWtCGTmrZmz07VJiVw87dG5oWVi2dGYzPl_F_EeJgqkPhz7a5US8NKR17wZ19aFsUxG7l24R/pub?gid=918492154&single=true&output=csv")

df_bencana = pd.merge(df_banjir, df_longsor)
df_bencana = pd.merge(df_bencana, df_gempa)
df_bencana = pd.merge(df_bencana, df_topan)

target_cols = ['jumlah_banjir', 'jumlah_tanah_longsor', 'jumlah_gempa_bumi', 'jumlah_puting_beliung']
shown_columns = ['nama_kabupaten_kota'] + target_cols

def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

def make_stacked_plot(df, target_cols, ylab, title):
    fig, ax = plt.subplots()

    x = df['nama_kabupaten_kota']
    
    sum = 0
    for i in range(0, len(target_cols)):
        ax.barh(x, df[target_cols[i]], 0.35, left=sum, label=target_cols[i])
        sum += df[target_cols[i]]
    ax.set_xlabel(ylab)
    ax.set_title(title)
    ax.legend()

    return fig, ax

def show_metric_element(text, df, target_col):
    value_end = int(df.loc[df['tahun'] == end_year, target_col].iloc[0])
    value_start = int(df.loc[df['tahun'] == start_year, target_col].iloc[0])
    delta_text = value_end-value_start if value_start == 0 else f'{round(100 * (value_end-value_start)/value_start, 2)}%'
    st.metric(text, f'{value_start} → {value_end}', delta_text, delta_color='inverse')

tab0, tab1, tab2 = st.tabs(['Kelompok Kerawanan Kota/Kabupaten','Bencana per Kota/Kabupaten', 'Kota/Kabupaten dengan Bencana Terbanyak'])

with tab0:

    df_cls = df_bencana.copy()
    cluster_container = st.container()
    cls_agg = cluster_container.radio(
        "Tampilkan metrik:",
        ['Rata-rata Jumlah Bencana', 'Total Jumlah Bencana'],
        horizontal=True
    )
    cls_disaster = cluster_container.radio(
        "Kelompokkan Berdasarkan Bencana:",
        ['Semua', 'Banjir', 'Longsor', 'Gempa', 'Puting Beliung'],
        horizontal=True
    )

    agg_fun = 'mean' if cls_agg == 'Rata-rata Jumlah Bencana' else 'sum'
    if cls_disaster == 'Semua':
        cls_cols = target_cols
        cls_title = ''
    elif cls_disaster == 'Banjir':
        cls_cols = [target_cols[0]]
        cls_title = cls_disaster
    elif cls_disaster == 'Longsor':
        cls_cols = [target_cols[1]]
        cls_title = cls_disaster
    elif cls_disaster == 'Gempa':
        cls_cols = [target_cols[2]]
        cls_title = cls_disaster
    else:
        cls_cols = [target_cols[3]]
        cls_title = cls_disaster

    df_cls = df_cls.groupby(['nama_kabupaten_kota'])[cls_cols].agg(agg_fun)

    AggClust = AgglomerativeClustering(n_clusters = 3).fit(df_cls)
    y = AggClust.labels_

    df_cls_res = df_cls.reset_index()
    df_cls_res['Cluster'] = y

    df1 = df_cls_res.loc[df_cls_res['Cluster'] == 0]
    df2 = df_cls_res.loc[df_cls_res['Cluster'] == 1]
    df3 = df_cls_res.loc[df_cls_res['Cluster'] == 2]

    df1 = (df1.loc[(df1[cls_cols].sum(axis=1)).sort_values(ascending=True).index,:]).reset_index()
    df2 = (df2.loc[(df2[cls_cols].sum(axis=1)).sort_values(ascending=True).index,:]).reset_index()
    df3 = (df3.loc[(df3[cls_cols].sum(axis=1)).sort_values(ascending=True).index,:]).reset_index()

    df_cls_show = [df1, df2, df3]
    df_cls_avgs = [(df[cls_cols].mean()).mean() for df in df_cls_show]
    sorted_idx = np.argsort(df_cls_avgs).tolist()[::-1]

    t0c1, t0c2, t0c3 = st.columns(3, gap='medium')
    with t0c1:
        cls_fig1, _ = make_stacked_plot(df_cls_show[sorted_idx[0]], cls_cols, cls_agg, f'{cls_agg} {cls_title} Tahun 2012-2021 Kategori Rawan')
        st.pyplot(cls_fig1)
    with t0c2:
        cls_fig2, _ = make_stacked_plot(df_cls_show[sorted_idx[1]], cls_cols, cls_agg, f'{cls_agg} {cls_title} Tahun 2012-2021 Kategori Siaga')
        st.pyplot(cls_fig2)
    with t0c3:
        cls_fig3, _ = make_stacked_plot(df_cls_show[sorted_idx[2]], cls_cols, cls_agg, f'{cls_agg} {cls_title} Tahun 2012-2021 Kategori Waspada')
        st.pyplot(cls_fig3)

with tab1:
    t1c1, t1c2= st.columns([1.5,1], gap='medium')

    with t1c1:
        # Plot banyak bencana dari tahun ke tahun

        kotakab = st.selectbox(
            "Pilih kota/kabupaten yang ingin ditampilkan:",
            df_bencana['nama_kabupaten_kota'].unique()
        )

        df_tsChart = df_bencana[df_bencana['nama_kabupaten_kota'] == kotakab]

        ts_bencana = plt.figure(figsize=(17.5,10))
        plt.plot(df_tsChart['tahun'], df_tsChart['jumlah_banjir'], label='Banjir', linestyle='-', marker='o')
        plt.plot(df_tsChart['tahun'], df_tsChart['jumlah_puting_beliung'], label='Puting Beliung', linestyle='--', marker='o')
        plt.plot(df_tsChart['tahun'], df_tsChart['jumlah_tanah_longsor'], label='Longsor', linestyle='-.', marker='o')
        plt.plot(df_tsChart['tahun'], df_tsChart['jumlah_gempa_bumi'], label='Gempa', linestyle=':', marker='o')
        plt.legend(loc='best')
        plt.ylabel('Jumlah Kejadian')
        plt.xlabel('Tahun')
        plt.title(f'Bencana Alam {kotakab.title()} 2012-2021')

        st.pyplot(ts_bencana)

    with t1c2:
        start_year, end_year = st.select_slider(
            "Pilih tahun perbandingan",
            df_bencana['tahun'].unique(),
            value=(2012, 2021)
        )
        st.write(f"Kenaikan jumlah kejadian bencana di {kotakab.title()} dari {start_year} ke {end_year}")
        show_metric_element("Kejadian Banjir", df_tsChart, target_cols[0])
        show_metric_element("Kejadian Longsor", df_tsChart, target_cols[1])
        show_metric_element("Kejadian Gempa", df_tsChart, target_cols[2])
        show_metric_element("Kejadian Puting Beliung", df_tsChart, target_cols[3])

with tab2:
    t2c1, t2c2 = st.columns([1,4], gap="medium")
    with t2c1:
        bencana = st.selectbox(
            "Pilih metrik bencana yang ingin ditampilkan:",
            ['Semua Bencana', 'Banjir','Tanah Longsor','Gempa Bumi','Puting Beliung']
        )

        aggregasi = st.radio(
            "Pilih jenis agregasi: ",
            ["Tahunan tanpa agregasi",'Rerata','Total'],
            horizontal=True
        )

        if aggregasi == "Tahunan tanpa agregasi":
            tahun = st.selectbox(
                "Pilih tahun: ",
                df_bencana['tahun'].unique(),
                len(df_bencana['tahun'].unique()) -1
            )
            if bencana != 'Semua Bencana':
                xlab = f"Kejadian Bencana {bencana} Tahun {tahun}"
            else:
                xlab = f"Kejadian Bencana Alam Tahun {tahun}"
            df_tahun = df_bencana[df_bencana['tahun'] == tahun]
        else:
            if aggregasi == "Rerata":
                df_tahun = df_bencana.groupby(['nama_kabupaten_kota']).agg("mean").reset_index()
                if bencana != 'Semua Bencana':
                    xlab = f"Rata-rata Kejadian Bencana {bencana} per Tahun"
                else:
                    xlab = f"Rata-rata Kejadian Bencana Alam per Tahun"
            else:
                df_tahun = df_bencana.groupby(['nama_kabupaten_kota']).agg("sum").reset_index()
                if bencana != 'Semua Bencana':
                    xlab = f"Total Kejadian Bencana {bencana} Tahun 2012-2021"
                else:
                    xlab = f"Total Kejadian Bencana Alam Tahun 2012-2021"

        ambil_n = st.slider(
            "Lihat berapa kota/kabupaten?",
            min_value=1,
            max_value=df_bencana['nama_kabupaten_kota'].nunique(),
            value=6,
            step=1
        )

    if bencana == 'Banjir':
        selected_metric = 'jumlah_banjir'
    elif bencana == 'Tanah Longsor':
        selected_metric = 'jumlah_tanah_longsor'
    elif bencana == 'Gempa Bumi':
        selected_metric = 'jumlah_gempa_bumi'
    elif bencana == 'Puting Beliung':
        selected_metric = 'jumlah_puting_beliung'
    else:
        selected_metric = 'total_bencana'

    df_temp = df_tahun.copy()
    df_temp['total_bencana'] = df_temp['jumlah_banjir'] + df_temp['jumlah_tanah_longsor'] + df_temp['jumlah_gempa_bumi'] + df_temp['jumlah_puting_beliung']
    df_sorted = df_temp.sort_values(by=selected_metric, ascending=False)
    df_sorted = df_sorted[shown_columns + ['total_bencana']]
    x = df_sorted[selected_metric].head(ambil_n)
    y = df_sorted['nama_kabupaten_kota'].head(ambil_n)

    bar_bencana, ax = plt.subplots()
    bar_bencana.set_figwidth(25)
    bar_bencana.set_figheight(10)
    ax.barh(y, x, color = get_color_gradient("#AF0000", "#00AF00", ambil_n))
    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)

    # Add x, y gridlines
    ax.grid(visible = True, color ='grey',
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
    
    ax.set_xlabel("Jumlah bencana")
    ax.set_title(xlab)
    with t2c2:
        st.pyplot(bar_bencana)