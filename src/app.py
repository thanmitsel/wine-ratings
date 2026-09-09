"""
Wine picker — filter Tom's wine ratings by name, category, shop, price, and rating.
"""

from __future__ import annotations

from pathlib import Path
from google_sheets_api import GoogleSheets

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Wine Ratings.xlsx"

# Class > Pass > Arse
RATING_ORDER = ["Class", "Pass", "Arse"]


def rating_sort_key(rating: str) -> tuple:
    try:
        return (0, RATING_ORDER.index(rating))
    except ValueError:
        return (1, rating)


def rating_rank(rating: str) -> int:
    try:
        return RATING_ORDER.index(rating)
    except ValueError:
        return len(RATING_ORDER) + 1

def clean_cols(df):
    # Normalize the pound-price column name (encoding can mangle the £ sign)
    price_col = next(c for c in df.columns if str(c).startswith("Price"))
    df = df.rename(columns={price_col: "Price"})
    df["Rating"] = df["Rating"].astype(str).str.strip()
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Tom's Pick"] = df["Tom's Pick"].astype(str).str.strip()
    return df

@st.cache_data
def load_wines(_mtime: float) -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH)
    return clean_cols(df)

# Load dataset from google sheet
@st.cache_resource
def load_google_sheet(aplatform):
    # Replace with your dataset
    sheet_obj = GoogleSheets(aplatform)
    df_ = sheet_obj.load_clean()
    return clean_cols(df_)

def main() -> None:
    st.set_page_config(page_title="Wine Picker", page_icon="🍷", layout="wide")
    st.title("Wine Picker")
    st.caption("Find the right bottle from Tom's wine ratings.")

    # df = load_wines(DATA_PATH.stat().st_mtime)
    df = load_google_sheet('wine_ratings')

    with st.sidebar:
        st.header("Filters")

        name_query = st.text_input("Wine name", placeholder="Search by name…")

        categories = sorted(df["Category"].dropna().unique().tolist())
        selected_categories = st.multiselect("Category", categories)

        shops = sorted(df["Shop"].dropna().unique().tolist())
        selected_shops = st.multiselect("Shop", shops)

        min_price = float(df["Price"].min())
        max_price = float(df["Price"].max())
        price_range = st.slider(
            "Price (£)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=0.25,
        )

        ratings = sorted(df["Rating"].dropna().unique().tolist(), key=rating_sort_key)
        selected_ratings = st.multiselect("Rating", ratings)

        toms_pick_only = st.checkbox("Tom's Pick only", value=False)

        st.divider()
        st.caption(f"{len(df)} wines in the dataset")

    filtered = df.copy()

    if name_query.strip():
        filtered = filtered[
            filtered["Name"].str.contains(name_query.strip(), case=False, na=False)
        ]

    if selected_categories:
        filtered = filtered[filtered["Category"].isin(selected_categories)]

    if selected_shops:
        filtered = filtered[filtered["Shop"].isin(selected_shops)]

    lo, hi = price_range
    filtered = filtered[(filtered["Price"] >= lo) & (filtered["Price"] <= hi)]

    if selected_ratings:
        filtered = filtered[filtered["Rating"].isin(selected_ratings)]

    if toms_pick_only:
        filtered = filtered[filtered["Tom's Pick"].str.lower() == "yes"]

    filtered = filtered.assign(_rating_rank=filtered["Rating"].map(rating_rank))
    filtered = filtered.sort_values(["_rating_rank", "Price"], ascending=[True, True])
    filtered = filtered.drop(columns=["_rating_rank"])

    st.subheader(f"{len(filtered)} wine{'s' if len(filtered) != 1 else ''} found")

    if filtered.empty:
        st.info("No wines match these filters. Try widening the price range or clearing a filter.")
        return

    display = filtered[
        ["Name", "Category", "Shop", "Price", "Rating", "Tom's Pick", "Best For"]
    ].rename(columns={"Price": "Price (£)"})

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Price (£)": st.column_config.NumberColumn(format="£%.2f"),
            "Tom's Pick": st.column_config.TextColumn("Tom's Pick"),
        },
    )

    st.download_button(
        "Download results as CSV",
        data=display.to_csv(index=False).encode("utf-8"),
        file_name="wine_picks.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
