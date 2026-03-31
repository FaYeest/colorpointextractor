# ColorPoint (Python)

Aplikasi desktop Python untuk mengekstrak warna dari gambar hingga level pixel.

## Fitur

- Upload gambar (bisa juga drag and drop)
- Pointer inspector + crosshair: saat cursor diarahkan ke gambar, warna pixel langsung terbaca dan crosshair mengikuti pixel
- Zoom gambar (scroll mouse), plus tombol `+`, `-`, dan `Reset Zoom`
- Menampilkan:
  - koordinat pixel
  - HEX
  - RGBA
  - nama warna (estimasi)
- Ekstraksi warna unik lengkap dengan jumlah pixel dan persentase
- Preview daftar pixel
- Tab **Semua Pixel** (virtual table) berisi HEX dan RGBA untuk seluruh pixel
- Dua mode highlight dari tab **Semua Pixel**:
  - hanya pixel yang dipilih
  - semua pixel dengan warna yang sama
- Dark mode switcher (tema tersimpan otomatis)
- Tombol **Panduan** + shortcut keyboard untuk alur kerja cepat
- Ekspor semua pixel ke CSV (`x`, `y`, `hex`, `nama_warna`, `r`, `g`, `b`, `a`)
- UI dengan gaya mirip macOS (rounded card, soft palette, typography)

## Instalasi

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Menjalankan

```bash
python app.py
```

## Cara pakai

1. Klik **Upload Gambar**.
2. Arahkan cursor ke area gambar untuk baca warna pixel real-time.
3. Gunakan scroll mouse atau tombol zoom untuk memperbesar area pixel.
4. Klik area gambar untuk memilih pixel di titik tersebut.
5. Cek tab **Warna Unik** untuk distribusi warna.
6. Cek tab **Preview Pixel** untuk daftar pixel (dibatasi agar UI tetap ringan).
7. Buka tab **Semua Pixel**, klik row pixel, lalu pilih mode highlight (pixel saja / warna sama).
8. Aktifkan tombol **Dark Mode** jika ingin tema gelap.
9. Klik **Ekspor CSV** untuk menyimpan seluruh data pixel.

## Shortcut

- `Ctrl+O`: upload gambar
- `Ctrl+S`: ekspor CSV
- `Ctrl+=`: zoom in
- `Ctrl+-`: zoom out
- `Ctrl+0`: reset zoom
- `Ctrl+L`: hapus highlight
- `Ctrl+D`: toggle dark mode
- `F1`: buka panduan cepat

## Catatan

- Untuk gambar sangat besar, proses ekstrak dan ekspor CSV bisa memakan waktu lebih lama.
- Nama warna bersifat pendekatan berbasis HSV, bukan kamus absolut.
