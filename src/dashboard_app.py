import streamlit as st
import pandas as pd
import plotly.express as px
import os
from route_optimization import optimize_routes
from generate_report import generate_final_report  # We’ll modify this import next

st.set_page_config(page_title="Solid Waste Route Optimization", layout="wide")

st.title("♻️ Solid Waste Route Optimization Dashboard")

# ---- File Upload Section ----
uploaded_file = st.file_uploader("📤 Upload clustered waste data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    # ---- Route Optimization ----
    if st.button("🚚 Run Route Optimization"):
        df.to_csv("data/clustered_points.csv", index=False)
        with st.spinner("Optimizing routes..."):
            optimize_routes()
        st.success("✅ Route optimization completed!")

        # Display summary
        summary = pd.read_csv("data/route_summary.csv")
        st.subheader("📊 Route Summary")
        st.dataframe(summary)

        # ---- Visualization ----
        st.subheader("🗺️ Cluster Visualization")
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="cluster",
            size="waste_kg",
            hover_name="id",
            zoom=10,
            height=600,
        )
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig, use_container_width=True)

        # ---- Report Generation ----
        if st.button("📑 Generate Final Report (Excel + PDF)"):
            with st.spinner("Generating report..."):
                os.makedirs("outputs", exist_ok=True)
                generate_final_report()  # Creates Excel + PDF
            st.success("✅ Reports generated successfully!")
            st.download_button("⬇️ Download Excel", open("outputs/final_report.xlsx", "rb"), file_name="final_report.xlsx")
            st.download_button("⬇️ Download PDF", open("outputs/final_report.pdf", "rb"), file_name="final_report.pdf")
else:
    st.info("👆 Please upload a clustered_points.csv file to begin.")
