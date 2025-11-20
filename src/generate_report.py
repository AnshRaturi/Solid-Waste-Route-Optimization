import os
import pandas as pd
from fpdf import FPDF

# File paths
clustered_points_path = "data/clustered_points.csv"
summary_path = "data/route_summary.csv"
report_excel_path = "outputs/final_report.xlsx"
report_pdf_path = "outputs/final_report.pdf"

# Ensure outputs folder exists
os.makedirs("outputs", exist_ok=True)

def main():
    # --- Load Data ---
    if not os.path.exists(clustered_points_path):
        print("❌ clustered_points.csv not found. Run the clustering step first.")
        return
    if not os.path.exists(summary_path):
        print("❌ route_summary.csv not found. Run route_optimization.py first.")
        return

    clustered_df = pd.read_csv(clustered_points_path)
    route_df = pd.read_csv(summary_path)

    # --- Clean Columns ---
    route_df.columns = route_df.columns.str.strip().str.lower()

    # --- Merge Cluster Summary ---
    cluster_summary = clustered_df.groupby("cluster").agg(
        Num_Points=('latitude', 'count')
    ).reset_index()

    final_summary = pd.merge(cluster_summary, route_df, on="cluster", how="left")

    # --- Calculate Totals ---
    total_distance = final_summary["distance_km"].sum()
    total_fuel = final_summary["fuel_liters"].sum()
    total_cost = final_summary["cost_rs"].sum()
    total_co2 = final_summary["co2_kg"].sum()

    # --- Save Excel Report ---
    with pd.ExcelWriter(report_excel_path) as writer:
        clustered_df.to_excel(writer, sheet_name="Clustered Points", index=False)
        final_summary.to_excel(writer, sheet_name="Cluster Summary", index=False)

    print(f"✅ Excel report saved: {report_excel_path}")

    # --- Generate PDF Report ---
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Solid Waste Route Optimization Report", ln=True, align="C")

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Clusters: {len(final_summary)}", ln=True)
    pdf.cell(200, 10, txt=f"Total Distance: {total_distance:.2f} km", ln=True)
    pdf.cell(200, 10, txt=f"Total Fuel Used: {total_fuel:.2f} L", ln=True)
    pdf.cell(200, 10, txt=f"Total Cost: Rs {total_cost:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total CO2 Emission: {total_co2:.2f} kg", ln=True)
    pdf.ln(10)

    # --- Table Header ---
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(20, 10, "Cluster", 1)
    pdf.cell(40, 10, "Points", 1)
    pdf.cell(40, 10, "Distance (km)", 1)
    pdf.cell(40, 10, "Fuel (L)", 1)
    pdf.cell(40, 10, "CO2 (kg)", 1, ln=True)

    # --- Table Data ---
    pdf.set_font("Arial", '', 12)
    for _, row in final_summary.iterrows():
        pdf.cell(20, 10, str(row['cluster']), 1)
        pdf.cell(40, 10, str(row['Num_Points']), 1)
        pdf.cell(40, 10, f"{row['distance_km']:.2f}", 1)
        pdf.cell(40, 10, f"{row['fuel_liters']:.2f}", 1)
        pdf.cell(40, 10, f"{row['co2_kg']:.2f}", 1, ln=True)

    pdf.output(report_pdf_path)
    print(f"✅ PDF report saved: {report_pdf_path}")

    print("\n📊 Report generation complete!")
    print(f"📁 Files created:\n- {report_excel_path}\n- {report_pdf_path}")

if __name__ == "__main__":
    main()
