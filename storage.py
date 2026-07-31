import sqlite3
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS anuncios (
            id TEXT PRIMARY KEY,
            titulo TEXT,
            url TEXT,
            visto_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def ja_visto(anuncio_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT 1 FROM anuncios WHERE id = ?", (anuncio_id,))
    existe = cur.fetchone() is not None
    conn.close()
    return existe


def marcar_como_visto(anuncio_id: str, titulo: str, url: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR IGNORE INTO anuncios (id, titulo, url) VALUES (?, ?, ?)",
        (anuncio_id, titulo, url),
    )
    conn.commit()
    conn.close()
