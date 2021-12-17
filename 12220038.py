'''
Hafizh Mualik
12220038
IF2112 - Pemrograman Komputer
'''

import pandas as pd
import streamlit as st
import altair as alt
from streamlit.type_util import data_frame_to_bytes

# Baca dataset dan assign ke variabel
dfNgr = pd.read_json("kode_negara_lengkap.json")
dfMny = pd.read_csv('produksi_minyak_mentah.csv', index_col="kode_negara")

# Menghilangkan nilai-nilai yang bukan negara (Menghilangkan kelompok negara)
for code in dfMny.index.unique().tolist():
    if code not in dfNgr['alpha-3'].tolist():
        print(code)
        dfMny.drop([code], inplace=True)
dfMny.reset_index(inplace=True)
tempCodeList = dfMny['kode_negara'].unique().tolist()
negaraList = []
for tempCode in tempCodeList:
    negaraList.append(dfNgr.loc[dfNgr['alpha-3'] == tempCode].values[0][0])

# Fungsi untuk print tabel berisi kode negara, nama negara, region, subregion, dan produksi.
# Dibuat fungsi agar tidak perlu menulis ulang berkali-kali.
def printDF(df_input):
    df_output=pd.DataFrame()
    codeInput = df_input['kode_negara'].values[0]
    namaInput = dfNgr[dfNgr["alpha-3"] == codeInput]["name"].values[0]
    regionInput = dfNgr[dfNgr["name"] == namaInput]["region"].values[0]
    subregionInput = dfNgr[dfNgr["name"] == namaInput]["sub-region"].values[0]
    inputTahun = df_input['produksi'].values[0]
    df_output['Nama'] = df_output.append({'Nama':namaInput}, ignore_index=True)
    df_output['Kode'],df_output['Region'],df_output['Sub-region'],df_output['Produksi'] = \
        codeInput,regionInput, subregionInput,inputTahun
    st.write(df_output)

# Container untuk nav menu
with st.container():
    from PIL import Image
    image = Image.open('itb.png')
    st.sidebar.image(image)
    st.sidebar.markdown("# Data Produksi Minyak Mentah")
    st.info("Selamat datang dalam halaman informasi data produksi minyak mentah")
    st.sidebar.info("Pilih bagian mana yang ingin anda kunjungi")
    MenuSelection = st.sidebar.selectbox('Menu', ('Data Produksi Tiap Negara', 'Produsen Terbesar Tahunan', \
        'Produsen Terbesar Kumulatif', 'Data Produsen Minyak'))

# Container untuk data negara produsen
if 'Data Produksi Tiap Negara' in MenuSelection :
    with st.container():
        st.markdown("## Data Produksi Tiap Negara")
        st.markdown("---")
        # Meminta input negara kepada user dengan dropdown menu
        negaraSelect = st.selectbox("Pilih negara", negaraList)
        st.info('Grafik data produksi sebuah negara terhadap tahun')
        # Cari kode negara dari nama negara yang dipilih user
        negaraCode = dfNgr[dfNgr["name"] == negaraSelect]["alpha-3"].values[0]
        # Ambil tahun dan produksi untuk negara yang dipilih
        negprodDF = dfMny[dfMny["kode_negara"] == negaraCode][['tahun', 'produksi']]
        negprodDF = negprodDF.rename(columns={'tahun':'index'}).set_index('index')
        # Keluarkan data
        left_col, right_col = st.columns([3,1.5])
        left_col.subheader('Grafik')
        left_col.line_chart(negprodDF)
        right_col.subheader('Tabel')
        right_col.dataframe(negprodDF)

# Container untuk negara produsen terbesar tiap tahunnya
if 'Produsen Terbesar Tahunan' in MenuSelection :
    with st.container():
        try:
            st.markdown("***")
            st.markdown('## Produsen Terbesar Tahunan')
            st.markdown("---")
            # Meminta input tahun kepada user
            inputTahun = st.slider('Pilih Tahun', min_value=1971, max_value=2020, value=1971, step=1)
            # Meminta input jumlah peringkat kepada user
            inputJumlah = st.text_input('Jumlah peringkat')
            st.info('Peringkat produsen minyak terbesar pada tahun yang diberikan')
            # Ambil data yang tahunnya sesuai dengan input user, dan sortir sesuai dengan jumlah produksi dari tertinggi ke terendah
            mnyTahun = dfMny.loc[dfMny["tahun"] == int(inputTahun)].sort_values(["produksi"], ascending=[0])
            # Slice data sebanyak input peringkat user
            mnyTahun = mnyTahun[:int(inputJumlah)].reset_index(drop=True)
            mnyTahunFinal = mnyTahun[['kode_negara', 'produksi']].rename(columns={'kode_negara':'index'}).set_index('index')
            # Tampilkan data
            left_col, right_col = st.columns([3,1.5])
            left_col.subheader('Grafik')
            left_col.bar_chart(mnyTahunFinal)
            right_col.subheader('Tabel')
            right_col.dataframe(mnyTahunFinal)
        except Exception:
            pass

# Container untuk produsen terbesar tahun 1971-2015
if 'Produsen Terbesar Kumulatif' in MenuSelection :
    with st.container():
        st.markdown('***')
        st.markdown('## Produsen Terbesar Kumulatif')
        st.markdown("---")
        try:
            # Minta input jumlah negara kepada user
            jmlnegara = st.text_input('Jumlah negara')
            st.info('Peringkat produsen minyak terbesar yang pernah ada')
            # Ambil data kode negara dan jumlah produksi, kemudian grup data berdasarkan kode negara, dan jumlahkan jumlah produksi, kemudian sortir berdasarkan produksi dari tinggi ke rendah
            totaljmlprodMinyak = (dfMny[['kode_negara', 'produksi']].groupby('kode_negara', as_index=False).sum().sort_values(['produksi'], ascending=[0])).reset_index(drop=True)
            # Slice data sebanyak input user
            totaljmlprodMinyak = totaljmlprodMinyak[:int(jmlnegara)].reset_index(drop=True)
            totaljmlprodMinyakFinal = totaljmlprodMinyak[['kode_negara', 'produksi']].rename(columns={'kode_negara':'index'}).set_index('index')
            # Tampilkan data
            left_col, right_col = st.columns([3,1.5])
            left_col.subheader('Grafik')
            left_col.bar_chart(totaljmlprodMinyakFinal)
            right_col.subheader('Tabel')
            right_col.dataframe(totaljmlprodMinyakFinal)
        except Exception:
            pass

# Container untuk filter negara produsen minyak mentah
if 'Data Produsen Minyak' in MenuSelection :
    with st.container():
        st.markdown("---")
        st.markdown('## Data Produsen Minyak')
        st.markdown("---")
        st.info('Lihat informasi negara berdasarkan filter yang anda pilih')

        # Ambil data untuk produksi 0
        nolDF = dfMny[dfMny['produksi'] == 0]
        nolDF.reset_index(inplace=True)
        # Ambil kode negara tanpa duplikat
        df0 = nolDF['kode_negara'].unique()
        # Buat dataframe baru yang akan jadi template output
        nolDFO = pd.DataFrame()
        # Masukkan data yang diinginkan satu per satu ke dataframe yang baru saja dibuat
        nolDFO['nama_negara'] = [dfNgr[dfNgr['alpha-3'] == x]['name'].values[0] for x in df0]
        nolDFO['kode_negara'] = [ct for ct in df0]
        nolDFO['region'] = [dfNgr[dfNgr['alpha-3'] == x]['region'].values[0] for x in df0]
        nolDFO['subregion'] = [dfNgr[dfNgr['alpha-3'] == x]['sub-region'].values[0] for x in df0]
        nolDFO['Tahun'] = [dfMny[dfMny['kode_negara'] == x]['tahun'].values[0] for x in df0]
        nolDFO['produksi'] = [dfMny[dfMny['kode_negara'] == x]['produksi'].values[0] for x in df0]

        # Minta user untuk memilih filter yang ingin digunakan
        filterSelection = st.selectbox('Produksi', ('produksi terbesar keseluruhan', 'produksi terbesar tahun', \
            'produksi terkecil keseluruhan', 'produksi terkecil tahun', 'produksi sama dengan nol tahun', \
                'produksi sama dengan nol keseluruhan'))

        # Case apabila user memilih produksi terbesar tahun tertentu
        if 'terbesar tahun' in filterSelection :
            # Minta input tahun kepada user
            inputTahun = st.slider('Tahun', value=1976, min_value=1971, max_value=2015, step=1)
            # Cari data yang tahunnnya sesuai dengan input user. Ambil nilai maksimum dari jumlah produksinya
            highDF = dfMny[dfMny['tahun'] == int(inputTahun)]['produksi'].idxmax()
            ngrYearHigh = dfMny[highDF:highDF+1]
            # Tampilkan data
            printDF(ngrYearHigh)

        # Case apabila user memilih produksi terbesar secara keseluruhan
        elif 'terbesar keseluruhan' in filterSelection:
            # Ambil data utama, cari yang nilai produksinya maksimum
            highDF = dfMny['produksi'].idxmax()
            ngrHigh = dfMny[highDF:highDF+1]
            # Tampilkan data
            printDF(ngrHigh)

        # Case apabila user memilih produksi terkecil tahun tertentu
        elif 'terkecil tahun' in filterSelection:
            # Minta input tahun kepada user
            inputtahunmin = st.slider('Tahun yang akan dicek untuk minimum', value=1976, min_value=1971, max_value=2015, step=1)
            # Cari data yang tahunnya sesuai dengan input user
            lowDF = dfMny[dfMny['tahun'] == int(inputtahunmin)]
            # Cari data yang jumlah produksinya bukan nol
            lowDF = lowDF[lowDF['produksi'] != 0]
            # Cari nilai minimum dari data jumlah produksi yang ada
            lowDFS = lowDF['produksi'].idxmin()
            ngrYearLow = dfMny[lowDFS:lowDFS+1]
            # Tampilkan data
            printDF(ngrYearLow)

        # Case apabila user memilih produksi terkecil secara keseluruhan
        elif 'terkecil keseluruhan' in filterSelection:
            # Cari data yang nilai produksinya bukan nol
            lowDF = dfMny[dfMny['produksi'] > 0]
            lowDF.reset_index(inplace=True)
            # Cari nilai jumlah produksi minimum
            lowDFS = lowDF['produksi'].idxmin()
            ngrLow = lowDF[lowDFS:lowDFS+1]
            # Tampilkan data
            printDF(ngrLow)

        # Case apabila user memilih produksi nol
        elif 'nol' in filterSelection:
            # Apabila user memilih produksi nol tahun tertentu
            if 'keseluruhan' not in filterSelection:
                inputnegaratahunan0 = st.slider('Tahun yang akan dicek untuk produksi kosong', value=1971, min_value=1971, max_value=2015, step=1)
                st.write(nolDFO[nolDFO['Tahun'] == int(inputnegaratahunan0)])
            # Apabila user memilih produksi nol secara keseluruhan
            else: st.write(nolDFO)