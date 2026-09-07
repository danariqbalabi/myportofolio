# Identitas Diri
Nama : Danar Iqbal Abi Zaidan Suharso
NPM : 2506534371
Kelas : PBP A
Bismillah A juga nilainya

# Portfolio Website


## About the Project

Tugas membuat portofolio pribadi static dengan HTML5 dan CSS3 (masih belum memakai database). Update website akan secara berkala

- Home:  hero section untuk intro, profile photo, CTA buttons (my newest update and contact), and social links
- About: short bio, NPM, informasi jurusan, and quick facts (location, interest, hobby)
- Experience: Timeline pengalaman kepanitiaan, ada expandable stat cards untuk latest updates and competition history (bisa di klik untuk expand informasinya)
- Education: Timeline riwayat pendidikan
- Featured Highlights: Highlight kegiatan terbaru seperti exchange, lomba, dll

Semua menggunakan html dan css tanpa javascripts

## Tech Stack

- HTML5 (semantic elements: `<section>`, `<article>`, `<dl>`)
- CSS3 (Grid, Flexbox, custom properties, no framework)
- Django (`manage.py runserver`) untuk templates and static files

## Setup

1. Clone repository
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. (Optional) Buat dan aktifkan virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run development server
   ```bash
   python manage.py runserver
   ```
5. Buka `http://127.0.0.1:8000` di browser

## Reflective Questions

### Tugas 1

1. Iya, dalam pengerjaan tugas 1 kemarin saya menggunakan elemen semantik HTML5 seperti `<section>` untuk memisahkan tiap bagian halaman (Home, About, Experience, Education, Featured Highlights), `<article>` untuk item yang berdiri sendiri secara konten (kartu About, kartu Featured Highlights), dan `<dl>`/`<dt>`/`<dd>` untuk data key value seperti NPM dan Program. Elemen2 ini membantu saya menjaga struktur HTML tetap jelas maknanya (bukan cuma `<div>` semua) sehingga meningkatkan readibility, memudahkan saya sendiri saat membaca ulang kode setelah beberapa hari, dan juga membantu styling CSS karena saya bisa menarget elemen berdasarkan struktur khususnya, bukan hanya class.

2. Menurut saya, tantangan terbesar yang saya temui adalah ketika grid dua kolom (misalnya di section About dan Experience) tidak otomatis menyempit jadi satu kolom di layar kecil, padahal saya sudah menulis media query. Setelah dicoba atur ulang berkali-kali akhirnya saya menemukan penyebabnya adalah urutan penulisan CSS. Beberapa aturan default untuk grid saya tulis ulang setelah blok `@media`, sehingga aturan itu nimpa balik aturan mobile karena CSS dibaca dari atas ke bawah. Ini menjadi ilmu baru bagi saya, karena ternyata urutan penulisan class itu penting agar tidak ada tumpang tindih. Saya juga sempat salah memberi nama class antara versi awal dan versi refactor (.about-grid dan .about-layout), yang membuat media query tidak pernah kepakai. Setelah saya otak-atik beberapa kode tetap tidak bisa, ternyata dari sini saya belajar untuk selalu meletakkan semua media query di paling bawah file dan konsisten menjaga penamaan class saat melakukan refactor. Untuk menentukan elemen mana yang perlu diubah posisinya di mobile, saya mengevaluasi lewat DevTools (pakai inspect ukuran HP), elemen yang menyebabkan scroll horizontal atau teks terlalu sempit itu yang saya prioritaskan untuk diubah jadi satu kolom atau ukurannya diperkecil saja

3. Karena murni static web, saya tidak bisa menyimpan atau mengambil data secara dinamis. Semua konten (misalnya daftar pengalaman dan lomba) harus ditulis manual di HTML. Ini terasa terbatas terutama untuk section seperti Experience dan Featured Highlights yang isinya akan terus bertambah seiring waktu, dan harus diubah manual, apalagi  perlu effort cukup banyak jika memiliki list experience atau news yang banyak, lalu setiap update saya harus edit HTML langsung. Saya juga tidak bisa membuat form kontak yang benar-benar mengirim pesan, atau menyimpan preferensi pengguna (misalnya foto avatar yang terakhir dipilih). Untuk iterasi proyek selanjutnya, fungsionalitas dinamis yang paling ingin saya tambahkan adalah BE dengan database (misalnya pakai Django models) supaya saya bisa add/edit pengalaman dan project lewat admin panel tanpa harus ubah ulang kode HTML.

## AI Disclosure

Saya menggunakan bantuan Codex sebagai peneman selama mengerjakan tugas ini. Berikut rincian bagian yang saya kerjakan dan yang saya minta bantuan AI:

Dibantu AI:
- Meminta AI menjelaskan ulang setiap part kode awal setelah menyelesaikan Tutorial1 agar saya paham setiap bagiannya.
- Menanyakan beberapa fungsi yang belum pernah saya pakai seperti <ul>, <li>, dll.
- Menjelaskan konsep CSS Grid `grid-template-areas`, general sibling selector (`~`), dan teknik checkbox/radio + CSS untuk membuat interaktivitas (avatar switcher, panel Experience/Competition yang bisa diklik) tanpa JavaScript
- Membantu debugging seperti mismatch nama class antara HTML dan CSS (.about-grid vs .about-layout)
- Membantu mencari bug seperti </div> yang belum ditutup dan salah urutan pada file
- Brainstorming konsep apa aja yang perlu diubah di kode ketika membuat section atau design yang belum pernah dibuat sebelumnya

Dikerjakan/diputuskan sendiri:
- Menentukan konsep utama, rancangan, dan tata letak halaman.
- Mengisi seluruh data personal (bio, NPM, pengalaman, riwayat lomba, riwayat pendidikan)
- Melakukan proses debugging awal secara mandiri (menyalakan DevTools, resize viewport, screenshot) sebelum meminta bantuan AI untuk mendiagnosis penyebab pastinya
- Keputusan desain akhir (tata letak, section mana yang ditambahkan, apa isi tiap kartu)
- Selalu mengerjakan manual terlebih dahulu, jika sudah buntu atau ada bug yang tidak terdeteksi biasanya saya minta bantuan Codex untuk mencari penyebabnya (bukan solve langsung pada kode)

Strategi prompting yang saya pakai biasanya saya selalu menulis kode manual, lalu jika ada yang belum saya pahami, saya minta bantuan AI untuk menjelaskan atau memberi referensi. Sisanya saya eksplor sendiri agar sesuai dengan keinginan saya.

Berikut link log prompting AI Codex:
https://chatgpt.com/s/cx_6a9ab968b70081919d0fd2929858b34c
https://chatgpt.com/s/cx_6a9e783cc14081919fccda9a703426ac