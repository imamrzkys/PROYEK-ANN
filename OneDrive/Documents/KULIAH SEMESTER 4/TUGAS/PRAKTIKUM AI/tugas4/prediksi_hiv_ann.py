import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import sys

def prediksi_hiv():
    try:
        data = pd.read_csv('dinkes-od_18510_jumlah_kasus_hiv_berdasarkan_kabupatenkota_v2_data.csv')
    except FileNotFoundError:
        print('File dataset tidak ditemukan! Pastikan file "dinkes-od_18510_jumlah_kasus_hiv_berdasarkan_kabupatenkota_v2_data.csv" ada di folder yang sama dengan script ini.')
        sys.exit(1)

    le = LabelEncoder()
    data['kode_kabupaten_kota'] = le.fit_transform(data['nama_kabupaten_kota'])
    scaler = MinMaxScaler()
    fitur = data[['tahun', 'kode_kabupaten_kota']].values
    fitur_normal = scaler.fit_transform(fitur)
    target = data['jumlah_kasus'].values

    X_train, X_test, y_train, y_test = train_test_split(
        fitur_normal, target, test_size=0.2, random_state=42
    )

    def buat_model():
        model = Sequential()
        model.add(Dense(10, activation='relu', input_shape=(2,)))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(1, activation='linear'))
        return model

    model = buat_model()
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    ehistory = model.fit(
        X_train, y_train,
        epochs=200,
        batch_size=16,
        validation_data=(X_test, y_test),
        verbose=0
    )

    # Evaluasi
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    # Prediksi tahun 2024 & 2025
    kabupaten_kota = data['nama_kabupaten_kota'].unique()
    kode_kabupaten_kota = le.transform(kabupaten_kota)
    tahun_prediksi = [2024, 2025]
    hasil_prediksi = []
    for tahun in tahun_prediksi:
        fitur_prediksi = np.array([
            [tahun, kode] for kode in kode_kabupaten_kota
        ])
        fitur_prediksi_norm = scaler.transform(fitur_prediksi)
        jumlah_kasus_pred = model.predict(fitur_prediksi_norm)
        for idx, kode in enumerate(kode_kabupaten_kota):
            hasil_prediksi.append({
                'nama_kabupaten_kota': le.inverse_transform([kode])[0],
                'tahun': tahun,
                'jumlah_kasus': int(np.round(jumlah_kasus_pred[idx][0]))
            })
    df_prediksi = pd.DataFrame(hasil_prediksi)
    return df_prediksi, tahun_prediksi, kabupaten_kota, hasil_prediksi

if __name__ == "__main__":
    df_prediksi, tahun_prediksi, kabupaten_kota, hasil_prediksi = prediksi_hiv()
    print('\nHasil Prediksi Jumlah Kasus HIV Tahun 2024 & 2025:')
    print(df_prediksi.to_string(index=False))
    
    # Simpan ke file CSV
    df_prediksi.to_csv('hasil_prediksi_hiv.csv', index=False)

    # --- GRAFIK: Data aktual dan prediksi (semua kabupaten/kota, tahun 2018-2025) ---
    import matplotlib.pyplot as plt
    import os
    df_aktual = pd.read_csv('dinkes-od_18510_jumlah_kasus_hiv_berdasarkan_kabupatenkota_v2_data.csv')
    df_gabungan = pd.concat([
        df_aktual[['tahun', 'nama_kabupaten_kota', 'jumlah_kasus']],
        df_prediksi.rename(columns={'jumlah_kasus': 'jumlah_kasus'})[['tahun', 'nama_kabupaten_kota', 'jumlah_kasus']]
    ])
    plt.figure(figsize=(14, 7))
    for nama in df_gabungan['nama_kabupaten_kota'].unique():
        data_kota = df_gabungan[df_gabungan['nama_kabupaten_kota'] == nama]
        plt.plot(data_kota['tahun'], data_kota['jumlah_kasus'], marker='o', label=nama, alpha=0.3)
    plt.title('Prediksi Jumlah Kasus HIV per Kabupaten/Kota (2018-2025)')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Kasus')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join('static', 'grafik_hiv.png'))
    plt.close()

    # Simpan ke file CSV
    df_prediksi.to_csv('hasil_prediksi_hiv.csv', index=False)
