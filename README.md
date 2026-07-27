# 🐳 Dockerized RAG & LLM Based Blender AI Layout Assistant (v7.0)

<img width="1920" height="1080" alt="2026-07-27-17-16-25-pjj7dyzg_kVjORyEQ" src="https://github.com/user-attachments/assets/3c96d76e-09e5-4ab4-b21f-c13904ea01b6" />

### 🎥 Proje Demosu 
https://youtu.be/7lmovybQdng

Bu proje; yapay zeka ve 3D pipeline süreçlerini modern yazılım mimarileriyle birleştiren, **Dockerize edilmiş, mikroservis tabanlı bir Blender yapay zeka yerleşim ve taslak oluşturma asistanıdır**. Sistem, doğal dil komutlarını anlamlandırıp sahneyi inşa etmek için ilişkisel hiyerarşi ve RAG (Retrieval-Augmented Generation) mimarisini kullanır.

📌 **v7.0 Güncelleme Notu:** Projenin bu sürümünde statik koordinat kısıtlamaları tamamen kaldırılmış; sistem çakışma önleyici (**Collision-Free**) ve asenkron (**Non-Blocking**) bir üretim standardına taşınmıştır.

---

## 🏗️ Sistem ve Mikroservis Mimarisi

Proje, istemci-sunucu (Client-Server) prensibine dayalı gevşek bağlı (loosely coupled) bir mikroservis mimarisine sahiptir:

1. **Arka Yüz (Backend Container):** Docker konteyneri içinde izole şekilde çalışır.
    - **FastAPI:** İstemciden (Blender) gelen talepleri karşılayan yüksek performanslı HTTP API.
    - **ChromaDB:** Yerel asset bilgilerini ve meta-verilerini saklayan, anlamsal aramayı (semantic search) yöneten Vektör Veritabanı.
    - **70B LLM Katmanı (`llama-3.3-70b-versatile`):** Kullanıcı isteklerindeki karmaşık Türkçe zincirleme iyelik ve referans ilişkilerini çözerek, koordinat uydurmak yerine nesnelerin uzamsal bağıntılarını tanımlayan hiyerarşik bir JSON üretir.

2. **Ön Yüz / İstemci (Blender Client):** Kullanıcının bilgisayarında çalışan Blender yazılımı.
    - Docker konteynerine asenkron **HTTP JSON** istekleri gönderir.
    - Gelen yanıtları, Blender UI'ını kilitlememek (non-blocking) adına `bpy.app.timers` mekanizması kullanarak arka planda dinler ve sahneyi gerçek zamanlı (canlı) olarak inşa eder.

---

## 🔥 v7.0 İle Gelen Gelişmiş Özellikler

- **Evrensel Geometri Motoru (Dynamic Bounding Box):** Modellerin isimlerine veya sabit sayılara bağımlılık yoktur. Blender, import edilen her nesnenin sınırlarını (Bounding Box) canlı olarak milimetrik ölçer. Bu sayede dikey istifleme kulesi (Stacking) ve yan yana dizilimler (`Row-Offset`) sıfır çakışma ile yerleşir.
- **Evrensel Rotasyon Kalibrasyonu:** 3B modellerin iç eksen yönelim farklılıklarından kaynaklanan ters bakma sorunları, esnekliği bozmamak adına tek bir global kalibrasyon çarpanı üzerinden kontrol altına alınmıştır. Sandalyelerin yüzleri her zaman nizamî olarak masaya kilitlenir.
- **Few-Shot Prompt Engineering:** Dil modeline kazandırılan çoklu nesne dizilim ve hiyerarşi şablonları sayesinde, kullanıcının devrik ve karmaşık komutları hiyerarşik yapı bozulmadan harfiyen işlenir.

---

## 🛠️ Kullanılan Teknolojiler & Kütüphaneler

- **3D API & İstemci:** Python, `bpy` (Blender Python API), `bpy.app.timers`, `requests`
- **API Katmanı:** FastAPI, Uvicorn, Pydantic
- **Yapay Zeka & RAG:** Groq SDK, ChromaDB
- **Altyapı:** Docker & Docker Compose


---

## 📅 Proje Yol Haritası ve Mevcut Durum

- [x] Sunucu bileşenlerinin (FastAPI + ChromaDB) Dockerize edilmesi
- [x] Blender üzerinden Docker konteynerine HTTP JSON istek/yanıt köprüsünün kurulması
- [x] `bpy.app.timers` ile gelen verilerin dondurma yapmadan (Non-Blocking) canlı sahneye işlenmesi
- [x] `Dynamic Bounding Box` ölçümü ile çakışmasız yerleşim ve kalibrasyonlu rotasyon motorunun kurulması
- [ ] RAG tabanlı dinamik yerel kütüphane asset tarama derinleştirmesi *(Gelecek Planı)*

---

## 💻 Kurulum ve Çalıştırma (Geliştiriciler İçin)

### 1. Arka Yüzün Başlatılması (Docker)
Proje dizininde terminali açın ve konteynerleri ayağa kaldırın:
```bash
docker-compose up --build
```
API servisiniz varsayılan olarak `http://localhost:8000` adresinde hazır olacaktır.

### 2. Blender Eklentisinin Kurulması
1. İstemci tarafındaki v7.1 eklenti kodunu Blender Scripting alanına aktarın ve **Run Script** butonuna basın.
2. 3D Viewport ekranında **N** tuşuna basarak **AI Safe Measurement** panelinden asistanı tetikleyip canlı inşa sürecini test edin.
