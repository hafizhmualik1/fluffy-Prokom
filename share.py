import matplotlib.pyplot as plt
from matplotlib import cm
import json
import pandas as pd
import streamlit as st

df = pd.read_csv('produksi_minyak_mentah.csv')
df['produksi'] = pd.to_numeric(df['produksi'])
file_json = open("kode_negara_lengkap.json")
data = json.loads(file_json.read())

name_country=[]
for z in range (len(df.index)):
    x=0
    indikator = 0
    for k in data:
        if df['kode_negara'][z] == data[x]['alpha-3'] :
            name_country.append(data[x]['name'])
            indikator +=1
        x+=1
    if indikator == 0:
        name_country.append(0)

df['name_country']=name_country
df = df[df.name_country != 0]


############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Mentah")
#st.markdown("*Sumber data berasal dari [Jakarta Open Data](https://data.jakarta.go.id/dataset/data-jumlah-penumpang-trans-jakarta-tahun-2019-kpi)*")
############### title ###############)

############### sidebar ###############
#image = Image.open('oil_logo.png')
#st.sidebar.image(image)

st.sidebar.title("Pengaturan")
left_col, mid_col, right_col = st.columns(3)

## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
country=list(dict.fromkeys(name_country))
country.remove(0)
negara = st.sidebar.selectbox("Pilih Negara", country)
n_country = st.sidebar.number_input("Jumlah Negara", min_value=1, max_value=None, value=1)
tahun_unik = list(df['tahun'].unique())
tahun = st.sidebar.selectbox ("Pilih Tahun", tahun_unik)

############### lower left column ###############
left_col.subheader("Produksi Minyak Mentah Per Negara")

jumlah_prod=[]
for i in df[df['name_country']==negara]['produksi'] :
    jumlah_prod.append(i)

fig, ax = plt.subplots()
cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(country)]
ax.bar(tahun_unik, jumlah_prod, color=colors)

left_col.pyplot(fig)
############### lower left column ###############

############### lower middle column ###############
mid_col.subheader("Produksi Terbesar")

df_2=df.sort_values(by=['produksi'], ascending=False)
df_2 = df_2.loc[df_2['tahun']==tahun]
jumlah_produksi = []
list_negara=[]
x=0
for i in df_2['produksi']:
    if x < n_country:
        jumlah_produksi.append(i)
        x+=1
x=0
for i in df_2['name_country']:
    if x < n_country:
        list_negara.append(i)
        x+=1

fig, ax = plt.subplots()
ax.bar(list_negara, jumlah_produksi, color=colors)

plt.tight_layout()

mid_col.pyplot(fig)
############### lower middle column ###############

############### lower right column ###############
right_col.subheader("---------------")

df_3 = pd.DataFrame(df, columns= ['name_country','produksi'])
df_3['total_prod'] =  df_3.groupby(['name_country'])['produksi'].transform('sum')
df_3 = df_3.drop_duplicates(subset=['name_country'])
df_3=df_3.sort_values(by=['total_prod'], ascending=False)
list_negara2=[]
total_prod=[]
y=0
for i in df_3['total_prod']:
    if y < n_country:
        total_prod.append(i)
        y+=1
y=0
for i in df_3['name_country']:
    if y < n_country:
        list_negara2.append(i)
        y+=1

fig, ax = plt.subplots()
ax.bar(list_negara2, total_prod, color=colors)

plt.tight_layout()

right_col.pyplot(fig)
############### lower right column ###############
