
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("penguins.csv")
    return df.dropna()

df = load_data()

# Sidebar filters
st.sidebar.title("🔧 Filters")
species = st.sidebar.multiselect("Species", options=df["species"].unique(), default=df["species"].unique())
island = st.sidebar.multiselect("Island", options=df["island"].unique(), default=df["island"].unique())
sex = st.sidebar.multiselect("Sex", options=df["sex"].dropna().unique(), default=df["sex"].dropna().unique())

filtered_df = df[
    (df["species"].isin(species)) &
    (df["island"].isin(island)) &
    (df["sex"].isin(sex))
]

# Page title
st.title("🐧 Penguins Dataset Visualization Dashboard")
st.markdown("Explore and visualize the Palmer Penguins dataset interactively.")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Dataset", "📊 Summary", "📌 Histogram", 
    "📈 Scatter Plot", "🎯 Boxplot", "🧠 Heatmap"
])

# Tab 1: Dataset
with tab1:
    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df)

# Tab 2: Summary stats
with tab2:
    st.subheader("Descriptive Statistics")
    st.write(filtered_df.describe())

# Tab 3: Histogram
with tab3:
    st.subheader("Distribution Plot")
    numeric_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    selected = st.selectbox("Select a numeric variable:", numeric_cols)
    fig, ax = plt.subplots()
    sns.histplot(filtered_df[selected], kde=True, ax=ax, color="skyblue")
    ax.set_title(f"Distribution of {selected}")
    st.pyplot(fig)

# Tab 4: Scatter Plot
with tab4:
    st.subheader("Flipper Length vs Body Mass")
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=filtered_df, x="sex", y="body_mass_g", hue="sex", palette="Set2", ax=ax2, legend=False)
    st.pyplot(fig2)

# Tab 5: Boxplot
with tab5:
    st.subheader("Body Mass by Sex")
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=filtered_df, x="sex", y="body_mass_g", palette="Set2", ax=ax3)
    st.pyplot(fig3)

# Tab 6: Correlation Heatmap
with tab6:
    st.subheader("Correlation Heatmap")
    fig4, ax4 = plt.subplots()
    sns.heatmap(filtered_df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax4)
    st.pyplot(fig4)

# Key insights
st.markdown("### 📌 Key Insights")
st.markdown("""
- **Gentoo penguins** are the largest in size and flipper length.
- **Males** weigh more than **females** across species.
- **Body mass** and **flipper length** are strongly correlated.
- Bill length and depth differ by species and help in classification.
""")
