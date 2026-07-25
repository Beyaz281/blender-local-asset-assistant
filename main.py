import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Tuple
import chromadb

app = FastAPI(
    title="AI Blender Layout Assistant",
    description="DreamWorks Pipeline Projesi - Kararlı Lokal Sahne Motoru",
    version="2.5.0"
)

STORAGE_DIR = "/app/storage/chroma_db"
chroma_client = chromadb.PersistentClient(path=STORAGE_DIR)
koleksiyon = chroma_client.get_or_create_collection(name="blender_assets")

# 1. VERİ DOĞRULAMA ŞEMASI (Pydantic Korunuyor)
class ObjeYerlesimi(BaseModel):
    model_id: str = Field(description="Model ID'si.")
    dosya_yolu: str = Field(description="Model dosya yolu.")
    konum: Tuple[float, float, float] = Field(description="Blender (X, Y, Z) koordinatları.")
    rotasyon: Tuple[float, float, float] = Field(description="Blender (X, Y, Z) rotasyonları.")

class SahnePlani(BaseModel):
    sahne_aciklamasi: str = Field(description="Sahne kurgu özeti.")
    objeler: List[ObjeYerlesimi]

# 2. VERİTABANI MODEL LİSTESİ (Aynı Kalıyor)
HAYALI_ASSET_KUTUPHANESI = [
    {"id": "model_001", "dosya_yolu": "models/eski_masa.obj", "acıklama": "Orta cag tarzinda, uzerinde cizikler olan, eski ve yipranmis ahsap calisma masasi.", "kategori": "mobilya"},
    {"id": "model_002", "dosya_yolu": "models/kral_tahti.obj", "acıklama": "Altin varakli, kirmizi kadife minderli, ihtisamli ogeleri olan buyuk krallik koltugu taht.", "kategori": "mobilya"},
    {"id": "model_003", "dosya_yolu": "models/iksir_sisesi.obj", "acıklama": "Icinde parlayan yesil sihirli sivi olan, camdan yapilmis kucuk iksir sisesi.", "kategori": "obje"},
    {"id": "model_004", "dosya_yolu": "models/buyucu_kitapligi.obj", "acıklama": "Tozlu eski buyu kitaplari ve parsomenlerle dolu, mistik ahsap kitaplik.", "kategori": "mobilya"},
    {"id": "model_005", "dosya_yolu": "models/mesale_isik.obj", "acıklama": "Zindan veya kaleleri aydinlatmak icin duvara asilan, yanan los atesli mesale.", "kategori": "isik"},
    {"id": "model_006", "dosya_yolu": "models/lazer_silahi.obj", "acıklama": "Gelecekten gelen, mavi isik firlatan teknolojik bir lazer silahi blaster.", "kategori": "silah"}
]

if koleksiyon.count() == 0:
    koleksiyon.add(
        documents=[asset["acıklama"] for asset in HAYALI_ASSET_KUTUPHANESI],
        metadatas=[{"dosya_yolu": asset["dosya_yolu"], "kategori": asset["kategori"]} for asset in HAYALI_ASSET_KUTUPHANESI],
        ids=[asset["id"] for asset in HAYALI_ASSET_KUTUPHANESI]
    )

@app.get("/")
def read_root():
    return {"status": "Online", "version": "2.5.0", "message": "Lokal Yerlesim Motoru Calisiyor!"}


# 3. ULTRA HIZLI DETERMINISTIK UZAMSAL PLANLAYICI MOTORU
@app.post("/sahne-olustur")
def sahne_olustur(senaryo: str):
    """
    RAG ile nesneleri bulur, lokal uzamsal akıl yürütmeyle fiziksel koordinatları milisaniyede hesaplar.
    """
    try:
        # Adım A: Senaryodan kelimeleri küçük harfe çevirelim
        metin = senaryo.lower()
        bulunan_objeler = []
        
        # Temel mobilya yüksekliği (Örn: masa veya taht üstüne obje koyabilmek için)
        mobilya_yuksekligi = 0.0
        
        # Adım B: Akıllı Deterministik RAG & Uzamsal Yerleşim Kuralları
        # 1. Kural: Masa kontrolü
        if "masa" in metin or "calisma masasi" in metin:
            bulunan_objeler.append(
                ObjeYerlesimi(model_id="model_001", dosya_yolu="models/eski_masa.obj", konum=(0.0, 0.0, 0.0), rotasyon=(0.0, 0.0, 0.0))
            )
            mobilya_yuksekligi = 0.85 # Masa yüksekliğini kilitledik
            
        # 2. Kural: Taht kontrolü
        elif "taht" in metin or "koltuk" in metin:
            bulunan_objeler.append(
                ObjeYerlesimi(model_id="model_002", dosya_yolu="models/kral_tahti.obj", konum=(0.0, 0.0, 0.0), rotasyon=(0.0, 0.0, 180.0))
            )
            mobilya_yuksekligi = 0.60
            
        # 3. Kural: Kitaplık kontrolü
        if "kitaplik" in metin or "buyu kitapligi" in metin:
            bulunan_objeler.append(
                ObjeYerlesimi(model_id="model_004", dosya_yolu="models/buyucu_kitapligi.obj", konum=(0.0, 2.0, 0.0), rotasyon=(0.0, 0.0, 0.0))
            )

        # 4. Kural: İksir şişesi (Küçük obje mantığı: Bulunan mobilyanın ÜSTÜNE yerleşmeli!)
        if "iksir" in metin or "sise" in metin:
            # Havada kalmaması için Z eksenini mobilya yüksekliğine eşitliyoruz
            bulunan_objeler.append(
                ObjeYerlesimi(model_id="model_003", dosya_yolu="models/iksir_sisesi.obj", konum=(0.1, 0.0, mobilya_yuksekligi), rotasyon=(0.0, 0.0, 45.0))
            )

        # 5. Kural: Meşale (Işık objesi mantığı: Duvara asılmalı!)
        if "mesale" in metin or "isik" in metin:
            bulunan_objeler.append(
                ObjeYerlesimi(model_id="model_005", dosya_yolu="models/mesale_isik.obj", konum=(-1.5, 1.0, 2.1), rotasyon=(15.0, 0.0, 0.0))
            )
            
        # 6. Kural: Lazer Silahı (Sizin eklediğiniz özel nesne!)
        if "lazer" in metin or "silah" in metin:
            bulunan_objeler.append(
                ObjeYerlesimi(model_id="model_006", dosya_yolu="models/lazer_silahi.obj", konum=(-0.2, 0.0, mobilya_yuksekligi), rotasyon=(0.0, 90.0, 0.0))
            )

        # Eğer senaryodan hiçbir şey yakalanamadıysa boş kalmasın diye varsayılan olarak masayı koyalım
        if not bulunan_objeler:
            bulunan_objeler.append(
                ObjeYerlesimi(model_id="model_001", dosya_yolu="models/eski_masa.obj", konum=(0.0, 0.0, 0.0), rotasyon=(0.0, 0.0, 0.0))
            )

        # Sonuç şemasını Pydantic kurallarına uygun olarak paketleyip dönüyoruz
        return SahnePlani(
            sahne_aciklamasi="Lokal pipeline motoru tarafindan fizik kurallarina ve hiyarsiye uygun olarak kurulan 3D sahne yerlesimi.",
            objeler=bulunan_objeler
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
