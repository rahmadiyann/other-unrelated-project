# Jobdesc Operation and Supply Chain Intern

![Sarwa](https://manggalla.com/beta/wp-content/uploads/2023/02/Logo-SMR-1.png)

## Tugas Utama:

Berurutan mulai dari pagi - sore. Silahkan diatur sesuai kebutuhan

1. Pisahkan dokumen balikan hari sebelumnya per segmen market dan digitalisasi/filing dokumen balikan.
   
2. Sales Order(SO) masuk dari Sales & Marketing (SM):
   - Input (SO) di [Wordpress Preorder](https://manggalla.com/sarwa/pesanan/)
   - SO SF: Pisahkan lembar hijau dari SO besar dan faktur, lalu input di wordpress preorder untuk SO besar dan [Wordpress Wellness Administrasi](https://manggalla.com/wellness/administrasi/) untuk faktur.
     - Berikan SO besar ke Finance, Accounting, and Tax(FAT) (Bu Hotma) untuk FAT check.
     - Setelah FAT check di ACC, info ke Pak Dany atau Pak Rafli untuk dibuatkan Surat Jalan (SJ).
     - Cap TTD dan Logo SMR di tiap lembar SJ.
     - TTD Apoteker Penanggung Jawab (APJ).
     - Turunin SJ ke gudang untuk dikirim.
     - Validasi preorder di [Wordpress Validasi Pesanan](https://manggalla.com/sarwa/validasi-pesanan/).
   - SO SD & GB-SD: Input di wordpress preorder.
     - FAT check ke Bu Hotma.
     - Apabila SO dikembalikan, SIMPAN sampai diminta lagi.
     - Info print SJ.
     - Cap TTD dan Logo SMR.
     - TTD APJ.
     - Turunkan ke gudang untuk dikirim.
     - Validasi di Wordpress Validasi Pesanan.
   - SO SM, MR, MS, DIY: Input di wordpress preorder.
     - FAT check ke Bu Atika.
     - Info print SJ.
     - Cap TTD dan Logo SMR.
     - Untuk DIY, cabut lembar Purchase Order(PO) dari SO dan straple ke SJ.
     - TTD APJ.
     - Turunkan ke gudang untuk dikirim.
     - Validasi di Wordpress Validasi Pesanan. (PASTIKAN MR, DIY dibuat invoicenya oleh FAT)
   - SO MT: Input di wordpress preorder.
     - FAT check ke Pak Geren.
     - Perhatikan mana SO yang di ACC, bisa di cek di [Logbook](https://docs.google.com/spreadsheets/d/1pcjYibnJNEp1jow9mpJSb63-fyGkOAodVwL1WblVtpM/edit#gid=642080019).
     - Info print SJ untuk SO yang di ACC.
     - Gabungkan lembar PO dan SJ, untuk beberapa customer tertentu diperlukan invoice.
     - Berikan SJ dan SO ke FAT untuk dibuatkan invoice. [List customer](#list-customer-mt-yang-memerlukan-invoice)
     - Cap TTD dan Logo SMR di tiap lembar SJ dan SO.
     - Turunkan ke bawah untuk dikirim.
     - Validasi di Wordpress Validasi Pesanan.
   - SO SF Cirebon & Bandung (SF/CRB & SF/BDG): Sama seperti SO SF, namun FAT check ke Bu Atika.

3. Input surat jalan lembar kuning ke [Outbound](https://manggalla.com/sarwa/outbound/)
    - Satu batch no satu inputan
    - SJ time hari itu jam 9
    - Invoice time hari itu jam 9.30
    - No plat nomor, tergantung driver. Lihat ke [Nama dan Plat Nomor Driver](#nama-dan-plat-nomor-driver)

4. Print Laporan Harian Driver.
[Link Document Manual](https://docs.google.com/document/d/1ZoA9T7PFwKXfAMxYduhBhbF7nA1RbRKW/edit?usp=sharing&ouid=111421654737140850251&rtpof=true&sd=true)

## Panduan Filing/Digitalisasi Dokumen Balikan:

### SD, SF JKT, GB-SD:
- Ketik di excel.
- Print table excel.
- Berikan semua dokumen ke FAT (Bu Hotma).
- TTD penerimaan dokumen balikan.

### SF BDG/CRB, MR, DIY:
- Ketik di excel.
- Input invoice time bila ada.
- Print table excel.
- Berikan semua dokumen ke FAT (Bu Atika).
- TTD penerimaan dokumen balikan.

### MT:
- Ketik di excel.
- Print table excel.
- Berikan semua dokumen ke FAT (Pak Geren) atau FAT intern.
- TTD penerimaan dokumen balikan.

## Automasi

Sangat disarankan menggunakan otomisasi input preorder, validasi, dan balikan dokumen.
Refer ke [WPAutomate](https://github.com/rianying/WPAutomate)

## Panduan Pengembalian Dokumen SO:

1. Urutkan file yang terbesar sampai terkecil berdasarkan nomor SO.

2. Pisahkan SO berdasarkan warna lembar:
   - Slip Putih = FAT
   - Slip Merah = S&M
   - Slip Kuning = OSC
   - Slip Hijau = OSJ

## List Customer MT yang memerlukan invoice:
- PT. Gogobli (Term Payment: COD)
- Masiva Guna
- Manna Manca
- Sumber Hidup Sehat/Vivahealth
- Ka Dua Empat
- Anugrah Argon Medica
- CV Kreasi Sukses Makmur
- PT. Teknologi Medika Pratama
- PT. Era Caring
- Kimia Farma

## Jam-jam penting:
- Jam 11.00: Pengiriman pagi untuk SF dan MT dalam kota. Biasanya PO dari PT. Sumber Alfaria Trijaya (SAT) datang dan akan dikirim di jam 11.00 di hari yang sama.
- Jam 15.00: Penjemputan barang untuk PO dari PT. Inti Cakrawala Citra (IDG), PT. Inti Cakrawala Maju (ICM) dan PT. Indomarco Prismatama (IDM). Biasanya PO datang dan akan dikirimkan di jam 15.00 di hari yang sama.
- Jam 17.00: Pengiriman sore untuk SF BDG, SF CRB, dan beberapa SD dan DIY luar kota.

## Panduan Laporan Harian Driver:
- Halaman Laporan Driver dapat dilihat di [sini](https://manggalla.com/sarwa/laporan-biaya-pengiriman-2/).
- Double check data yang sudah di input driver di [WP Admin Cost Delivery](https://manggalla.com/sarwa/wp-admin/admin.php?page=tabulate&controller=table&table=cost_delivery) dan pastikan SJ sudah masuk di WP Admin Outbound.
- Apabila semua laporan sudah sesuai, print laporan di halaman laporan driver.
- TTD laporan driver.

## Nama dan Plat Nomor Driver
- Eko         : B 9728
- Bayu        : B 5467
- Mauto       : B 9729
- Retza       : B 4010
- Bambang     : B 9018
- Esa         : B 9793

Kemungkinan driver bertukar kendaraan. Pastikan ulang dan cek dari Grup WA Ekspedisi SMR