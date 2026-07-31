import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def enviar_telegram(mensagem: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}, timeout=15)
        if resp.status_code != 200:
            print(f"[notifier] Falha ao enviar Telegram: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"[notifier] Erro ao enviar Telegram: {e}")


def notificar_anuncio(titulo: str, preco: str, local: str, url: str, origem: str):
    msg = (
        f"🏠 Novo anúncio ({origem})\n"
        f"{titulo}\n"
        f"💰 {preco}\n"
        f"📍 {local}\n"
        f"🔗 {url}"
    )
    enviar_telegram(msg)
