from datetime import datetime, timezone
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Rádio MB API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

STORES = [
    {"slug": "panambi", "name": "MB Lojas Panambi"},
    {"slug": "palmeira", "name": "MB Lojas Palmeira das Missões"},
    {"slug": "sao-borja", "name": "MB Lojas São Borja"},
    {"slug": "tupancireta", "name": "MB Lojas Tupanciretã"},
    {"slug": "megashop", "name": "Megashop Santo Ângelo"},
    {"slug": "mix", "name": "Mix Atakadão São Borja"},
]

MEDIA = [
    {
        "id": 1,
        "type": "music",
        "title": "Faixa piloto aprovada",
        "artist": "Catálogo de teste",
        "file_url": "",
        "energy_level": 3,
        "license_status": "approved",
    },
    {
        "id": 2,
        "type": "music",
        "title": "Faixa bloqueada",
        "artist": "Sem licença",
        "file_url": "",
        "energy_level": 3,
        "license_status": "pending",
    },
]

HEARTBEATS: Dict[str, str] = {}
PLAYBACK_LOG: List[dict] = []


class PlaybackEvent(BaseModel):
    media_id: int


def _get_store(store_slug: str):
    store = next((s for s in STORES if s["slug"] == store_slug), None)
    if not store:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return store


@app.get("/health")
def health():
    return {"status": "ok", "service": "radio-mb", "version": "0.1.0"}


@app.get("/api/stores")
def list_stores():
    return STORES


@app.get("/api/player/{store_slug}/next")
def next_media(store_slug: str):
    _get_store(store_slug)
    approved = [m for m in MEDIA if m.get("license_status") == "approved"]
    if not approved:
        raise HTTPException(status_code=404, detail="Nenhuma mídia aprovada disponível")
    return approved[0]


@app.post("/api/player/{store_slug}/heartbeat")
def heartbeat(store_slug: str):
    _get_store(store_slug)
    HEARTBEATS[store_slug] = datetime.now(timezone.utc).isoformat()
    return {"status": "ok", "store": store_slug, "last_heartbeat_at": HEARTBEATS[store_slug]}


@app.post("/api/player/{store_slug}/playback/start")
def playback_start(store_slug: str, event: PlaybackEvent):
    _get_store(store_slug)
    PLAYBACK_LOG.append(
        {
            "store_slug": store_slug,
            "media_id": event.media_id,
            "event": "start",
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return {"status": "logged"}


@app.post("/api/player/{store_slug}/playback/end")
def playback_end(store_slug: str, event: PlaybackEvent):
    _get_store(store_slug)
    PLAYBACK_LOG.append(
        {
            "store_slug": store_slug,
            "media_id": event.media_id,
            "event": "end",
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return {"status": "logged"}


@app.get("/api/debug/status")
def debug_status():
    return {"heartbeats": HEARTBEATS, "playback_log": PLAYBACK_LOG}
