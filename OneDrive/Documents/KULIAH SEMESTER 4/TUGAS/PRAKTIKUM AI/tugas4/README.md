# Prediksi Kasus HIV Jawa Barat dengan ANN

Program ini memprediksi jumlah kasus HIV di kabupaten/kota Jawa Barat menggunakan Artificial Neural Network (ANN) berbasis TensorFlow/Keras.

## Isi Proyek
- `prediksi_hiv_ann.py` — Script Python untuk prediksi kasus HIV
- `dinkes-od_18510_jumlah_kasus_hiv_berdasarkan_kabupatenkota.csv` — Dataset (2018–2023)
- `requirements.txt` — Daftar library Python yang dibutuhkan
- `templates/base.html` — Template HTML dasar (Bootstrap, untuk pengembangan web ke depan)
- `static/` — Folder untuk file statis (CSS/JS, masih kosong)

## Cara Menjalankan
1. **Aktifkan virtual environment (opsional tapi disarankan):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
2. **Install library yang dibutuhkan:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan script prediksi:**
   ```bash
   python prediksi_hiv_ann.py
   ```

Hasil prediksi untuk tahun 2024 dan 2025 akan ditampilkan dalam bentuk tabel di terminal.
