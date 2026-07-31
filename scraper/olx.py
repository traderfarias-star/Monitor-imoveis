from playwright.sync_api import sync_playwright

HEADLESS = True


def buscar_anuncios(url: str) -> list[dict]:
    anuncios = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        )
        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(4000)

            cards = page.query_selector_all('[data-testid*="ad-card"], a[href*="/vi/"]')

            for card in cards:
                try:
                    href = card.get_attribute("href") or ""
                    if "/vi/" not in href and "olx.com.br" not in href:
                        continue

                    titulo_el = card.query_selector("h2, h3")
                    titulo = titulo_el.inner_text().strip() if titulo_el else "(sem título)"

                    preco_el = card.query_selector('[data-testid*="price"], span:has-text("R$")')
                    preco = preco_el.inner_text().strip() if preco_el else "Preço não informado"

                    texto_completo = card.inner_text()
                    direto_dono = "direto com o proprietário" in texto_completo.lower()

                    anuncio_id = href.rstrip("/").split("-")[-1]

                    anuncios.append({
                        "id": anuncio_id,
                        "titulo": titulo,
                        "preco": preco,
                        "url": href if href.startswith("http") else f"https://www.olx.com.br{href}",
                        "direto_dono": direto_dono,
                        "texto_completo": texto_completo,
                    })
                except Exception as e:
                    print(f"[olx] Erro ao ler um card: {e}")
                    continue

        finally:
            browser.close()

    return anuncios
