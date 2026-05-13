from playwright.sync_api import sync_playwright
import pandas as pd
import time
from datetime import datetime

all_data = []

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    # =========================
    # ABRIR SITE
    # =========================

    page.goto(
        "https://www.c500.fun/metrics/commanders"
    )

    time.sleep(2)

    print("Site carregado")

    # =========================
    # ABRIR FILTROS
    # =========================

    filters_button = page.locator(
        "body > main > div > div:nth-child(2) > div > "
        "div.rounded-lg.border.bg-card.text-card-foreground.shadow-sm > "
        "div.p-6.pt-0 > div.w-full.flex.flex-col.gap-3 > "
        "div.flex.flex-col.md\\:flex-row.md\\:items-center.gap-2.md\\:gap-4.w-full > "
        "button.justify-center.text-sm.font-medium.ring-offset-background."
        "transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-2."
        "focus-visible\\:ring-ring.focus-visible\\:ring-offset-2."
        "disabled\\:pointer-events-none.disabled\\:opacity-50."
        "border.border-input.bg-background.hover\\:bg-accent."
        "hover\\:text-accent-foreground.rounded-md.px-3."
        "flex.items-center.gap-1.min-w-\\[150px\\].h-10"
    )

    filters_button.click()

    print("Filtros abertos")

    time.sleep(1)

    # =========================
    # PEGAR DIA ATUAL
    # =========================

    today_day = str(datetime.now().day)

    # =========================
    # ABRIR CALENDÁRIO FINAL
    # =========================

    end_date_button = page.locator(
        "button.w-\\[200px\\]"
    ).nth(1)

    end_date_button.click()

    print("Calendário final aberto")

    time.sleep(1)

    print(f"Dia atual: {today_day}")

    # =========================
    # SELECIONAR HOJE
    # =========================

    today_button = page.locator(
        ".rdp-today button"
    )

    today_button.click()

    print("Hoje selecionado")

    time.sleep(1)

    # =========================
    # ABRIR CALENDÁRIO INICIAL
    # =========================

    start_date_button = page.locator(
        "button.w-\\[200px\\]"
    ).nth(0)

    start_date_button.click()

    print("Calendário inicial aberto")

    time.sleep(1)

    # =========================
    # VOLTAR 5 MESES
    # =========================

    previous_month = page.locator(
        ".rdp-button_previous"
    )

    for _ in range(5):

        previous_month.click()

        time.sleep(0.5)

    print("Voltou 5 meses")

    # =========================
    # SELECIONAR MESMO DIA
    # =========================

    weeks = page.locator(
        "tbody.rdp-weeks tr.rdp-week"
    )

    week_count = weeks.count()

    clicked = False

    for i in range(week_count):

        week = weeks.nth(i)

        days = week.locator("td")

        day_count = days.count()

        for j in range(day_count):

            try:

                td = days.nth(j)

                classes = td.get_attribute("class") or ""

                if "outside" in classes:
                    continue

                button = td.locator("button")

                if button.count() == 0:
                    continue

                text = button.inner_text().strip()

                if text == today_day:

                    print(f"Clicando no dia {today_day}")

                    button.click()

                    clicked = True

                    break

            except Exception as e:

                print(e)

        if clicked:
            break

    if not clicked:
        print("Dia não encontrado")

    time.sleep(1)

    # =========================
    # ALTERAR TAMANHO DA PÁGINA
    # =========================

    page_size_button = page.locator(
        "body > main > div > div:nth-child(2) > div > "
        "div.rounded-lg.border.bg-card.text-card-foreground.shadow-sm > "
        "div.p-6.pt-0 > div.flex.flex-col.md\\:flex-row."
        "items-start.md\\:items-center.justify-between.gap-4."
        "mt-4.pt-4.border-t > div.flex.flex-col.sm\\:flex-row."
        "items-start.sm\\:items-center.gap-2.w-full > button"
    )

    current_value = (
        page_size_button
        .locator("span")
        .inner_text()
        .strip()
    )

    print(f"Valor atual: {current_value}")

    page_size_button.click()

    time.sleep(1)

    page.get_by_role(
        "option",
        name="50"
    ).click()

    print("50 linhas selecionadas")

    time.sleep(1)

    # =========================
    # EXTRAÇÃO DAS TABELAS
    # =========================

    while True:

        rows = page.locator(
            "table tbody tr"
        )

        row_count = rows.count()

        print(f"\nLinhas encontradas: {row_count}")

        for i in range(row_count):

            row = rows.nth(i)

            try:

                cells = row.locator("td")

                # =========================
                # COMMANDER
                # =========================

                commander = (
                    cells.nth(1)
                    .locator("span.truncate")
                    .inner_text()
                    .strip()
                )

                # =========================
                # PARTNER
                # =========================

                partner = None

                partner_locator = cells.nth(3).locator(
                    "span.font-semibold"
                )

                if partner_locator.count() > 0:

                    partner = (
                        partner_locator
                        .inner_text()
                        .strip()
                    )

                # =========================
                # CORES (WUBRG LIMPO)
                # =========================

                ORDER = ["W", "U", "B", "R", "G"]

                color_divs = cells.nth(2).locator("div")

                colors = set()

                for j in range(color_divs.count()):

                    text = color_divs.nth(j).inner_text().strip()

                    if text in ORDER:
                        colors.add(text)

                # ordena na ordem WUBRG e junta SEM separador
                colors = "".join(sorted(colors, key=lambda x: ORDER.index(x)))

                # =========================
                # WINRATE
                # =========================

                winrate_raw = (
                    cells.nth(4)
                    .inner_text()
                    .strip()
                )

                winrate = float(winrate_raw.replace("%", "").strip())

                # =========================
                # RECORD
                # =========================

                record = (
                    cells.nth(5)
                    .inner_text()
                    .strip()
                )

                # =========================
                # CHAMPIONS
                # =========================

                champions = (
                    cells.nth(6)
                    .inner_text()
                    .strip()
                )

                # =========================
                # ENTRIES
                # =========================

                entries = (
                    cells.nth(7)
                    .inner_text()
                    .strip()
                )

                all_data.append({
                    "commander": commander,
                    "partner": partner,
                    "colors": colors,
                    "winrate": f"{winrate:.2f}%",
                    "record": record,
                    "champions": champions,
                    "entries": entries
                })

                print(commander)

            except Exception as e:

                print(f"Erro linha {i}: {e}")

        # =========================
        # PRÓXIMA PÁGINA
        # =========================

        next_button = page.locator(
            "body > main > div > div:nth-child(2) > div > "
            "div.rounded-lg.border.bg-card.text-card-foreground.shadow-sm > "
            "div.p-6.pt-0 > div.flex.flex-col.md\\:flex-row."
            "items-start.md\\:items-center.justify-between.gap-4."
            "mt-4.pt-4.border-t > div.flex.items-center.gap-1."
            "w-full.justify-center.md\\:justify-end.md\\:w-auto > "
            "button:nth-child(4)"
        )

        if next_button.count() == 0:

            print("\nBotão next não encontrado")
            break

        disabled = next_button.get_attribute("disabled")

        if disabled is not None:

            print("\nÚltima página")
            break

        next_button.click()

        print("\nPróxima página")

        time.sleep(1)

    browser.close()

# =========================
# DATAFRAME
# =========================

df = pd.DataFrame(all_data)

df = pd.DataFrame(all_data)

import requests


# =========================
# BAIXAR COMMANDERS PARTNER
# =========================

print("\nBaixando lista de partners do Scryfall...")

url = (
    "https://api.scryfall.com/cards/search"
    "?q=otag:pair-commander"
    "&unique=cards"
)

partner_cards = set()

while url:

    response = requests.get(url)

    data = response.json()

    for card in data["data"]:

        partner_cards.add(
            card["name"]
        )

    url = data.get("next_page")

print(f"Partners válidos encontrados: {len(partner_cards)}")


# =========================
# LIMPAR PARTNERS INVÁLIDOS
# =========================

def validate_partner(row):

    partner = row["partner"]

    if pd.isna(partner):
        return None

    if partner in partner_cards:
        return partner

    return None


df["partner"] = df.apply(
    validate_partner,
    axis=1
)

print("\nDATAFRAME:")
print(df.head())

print("\nTOTAL:")
print(len(df))

# =========================
# SALVAR CSV
# =========================

df.to_csv("commander_data.csv", index=False, encoding="utf-8-sig")
)

print("\nCSV salvo!")