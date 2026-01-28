import streamlit as st
import pipeline_functions as pf

st.set_page_config(page_title="Top Apps Pipeline", layout="wide")
st.title("📊 Top Apps Pipeline (Dynamic Filters)")
st.write("Select the filters below, then run the pipeline and view the result.")

# ---- Category options ----
CATEGORIES = [
    "ART_AND_DESIGN",
    "AUTO_AND_VEHICLES",
    "BEAUTY",
    "BOOKS_AND_REFERENCE",
    "BUSINESS",
    "COMICS",
    "COMMUNICATION",
    "DATING",
    "EDUCATION",
    "ENTERTAINMENT",
    "EVENTS",
    "FAMILY",
    "FINANCE",
    "FOOD_AND_DRINK",
    "GAME",
]

# ---- Controls (main page) ----
col1, col2, col3 = st.columns(3)

with col1:
    category = st.selectbox(
        "Category",
        options=CATEGORIES,
        index=CATEGORIES.index("FOOD_AND_DRINK"),
    )

with col2:
    min_rating = st.number_input(
        "Minimum rating",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1,
    )

with col3:
    min_reviews = st.number_input(
        "Minimum reviews",
        min_value=0,
        value=1000,
        step=100,
    )

st.divider()

# ---- Run pipeline ----
if st.button("▶ Run pipeline"):
    with st.spinner("Running pipeline..."):
        apps_data = pf.extract("apps_data.csv")
        reviews_data = pf.extract("review_data.csv")

        top_apps_data = pf.transform(
            apps=apps_data,
            reviews=reviews_data,
            category=category,
            min_rating=float(min_rating),
            min_reviews=int(min_reviews),
        )

        pf.load(
            dataframe=top_apps_data,
            database_name="market_research",
            table_name="top_apps"
        )

    st.success("Pipeline completed!")
    st.write(f"Returned rows: {len(top_apps_data)}")
    st.dataframe(top_apps_data, use_container_width=True)
