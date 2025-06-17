
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
st.sidebar.header("🔍 Filter Options")
species = st.sidebar.multiselect("Species", options=df["species"].unique(), default=df["species"].unique())
island = st.sidebar.multiselect("Island", options=df["island"].unique(), default=df["island"].unique())
sex = st.sidebar.multiselect("Sex", options=df["sex"].dropna().unique(), default=df["sex"].dropna().unique())

filtered_df = df[
    (df["species"].isin(species)) &
    (df["island"].isin(island)) &
    (df["sex"].isin(sex))
]

# Main title
st.title("🐧 Penguins Dashboard")

# Dataset preview
st.subheader("📄 Filtered Dataset")
st.dataframe(filtered_df)

# Summary statistics
st.subheader("📊 Summary Statistics")
st.write(filtered_df.describe())

# Histogram with dynamic variable selection
st.subheader("📌 Histogram")
numeric_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
selected_feature = st.selectbox("Select a variable", numeric_cols)
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df[selected_feature], kde=True, ax=ax1, color='skyblue')
ax1.set_title(f"Distribution of {selected_feature}")
st.pyplot(fig1)

# Scatterplot: Flipper Length vs. Body Mass
st.subheader("📈 Flipper Length vs Body Mass")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtered_df, x="flipper_length_mm", y="body_mass_g", hue="species", ax=ax2)
st.pyplot(fig2)

# Boxplot: Body Mass by Sex
st.subheader("🎯 Body Mass by Sex")
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_df, x="sex", y="body_mass_g", hue="sex", palette="Set2", ax=ax3, legend=False)
st.pyplot(fig3)

# Correlation heatmap
st.subheader("🧠 Correlation Heatmap")
fig4, ax4 = plt.subplots()
sns.heatmap(filtered_df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax4)
st.pyplot(fig4)

# Download filtered data
st.subheader("⬇️ Download Filtered Data")
csv = filtered_df.to_csv(index=False)
st.download_button("Download CSV", data=csv, file_name="filtered_penguins.csv", mime="text/csv")

# Key insights
st.markdown("### 📌 Key Insights")
st.markdown("""
- **Gentoo penguins** show higher body mass and longer flippers.
- **Males** typically weigh more than **females**, regardless of species.
- There's a clear **positive correlation** between body mass and flipper length.
- Bill dimensions vary distinctly by species — aiding in classification.
""")
