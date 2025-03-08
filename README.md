## 🛠️ Instalasi

Pastikan kamu sudah menginstal Python di komputermu. Ikuti langkah berikut untuk menjalankan dashboard:

### 1. Clone repositori atau pindahkan file ke direktori kerja

```bash
cd path/ke/folder
```

### 2. Buat Virtual Environment (Opsional, Tapi Disarankan)

```bash
python -m venv env
```

#### _Aktifkan Virtual Environment_

- **Untuk Mac/Linux:**
  ```bash
  source env/bin/activate
  ```
- **Untuk Windows:**
  ```bash
  env\Scripts\activate
  ```

### 3. Instal Dependensi

```bash
pip install -r requirements.txt
```

## 🚀 Menjalankan Dashboard

Jalankan perintah berikut di terminal atau command prompt:

```bash
streamlit run dashboard/dashboard.py
```

## 📂 Struktur Folder

```
submission/
│── dashboard/
│   │── dashboard.py
│   │── all_data.csv
│   │── data/
│   │   │── day.csv
│   │   │── hour.csv
│   │── requirements.txt
│── README.md
```

## 🔧 Catatan

- Pastikan file `day.csv` dan `hour.csv` berada di dalam folder `data/`
- Pastikan file `dashboard.py` ada di dalam folder `dashboard/`
- Jika ada error _module missing_, jalankan kembali:
  ```bash
  pip install -r requirements.txt
  ```
