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

## Setup Minggu 1

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



### About the Project MINGGU 2

Website portofolio pribadi yang sekarang sudah dibangun menggunakan Django, HTML, CSS, JavaScript, dan database SQLite.

- Home: profil singkat, foto, NPM, program studi, tombol CTA, dan social links.
- Experience: daftar pengalaman yang diambil dari model `Experience`.
- Highlights: daftar pencapaian dan kegiatan dari model `Highlight`.
-*Gallery: kumpulan foto-foto koleksi dan aktivitas dari model `GalleryItem`.

Data pada halaman Experience, Highlights, dan Gallery disimpan di database dan ditampilkan melalui Django view serta template.


### Setup Minggu 2
1. Aktifkan virtual environment:
   ```bash
   env\Scripts\activate
2. Jalankan migrasi database: python manage.py migrate
3. Jalankan server: python manage.py runserver
4. Buka web di local http://127.0.0.1:8000
5. Jalankan test:
python manage.py check
python manage.py test

Page URL baru
/experience/
/highlights/
/gallery/

### Tugas 2
1. Alur ketika membuka halaman portofolio baru:
- Ketika user membuka halaman portofolio saya yang terbaru, browser mengirimkan HTTP request ke alamat URL, misalnya `/gallery/` atau `/highlight/`
- Request tersebut akan langsung diterima oleh `portofolio/urls.py` sebagai URL configuration utama project porto ini. Pada file tersebut, pola URL kosong diarahkan ke `main.urls` menggunakan `include("main.urls")` yg tersedia.
- Lalu, Django mencari pola URL yang sesuai di `main/urls.py`. Contohnya utk alamat `/gallery/`, Django menemukan named route `show_gallery` yang mengarah ke function view `show_gallery` di `main/views.py`.
- View kemudian mengambil data dari model `GalleryItem` menggunakan query: ```python GalleryItem.objects.all().order_by("-featured", "-year")
- Data tersebut akan masuk ke context dengan nama (contohnya) gallery_items, lalu dikirim ke template gallery.html menggunakan fungsi render().
- Di dalam gallery.html, Django Template Language melakukan perulangan terhadap gallery_items. Setiap objek ditampilkan sebagai kartu gallery yang berisi judul, caption, lokasi, tahun, dan gambar. Jika tidak ada data, bagian {% empty %} menampilkan pesan bahwa belum ada foto di gallery.
- Setelah template selesai diproses, Django mengirimkan HTML sebagai HTTP response kepada browser. Browser kemudian merender HTML tersebut dan memuat file CSS serta gambar dari folder static sehingga halaman dapat ditampilkan secara utuh.
- Pola ini repetitif dan akan sama pada page lain seperti experience dan highlights yang saya tambahkan

2. Alasan menggunakan model:
Data portofolio sebaiknya disimpan di dalam model dan tidak ditulis secara hardcode lgsg di dalam template karena model berfungsi sebagai representasi data di db. Dengan cara ini, isi portofolio dapat diubah, ditambah, atau dihapus tanpa harus mengubah kode HTML satu-persatu yang berpotensi menimbulkan risiko eror.

Jika input ditulis langsung di template, setiap perubahan informasi mengharuskan developer membuka dan mengedit file HTML. Cara tersebut kurang efisien dan lebih mudah menyebabkan kesalahan, terutama ketika jumlah data semakin banyak.

Dengan menggunakan model, data dapat dikelola melalui Django Admin atau sistem lain (seperti python migration) yang terhubung dengan database. Template hanya bertugas menampilkan data menggunakan perulangan, sehingga kode menjadi lebih bersih dan terpisah antara data, logika aplikasi, dan tampilan.

3. Perbedaan makemigrations dan migrate
Command makemigrations digunakan untuk membuat berkas migrasi berdasarkan perubahan pada model. Berkas tersebut berisi instruksi perubahan struktur db yang perlu dilakukan oleh Django.

Perintah migrate digunakan untuk menerapkan berkas migrasi tersebut ke db. Dengan menjalankan migrate tsb, tabel atau kolom baru benar-benar dibuat atau diubah di dalam database yang ada.

Contoh ketika saya menambahkan model GalleryItem dengan field title, caption, location, year, dan image, saya harus run:
makemigrations membuat berkas migrasi baru, sedangkan migrate menerapkan perubahan tersebut ke database sehingga data GalleryItem dapat disimpan dan digunakan oleh view.

### Tentang AI
Saya menggunakan bantuan CODEX AI  untuk membantu solve problem yang sedikit sulit terjangkau secara manual seperti:
- Mencari bug dari kode baru
- Mencari informasi apakah suatu ide possible untuk diterapkan
- Membantu dalam javascript

Saya banyak menyusun kode ini secara mandiri tanpa AI pada bagian:
- Brainstorming dan ide project
- Coding manual, jika terdesak atau tidak works saya minta crosscheck ke AI

https://chatgpt.com/s/cx_6aa7b6345100819186c6964a7cc1c47d


### About The Project MINGGU - 3
Jadi di minggu ketiga ini website portofolio pribadi sudah dikembangkan dengan menambahkan fitur form dan data delivery menggunakan Django. Pada tahap ini kita harus melakukan refactoring terhadap halaman HTML yang memiliki struktur sama dengan menggunakan template inheritance (`base.html`) sehingga navbar, footer, dan struktur utama tidak perlu ditulis berulang pada setiap halaman.

Fitur baru yang ditambahkan:
- Form untuk menambahkan data baru menggunakan Django ModelForm.
- Fitur update/edit data menggunakan form berdasarkan id data yang dipilih.
- Fitur delete data untuk menghapus data dari database.
- Penyediaan data portofolio dalam format JSON melalui view Django.
- Deserialisasi data JSON agar data dapat kembali digunakan oleh aplikasi.

Bagian portofolio yang dikembangkan menggunakan fitur ini adalah:
- Projects: data proyek dapat ditambahkan, diperbarui, dihapus, serta tersedia dalam format JSON.
- Highlights: data pencapaian/kegiatan dapat dikelola secara dinamis melalui database.

Dengan implementasi ini, data portofolio tidak lagi ditulis secara hardcode di HTML, tetapi sudah tersimpan dalam database dan dapat dikelola melalui sistem Django.

### Setup Minggu 3
1. Aktifkan virtual environment:
```bash
env\Scripts\activate

2. Pastikan dependencies udah aktif:
'''pip install -r requirements.txt'''

3. Jalankan migrasi db:
python manage.py makemigrations
python manage.py migrate

4. Jalankan checker Django
python manage.py check

5. Run serve Django:
python manage.py runserver

6. Buka website lewat local:
'''http://127.0.0.1:8000'''


### Setup Minggu 3

1. Jelaskan mengapa menggunakan ModelForm dan mengapa perlu menambahkan {% csrf_token %} pada form.
Saya menggunakan ModelForm dibandingkan membuat form HTML secara manual karena ModelForm memudahkan proses pembuatan form dengan cara ambil lansgung struktur field dari model yang sudah dibuat sebelumnya, seperti Highlight / Project. Sehingga saya tidak perlu menuliskan setiap elemen <input> secara manual lagi. Selain itu, validasi data juga otomatis mengikuti tipe field yang ada di model. Misalnya field year akan divalidasi sebagai angka dan field seperti thumbnail atau URL akan mengikuti aturan validasi URL yang sudah tersedia di Django.

Saya juga menambahkan {% csrf_token %} pada setiap form karena Django membutuhkan token tsb untuk memastikan bahwa request POST yang dikirim benar-benar berasal dari halaman website saya sendiri. Token ini digunakan untuk mencegah serangan CSRF yaitu kondisi ketika website lain mencoba mengirim request palsu menggunakan sesi pengguna yang sedang aktif. Dengan adanya CSRF token, Django dapat memverifikasi bahwa data yang dikirim berasal dari sumber yang valid sehingga proses CRUD menjadi lebih aman.

2. Mengapa JSON lebih sering digunakan dibandingkan XML dalam pengembangan web modern?
JSON lebih banyak digunakan dalam pengembangan web modern karena memiliki struktur yang lebih sederhana dan bisa dimengerti dibandingkan XML. Pada XML, setiap elemen harus memiliki tag pembuka dan penutup sehingga ukuran data yang dikirim cenderung lebih besar. Sementara itu, JSON menggunakan format pasangan key-value sehingga lebih ringkas dan lebih cepat dikirim melalui jaringan.

Selain itu, JSON sangat mudah dicombine dengan JS karena dapat langsung dikonversi menjadi object menggunakan fungsi seperti JSON.parse(). Hal ini membuat JSON lebih cocok digunakan pada sisi frontend, terutama dalam komunikasi antara client dan server. Berbeda dengan XML yang biasanya membutuhkan proses parsing tambahan. Hampir semua bahasa pemrograman modern juga sudah mendukung JSON sehingga format ini sering digunakan dalam pembuatan REST API untuk pertukaran data antara aplikasi, server, maupun frontend.

3. Jelaskan alur ketika view mengembalikan data dalam bentuk JSON dan alasan perlu melakukan serialization.
Ketika view mengembalikan data dalam bentuk response JSON, prosesnya dimulai dengan mengambil data dari database melalui model Django. Misalnya pada bagian project, saya mengambil data menggunakan Project.objects.all(), sedangkan pada bagian highlights menggunakan Highlight.objects.all().

Data yang diambil tersebut masih berupa objek Django, sehingga belum bisa langsung dikirim sebagai response HTTP. Oleh karena itu, dilakukan proses serialization menggunakan serializers.serialize("json", queryset) untuk mengubah objek Django tsb ke format JSON yang dapat dibaca oleh browser atau aplikasi lain. Setelah berhasil diubah menjadi JSON, data tersebut dikirim melalui Http Response dengan content_type="application/json" agar client mengetahui bahwa response yang diterima berupa data JSON, bukan halaman HTML biasa lagi

Serialization diperlukan karena objek model Django memiliki struktur khusus yang hanya dipahami oleh Python dan Django, seperti hubungan dengan database serta method tertentu. Dengan serialization, data tersebut diubah menjadi format teks yang lebih umum sehingga dapat digunakan oleh berbagai platform atau bahasa pemrograman lain. Dan sebaliknya, ketika data JSON ingin digunakan kembali dalam aplikasi, proses deserialization dilakukan untuk mengubah data JSON kembali menjadi objek yang dapat diakses dalam Django. Dengan begitu, data seperti project.title atau highlight.year dapat digunakan kembali dan ditampilkan pada template website.

### AI DISCLOSURE
Pada minggu ini saya menggunakan Claude untu:
- Membantu debug error pada tutorial3 dan tugas3 ketika data primary.id mengalami mismatch.
- Membantu debug navbar yang tidak konsisten dan error ditampilan local host
- Membantu debug ketika ada typo dalam code yang tidak terdeteksi secara manual
https://claude.ai/share/0eadd853-5eea-4920-aa15-7a2d0392b5ea

Sisanya saya melakukan explore sendiri karena tutorial3 sudah memberikan instruksi dengan jelas, dan tugas3 hanya melanjutkan tutorial3 saja.


### About The Project MINGGU - 4

Pada minggu 4 ini website portofolio pribadi kita dikembangkan dengan fitur autentikasi, otorisasi, session, cookie, role permission, dan fitur star pada project.

Fitur baru yang ditambahkan:
- Register, login, dan logout menggunakan sistem autentikasi bawaan Django
- Navbar menampilkan status login dan register utk pengguna
- Cookie `last_login` disimpan saat login dan dihapus saat logout
- Pembatasan akses server-side menggunakan `@login_required`, `PermissionDenied`, superuser, dan group `Editor`
- Role `Editor` dapat mengubah data portfolio, tetapi tidak dapat membuat atau menghapus data
- User biasa dapat membaca data dan memberi/membatalkan star pada project
- Superuser sebagai pemilik portfolio dapat membuat, mengubah, dan menghapus data
- Tombol create, edit, dan delete disembunyikan dari pengguna yang tidak memiliki hak akses tertentu

Hak akses yang diterapkan per role nya:
- Pengunjung tanpa login (guest): dapat membaca halaman portfolio, tetapi diarahkan ke login saat mencoba sesuatu yang membutuhkan login
- User: dapat membaca data dan memberi/membatalkan star
- Editor: dapat membaca dan mengubah data portfolio, tetapi tidak dapat membuat atau menghapus data
- Superuser: dapat melakukan semua fitur CRUD (create, read, update, dan delete)

### Setup Minggu 4

1. Aktifkan virtual environment:
```bash
env\Scripts\activate
```

2. Jalankan migrasi database:
```bash
python manage.py migrate
```

3. Jalankan checker Django:
```bash
python manage.py check
```

4. Jalankan server:
```bash
python manage.py runserver
```

5. Buka website:
```bash
http://127.0.0.1:8000
```

### Catatan Role Editor

Migration `0010_create_editor_group` membuat group bernama `Editor`. Untuk memberikan akses  ke editor:

1. Login ke Django Admin sebagai superuser
2. Buka menu Users
3. Pilih user yang ingin dijadikan editor
4. Masukkan user tersebut ke group `Editor`
5. Simpan perubahan

Setelah itu user tersebut dapat melihat tombol edit dan mengubah data, tetapi tetap tidak dapat melihat tombol tambah atau hapus.

### Reflective Questions Tugas 4

1. Mengapa pembatasan akses harus dilakukan di view/server-side, bukan hanya menyembunyikan tombol di template?

Menyembunyikan tombol di template hanya mengubah tampilan dan bukan fitur keamanan. Pengguna masih bisa mengetik URL secara langsung, misalnya `/projects/add/` atau masuk endpoint delete tertentu. Karena itu, validasi hak akses harus tetap dilakukan di view menggunakan `@login_required` dan pengecekan role. Template tsb hanya berfungsi agar UI lebih rapi dan tidak menampilkan aksi yang memang tidak bisa digunakan

2. Apa perbedaan user biasa, editor, dan superuser pada implementasi ini?

User biasa hanya dapat membaca data dan memberi star pada project. Editor memiliki hak tambahan untuk mengubah data portfolio, tetapi tidak boleh membuat atau menghapus data. Superuser dianggap sebagai pemilik portfolio, sehingga dapat membuat, mengubah, dan menghapus data. Pembagian ini membuat perubahan data lebih terkontrol karena setiap role hanya mendapat akses sesuai kebutuhan

3. Mengapa fitur star menggunakan `ManyToManyField` ke model `User`?

Satu project dapat diberi star oleh banyak user, dan satu user juga dapat memberi star ke banyak project. Relasi seperti ini cocok menggunakan `ManyToManyField`. Dengan relasi tersebut, Django juga mencegah duplikasi relasi yang sama, sehingga satu user tidak bisa memberi star berkali-kali pada project yang sama

### AI DISCLOSURE MINGGU 4

Pada minggu ini saya menggunakan bantuan Codex dengan log prompt yg sama untuk:
- Mengecek kembali isi instruksi Tugas4 dan membedakannya dari instruksi di file PDF, apakah lanjutan dari Tutorial4 saja atau ada yang harus ditambahkan
- Membantu debugging error `runserver` dan error URL import
- Membantu mengecek kesesuaian Tutorial 4 dan Tugas 4 terhadap kode yang sudah dibuat
- Membantu debug role `Editor`, pembatasan akses server-side, update project, dan penyesuaian tombol di template.

Bagian yang tetap saya tentukan sendiri:
- Struktur halaman portfolio yang ingin digunakan tetap berdasarkan apa yagn sudah saya buat dan saya ingingkan
- Review akhir terhadap fitur yang muncul di halaman portfolio.
- Manual coding mengikuti instruksi di Tutorial4

AI LOG: https://chatgpt.com/s/cx_6aba196bbb448191b5da91e32978a3f5


### About The Project MINGGU - 5

Di minggu 5 ini web portofolio pribadi dikembangkan dengan penambahan JS dan AJAX. Bagian yang saya kembangkan untuk tugas ini adalah section page Gallery, karena halaman Projects sudah digunakan sebagai contoh pada tutorial 5

Fitur baru yang ditambahkan:
- Data Gallery dimuat menggunakan AJAX melalui endpoint `/api/gallery/`
- Search Gallery berdasarkan judul foto berjalan tanpa reload halaman
- Search menggunakan debouncing agar request tidak dikirim setiap kali user mengetik satu huruf
- Form tambah foto Gallery ditampilkan di dalam modal pada halaman Gallery
- Penambahan foto dilakukan menggunakan Fetch API ke endpoint `/gallery/add-ajax/`
- Setelah foto berhasil ditambahkan, daftar Gallery diperbarui tanpa reload halaman
- Toast ditampilkan ketika tambah foto berhasil atau gagal
- Gallery memiliki fitur star seperti Projects, lengkap dengan jumlah star dan status star user saat ini
- Data yang dirender lewat JavaScript di-escape menggunakan `escapeHtml`
- Input teks Gallery dibersihkan di sisi server menggunakan `strip_tags` pada `GalleryItemForm`

### Setup Minggu 5

1. Aktifkan virtual environment:
```bash
env\Scripts\activate
```

2. Jalankan migrasi database:
```bash
python manage.py migrate
```

3. Jalankan checker Django:
```bash
python manage.py check
```

4. Jalankan server:
```bash
python manage.py runserver
```

5. Buka halaman Gallery:
```bash
http://127.0.0.1:8000/gallery/
```

6. Untuk mencoba fitur tambah foto, login sebagai superuser terlebih dahulu. User biasa dan guest tetap dapat melihat data Gallery, tetapi tidak dapat menambahkan data.

### Tugas 5

1. Debouncing adalah cara menunda eksekusi fungsi sampai user berhenti melakukan input selama durasi tertentu. Pada fitur pencarian AJAX, debouncing sangat penting karena tanpa debounce browser akan mengirim request untuk setiap karakter yang diketik. Misalnya ketika user mengetik kata `bangkok`, aplikasi bisa mengirim banyak request berurutan ke server. Dengan debouncing, request hanya dikirim setelah user berhenti mengetik sebentar, misalnya 300 ms. Ini membuat fitur search tetap terasa responsif, tapi juga lebih hemat request dan tidak membebani server

2. `await` digunakan untuk menunggu proses asynchronous selesai sebelum kode lanjut ke line berikutnya. Saat memakai `fetch()`, browser mengirim request ke server dan butuh waktu sampai response diterima. Dengan `await`, kode seperti `const response = await fetch(url)` akan menunggu response dulu, lalu baru menjalankan proses berikutnya seperti `await response.json()`. Jika tidak menggunakan `await`, variabel yang didapat masih berupa Promise, bukan data response yang sudah selesai. Akibatnya kode bisa mencoba membaca data sebelum request selesai dan menyebabkan error atau hasil yang tidak sesuai

3. XSS atau Cross-Site Scripting adalah serangan ketika penyerang menyisipkan script berbahaya ke halaman web agar dijalankan di browser pengguna lain. Data yang ditampilkan lewat AJAX/JavaScript lebih rentan jika kita memasukkan data ke halaman menggunakan `innerHTML`, karena browser akan memperlakukan string tersebut sebagai HTML sungguhan. Pada template Django biasa, variabel seperti `{{ title }}` otomatis di-escape sehingga tag HTML berbahaya tampil sebagai teks. Namun ketika data JSON dirender manual dengan JavaScript, perlindungan auto-escape Django tidak berlaku. Karena itu, setiap data dari JSON yang dimasukkan ke HTML harus di-escape dengan fungsi seperti `escapeHtml`, dan input teks juga dibersihkan di server menggunakan `strip_tags`

### AI DISCLOSURE MINGGU 5

Pada minggu ini saya menggunakan bantuan Codex untuk:
- Membaca instruksi Tugas 5 dari PDF dan membedakan instruksi tugas dari instruksi pengguna
- Memecah pengerjaan menjadi commit bertahap agar riwayat Git lebih rapi
- Membantu debugging masalah Git permission di folder OneDrive saat commit

Bagian yang tetap saya tentukan sendiri:
- Memilih Gallery sebagai bagian portofolio yang dikembangkan untuk Tugas 5
- Menentukan isi data portofolio dan arah tampilan halaman
- Melakukan review hasil akhir di browser lokal
- Menentukan kapan setiap tahap harus di-commit agar sesuai kebutuhan pengumpulan bertahap
- Coding based on tutorial 5

Strategi prompting yang saya gunakan adalah meminta Codex mengecek instruksi terlebih dahulu, lalu mengerjakan fitur per tahap sendiridan melakukan commit yg punya cakupan yang jelas. Saya juga meminta Codex menjalankan test setelah setiap tahap supaya bug dapat ditemukan sebelum push ke GitHub atau PWS.

https://chatgpt.com/s/cx_6aa7b6345100819186c6964a7cc1c47d
