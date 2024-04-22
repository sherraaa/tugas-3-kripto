# Suslicious
Tugas 3 II44031 Kriptografi dan Koding : Implementasi Algoritma RSA untuk Simulasi Enkripsi pada Aplikasi Percakapan (chat)
18221121 Natasya Vercelly Harijadi - 18221121 Rozan Ghosani

## About
Program ini merupakan program chatting yang menerapkan algoritma RSA untuk mengenkripsi dan mendekripsi pesan dan file yang dikirimkan/diterima. Pesan akan dienkripsi menggunakan kunci publik penerima, lalu penerima akan mendekripsi pesan menggunakan kunci private milik penerima.

## How to Use
### Cloning repository
1. Pada halaman utama repository [GitHub](https://github.com/sherraaa/tugas-3-kripto), buka menu **Clone** lalu salin URL dari repository
2. Buka Terminal
3. Pindah ke direktori yang diinginkan
4. Ketikan `git clone`, lalu tempelkan URL yang telah disalin tadi 
   ```sh
   git clone https://github.com/sherraaa/tugas-3-kripto.git
   ```

### Running the app
1. Pindah ke directory `tugas-3-kripto`
2. Install depedencies yang diperlukan
```sh
pip install -r requirements.txt
```
3. Jalankan app dengan cara
```sh
flet main.py
```