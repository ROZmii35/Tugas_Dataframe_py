import pandas as pd
# Mengambil Data dari exel yang ada di folder
df_sampah_provinsi = pd.read_excel('data_jumlah_produksi_sampah_berdasarkan_kabupatenkota.xlsx')
# Memprint dan mengubah data ke string sehingga bisa dimunculkan di terminal
print(df_sampah_provinsi.to_string(index=False))

df_sampah_prov_thn = df_sampah_provinsi.loc[:,['id','jumlah_produksi_sampah','satuan','tahun']]
# untuk menghitung di tahun 2016
tot_sampah = 0
for index,row in df_sampah_prov_thn.iterrows():
    if pd.to_numeric(row['tahun']) == 2016 and pd.notnull(row['jumlah_produksi_sampah']):
        tot_sampah += row['jumlah_produksi_sampah']
# memprint jumlah sampah pada tahun 2016
print(f"Total Jumlah sampah pada tahun 2016:{tot_sampah:.2f} ton/hari ")
# Menghitung total sampah pertahunnya
tot_sampah_perthn = {}
for index,row in df_sampah_prov_thn.iterrows():
    thn = row['tahun']
    if pd.notnull(thn) and pd.notnull(row['jumlah_produksi_sampah']):
        if thn in tot_sampah_perthn:
            tot_sampah_perthn[thn] += row['jumlah_produksi_sampah']
        else:
            tot_sampah_perthn[thn] = row['jumlah_produksi_sampah']

print("Total jumlah produksi sampah per tahun:")
for tahun, total in tot_sampah_perthn.items():
    print(f"Tahun {int(tahun)}: {total:.2f} ton")
# Membuat dataframe total sampah pertahunnya
df_tot_sampah_perthn = pd.DataFrame(list(tot_sampah_perthn.items()), columns=['Tahun', 'Total Sampah (ton/hari)'])
# Memfilter dataframe nama kabupaten/Kota dan tahun
df_sampah_thn_kab = df_sampah_provinsi.loc[:,[ 'id','nama_kabupaten_kota','jumlah_produksi_sampah','satuan','tahun']]
# Menhitung total sampah per kabupaten dan tahun
tot_sampah_prkab_perthn = {}
for index , row in df_sampah_thn_kab.iterrows():
    thn = row['tahun']
    kab_kot = row['nama_kabupaten_kota']
    if pd.notnull(row['jumlah_produksi_sampah']):
        if (kab_kot,thn) in tot_sampah_prkab_perthn:
            tot_sampah_prkab_perthn[(kab_kot,thn)] += row['jumlah_produksi_sampah']
        else:
            tot_sampah_prkab_perthn[(kab_kot,thn)] = row['jumlah_produksi_sampah']


print("Total produksi sampah per kota/kabupaten dan per tahunnya:")
for (kab_kot, tahun), total_sampah in tot_sampah_prkab_perthn.items():
    print(f"total sampah di Kota/Kabupaten: {kab_kot}, pada tahun {tahun}: {total_sampah:.2f} ton/hari")
# Membuat dataframe total sampah per kabupaten/kota dan per tahunnya
df_tot_sampah_prkab = pd.DataFrame(list(tot_sampah_prkab_perthn.items()), columns=['Kabupaten/Kota, Tahun', 'Total sampah (ton/hari)'])
# Ngepisah kolom 'Kabupaten/kota,tahun' menjadi dua kolom
df_tot_sampah_prkab[['Kabupaten/Kota', 'Tahun']] = pd.DataFrame(df_tot_sampah_prkab['Kabupaten/Kota, Tahun'].to_list(), index=df_tot_sampah_prkab.index)
# Menghapus kolom 'Kabupaten/kota,tahun'
df_tot_sampah_prkab = df_tot_sampah_prkab.drop(columns=['Kabupaten/Kota, Tahun'])
# membuat ulang kolomnya
df_tot_sampah_prkab = df_tot_sampah_prkab[['Kabupaten/Kota', 'Tahun', 'Total sampah (ton/hari)']]
# Mengkonversikan dataframe ke bentuk exel dan csv
df_tot_sampah_perthn.to_excel('Total_sampah_Pertahun.xlsx')
df_tot_sampah_perthn.to_csv('Total_sampah_Pertahun.csv')
df_tot_sampah_prkab.to_excel('Total_sampah_PerkabupatenKota_Pertahun.xlsx')
df_tot_sampah_prkab.to_csv('Total_sampah_PerkabupatenKota_Pertahun.csv')