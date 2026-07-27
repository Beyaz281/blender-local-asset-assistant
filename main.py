import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from groq import Groq

app = FastAPI(title="Ultimate Spatial & Rotation AI Layout Engine", version="5.2.0")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

GERCEK_ASSET_KUTUPHANESI = [
    {"id": "WoodenTable_03_4k", "dosya_yolu": "models/WoodenTable_03_4k.usdc", "acıklama": "Rustik buyuk ahsap yemek ve calisma masasi."},
    {"id": "Rockingchair_01_4k", "dosya_yolu": "models/Rockingchair_01_4k.usdc", "acıklama": "Ahsap sallanan sandalye koltuk esyasi."},
    {"id": "Television_01_4k", "dosya_yolu": "models/Television_01_4k.usdc", "acıklama": "Nostaljik eski model tup televizyon tv ekran esyasi."},
    {"id": "cardboard_box_01_4k", "dosya_yolu": "models/cardboard_box_01_4k.usdc", "acıklama": "Karton koli ambalaj kutusu depo malzemesi."}
]

class AIObje(BaseModel):
    id: str  
    model_id: str  
    referans_id: Optional[str] = None  
    iliski_tipi: str           
    rotasyon_tipi: str         
    zemin_seviyesi: bool 

class SahnePlani(BaseModel):
    sahne_aciklamasi: str
    objeler: List[AIObje]

class SenaryoIstemi(BaseModel):
    senaryo: str

@app.post("/sahne-olustur", response_model=SahnePlani)
def sahne_olustur(istem: SenaryoIstemi):
    try:
        context_string = json.dumps(GERCEK_ASSET_KUTUPHANESI, ensure_ascii=False)
        
        system_prompt = f"""
        Sen profesyonel bir 3B Uzamsal İlişki, Hiyerarşi ve Rotasyon Yapay Zekasısın. Görevin, nesneleri seçmek, konum ilişkilerini kurmak ve yönelimlerini (rotasyon) belirlemektir.
        
        ASLA koordinat (X,Y,Z) veya derece hesabı yapma! Sadece nesnelerin birbirine göre bağıntılarını tanımla.
        Kullanıcı belirtmedikçe kafandan ekstra nesne uydurma. Kullanıcı kaç adet nesne istediyse TAM OLARAK o sayıda nesne üret,kafandan kuralları değiştirme veya nesneleri dağıtma!
        
        YALNIZCA ŞU ASSET HAVUZU İÇİNDEKİ ID'LERİ KULLANABİLİRSİN:
        {context_string}
        
        İLİŞKİ TİPİ KURALLARI:
        1. "merkez": Sahnenin odak nesnesi (genelde masa) için kullanılır. referans_id null, zemin_seviyesi true olur.
        2. "ustune": Bir nesnenin diğerinin TAM üst yüzeyine oturacağını belirtir. zemin_seviyesi false olur.
        3. "altina": Bir nesnenin diğerinin altına yerleşeceğini belirtir. zemin_seviyesi true olur.
        4. "sagina" / "soluna": Nesnenin sağ/sol kenar hizasıdır. Zeminde duracaksa zemin_seviyesi true yap.
        5. "onune" / "arkasina": Nesnenin ön/arka hizasıdır. Sandalye veya yerdeki koliler için zemin_seviyesi true olmalıdır.
        
        ROTASYON TİPİ KURALLARI:
        1. "hedefe_donuk": Sandalye gibi nesnelerin masaya/hedefe dönük olmasını sağlar.
        2. "yana_donuk_sag" / "yana_donuk_sol": Nesnenin yan durmasını sağlar (90 derece sağa/sola dönüş).
        3. "orijinal": Modelin varsayılan duruşudur. Koliler ve televizyonlar için bunu seç.

        KRİTİK ÖRNEKLER VE KULLANICI HATALARINI TOLERE ETME (FEW-SHOT):
        - Örnek 1: 'masanın üstüne üst üste 2 koli koy' denirse:
          * İlk koliyi masaya bağla (iliski_tipi: 'ustune', zemin_seviyesi false).
          * İkinci koliyi İLK KOLİYE bağla (referans_id: 'koli_1') ve iliski_tipini 'ustune' yap, zemin_seviyesi false olsun.
        - Örnek 2: 'masanın önüne iki sandalye yan yana koy' denirse:
          * İki sandalyenin de `referans_id` değerini KESİNLİKLE 'masa_1' (aynı ana nesne) yapmalısın. 
          * İki sandalyenin de `iliski_tipi` KESİNLİKLE 'onune' (veya istendiyse 'arkasina') olmalıdır.
          * Sandalyelerden birini kafana göre 'sagina' veya 'soluna' diye değiştirerek köşelere dağıtma! İkisini de aynı yöne kilitle. Yan yana dizme ve çakışma engelleme işini Blender motoru yapacaktır.
        
        KUSURSUZ ÖRNEKLER (FEW-SHOT):
        
        ÖRNEK 1:Kullanıcı İstemi: "Masa koy, masanın arkasına masaya dönük bir sandalye yerleştir, masanın önüne iki tane masaya dönük sandalye yan yana koy."
        Döndürmen Gereken JSON Yapısı:
        {{
            "sahne_aciklamasi": "Masanın arkasında 1, önünde yan yana 2 sandalye bulunan nizamî düzen.",
            "objeler": [
                {{"id": "masa_1", "model_id": "WoodenTable_03_4k", "referans_id": null, "iliski_tipi": "merkez", "rotasyon_tipi": "orijinal", "zemin_seviyesi": True}},
                {{"id": "sandalye_arka", "model_id": "Rockingchair_01_4k", "referans_id": "masa_1", "iliski_tipi": "arkasina", "rotasyon_tipi": "hedefe_donuk", "zemin_seviyesi": True}},
                {{"id": "sandalye_on_1", "model_id": "Rockingchair_01_4k", "referans_id": "masa_1", "iliski_tipi": "onune", "rotasyon_tipi": "hedefe_donuk", "zemin_seviyesi": True}},
                {{"id": "sandalye_on_2", "model_id": "Rockingchair_01_4k", "referans_id": "masa_1", "iliski_tipi": "onune", "rotasyon_tipi": "hedefe_donuk", "zemin_seviyesi": True}}
            ]
        }}
        
          
        ÖRNEK 2 (YAN YANA VE KARŞILIKLI ÇOKLU NESNE DÜZENİ):
        Kullanıcı İstemi: "Masa koy, masanın sağına yere üst üste 2 koli koy."
        Döndürmen Gereken JSON:
        {{
            "sahne_aciklamasi": "Sahnenin uzamsal özeti",
            "objeler": [
                {{"id": "masa_1", "model_id": "WoodenTable_03_4k", "referans_id": null, "iliski_tipi": "merkez", "rotasyon_tipi": "orijinal", "zemin_seviyesi": true}},
                {{"id": "koli_1", "model_id": "cardboard_box_01_4k", "referans_id": "masa_1", "iliski_tipi": "sagina", "rotasyon_tipi": "orijinal", "zemin_seviyesi": true}},
                {{"id": "koli_2", "model_id": "cardboard_box_01_4k", "referans_id": "koli_1", "iliski_tipi": "ustune", "rotasyon_tipi": "orijinal", "zemin_seviyesi": false}}
            ]
        }}
        DÖNDÜRECEĞİN NİHAİ JSON FORMATI (Yukarıdaki şablonlara tam sadık kal):
        {{
            "sahne_aciklamasi": "Sahnenin genel özeti",
            "objeler": []
        }}
        
        """

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Senaryo: {istem.senaryo}"}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        # 🚀 KESİN DÜZELTME: [0] indeksi eklendi, liste hatası giderildi
        raw_content = chat_completion.choices[0].message.content.strip()
        parsed_data = json.loads(raw_content)
        
        cleaned_objeler = []
        for obj in parsed_data.get("objeler", []):
            m_id = obj.get("model_id")
            if not any(a["id"] == m_id for a in GERCEK_ASSET_KUTUPHANESI):
                continue
                
            cleaned_objeler.append({
                "id": str(obj.get("id", f"obj_{m_id}")),
                "model_id": str(m_id),
                "referans_id": obj.get("referans_id") if obj.get("referans_id") else None,
                "iliski_tipi": str(obj.get("iliski_tipi", "merkez")),
                "rotasyon_tipi": str(obj.get("rotasyon_tipi", "orijinal")),
                "zemin_seviyesi": bool(obj.get("zemin_seviyesi", True))
            })
            
        return {
            "sahne_aciklamasi": str(parsed_data.get("sahne_aciklamasi", "AI Layout")),
            "objeler": cleaned_objeler
        }
        
    except Exception as e:
        print(f"❌ Backend İç Hatası Detayı: {e}")  
        raise HTTPException(status_code=500, detail=str(e))