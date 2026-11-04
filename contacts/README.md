# Tutorial 06: Pengelola Kontak dengan HTMX

Aplikasi terpisah bernama `contacts` menggunakan namespace `contacts:` dan
template `templates/contacts/` agar tidak berbenturan dengan portofolio.

## Menjalankan

```sh
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Buka http://127.0.0.1:8000/contacts/ atau tautan Contacts pada navigasi
portofolio. Untuk data uji, tambahkan kontak melalui form halaman tersebut
atau Django admin setelah membuat superuser. Database lokal tidak disertakan
dalam commit. Pada deployment, jalankan migrasi terlebih dahulu.

## Implementasi panduan dan latihan

- Model `Contact` memiliki `name`, `email`, dan `phone` (opsional).
- Daftar dan pencarian nama memakai GET serta partial baris tabel. Pencarian
  menunggu 300 ms setelah input berubah dan tidak membedakan kapitalisasi.
- Tambah memakai POST, mengembalikan satu baris baru, dan menyisipkannya
  melalui `hx-swap="beforeend"`. Form hanya direset setelah berhasil.
- Pesan “Kontak berhasil ditambahkan!” memperbarui `#feedback` dengan
  `hx-swap-oob`, dalam respons yang sama dengan baris baru.
- Edit memakai GET untuk form di dalam tabel, PUT untuk menyimpan, dan GET
  untuk membatalkan. Input menggunakan atribut `form` agar HTML tetap valid.
- Hapus memakai DELETE, konfirmasi, `closest tr`, dan `outerHTML` dengan
  respons kosong berstatus 200. Pesan kosong muncul ketika baris terakhir hilang.
- Semua mutasi dilindungi CSRF. ModelForm memvalidasi data di server;
  respons 422 menampilkan kesalahan tanpa menyimpan data atau mereset form.
- Jika menambah saat pencarian aktif, pencarian dikosongkan dan daftar
  disegarkan agar seluruh kontak kembali terlihat. Request diserialkan
  melalui `hx-sync` agar hasil pencarian tidak menimpa mutasi yang berjalan.
- HTMX 2.0.11 disimpan lokal di `static/js/vendor/`, beserta lisensinya.
  Tidak perlu mengakses CDN saat menjalankan halaman.

## Pengujian

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Pengujian mencakup CRUD, pencarian, fragment/OOB, field telepon, Unicode,
validasi data, metode HTTP, kontak hilang, escaping HTML, dan CSRF.

Uji browser opsional (Playwright hanya untuk pengembangan):

```sh
python -m pip install playwright
python -m playwright install chromium
python manage.py test contacts.browser_checks
```

Uji ini memeriksa swap HTMX, tambah saat pencarian aktif, validasi 422,
edit/simpan/batal, dialog hapus, kondisi kosong, serta lebar layar seluler.
Untuk memakai Microsoft Edge yang sudah terpasang, set environment variable
`CONTACTS_BROWSER_CHANNEL=msedge` sebelum menjalankan uji browser.
