import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# =========================
# TÍTULO (VOLTOU)
# =========================
st.markdown("""
<h1 style="
    white-space: nowrap;
    text-align: center;
    margin-bottom: 10px;
">
Resultados Commander 500 - Últimos 6 meses
</h1>
""", unsafe_allow_html=True)

df = pd.read_csv("commander_data.csv")

# =========================
# WINRATE (NUMÉRICO + FORMATADO)
# =========================
df["winrate"] = (
    df["winrate"]
    .astype(str)
    .str.replace("%", "", regex=False)
)

df["winrate"] = pd.to_numeric(df["winrate"], errors="coerce")
df["winrate"] = df["winrate"].map(lambda x: f"{x:.2f}%")

# =========================
# SLUG EDHREC (COMMANDER + PARTNER)
# =========================
def slug(name):
    if pd.isna(name):
        return None
    return (
        name.lower()
        .replace(",", "")
        .replace("'", "")
        .replace("’", "")
        .strip()
        .replace(" ", "-")
    )

def edhrec_url(row):
    commander = slug(row["commander"])

    partner = row["partner"]

    if pd.notna(partner) and partner != "":
        partner = slug(partner)
        return f"https://edhrec.com/commanders/{commander}-{partner}"

    return f"https://edhrec.com/commanders/{commander}"

df["edhrec_url"] = df.apply(edhrec_url, axis=1)

# =========================
# DATAFRAME FINAL
# =========================
st.dataframe(
    df,
    use_container_width=True,
    height=850,
    column_config={
        "edhrec_url": st.column_config.LinkColumn(
            "Commander",
            display_text="Open EDHREC"
        )
    }
)