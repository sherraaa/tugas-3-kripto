# Suslicious

![alt text](/assets/header.png "Krip-Chip Icon")
  
<p align="center">
Tugas 3 II44031 Kriptografi dan Koding : Implementasi Algoritma RSA untuk Simulasi Enkripsi pada Aplikasi Percakapan (Chat)
</p>

<p align="center">
18221121 Natasya Vercelly Harijadi - 18221121 Rozan Ghosani
</p>

<p align="center">
  <a href="#about">About</a> |
  <a href="#system-requirement">System Requirements</a> |
  <a href="#how-to-run">How to Run</a> |
  <a href="#apk-installation">APK Installation (Coming Soon)</a> |
  <a href="#features">Features</a>
</p>

## About
Program ini merupakan program Chatting App yang menerapkan algoritma RSA untuk mengenkripsi dan mendekripsi pesan dan file yang dikirimkan/diterima. Pesan akan dienkripsi menggunakan kunci publik penerima, lalu penerima akan mendekripsi pesan menggunakan kunci private milik penerima.

Program ini ditulis dalam bahasa Python yang dibantu dengan library Flet (Flutter) untuk membuat program kompatibel dengan sistem operasi Android.

## System Requirement

- Python 3.8 atau lebih baru.
- Library Flet versi terbaru
- Flutter SDK 3.16 atau lebih baru (apabila ingin melakukan build)
- Developer mode pada Windows 11
- Visual Studio Code

## How to Run
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


    Aplikasi dijalankan di komputer secara langsung
    ```sh
        flet run
    ```

    Aplikasi dijalankan di device Android melalui aplikasi [Flet](https://play.google.com/store/apps/details?id=com.appveyor.flet)
    ```sh
        flet run --android
    ```

    Aplikasi dijalankan di device iOS melalui aplikasi [Flet](https://apps.apple.com/app/flet/id1624979699)
    ```sh
        flet run --ios
    ```

### Building it Instead
Saat ini aplikasi Suslicious hanya dibuat kompatibel untuk dibuild di Android. Namun, aplikasi tetap bisa dijalankan di sistem operasi manapun dengan bantuan Flet. Untuk melakukan build pastikan requirements berikut ini sudah terinstall:

- Library Flet versi terbaru
- Flutter SDK 3.16 atau lebih baru (apabila ingin melakukan build)
- Developer mode pada Windows 11
- Visual Studio Code

Kemudian jalankan perintah berikut ini pada terminal di direktori `tugas-3-kripto/`

```sh
flet build apk
```

Tunggu 5-20 menit hingga aplikasi telah berhasil di-build

```
Creating Flutter bootstrap project...OK
Customizing app icons and splash images...OK    
Generating app icons...OK
Generating splash screens...OK
Packaging Python app...OK
Building .apk for Android...OK
Copying build to build\apk directory...OK
Success!
```

## APK Installation
Coming Soon! Aplikasi sedang di-build!

## Features
Program ini memiliki fitur:
- Login dan pendaftaran akun
- Berteman dengan siapapun
- Penerimaan pesan secara realtime
- Pengiriman pesan file terenkripsi
- Enkripsi pesan dengan menggunakan algoritma RSA
- Penampilan pesan plainteks dan cipherteks
- Kostumisasi kunci RSA