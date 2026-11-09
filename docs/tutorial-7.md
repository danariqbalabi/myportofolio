# Tutorial 07: Django REST Framework

Implementasi melanjutkan model, data, autentikasi session, dan halaman dari
tutorial sebelumnya. Projects adalah contoh utama; Gallery adalah bagian
pilihan tugas yang sudah memiliki AJAX, star, serta peran Editor.
Profil memakai data Danar yang sudah ada. Tidak ada model atau database baru.

## Menjalankan lokal

```sh
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Dependency mengikuti tutorial: Django `~=5.2` dan DRF `~=3.18.3`.
Versi yang diuji: Django 5.2.18, DRF 3.18.3.
Halaman utama tetap berada di `/`, `/experience/`, `/projects/`, `/gallery/`,
dan `/contacts/`. Data portofolio lama tetap digunakan.

## Kontrak API

| Resource | Daftar dan tambah | Detail, ubah, hapus | Toggle star |
| --- | --- | --- | --- |
| Projects | `/api/v1/projects/` | `/api/v1/projects/<uuid>/` | `/api/v1/projects/<uuid>/star/` |
| Gallery | `/api/v1/gallery/` | `/api/v1/gallery/<id>/` | `/api/v1/gallery/<id>/star/` |

Daftar menerima GET/HEAD dan POST. Detail menerima GET/HEAD, PUT/PATCH,
dan DELETE. Star hanya POST. OPTIONS tersedia tanpa mengubah data.
Pencarian nama menggunakan `?title=...`, tidak membedakan kapitalisasi.
Daftar kosong menghasilkan `[]` dengan 200, objek hilang menghasilkan 404.
GET/update/star berhasil dengan 200, create dengan 201, delete dengan body
kosong dan 204. Input tidak valid menghasilkan error per field dengan 400.

Objek JSON berbentuk datar: gunakan `id` dan `title`, bukan `pk`/`fields`.
`id`, `star_count`, `is_starred`, dan `starred_by_names` hanya bisa dibaca.
Nama akun pemberi star tetap tampil sesuai fitur sebelumnya; email,
password, dan objek User tidak dikirimkan oleh serializer.

| Peran | Baca | Star | Kelola Projects | Update Gallery | Tambah/hapus Gallery |
| --- | --- | --- | --- | --- | --- |
| Pengunjung | Ya | Tidak | Tidak | Tidak | Tidak |
| Pengguna biasa | Ya | Ya | Tidak | Tidak | Tidak |
| Editor | Ya | Ya | Tidak | Ya | Tidak |
| Superuser | Ya | Ya | Ya | Ya | Ya |

Status staff saja tidak memberi hak kelola. Permission diperiksa server,
bukan hanya melalui tombol yang disembunyikan. Star selalu menggunakan
`request.user`. SessionAuthentication menjaga CSRF pada operasi tulis.
Tidak ada `csrf_exempt` baru. Login portofolio tetap berfungsi;
`/api-auth/login/` menyediakan login untuk Browsable API.
Buka endpoint langsung untuk Browsable API, atau pakai `?format=json` /
header `Accept: application/json` untuk JSON.

## Integrasi frontend dan validasi

- Projects dan Gallery memakai API baru untuk daftar, tambah, star, dan hapus.
  Modal, toast, debounce 300 ms, loading/error/empty state, dan filter aktif
  setelah mutasi tetap dipertahankan. AbortController mengabaikan pencarian lama.
- Form edit Gallery mengirim PATCH ke API, termasuk ketika dipakai Editor.
  Form tambah mandiri Gallery juga menggunakan POST API. Halaman dan endpoint
  lama tetap ada untuk kompatibilitas dengan pekerjaan sebelumnya.
  Tugas 6 menambahkan modal edit langsung di Gallery; detailnya ada di
  [README bagian Tugas 6](../README.md#tugas-6).
- Projects dapat diubah memakai PUT/PATCH API; tautan halaman edit lama tetap
  tersedia untuk pemilik. Helper `writeProject` dan `projectEndpoint` tersedia
  di Console halaman Projects, mengikuti pola tutorial.
- Request tulis memakai JSON, header CSRF, serta pesan error DRF. DELETE 204
  tidak dipaksa dibaca sebagai JSON. Tombol dinonaktifkan selama request.
- Serializer membersihkan tag teks dan memvalidasi judul serta URL. Frontend
  tetap melakukan escaping dan membatasi protokol tautan/gambar HTTP/HTTPS,
  termasuk untuk data lama yang masuk melalui admin atau shell.
- Gambar Gallery menerima URL HTTP/HTTPS atau path `/static/...` yang sudah
  digunakan data lama; input HTML-nya disesuaikan agar edit foto lama tetap bisa.

## Pengujian

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test main.tests_api --verbosity 2
python manage.py test main contacts
```

Ada 13 tes API Projects sesuai panduan, ditambah tes Gallery dan regresi lama.
Total 51 tes Django lulus. Pemeriksaan migrasi tidak mendeteksi perubahan model.
Percobaan permission yang sengaja dilonggarkan dilakukan dengan mock di memori;
tes akses mendeteksi pelanggarannya. Percobaan tersebut tidak mengubah kode repo.

Untuk pengujian browser opsional:

```sh
python -m pip install playwright
python -m playwright install chromium
python manage.py test main.browser_checks contacts.browser_checks
```

Di Windows dengan Edge terpasang, set `$env:CONTACTS_BROWSER_CHANNEL = 'msedge'`
di PowerShell sebelum menjalankan uji browser. Lima tes browser portofolio
memeriksa CRUD, PATCH, star, filter, session/CSRF, Editor, error jaringan,
validasi dan XSS. Dua tes browser kontak memeriksa regresi Tutorial 06.
Test account hanya dibuat di database pengujian; tidak ada password produksi
yang disimpan dalam kode atau dokumentasi.

Catatan Tugas 6: jumlah tes bertambah dan tes browser Gallery kini memakai
modal edit. Gunakan perintah tes di atas untuk hasil terbaru, serta
`requirements-dev.txt` untuk memasang dependency pengujian browser.

## Deployment dan pengumpulan

Domain proyek: `https://danar-iqbal-myportofolio.pws.cs.ui.ac.id/`.
Domain ini sudah tercantum pada ALLOWED_HOSTS dan CSRF_TRUSTED_ORIGINS.
URL website berbeda dengan URL Git remote PWS; ambil remote dari dashboard
proyek PWS, tanpa menyimpan token dalam source code atau README.

Setelah remote `pws` serta autentikasi Git tersedia, deploy branch ini ke branch
`master` PWS sesuai Tutorial 01:

```sh
git push pws tutorial-7-drf:master
```

Periksa log build/migrasi PWS, lalu uji GET, login, dan operasi tulis di website.
Konfigurasi deployment tetap memakai environment proyek sebelumnya, termasuk
database produksi. Jangan upload database lokal, `.env`, atau virtual environment.

Untuk SCELE, gunakan tautan ke commit hasil akhir di GitHub, sesuai bagian
Pengumpulan tutorial. Repo sudah diperiksa bersifat publik. Pengumpulan SCELE
dan deployment membutuhkan akses layanan masing-masing; push GitHub saja
tidak menjalankan keduanya secara otomatis.
