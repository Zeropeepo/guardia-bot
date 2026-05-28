# Guardia Guide

Guardia adalah aplikasi chatbot pembelajaran cybersecurity berbasis Retrieval-Augmented Generation (RAG) yang dibuat agar jawaban model tidak hanya mengandalkan pengetahuan bawaan model, tetapi juga mengambil konteks dari dokumen belajar yang sudah disiapkan lebih dulu. Pendekatan ini cocok untuk aplikasi belajar karena jawaban bisa lebih terarah, lebih relevan dengan materi yang diajarkan, dan lebih mudah dilacak ke sumbernya.

Dokumen ini menjelaskan struktur folder proyek, konsep dasar RAG, alur kerja sistem, komponen yang perlu di-tweak, dan hal-hal penting yang perlu dipahami saat membangun Guardia dengan Python untuk frontend dan backend. FastAPI cocok untuk backend karena mendukung pengembangan API yang cepat, validasi data, dan dokumentasi API otomatis, sedangkan Streamlit cocok untuk frontend awal karena memungkinkan pembuatan antarmuka chat interaktif langsung dengan Python.

## Tujuan Guardia

Tujuan utama Guardia adalah menjadi asisten belajar cybersecurity yang bisa membantu pengguna memahami istilah, konsep, dan materi teknis dengan jawaban yang lebih ter-grounding ke dokumen yang sudah dikurasi. Aplikasi ini sebaiknya fokus pada peran sebagai tutor pembelajaran, bukan sebagai alat otomatisasi ofensif atau sistem yang mengeksekusi tindakan berisiko.

Dalam konteks pembelajaran, Guardia sebaiknya menjawab dengan gaya yang ramah untuk pemula: mulai dari jawaban singkat, lalu penjelasan bertahap, lalu contoh atau istilah penting. Pola ini membantu pengguna yang baru belajar RAG atau cybersecurity agar tidak langsung tenggelam dalam istilah teknis yang terlalu padat.

## Apa itu RAG

RAG adalah singkatan dari Retrieval-Augmented Generation. Intinya, sebelum model bahasa menjawab pertanyaan, sistem akan lebih dulu mencari potongan informasi yang paling relevan dari dokumen yang dimiliki, lalu potongan itu diberikan ke model sebagai konteks tambahan saat menyusun jawaban.

Tanpa RAG, chatbot hanya mengandalkan parameter model dan bisa lebih mudah berhalusinasi atau memberi jawaban yang terlalu umum. Dengan RAG, jawaban menjadi lebih dekat ke isi dokumen, lebih mudah diberi sumber, dan lebih mudah dikontrol untuk domain tertentu seperti cybersecurity learning.

### Mental model sederhana

Cara paling mudah memahami RAG adalah membayangkannya sebagai proses tiga tahap:

1. **Simpan ilmu**: dokumen dipecah menjadi potongan kecil lalu direpresentasikan menjadi embedding.
2. **Cari konteks**: saat ada pertanyaan, sistem mencari potongan dokumen yang paling relevan.
3. **Susun jawaban**: model menjawab berdasarkan konteks yang ditemukan itu.

Kalau disederhanakan lagi, RAG adalah kombinasi antara search engine kecil dan chatbot. Search engine bertugas menemukan materi yang relevan, sedangkan LLM bertugas menjelaskan materi itu dengan bahasa alami.

## Alur kerja RAG di Guardia

Alur kerja Guardia sebaiknya dibagi menjadi dua jalur utama: **offline ingestion** dan **online question answering**. Pemisahan ini penting supaya pemula bisa memahami bahwa indexing dokumen dan menjawab pertanyaan adalah dua proses yang berbeda.

### 1. Ingestion

Pada tahap ingestion, dokumen seperti PDF, Markdown, catatan belajar, atau ringkasan lab dibaca lalu dibersihkan. Setelah itu dokumen dipecah menjadi chunk kecil agar sistem bisa mengambil bagian yang relevan, bukan seluruh dokumen sekaligus.

Setelah chunk terbentuk, setiap chunk diubah menjadi embedding dan disimpan ke vector store. Biasanya metadata seperti judul dokumen, topik, tingkat kesulitan, dan kategori juga ikut disimpan agar retrieval nanti bisa lebih cerdas.

### 2. Retrieval

Saat user bertanya, pertanyaan itu juga diubah menjadi embedding. Sistem lalu mencari chunk yang paling dekat secara semantik di vector store, lalu mengembalikan beberapa hasil teratas untuk dijadikan konteks.

Di tahap ini bisa ditambahkan filter metadata, misalnya hanya ambil materi kategori “web security” atau hanya materi tingkat “beginner”. Ini sangat berguna untuk chatbot edukasi karena pengguna pemula sering membutuhkan materi yang sesuai level, bukan hanya yang paling mirip secara semantik.

### 3. Generation

Setelah konteks ditemukan, prompt dikirim ke model dengan instruksi yang jelas. Model diminta menjawab berdasarkan konteks yang tersedia, menjelaskan istilah penting, dan mengatakan dengan jujur jika informasi di konteks belum cukup.

Untuk aplikasi belajar, format jawaban bisa diatur menjadi tiga bagian: jawaban singkat, penjelasan detail, dan referensi sumber. Pola ini membuat chatbot terasa lebih seperti tutor daripada sekadar mesin tanya jawab.

## Kenapa RAG cocok untuk cybersecurity learning

Cybersecurity punya banyak istilah, prosedur, standar, dan praktik yang harus akurat. Karena itu, menggunakan konteks dari materi yang dikurasi jauh lebih aman daripada membiarkan model menjawab bebas tanpa grounding.

Di sisi lain, aplikasi cybersecurity juga harus lebih waspada terhadap prompt injection dan input berbahaya. OWASP menempatkan prompt injection sebagai risiko utama pada aplikasi LLM, sehingga dokumen yang di-retrieve dan pertanyaan user harus selalu dianggap tidak sepenuhnya terpercaya.

## Struktur folder proyek

Berikut struktur proyek yang disarankan:

```text
guardia/
├── README.md
├── .env.example
├── requirements.txt
├── docker-compose.yml
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── routes_chat.py
│   │   ├── routes_admin.py
│   │   ├── routes_ingest.py
│   │   └── routes_eval.py
│   ├── core/
│   │   ├── logging.py
│   │   ├── security.py
│   │   ├── prompts.py
│   │   └── dependencies.py
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── retrieval.py
│   │   ├── reranking.py
│   │   ├── generation.py
│   │   ├── citations.py
│   │   └── guardrails.py
│   ├── data/
│   │   ├── raw/
│   │   ├── cleaned/
│   │   └── eval/
│   ├── db/
│   │   ├── models.py
│   │   ├── vector_store.py
│   │   └── metadata_store.py
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── embedding_service.py
│   │   └── document_service.py
│   └── schemas/
│       ├── chat.py
│       ├── document.py
│       └── admin.py
├── frontend/
│   └── streamlit_app.py
├── tests/
│   ├── test_ingest.py
│   ├── test_retrieval.py
│   ├── test_chat.py
│   └── test_security.py
└── docs/
    ├── PRD.md
    ├── architecture.md
    ├── ingestion-guide.md
    └── guide.md
```

### Penjelasan root folder

#### `README.md`

File ini berisi gambaran singkat proyek, cara menjalankan aplikasi, dan penjelasan cepat tentang tujuan Guardia. README penting karena biasanya menjadi pintu masuk pertama bagi developer baru yang membuka repository.

#### `.env.example`

File ini menyimpan contoh environment variables yang dibutuhkan aplikasi, misalnya API key model, URL database, dan nama koleksi vector store. File contoh ini sebaiknya tidak berisi secret asli, hanya template yang bisa disalin menjadi `.env`.

#### `requirements.txt`

File ini berisi daftar dependency Python yang dipakai proyek. Karena Guardia dibuat full Python untuk rapid development, semua library utama seperti FastAPI, Uvicorn, Streamlit, dan library RAG akan dikelola dari sini.

#### `docker-compose.yml`

File ini digunakan bila ingin menjalankan service pendukung seperti database, vector database, atau tool lain secara konsisten di environment lokal. Untuk fase awal belajar, file ini opsional, tetapi sangat membantu saat proyek mulai punya banyak service.

## Folder `app/`

Folder `app/` adalah inti backend aplikasi. Semua logika utama Guardia sebaiknya berada di sini agar kode tetap terorganisir dan tidak menumpuk di satu file besar.

### `app/main.py`

Ini adalah entry point aplikasi FastAPI. Biasanya file ini membuat instance aplikasi, mendaftarkan router, dan memanggil konfigurasi awal sistem.

Kalau aplikasi dijalankan dengan Uvicorn, file ini biasanya menjadi target utama. Contohnya, perintah bisa mengarah ke `app.main:app`.

### `app/config.py`

File ini digunakan untuk membaca konfigurasi dari environment variables. Tujuannya supaya API key, model name, lokasi database, dan pengaturan lain tidak hardcoded di banyak tempat.

Bagi pemula, file ini penting karena membuat project lebih rapi dan lebih mudah diubah saat pindah environment. Misalnya, mengganti embedding model tidak perlu mengedit banyak file, cukup dari config.

## Folder `app/api/`

Folder ini menyimpan endpoint HTTP yang diakses oleh frontend atau admin tools. Tujuannya adalah memisahkan lapisan API dari logika bisnis RAG.

### `routes_chat.py`

File ini menangani endpoint utama untuk bertanya ke chatbot. Dari sinilah pertanyaan masuk, diteruskan ke pipeline retrieval dan generation, lalu hasil jawaban dikembalikan ke frontend.

### `routes_admin.py`

File ini berisi endpoint untuk kebutuhan admin, seperti melihat daftar dokumen, mengecek status indexing, atau menghapus koleksi tertentu. Folder ini berguna saat Guardia mulai dipakai lebih serius dan butuh panel kontrol sederhana.

### `routes_ingest.py`

File ini menangani upload dokumen, trigger indexing, atau proses ingest ulang dokumen. Dalam proyek RAG, ingestion sering kali menjadi fitur sendiri, jadi memisahkannya dari chat route membuat arsitektur lebih jelas.

### `routes_eval.py`

File ini dipakai untuk evaluasi, misalnya menjalankan daftar pertanyaan uji dan melihat apakah retrieval atau jawaban sudah memadai. Banyak pemula fokus pada “bisa jalan” padahal kualitas RAG sangat bergantung pada evaluasi yang konsisten.

## Folder `app/core/`

Folder ini menaruh komponen inti yang dipakai lintas modul. Anggap folder ini sebagai tempat utilitas penting dan aturan umum sistem.

### `logging.py`

Dipakai untuk mengatur format log aplikasi. Log yang rapi membantu debugging, misalnya untuk melihat dokumen mana yang gagal di-index atau pertanyaan mana yang menghasilkan retrieval buruk.

### `security.py`

Berisi helper untuk validasi, sanitasi input, dan aturan keamanan dasar. Ini penting karena aplikasi LLM perlu memperlakukan input user dan dokumen retrieved sebagai untrusted input, terutama terkait prompt injection.

### `prompts.py`

File ini menyimpan template prompt sistem dan prompt tugas. Menyimpan prompt di satu tempat memudahkan iterasi karena developer bisa membandingkan perubahan prompt tanpa membongkar file route atau service.

### `dependencies.py`

Biasanya berisi dependency injection untuk FastAPI, misalnya koneksi database, object service, atau helper autentikasi. Tujuannya agar route tetap tipis dan fokus pada request-response.

## Folder `app/rag/`

Ini adalah folder paling penting untuk logika RAG. Semua tahap pipeline sebaiknya dipisah agar mudah diuji, diganti, dan dipahami.

### `ingest.py`

Menangani alur masuk dokumen ke sistem RAG. File ini bisa memanggil parser dokumen, cleaning text, chunking, embedding, lalu menyimpan hasilnya ke vector store.

### `chunking.py`

Berisi logika pemotongan dokumen menjadi chunk kecil. Chunking adalah salah satu bagian paling penting dalam RAG karena ukuran chunk, overlap, dan pemisahan paragraf bisa sangat memengaruhi kualitas retrieval.

Kalau chunk terlalu besar, retrieval bisa membawa terlalu banyak noise. Kalau chunk terlalu kecil, konteks bisa terpotong dan jawaban menjadi tidak utuh.

### `embeddings.py`

File ini mengubah teks menjadi vektor numerik yang bisa dicari berdasarkan kemiripan semantik. Tanpa embedding, sistem tidak bisa melakukan semantic search.

### `retrieval.py`

Berisi logika pencarian chunk yang relevan dari vector store. Di sinilah top-k, metadata filtering, dan strategi pengambilan konteks biasanya diatur.

### `reranking.py`

Modul ini opsional untuk v1, tetapi sangat berguna. Setelah retrieval awal mengambil beberapa kandidat chunk, reranker bisa menyusun ulang hasil agar konteks yang paling relevan berada di atas.

### `generation.py`

Berisi logika pemanggilan model bahasa untuk menyusun jawaban akhir. File ini biasanya menerima pertanyaan user, context chunks, dan prompt template lalu mengembalikan jawaban akhir.

### `citations.py`

Mengatur bagaimana sumber ditampilkan ke user. Untuk aplikasi belajar, keberadaan sumber sangat penting karena user bisa membaca materi asli dan tidak sekadar percaya pada output model.

### `guardrails.py`

Berisi aturan tambahan untuk mengontrol perilaku sistem, misalnya menolak pertanyaan tertentu, membatasi jawaban agar tetap edukatif, atau menandai dokumen yang terlihat berisi instruksi injeksi. Guardrails relevan karena OWASP menyoroti pentingnya mitigasi prompt injection pada aplikasi LLM.

## Folder `app/data/`

Folder ini menyimpan data lokal proyek. Pada fase eksperimen, folder ini membantu memisahkan data mentah, data hasil pembersihan, dan data evaluasi.

### `raw/`

Tempat menyimpan dokumen asli sebelum dibersihkan atau dipecah. Contohnya PDF, markdown, atau catatan cybersecurity.

### `cleaned/`

Berisi hasil ekstraksi teks yang sudah dibersihkan. Ini berguna untuk debugging bila hasil parsing dokumen ternyata berantakan.

### `eval/`

Berisi dataset evaluasi, misalnya daftar pertanyaan dan expected source. Folder ini penting karena kualitas RAG sebaiknya diuji dengan pertanyaan tetap, bukan hanya lewat rasa subjektif saat chat manual.

## Folder `app/db/`

Folder ini mengelola interaksi dengan penyimpanan data. Walaupun vector database adalah inti pencarian semantik, metadata biasa tetap perlu dikelola dengan rapi.

### `models.py`

Berisi definisi model data jika memakai ORM atau skema database tertentu. Misalnya model document, chunk record, atau histori evaluasi.

### `vector_store.py`

Berisi adapter ke vector store yang dipilih, misalnya Chroma, Qdrant, FAISS, atau PostgreSQL dengan pgvector. File ini membuat sisa aplikasi tidak terlalu bergantung pada implementasi satu vendor tertentu.

### `metadata_store.py`

Mengelola metadata dokumen yang tidak selalu cocok ditaruh langsung di vector store. Contohnya author, kategori, tingkat kesulitan, atau status publish.

## Folder `app/services/`

Folder ini berisi service layer, yaitu jembatan antara route, logic RAG, dan provider eksternal. Tujuannya agar pemanggilan model atau parser tidak menyebar ke banyak tempat.

### `llm_service.py`

Mengatur cara aplikasi berbicara ke large language model. Kalau nanti model diganti, biasanya perubahan terbesar cukup terlokalisasi di sini.

### `embedding_service.py`

Mengatur pemanggilan embedding model. Ini dipisahkan dari `embeddings.py` agar ada pembagian antara logika pipeline dan integrasi provider.

### `document_service.py`

Berisi fungsi untuk load, parse, dan preprocessing dokumen. Service ini membantu ingestion tetap modular.

## Folder `app/schemas/`

Folder ini mendefinisikan bentuk data masuk dan keluar API. Dalam FastAPI, schema sangat membantu karena request dan response jadi terdokumentasi dengan jelas.

### `chat.py`

Schema untuk request chat, response chat, source snippets, dan metadata jawaban.

### `document.py`

Schema untuk upload dokumen, status ingest, dan ringkasan file.

### `admin.py`

Schema untuk aksi admin seperti reindex, delete source, atau melihat statistik sederhana.

## Folder `frontend/`

Folder ini berisi antarmuka pengguna. Untuk versi awal, menggunakan Streamlit adalah pilihan yang sangat baik karena satu bahasa dengan backend dan jauh lebih cepat diprototipekan.

### `streamlit_app.py`

Ini adalah entry point frontend. Biasanya file ini menampilkan chat box, riwayat percakapan, daftar sumber, dan mungkin panel kecil untuk memilih mode belajar atau topik.

Di versi awal, Streamlit cukup untuk membuktikan ide dan menguji kualitas RAG. Kalau nanti ingin UI yang lebih kaya, frontend bisa dipindah ke framework lain tanpa harus menulis ulang seluruh backend.

## Folder `tests/`

Folder ini berisi pengujian. Untuk pemula, testing sering terasa membosankan, tetapi pada proyek RAG justru testing membantu membedakan masalah retrieval, prompt, dan kualitas data.

### `test_ingest.py`

Menguji apakah dokumen bisa diproses dengan benar. Misalnya, apakah chunk terbentuk, metadata tersimpan, dan embedding berhasil dibuat.

### `test_retrieval.py`

Menguji apakah query tertentu mengembalikan chunk yang relevan. Test ini sangat penting karena banyak masalah RAG sebenarnya berasal dari retrieval yang jelek, bukan dari LLM.

### `test_chat.py`

Menguji endpoint chat secara end-to-end. Tujuannya memastikan seluruh pipeline dari pertanyaan user sampai jawaban akhir berjalan sesuai harapan.

### `test_security.py`

Menguji ketahanan dasar terhadap prompt injection, input aneh, atau pola pertanyaan berbahaya. Ini relevan karena OWASP secara eksplisit menekankan prompt injection prevention untuk aplikasi LLM.

## Folder `docs/`

Folder ini menyimpan dokumentasi proyek. Menaruh dokumentasi di folder khusus membantu tim membedakan antara kode aplikasi dan dokumen penjelasan.

### `PRD.md`

Product Requirements Document yang menjelaskan tujuan produk, user utama, fitur inti, non-goals, dan metrik sukses.

### `architecture.md`

Menjelaskan arsitektur teknis tingkat tinggi, misalnya bagaimana frontend, backend, vector store, dan model saling terhubung.

### `ingestion-guide.md`

Panduan khusus untuk proses upload dan indexing dokumen. Ini berguna karena ingestion biasanya menjadi sumber bug paling sering pada RAG awal.

### `guide.md`

File ini adalah panduan menyeluruh untuk developer baru yang ingin memahami proyek Guardia dari nol.

## Hal penting yang harus dipahami tentang RAG

Ada beberapa konsep yang wajib dipahami sebelum mulai terlalu banyak eksperimen.

### Chunking lebih penting dari yang sering dibayangkan

Pemula sering langsung fokus ke model LLM, padahal masalah pertama pada RAG biasanya justru ada di chunking. Jika struktur chunk buruk, retrieval akan ikut buruk, lalu generation tidak punya konteks bagus untuk dijelaskan.

### Retrieval adalah jantung sistem

Kalau retrieval salah, model sehebat apa pun akan menjawab dari konteks yang salah. Karena itu, sebelum ganti model mahal, lebih baik cek dulu apakah chunk yang diambil memang relevan dengan pertanyaan.

### Metadata sangat membantu

Metadata seperti topik, tingkat kesulitan, sumber, dan tipe dokumen dapat meningkatkan kualitas pencarian. Dalam chatbot edukasi, metadata bisa dipakai untuk memastikan user pemula tidak malah diberi materi yang terlalu lanjut.

### Prompt bukan satu-satunya jawaban

Memperbaiki prompt memang penting, tetapi prompt tidak akan menyelamatkan retrieval yang buruk. Banyak pemula terlalu lama tweaking prompt padahal akar masalahnya ada di kualitas dokumen, chunking, atau ranking hasil.

### Evaluasi harus dibuat sejak awal

Tanpa evaluasi, developer mudah tertipu karena beberapa demo terlihat bagus padahal performa sebenarnya tidak stabil. Menyiapkan daftar pertanyaan uji sejak awal akan membuat iterasi jauh lebih objektif.

## Hal-hal yang perlu di-tweak

Berikut area yang paling sering diubah saat mengembangkan RAG:

| Komponen | Yang di-tweak | Dampaknya |
|---|---|---|
| Chunking | Chunk size, overlap, split strategy | Menentukan kualitas konteks yang diambil |
| Retrieval | Top-k, similarity threshold, metadata filter | Menentukan seberapa relevan chunk yang diberikan ke model |
| Reranking | Pakai atau tidak, jumlah kandidat | Membantu menyusun urutan konteks terbaik |
| Prompt | Gaya jawaban, instruksi sitasi, level penjelasan | Mengubah kualitas penyajian jawaban |
| Data | Kualitas dokumen, struktur materi, trust level | Sangat memengaruhi grounding jawaban |
| Safety | Filter input, guardrails, injection handling | Menjaga aplikasi tetap aman dan stabil |

Untuk Guardia, tweak yang sangat penting adalah trust level source, tingkat kesulitan materi, dan format jawaban edukatif. Ini karena tujuan aplikasi bukan sekadar menjawab benar, tetapi juga membantu pengguna benar-benar belajar.

## Saran implementasi v1

Untuk versi pertama, fokus saja pada ruang lingkup kecil tetapi rapi.

- Gunakan FastAPI untuk backend chat dan ingestion.
- Gunakan Streamlit untuk frontend chat sederhana.
- Mulai dari satu jenis dokumen seperti Markdown dan PDF.
- Simpan metadata dasar: judul, topik, level, dan sumber.
- Tampilkan sumber di bawah setiap jawaban.
- Buat 20 sampai 50 pertanyaan evaluasi dasar.
- Tambahkan proteksi awal terhadap prompt injection.

Ruang lingkup yang sederhana ini lebih cocok untuk pemula dibanding langsung membangun banyak mode agent, tools, atau sistem multi-tenant. Versi awal yang stabil jauh lebih berharga daripada sistem besar yang sulit dijelaskan dan sulit diuji.

## Kesalahan umum yang perlu dihindari

Beberapa kesalahan paling umum pada proyek RAG pemula adalah:

- Semua logika ditaruh dalam satu file besar.
- Langsung fokus ke model LLM tanpa mengecek retrieval.
- Tidak menyimpan metadata dokumen.
- Tidak membuat evaluasi tetap.
- Tidak menampilkan sumber jawaban.
- Menganggap dokumen retrieved selalu aman, padahal prompt injection bisa datang dari konten retrieved maupun input user.

Kalau Guardia dibangun dengan struktur modular sejak awal, sebagian besar masalah ini akan jauh lebih mudah diatasi. Struktur folder yang rapi bukan hanya soal estetika, tetapi memengaruhi seberapa cepat sistem bisa dipahami, diuji, dan dikembangkan.

## Penutup

Guardia paling mudah dipahami sebagai chatbot tutor cybersecurity yang berdiri di atas pipeline RAG: dokumen di-ingest, diubah menjadi embedding, dicari kembali saat user bertanya, lalu dijelaskan oleh model dengan bahasa yang lebih mudah dipahami. Dengan Python-only stack untuk fase awal, FastAPI dan Streamlit memberi jalur yang cepat untuk belajar, membangun, dan menguji ide tanpa kompleksitas frontend-backend multi-bahasa.

Jika fondasi seperti chunking, retrieval, metadata, evaluasi, dan guardrails dipahami dengan benar, maka pengembangan fitur lanjutan akan jauh lebih mudah. Sebaliknya, jika fondasi ini diabaikan, sistem mungkin terlihat berjalan tetapi kualitas jawaban akan sulit dikendalikan.
