# Maze Solver



Algorithma aplikasi web interaktif untuk menghasilkan, memvisualisasikan, dan menyelesaikan maze (labirin) menggunakan dua algoritma pencarian rute: Recursive Backtracking dan Binary Tree. Aplikasi ini memisahkan logika pemrosesan di backend (Python/Flask) dan antarmuka pengguna interaktif di frontend (HTML).  



##### Fitur Utama


*maze solver* ini yaitu menyediakan opsi penyelesaian menggunakan algoritma Recursive Backtracking atau Binary Tree.  



Mode Komparasi: Membandingkan kedua algoritma secara langsung untuk melihat mana yang menghasilkan rute terpendek, waktu eksekusi tercepat, dan recursion depth terdalam. Hasil komparasi dilengkapi dengan grafik batang (bar chart) dan mini canvas.  



Generate Maze Acak: Membuat maze baru secara instan dengan menyesuaikan jumlah baris (rows), kolom (cols), dan tingkat kepadatan tembok (density).  Dukungan Input Gambar: Menerima unggahan gambar maze (JPG/PNG) dan mengubahnya menjadi matriks angka menggunakan penyesuaian resolusi dan batas gelap/terang (threshold) piksel.

Visualisasi Interaktif: Menampilkan pergerakan dan rute secara real time dengan HTML.


##### Algoritma yang Digunakan

1\. Recursive Backtracking (Rute Biru) Menggunakan pendekatan explicit stack untuk mencegah stack overflow pada labirin yang sangat besar.  Sistem mengeksplorasi 4 arah yang diacak pada setiap node untuk memastikan keragaman jalur (path diversity). Jika menemukan jalan buntu (dead end), algoritma akan melakukan backtrack dengan melakukan pop dari stack.  



2\. Binary Tree (Rute Merah) Menggunakan pendekatan Level by Level Expansion dengan antrean (queue). Setiap node yang masuk ke dalam antrean membawa salinan rute lengkapnya sendiri. Prioritas arah ekspansi adalah ke Kanan \& Bawah. Jika terjadi dead-end, sistem akan melakukan kompensasi (fallback) ke Kiri \& Atas dengan mengeksplorasi ulang dari titik kakek/neneknya (grandparent).  



##### Panduan Instalasi \& Menjalankan Aplikasi

Pastikan komputer Anda telah menginstall Python 3.x.



Langkah 1: Menjalankan backend (Flask) dengan membuka terminal lalu Instal dependensi Flask dengan cara menngetik diterminal: pip install flask ; pip install flask\_cors. Lalu jalankan file python yaitu app.py

Pastikan terminal memunculkan pesan: Maze Solver Backend 2 Algorithms dan berjalan di \[http://127.0.0.1:5000](http://127.0.0.1:5000). 
 

Langkah 2: Menjalankan Frontend dengan membuka file HTML frontend yaitu mazeee.html dengan langsung menggunakan web browser (Edge, Brave, Chrome), pada VsCode beberapa browser tidak dapat menampilkan secara langsung, harus membuat file json yang diperintahkan vscode.Status di pojok kanan atas layar secara otomatis akan mendeteksi dan menampilkan Backend Online jika koneksi berhasil.


##### Cara Penggunaan Aplikasi

Pilih Algoritma dengan cara klik tab Recursive Backtracking atau Binary Tree di panel sisi kiri. Masukkan labirin dengan start kiri atas beserta finish yaitu kanan bawah. 



Fitur teks dapat digunakan dengan menggunakan format angka 0 untuk jalan dan 1 untuk tembok, dapat dengan cara menginput labirin secara manual pada panel kiri atas, serta dapat dengan cara meminta hasil generate secara random pada sistem untuk membuatkan sebuah labirin secara acak, user dapat mengkreasikan sendiri berapa banyak rows, cols, dan density yang mereka mau., lalu mulai simulasi dengan cara klik "Solve dengan Algoritma Terpilih" untuk menyelesaikan satu simulasi, atau klik "Bandingkan Kedua Algoritma" untuk melihat komparasi penuh.



Fitur gambar dapat digunakan dengan mengunggah atau drag and drop gambar labirin, pastikan samping kanan kiri sebuah gambar adalah dinding sehingga program tidak mengsalah artikan bahwa kanan kiri ada jalan pintas, serta pastikan sebuah start point (kiri atas) dan finish point (kanan bawah) labirin tidak terhalang, lalu sesuaikan parameter batas kontras/resolusi, lalu mulai simulasi dengan cara klik "Solve dengan Algoritma Terpilih" untuk menyelesaikan satu simulasi, atau klik "Bandingkan Kedua Algoritma" untuk melihat komparasi penuh.





