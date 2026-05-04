import streamlit as st
import pandas as pd
from data_utils import missing_values_table
from data_utils import detect_outliers_iqr, remove_outliers, cap_outliers, fill_missing
from ai_utils import generate_insights
from data_utils import auto_clean
import seaborn as sns
import matplotlib.pyplot as plt

# Page Settings

st.set_page_config(
    page_title="AI Dataset Cleaner",
    layout="wide"
)

#Dashboard Style

st.markdown("""
<style>

/* MAIN BACKGROUND (BRIGHT + MODERN) */
.stApp {
    background: linear-gradient(135deg, #f8fafc, #e0f2fe);
    color: #0f172a;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #6F9CDE, #5A86C9);
    color: #0f172a;
    padding: 30px 20px;
}

/* Sidebar title */
[data-testid="stSidebar"] h2 {
    color: black;
    font-weight: 700;
    font-size: 45px;
}


/* TITLE */
h1 {
    text-align: center;
    font-weight: 800;
    color: #2563eb;
}

/* SUBHEADERS */
h2, h3 {
    color: #1e40af;
}

/* METRIC CARDS (GLASS EFFECT) */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    text-align: center;
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #1d4ed8, #6d28d9);
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.7);
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #cbd5f5;
}

/* DATAFRAME (IMPORTANT FIX) */
[data-testid="stDataFrame"] {
    background-color: white !important;
    color: black !important;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

/* INFO BOX */
[data-testid="stAlert"] {
    background-color: #e0f2fe;
    color: #0369a1;
    border-radius: 10px;
}
            
div[role="radiogroup"] {
    margin-top: 20px;
}

/* Each navigation item */
div[role="radiogroup"] > label {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
    border-radius: 10px;
    transition: all 0.25s ease;
    cursor: pointer;
}

/* Hover effect */
div[role="radiogroup"] > label:hover {
    background: rgba(255,255,255,0.2);
    transform: translateX(5px);
}

/* Active item */
input[type="radio"]:checked + div {
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<h2 style='margin-bottom:10px;'>Dashboard</h2>
""", unsafe_allow_html=True)
#Sidebar Navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "",
    [
        "📁 Upload Dataset",
        "📊 Preview Dataset",
        "📑 Dataset Info",
        "📈 Data Quality",
        "🧠 AI Insights",
        "🛠️ Data Cleaning"
        
    ]
)

# Upload dataset page
if page == "📁 Upload Dataset":

    st.header("Upload CSV Dataset")

    st.info("Upload a CSV file to begin analysis")

    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.session_state["data"] = df
        st.session_state["original_data"] = df.copy()

        st.success("Dataset uploaded successfully!")


# Dataset Preview Page


elif page == "📊 Preview Dataset":

    st.header("Dataset Preview")

    if "data" in st.session_state:

        df = st.session_state["data"]

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.warning("Please upload dataset first.")


# Dataset Info Page


elif page == "📑 Dataset Info":

    st.header("Dataset Information")

    if "data" in st.session_state:

        df = st.session_state["data"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📄 Rows", df.shape[0])

        with col2:
            st.metric("📊 Columns", df.shape[1])

        with col3:
            st.metric(
                "⚠️ Missing Values",
                df.isnull().sum().sum()
            )

        st.subheader("Column Types")

        st.write(df.dtypes)

    else:
        st.warning("Please upload dataset first.")

#Data Quality Page
elif page == "📈 Data Quality":

    st.header("📈 Data Quality Analysis")

    if "data" in st.session_state:

        df = st.session_state["data"]

        # -------- Missing Values Table --------
        st.subheader("Missing Values Analysis")

        missing_table = missing_values_table(df)

        if missing_table.empty:
            st.success("No missing values found 🎉")
        else:
            st.dataframe(missing_table, use_container_width=True)

        st.markdown("---")

        # -------- Correlation Heatmap --------
        st.subheader("Correlation Heatmap")

        numeric_df = df.select_dtypes(include=["number"])

        if numeric_df.shape[1] > 1:

            fig, ax = plt.subplots(figsize=(8,5))

            sns.heatmap(
                numeric_df.corr(),
                annot=True,
                cmap="Blues",
                ax=ax
            )

            st.pyplot(fig)

        else:
            st.warning("Not enough numeric columns for correlation")

    else:
        st.warning("Please upload dataset first.")

elif page == "🧠 AI Insights":

    st.header("🧠 AI Insights & Suggestions")

    if "data" in st.session_state:

        df = st.session_state["data"]

        st.subheader("Smart Analysis")

        insights = generate_insights(df)

        for insight in insights:
            st.info(insight)

elif page == "🛠️ Data Cleaning":

    st.header("🛠️ Data Cleaning Tools")

    if "data" in st.session_state:

        df = st.session_state["data"]

        # -------- OUTLIER DETECTION --------
        st.subheader("Outlier Detection")

        outlier_info = detect_outliers_iqr(df)
        outlier_df = pd.DataFrame(outlier_info).T

        st.dataframe(outlier_df, use_container_width=True)

        st.markdown("---")

        # -------- OUTLIER ACTION --------
        st.subheader("Handle Outliers")

        numeric_cols = df.select_dtypes(include="number").columns

        selected_col = st.selectbox("Select column", numeric_cols)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Remove Outliers"):
                df = remove_outliers(df, selected_col)
                st.session_state["data"] = df
                st.success("Outliers removed!")

        with col2:
            if st.button("Cap Outliers"):
                df = cap_outliers(df, selected_col)
                st.session_state["data"] = df
                st.success("Outliers capped!")

        st.markdown("---")

        # -------- MISSING VALUES --------
        st.subheader("Handle Missing Values")

        cols_with_missing = df.columns[df.isnull().sum() > 0]

        if len(cols_with_missing) > 0:

            selected_missing_col = st.selectbox(
                "Select column with missing values",
                cols_with_missing
            )

            method = st.selectbox(
                "Select method",
                ["Mean", "Median", "Mode"]
            )

            if st.button("Fill Missing Values"):
                df = fill_missing(df, selected_missing_col, method)
                st.session_state["data"] = df
                st.success("Missing values handled!")

        else:
            st.success("No missing values 🎉")

        # ✅ VERY IMPORTANT PART
        st.markdown("---")
        st.subheader("📊 Before vs After")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Before")
            st.dataframe(st.session_state["original_data"].head(), use_container_width=True)

        with col2:
            st.markdown("### After")
            st.dataframe(st.session_state["data"].head(), use_container_width=True)

        import io

        if "data" in st.session_state:

            st.markdown("---")
            st.subheader("⬇️ Download Cleaned Dataset")

            csv = st.session_state["data"].to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

        else:
            st.warning("Please upload dataset first.")



        
        
