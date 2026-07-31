import sys
import traceback
from datetime import datetime

from config import OLX_URLS, KEYWORDS_FILTER
from storage import init_db, ja_visto, marcar_como_visto
from notifier import notificar_anuncio
from scraper.olx import buscar_anuncios


def passa_no_filtro(anuncio: dict) -> bool:
    if not KEYWORDS_FILTER:
        return True
    texto = anuncio["texto_completo"].lower()
    return any(kw.lower() in texto for kw in KEYWORDS_FILTER)


def rodar_checagem():
    total_novos = 0
    for url in OLX_URLS:
        print(f"[{datetime.now():%H:%M:%S}] Checando {url} ...")
        try:
            anuncios = buscar_anuncios(url)
        except Exception:
            print(f"[main] Falha ao buscar {url}:")
            traceback.print_exc()
            continue

        print(f"  -> {len(anuncios)} anúncios encontrados na página")

        for anuncio in anuncios:
            if ja_visto(anuncio["id"]):
                continue
            if not passa_no_filtro(anuncio):
                marcar_como_visto(anuncio["id"], anuncio["titulo"], anuncio["url"])
                continue

            marca = "🏷️ Direto com o proprietário" if anuncio["direto_dono"] else ""
            print(f"  [NOVO] {anuncio['titulo']} - {anuncio['preco']} {marca}")

            notificar_anuncio(
                titulo=anuncio["titulo"],
                preco=anuncio["preco"],
                local="",
                url=anuncio["url"],
                origem="OLX",
            )
            marcar_como_visto(anuncio["id"], anuncio["titulo"], anuncio["url"])
            total_novos += 1

    print(f"[{datetime.now():%H:%M:%S}] Checagem concluída. {total_novos} novo(s) anúncio(s) notificado(s).")


if __name__ == "__main__":
    init_db()
    rodar_checagem()
