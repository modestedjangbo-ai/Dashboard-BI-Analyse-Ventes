import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ===== 1. CONFIGURATION =====

st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ====== 2. STYLE ======

st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    .dashboard-header {
        background: linear-gradient(135deg, #0f2747 0%, #173f6d 100%);
        padding: 2rem 2.2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        color: white;
    }

    .dashboard-header h1 {
        margin: 0;
        font-size: 2.25rem;
        font-weight: 700;
    }

    .dashboard-header p {
        margin: 0.45rem 0 0;
        font-size: 1rem;
        opacity: 0.85;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #173f6d;
        margin: 1.25rem 0 0.7rem;
    }

    .insight-box {
        background-color: white;
        border-left: 5px solid #1f8a70;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(15, 39, 71, 0.06);
        margin-bottom: 1rem;
    }

    .insight-box strong {
        color: #173f6d;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 1rem 1.15rem;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(15, 39, 71, 0.06);
        border: 1px solid #e7ebf0;
    }

    [data-testid="stMetricLabel"] {
        color: #657184;
    }

    [data-testid="stMetricValue"] {
        color: #173f6d;
        font-weight: 700;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    .sidebar-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #173f6d;
        margin-bottom: 0.2rem;
    }

    .sidebar-subtitle {
        color: #657184;
        font-size: 0.85rem;
        margin-bottom: 1.2rem;
    }

    .footer {
        text-align: center;
        color: #7a8492;
        font-size: 0.8rem;
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# === 3. CHARGEMENT DES DONNÉES =====

@st.cache_data
def load_data():
    data = pd.read_csv(
        "sales_data.csv",
        encoding="latin1"
    )

    data["ORDERDATE"] = pd.to_datetime(
        data["ORDERDATE"],
        errors="coerce"
    )

    return data


df = load_data()


# ====== 4. FONCTION DE RÉINITIALISATION DES FILTRES ======

def reset_filters():
    for year in years:
        st.session_state[f"year_{year}"] = False

    for country in countries:
        st.session_state[f"country_{country}"] = False

    for product in productlines:
        st.session_state[f"product_{product}"] = False

    for deal in dealsizes:
        st.session_state[f"deal_{deal}"] = False

    for status in statuses:
        st.session_state[f"status_{status}"] = False


# ======= 5. OPTIONS DES FILTRES =======

years = sorted(df["YEAR_ID"].dropna().unique())
countries = sorted(df["COUNTRY"].dropna().unique())
productlines = sorted(df["PRODUCTLINE"].dropna().unique())
dealsizes = sorted(df["DEALSIZE"].dropna().unique())
statuses = sorted(df["STATUS"].dropna().unique())


# ===== 6. SIDEBAR — FILTRES =========

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🔎 Filtres</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Cochez les critères à analyser'
        '</div>',
        unsafe_allow_html=True
    )

    # -------- ANNÉE -----

    with st.expander("📅 Année", expanded=False):

        year_selection = []

        for year in years:
            if st.checkbox(
                str(year),
                key=f"year_{year}"
            ):
                year_selection.append(year)

    # ------ PAYS ----

    with st.expander("🌍 Pays", expanded=False):

        country_selection = []

        for country in countries:
            if st.checkbox(
                country,
                key=f"country_{country}"
            ):
                country_selection.append(country)

    # -------- GAMME DE PRODUITS ------

    with st.expander("📦 Gamme de produits", expanded=False):

        product_selection = []

        for product in productlines:
            if st.checkbox(
                product,
                key=f"product_{product}"
            ):
                product_selection.append(product)

    # --------- DEAL SIZE --------

    with st.expander("💰 Taille de vente", expanded=False):

        dealsize_selection = []

        for deal in dealsizes:
            if st.checkbox(
                deal,
                key=f"deal_{deal}"
            ):
                dealsize_selection.append(deal)

    # ------ STATUT -------

    with st.expander("📋 Statut", expanded=False):

        status_selection = []

        for status in statuses:
            if st.checkbox(
                status,
                key=f"status_{status}"
            ):
                status_selection.append(status)

    st.divider()

    st.button(
        "↻ Réinitialiser les filtres",
        width="stretch",
        on_click=reset_filters
    )


# ===== 7. APPLICATION DES FILTRES =======

# Aucune case cochée = toutes les valeurs
selected_years = year_selection if year_selection else years
selected_countries = country_selection if country_selection else countries
selected_productlines = product_selection if product_selection else productlines
selected_dealsizes = dealsize_selection if dealsize_selection else dealsizes
selected_statuses = status_selection if status_selection else statuses


df_filtered = df[
    df["YEAR_ID"].isin(selected_years)
    & df["COUNTRY"].isin(selected_countries)
    & df["PRODUCTLINE"].isin(selected_productlines)
    & df["DEALSIZE"].isin(selected_dealsizes)
    & df["STATUS"].isin(selected_statuses)
].copy()


if df_filtered.empty:
    st.warning(
        "Aucune donnée ne correspond aux critères sélectionnés."
    )
    st.stop()


# ===== 8. EN-TÊTE ======

st.markdown("""
<div class="dashboard-header">
    <h1>Sales Performance Dashboard</h1>
    <p>Analyse interactive des performances commerciales</p>
</div>
""", unsafe_allow_html=True)


# ===== 9. KPI =====

st.markdown(
    '<div class="section-title">📌 Vue d’ensemble</div>',
    unsafe_allow_html=True
)

total_sales = df_filtered["SALES"].sum()
average_sales = df_filtered["SALES"].mean()
unique_orders = df_filtered["ORDERNUMBER"].nunique()
unique_customers = df_filtered["CUSTOMERNAME"].nunique()
total_quantity = df_filtered["QUANTITYORDERED"].sum()
average_price = df_filtered["PRICEEACH"].mean()

k1, k2, k3, k4 = st.columns(4)

k1.metric("CA total", f"{total_sales:,.2f}")
k2.metric("Commandes", f"{unique_orders:,}")
k3.metric("Clients", f"{unique_customers:,}")
k4.metric("Quantité vendue", f"{total_quantity:,}")

k5, k6 = st.columns(2)

k5.metric("CA moyen / ligne", f"{average_sales:,.2f}")
k6.metric("Prix moyen", f"{average_price:,.2f}")


# ======= 10. ONGLETS ========

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Performance commerciale",
    "📅 Analyse temporelle",
    "🔗 Relations entre variables",
    "⚠️ Valeurs atypiques"
])


# ========== OUTILS GRAPHIQUES ==========

def clean_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#d9dee6")
    ax.spines["bottom"].set_color("#d9dee6")
    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)


def add_horizontal_labels(ax, values):
    for i, value in enumerate(values):
        ax.text(
            value,
            i,
            f" {value:,.0f}",
            va="center",
            fontsize=9
        )


# ======= TAB 1 — PERFORMANCE COMMERCIALE ========

with tab1:

    st.markdown(
        '<div class="section-title">'
        'Où se concentre le chiffre d’affaires ?'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # ---- CA PAR GAMME ------

    with col1:

        sales_by_product = (
            df_filtered
            .groupby("PRODUCTLINE")["SALES"]
            .sum()
            .sort_values()
        )

        fig, ax = plt.subplots(figsize=(8, 4.8))

        sns.barplot(
            x=sales_by_product.values,
            y=sales_by_product.index,
            ax=ax
        )

        clean_axes(ax)

        ax.set_title(
            "CA par gamme de produits",
            loc="left",
            fontweight="bold"
        )

        ax.set_xlabel("Chiffre d'affaires")
        ax.set_ylabel("")

        add_horizontal_labels(
            ax,
            sales_by_product.values
        )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ---- TOP 10 PAYS -----

    with col2:

        sales_by_country = (
            df_filtered
            .groupby("COUNTRY")["SALES"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
        )

        fig, ax = plt.subplots(figsize=(8, 4.8))

        sns.barplot(
            x=sales_by_country.values,
            y=sales_by_country.index,
            ax=ax
        )

        clean_axes(ax)

        ax.set_title(
            "Top 10 pays par CA",
            loc="left",
            fontweight="bold"
        )

        ax.set_xlabel("Chiffre d'affaires")
        ax.set_ylabel("")

        add_horizontal_labels(
            ax,
            sales_by_country.values
        )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ----- INSIGHT ------

    product_share = (
        df_filtered
        .groupby("PRODUCTLINE")["SALES"]
        .sum()
        / df_filtered["SALES"].sum()
        * 100
    ).sort_values(ascending=False)

    top_product = product_share.index[0]
    top_product_share = product_share.iloc[0]

    top_country = (
        df_filtered
        .groupby("COUNTRY")["SALES"]
        .sum()
        .idxmax()
    )

    st.markdown(
        f"""
        <div class="insight-box">
            💡 <strong>À retenir :</strong>
            <strong>{top_product}</strong> est la gamme dominante
            avec <strong>{top_product_share:.2f}%</strong> du CA de la sélection.
            <strong>{top_country}</strong> est le premier marché de la sélection.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- CA PAR ANNÉE + DEAL SIZE -------

    col1, col2 = st.columns(2)

    with col1:

        sales_by_year = (
            df_filtered
            .groupby("YEAR_ID")["SALES"]
            .sum()
            .sort_index()
        )

        fig, ax = plt.subplots(figsize=(8, 4.6))

        sns.barplot(
            x=sales_by_year.index.astype(str),
            y=sales_by_year.values,
            ax=ax
        )

        clean_axes(ax)

        ax.set_title(
            "CA par année",
            loc="left",
            fontweight="bold"
        )

        ax.set_xlabel("Année")
        ax.set_ylabel("Chiffre d'affaires")

        for i, value in enumerate(sales_by_year.values):
            ax.text(
                i,
                value,
                f"{value:,.0f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:

        sales_by_dealsize = (
            df_filtered
            .groupby("DEALSIZE")["SALES"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 4.6))

        sns.barplot(
            x=sales_by_dealsize.index,
            y=sales_by_dealsize.values,
            ax=ax
        )

        clean_axes(ax)

        ax.set_title(
            "CA par taille de vente",
            loc="left",
            fontweight="bold"
        )

        ax.set_xlabel("Taille de vente")
        ax.set_ylabel("Chiffre d'affaires")

        for i, value in enumerate(sales_by_dealsize.values):
            ax.text(
                i,
                value,
                f"{value:,.0f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ----- STATUT -----

    st.markdown(
        '<div class="section-title">'
        'Comment se répartissent les commandes ?'
        '</div>',
        unsafe_allow_html=True
    )

    status_counts = df_filtered["STATUS"].value_counts()

    fig, ax = plt.subplots(figsize=(10, 4.8))

    sns.barplot(
        x=status_counts.values,
        y=status_counts.index,
        ax=ax
    )

    clean_axes(ax)

    ax.set_title(
        "Répartition des commandes par statut",
        loc="left",
        fontweight="bold"
    )

    ax.set_xlabel("Nombre de lignes")
    ax.set_ylabel("")

    add_horizontal_labels(
        ax,
        status_counts.values
    )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # ------ PRODUIT × DEAL SIZE ------

    st.markdown(
        '<div class="section-title">'
        'Analyse croisée produit × taille de vente'
        '</div>',
        unsafe_allow_html=True
    )

    sales_pivot = (
        df_filtered
        .pivot_table(
            index="PRODUCTLINE",
            columns="DEALSIZE",
            values="SALES",
            aggfunc="sum",
            fill_value=0
        )
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))

    sns.heatmap(
        sales_pivot,
        annot=True,
        fmt=".0f",
        ax=ax
    )

    ax.set_title(
        "CA par gamme et taille de vente",
        loc="left",
        fontweight="bold"
    )

    ax.set_xlabel("Taille de vente")
    ax.set_ylabel("Gamme de produits")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # ----- QUANTITÉ MOYENNE × CA MOYEN -------

    product_performance = (
        df_filtered
        .groupby("PRODUCTLINE")
        .agg(
            QUANTITY_MEAN=("QUANTITYORDERED", "mean"),
            SALES_MEAN=("SALES", "mean")
        )
        .sort_values("SALES_MEAN", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))

    sns.scatterplot(
        data=product_performance,
        x="QUANTITY_MEAN",
        y="SALES_MEAN",
        s=110,
        ax=ax
    )

    for product, row in product_performance.iterrows():
        ax.annotate(
            product,
            (
                row["QUANTITY_MEAN"],
                row["SALES_MEAN"]
            ),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=9
        )

    ax.set_title(
        "Quantité moyenne vs CA moyen par gamme",
        loc="left",
        fontweight="bold"
    )

    ax.set_xlabel("Quantité moyenne")
    ax.set_ylabel("CA moyen")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ===== TAB 2 — ANALYSE TEMPORELLE ======

with tab2:

    st.markdown(
        '<div class="section-title">'
        'Évolution du chiffre d’affaires'
        '</div>',
        unsafe_allow_html=True
    )

    monthly_sales = (
        df_filtered
        .groupby(
            df_filtered["ORDERDATE"].dt.to_period("M")
        )["SALES"]
        .sum()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(13, 5.2))

    ax.plot(
        monthly_sales.index.astype(str),
        monthly_sales.values,
        marker="o"
    )

    ax.set_title(
        "Évolution mensuelle du chiffre d’affaires",
        loc="left",
        fontweight="bold"
    )

    ax.set_xlabel("Mois")
    ax.set_ylabel("Chiffre d'affaires")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.15)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    if len(monthly_sales) > 0:

        best_month = monthly_sales.idxmax()
        best_month_value = monthly_sales.max()

        c1, c2 = st.columns(2)

        c1.metric(
            "Meilleur mois",
            str(best_month)
        )

        c2.metric(
            "CA du meilleur mois",
            f"{best_month_value:,.2f}"
        )

    st.markdown(
        '<div class="section-title">'
        'CA par mois de l’année'
        '</div>',
        unsafe_allow_html=True
    )

    sales_by_month = (
        df_filtered
        .groupby("MONTH_ID")["SALES"]
        .sum()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(10, 4.8))

    sns.barplot(
        x=sales_by_month.index,
        y=sales_by_month.values,
        ax=ax
    )

    clean_axes(ax)

    ax.set_title(
        "Chiffre d’affaires total par mois",
        loc="left",
        fontweight="bold"
    )

    ax.set_xlabel("Mois")
    ax.set_ylabel("Chiffre d'affaires")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    yearly_summary = (
        df_filtered
        .groupby("YEAR_ID")["SALES"]
        .agg(["count", "sum", "mean", "median"])
        .sort_index()
    )

    st.markdown(
        '<div class="section-title">'
        'Synthèse annuelle'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        yearly_summary,
        width="stretch"
    )


# ===== TAB 3 — RELATIONS ENTRE VARIABLES ======

with tab3:

    st.markdown(
        '<div class="section-title">'
        'Relations entre les variables numériques'
        '</div>',
        unsafe_allow_html=True
    )

    numeric_cols = df_filtered.select_dtypes(
        include="number"
    ).columns

    correlation_matrix = (
        df_filtered[numeric_cols]
        .corr()
    )

    fig, ax = plt.subplots(figsize=(12, 8))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        ax=ax
    )

    ax.set_title(
        "Matrice de corrélation",
        loc="left",
        fontweight="bold"
    )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    main_correlations = pd.DataFrame({
        "Variable": [
            "PRICEEACH",
            "QUANTITYORDERED",
            "MSRP"
        ],
        "Corrélation avec SALES": [
            df_filtered["PRICEEACH"].corr(
                df_filtered["SALES"]
            ),
            df_filtered["QUANTITYORDERED"].corr(
                df_filtered["SALES"]
            ),
            df_filtered["MSRP"].corr(
                df_filtered["SALES"]
            )
        ]
    }).sort_values(
        "Corrélation avec SALES",
        ascending=False
    )

    st.markdown(
        '<div class="section-title">'
        'Corrélations principales avec le CA'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        main_correlations,
        width="stretch"
    )

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.scatterplot(
            data=df_filtered,
            x="QUANTITYORDERED",
            y="SALES",
            ax=ax
        )

        clean_axes(ax)

        ax.set_title(
            "Quantité commandée vs CA",
            loc="left",
            fontweight="bold"
        )

        ax.set_xlabel("Quantité commandée")
        ax.set_ylabel("CA")

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.scatterplot(
            data=df_filtered,
            x="PRICEEACH",
            y="SALES",
            ax=ax
        )

        clean_axes(ax)

        ax.set_title(
            "Prix unitaire vs CA",
            loc="left",
            fontweight="bold"
        )

        ax.set_xlabel("Prix unitaire")
        ax.set_ylabel("CA")

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.scatterplot(
        data=df_filtered,
        x="MSRP",
        y="SALES",
        ax=ax
    )

    clean_axes(ax)

    ax.set_title(
        "MSRP vs CA",
        loc="left",
        fontweight="bold"
    )

    ax.set_xlabel("MSRP")
    ax.set_ylabel("CA")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "Une corrélation mesure une association linéaire entre deux "
        "variables. Elle ne permet pas, à elle seule, de conclure "
        "à une relation de causalité."
    )


# ==== TAB 4 — VALEURS ATYPIQUES ====

with tab4:

    st.markdown(
        '<div class="section-title">'
        'Détection des valeurs potentiellement atypiques'
        '</div>',
        unsafe_allow_html=True
    )

    Q1 = df_filtered["SALES"].quantile(0.25)
    Q3 = df_filtered["SALES"].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df_filtered[
        (df_filtered["SALES"] < lower_bound)
        | (df_filtered["SALES"] > upper_bound)
    ]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Q1", f"{Q1:,.2f}")
    c2.metric("Q3", f"{Q3:,.2f}")
    c3.metric("IQR", f"{IQR:,.2f}")
    c4.metric(
        "Valeurs atypiques",
        f"{len(outliers):,}"
    )

    fig, ax = plt.subplots(figsize=(11, 3.8))

    ax.boxplot(
        df_filtered["SALES"],
        orientation="horizontal"
    )

    ax.set_title(
        "Distribution du chiffre d'affaires",
        loc="left",
        fontweight="bold"
    )

    ax.set_xlabel("Chiffre d'affaires")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown(
        f"""
        <div class="insight-box">
            ⚠️ <strong>Décision :</strong>
            les valeurs atypiques ne sont pas supprimées automatiquement.
            Une valeur élevée peut correspondre à une transaction commerciale
            réelle. Le seuil supérieur calculé est de
            <strong>{upper_bound:,.2f}</strong>.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        'Principales observations atypiques'
        '</div>',
        unsafe_allow_html=True
    )

    outliers_display = (
        outliers[
            [
                "ORDERNUMBER",
                "QUANTITYORDERED",
                "PRICEEACH",
                "SALES",
                "PRODUCTLINE",
                "DEALSIZE",
                "STATUS"
            ]
        ]
        .sort_values(
            "SALES",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        outliers_display,
        width="stretch"
    )


# ========= 11. DONNÉES FILTRÉES =====

st.divider()

with st.expander("📄 Explorer les données filtrées"):

    st.write(
        f"{len(df_filtered):,} lignes affichées sur "
        f"{len(df):,} lignes au total."
    )

    st.dataframe(
        df_filtered,
        width="stretch"
    )

csv = df_filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Télécharger les données filtrées",
    data=csv,
    file_name="sales_data_filtre.csv",
    mime="text/csv",
    width="stretch"
)


# ===== 12. PIED DE PAGE ======

st.markdown("""
<div class="footer">
    Sales Data Analysis · Data Cleaning & Exploration
    <br>
    Dashboard interactif développé avec Streamlit
</div>
""", unsafe_allow_html=True)
