import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from geopy.distance import geodesic

# --------------------------
# CONFIGURATION CONSTANTS
# --------------------------
VEHICLE_MILEAGE = 4.0           # km per liter
FUEL_COST_PER_LITER = 90.0      # ₹ per liter
CO2_PER_KM = 2.68               # kg CO₂ emitted per km

# --------------------------
# CORE ROUTE COMPUTATION
# --------------------------
def compute_shortest_route(points):
    """Compute the shortest route using a simple nearest-neighbor heuristic."""
    G = nx.Graph()

    for i, row in points.iterrows():
        G.add_node(i, pos=(row['latitude'], row['longitude']))

    for i, r1 in points.iterrows():
        for j, r2 in points.iterrows():
            if i != j:
                dist = geodesic((r1['latitude'], r1['longitude']),
                                (r2['latitude'], r2['longitude'])).km
                G.add_edge(i, j, weight=dist)

    visited = [points.index[0]]
    total_distance = 0
    while len(visited) < len(points):
        last = visited[-1]
        remaining = [n for n in points.index if n not in visited]
        next_node = min(remaining, key=lambda n: G[last][n]['weight'])
        total_distance += G[last][next_node]['weight']
        visited.append(next_node)

    total_distance += G[visited[-1]][visited[0]]['weight']
    visited.append(visited[0])

    return visited, total_distance


# --------------------------
# OPTIMIZATION & ANALYSIS
# --------------------------
def optimize_routes():
    df = pd.read_csv('data/clustered_points.csv')

    results = []
    total_distance_all = 0
    total_fuel = 0
    total_cost = 0
    total_co2 = 0

    for cluster_id in df['cluster'].unique():
        cluster_points = df[df['cluster'] == cluster_id].reset_index(drop=True)
        route, total_distance = compute_shortest_route(cluster_points)

        # ---- Calculations ----
        fuel_used = total_distance / VEHICLE_MILEAGE
        cost = fuel_used * FUEL_COST_PER_LITER
        co2_emission = total_distance * CO2_PER_KM

        total_distance_all += total_distance
        total_fuel += fuel_used
        total_cost += cost
        total_co2 += co2_emission

        results.append({
            'cluster': cluster_id,
            'distance_km': round(total_distance, 2),
            'fuel_liters': round(fuel_used, 2),
            'cost_rs': round(cost, 0),
            'co2_kg': round(co2_emission, 1)
        })

        # ---- Plot the route ----
        plt.figure(figsize=(8, 6))
        plt.scatter(cluster_points['latitude'], cluster_points['longitude'], c='blue', s=40)
        for i in range(len(route) - 1):
            p1 = cluster_points.iloc[route[i]]
            p2 = cluster_points.iloc[route[i + 1]]
            plt.plot([p1['latitude'], p2['latitude']], [p1['longitude'], p2['longitude']], 'r-')

        plt.title(f"Cluster {cluster_id} | {total_distance:.2f} km | ₹{cost:.0f} | {co2_emission:.1f} kg CO₂")
        plt.xlabel("Latitude")
        plt.ylabel("Longitude")
        plt.grid(True)
        plt.savefig(f"data/route_cluster_{cluster_id}.png")

        print(f"✅ Cluster {cluster_id}: {total_distance:.2f} km | Fuel {fuel_used:.2f} L | ₹{cost:.0f} | CO₂ {co2_emission:.1f} kg")

    # ---- Save summary ----
    df_summary = pd.DataFrame(results)
    df_summary.to_csv("data/route_summary.csv", index=False)

    print("\n🌍 TOTAL SYSTEM SUMMARY")
    print(f"   Total Distance: {total_distance_all:.2f} km")
    print(f"   Total Fuel Used: {total_fuel:.2f} L")
    print(f"   Total Fuel Cost: ₹{total_cost:.0f}")
    print(f"   Total CO₂ Emission: {total_co2:.1f} kg")
    print("\n📁 Saved route summary to data/route_summary.csv")


if __name__ == "__main__":
    optimize_routes()
