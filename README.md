# 🐳 Dockerized RAG & LLM Based Blender AI Layout Assistant

Bu proje; yapay zeka ve 3D modelleme dünyasını modern yazılım mimarileriyle birleştiren, **Dockerize edilmiş, mikroservis tabanlı bir Blender yapay zeka yerleşim ve taslak oluşturma asistanıdır**. Sistem, yerel kütüphanelerden akıllıca veri çekmek ve sahneyi inşa etmek için RAG (Retrieval-Augmented Generation) mimarisini kullanır.

> 🛠️ **Geliştirme Notu:** Proje şu anda aktif test ve entegrasyon aşamasındadır (Beta). Temel mikroservis iletişimi kurulmuş olup, sahne içi optimizasyonlar devam etmektedir.

---

## 🏗️ Sistem ve Mikroservis Mimarisi

Proje, istemci-sunucu (Client-Server) prensibine dayalı gevşek bağlı (loosely coupled) bir mikroservis mimarisine sahiptir:

1. **Arka Yüz (Backend Container):** Docker konteyneri içinde izole şekilde çalışır.
   - **FastAPI:** İstemciden (Blender) gelen talepleri karşılayan yüksek performanslı HTTP API.
   - **ChromaDB:** Yerel asset bilgilerini ve meta-verilerini saklayan, anlamsal aramayı (semantic search) yöneten Vektör Veritabanı.
   - **LLM Entegrasyonu:** Kullanıcı isteklerini anlamlandırıp sahne koordinatlarına ve asset seçimlerine dönüştüren Büyük Dil Modeli katmanı.
2. **Ön Yüz / İstemci (Blender Client):** Kullanıcının bilgisayarında çalışan Blender yazılımı.
   - Docker konteynerine asenkron **HTTP JSON** istekleri gönderir.
   - Gelen yanıtları, Blender UI'ını kilitlememek (non-blocking) adına `bpy.app.timers` mekanizması kullanarak arka planda dinler ve sahneyi gerçek zamanlı (canlı) olarak inşa eder.

---

## 🛠️ Kullanılan Teknolojiler & Kütüphaneler

- **3D API & İstemci:** Python, `bpy` (Blender Python API), `bpy.app.timers`, `requests`
- **API Katmanı:** FastAPI, Uvicorn, Pydantic
- **Yapay Zeka & RAG:** ChromaDB, OpenAI / Gemini API, LangChain
- **Altyapı:** Docker & Docker Compose

---

## 📅 Proje Yol Haritası ve Mevcut Durum

- [x] Sunucu bileşenlerinin (FastAPI + ChromaDB) Dockerize edilmesi
- [x] Blender üzerinden Docker konteynerine HTTP JSON istek/yanıt köprüsünün kurulması
- [/] `bpy.app.timers` ile gelen verilerin canlı sahneye işlenmesi *(Test aşamasında)*
- [ ] LLM prompt mühendisliği ve sahne yerleşim doğruluğunun optimizasyonu *(Gelecek Planı)*

---

## 💻 Kurulum ve Çalıştırma (Geliştiriciler İçin)

### 1. Arka Yüzün Başlatılması (Docker)
Proje dizininde terminali açın ve konteynerleri ayağa kaldırın:
```bash
docker-compose up --build
```
API servisiniz varsayılan olarak `http://localhost:8000` adresinde hazır olacaktır.

### 2. Blender Eklentisinin Kurulması
1. İstemci tarafındaki `.py` uzantılı eklenti dosyasını Blender'a aktarın (`Edit > Preferences > Add-ons > Install`).
2. Eklenti panelinden Docker sunucu adresini doğrulayın ve asistanı tetikleyerek canlı inşa sürecini test edin.
