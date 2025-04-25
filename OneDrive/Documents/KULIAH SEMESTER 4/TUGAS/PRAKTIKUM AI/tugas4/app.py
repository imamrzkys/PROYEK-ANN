from flask import Flask, render_template, url_for
import pandas as pd

app = Flask(__name__)

from flask import send_file, request, make_response
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os

@app.route("/", methods=["GET"])
def index():
    df_prediksi = pd.read_csv('hasil_prediksi_hiv.csv')
    kabupaten_list = sorted(df_prediksi['nama_kabupaten_kota'].unique())
    selected_kabupaten = request.args.get('kabupaten')
    # Grafik URL akan mengandung parameter filter
    grafik_url = url_for('grafik_dynamic', kabupaten=selected_kabupaten if selected_kabupaten else 'ALL')
    if selected_kabupaten and selected_kabupaten != 'ALL':
        df_prediksi = df_prediksi[df_prediksi['nama_kabupaten_kota'] == selected_kabupaten]
    tabel_prediksi_data = df_prediksi.to_dict(orient='records')
    return render_template("index.html",
                           tabel_prediksi_data=tabel_prediksi_data,
                           grafik_url=grafik_url,
                           kabupaten_list=kabupaten_list,
                           selected_kabupaten=selected_kabupaten)

@app.route('/grafik_dynamic')
def grafik_dynamic():
    kabupaten = request.args.get('kabupaten')
    df_prediksi = pd.read_csv('hasil_prediksi_hiv.csv')
    df_aktual = pd.read_csv('dinkes-od_18510_jumlah_kasus_hiv_berdasarkan_kabupatenkota_v2_data.csv')
    plt.figure(figsize=(10,5))
    if kabupaten and kabupaten != 'ALL':
        # Plot hanya kabupaten/kota terpilih dengan warna soft
        data_aktual = df_aktual[df_aktual['nama_kabupaten_kota'] == kabupaten]
        data_pred = df_prediksi[df_prediksi['nama_kabupaten_kota'] == kabupaten]
        plt.plot(data_aktual['tahun'], data_aktual['jumlah_kasus'], marker='o', label=f'Aktual {kabupaten}', color='#40E0D0', linewidth=3)
        plt.plot(data_pred['tahun'], data_pred['jumlah_kasus'], marker='o', label=f'Prediksi {kabupaten}', color='#FFD1DC', linewidth=3, linestyle='dashed')
        plt.title(f'Grafik Prediksi & Data Aktual\n{kabupaten}')
    else:
        # Plot semua kabupaten/kota dengan colormap tab20
        import matplotlib.cm as cm
        import numpy as np
        kota_list = list(df_aktual['nama_kabupaten_kota'].unique())
        colors = cm.get_cmap('tab20', len(kota_list))
        for idx, nama in enumerate(kota_list):
            data_kota = df_aktual[df_aktual['nama_kabupaten_kota'] == nama]
            plt.plot(data_kota['tahun'], data_kota['jumlah_kasus'], marker='o', alpha=0.6, label=nama, color=colors(idx))
        for idx, nama in enumerate(df_prediksi['nama_kabupaten_kota'].unique()):
            data_pred = df_prediksi[df_prediksi['nama_kabupaten_kota'] == nama]
            plt.plot(data_pred['tahun'], data_pred['jumlah_kasus'], marker='o', alpha=0.6, linestyle='dashed', color=colors(idx))
        plt.title('Prediksi Jumlah Kasus HIV per Kabupaten/Kota (2018-2025)')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Kasus')
    # Tidak ada legend
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/download/csv')
def download_csv():
    return send_file('hasil_prediksi_hiv.csv', as_attachment=True)

@app.route('/download/grafik')
def download_grafik():
    kabupaten = request.args.get('kabupaten')
    df_prediksi = pd.read_csv('hasil_prediksi_hiv.csv')
    df_aktual = pd.read_csv('dinkes-od_18510_jumlah_kasus_hiv_berdasarkan_kabupatenkota_v2_data.csv')
    plt.figure(figsize=(10,5))
    if kabupaten and kabupaten != 'ALL':
        data_aktual = df_aktual[df_aktual['nama_kabupaten_kota'] == kabupaten]
        data_pred = df_prediksi[df_prediksi['nama_kabupaten_kota'] == kabupaten]
        plt.plot(data_aktual['tahun'], data_aktual['jumlah_kasus'], marker='o', label=f'Aktual {kabupaten}', color='#0d6efd')
        plt.plot(data_pred['tahun'], data_pred['jumlah_kasus'], marker='o', label=f'Prediksi {kabupaten}', color='#dc3545')
        plt.title(f'Grafik Prediksi & Data Aktual\n{kabupaten}')
    else:
        for nama in df_aktual['nama_kabupaten_kota'].unique():
            data_kota = df_aktual[df_aktual['nama_kabupaten_kota'] == nama]
            plt.plot(data_kota['tahun'], data_kota['jumlah_kasus'], marker='o', alpha=0.3, label=nama)
        for nama in df_prediksi['nama_kabupaten_kota'].unique():
            data_pred = df_prediksi[df_prediksi['nama_kabupaten_kota'] == nama]
            plt.plot(data_pred['tahun'], data_pred['jumlah_kasus'], marker='o', alpha=0.3, linestyle='dashed')
        plt.title('Prediksi Jumlah Kasus HIV per Kabupaten/Kota (2018-2025)')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Kasus')
    plt.legend(loc='best', fontsize=8)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return send_file(img, mimetype='image/png', as_attachment=True, download_name='grafik_hiv.png')

if __name__ == "__main__":
    app.run(debug=True)
