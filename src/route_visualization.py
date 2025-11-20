import pandas as pd
import plotly.graph_objects as go

def visualize_route_efficiency():
    df = pd.read_csv("data/route_summary.csv")

    # Create a simple efficiency metric
    df["efficiency_score"] = (df["distance_km"] / df["fuel_liters"]).round(2)

    # ---- Bar chart for Distance, Fuel, and Cost ----
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["cluster"], y=df["distance_km"],
        name="Distance (km)", marker_color="royalblue"
    ))
    fig.add_trace(go.Bar(
        x=df["cluster"], y=df["fuel_liters"],
        name="Fuel (L)", marker_color="orange"
    ))
    fig.add_trace(go.Bar(
        x=df["cluster"], y=df["cost_rs"],
        name="Cost (₹)", marker_color="green"
    ))

    fig.update_layout(
        title="🚛 Route Efficiency per Cluster",
        xaxis_title="Cluster ID",
        yaxis_title="Value",
        barmode="group",
        template="plotly_white"
    )

    fig.show()

    # ---- CO₂ emissions ----
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df["cluster"], y=df["co2_kg"],
        name="CO₂ Emission (kg)", marker_color="red"
    ))
    fig2.update_layout(
        title="🌍 CO₂ Emission per Cluster",
        xaxis_title="Cluster ID",
        yaxis_title="CO₂ (kg)",
        template="plotly_white"
    )
    fig2.show()

    # ---- Efficiency metric ----
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df["cluster"], y=df["efficiency_score"],
        mode="lines+markers",
        name="Efficiency Score",
        marker_color="purple"
    ))
    fig3.update_layout(
        title="⚙️ Efficiency Score (Distance per Liter of Fuel)",
        xaxis_title="Cluster ID",
        yaxis_title="Efficiency Score",
        template="plotly_white"
    )
    fig3.show()

if __name__ == "__main__":
    visualize_route_efficiency()
