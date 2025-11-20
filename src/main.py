# src/main.py
import subprocess
import sys
import importlib
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

print("\n=== ♻️ Solid Waste Route Optimization Project ===\n")

# Helper: install missing packages automatically
def ensure_package(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"📦 Installing missing package: {package} ...")
        subprocess.run([sys.executable, "-m", "pip", "install", package])

# Required packages
for pkg in ["pandas", "matplotlib", "scikit-learn", "networkx", "geopy", "fpdf", "plotly"]:
    ensure_package(pkg)

# Step 1: Simulate Data
print("\n🚀 Running data_simulation.py ...")
subprocess.run([sys.executable, "src/data_simulation.py"])

# Step 2: Intelligent Clustering
print("\n🚀 Running clustering.py (auto-optimization mode)...")
from clustering import cluster_points, dbscan_clustering

def evaluate_silhouette(use_waste=True):
    df = pd.read_csv("data/clustered_points.csv")
    features = ['latitude', 'longitude']
    if use_waste and 'waste_kg' in df.columns:
        features.append('waste_kg')
    X_scaled = StandardScaler().fit_transform(df[features])
    return silhouette_score(X_scaled, df['cluster'])

try:
    print("🧠 Attempt 1: KMeans with waste_kg ...")
    cluster_points(n_clusters=None, use_waste=True, k_min=2, k_max=10)
    sil = evaluate_silhouette(use_waste=True)

    if sil < 0.5:
        print(f"\n⚠️ Silhouette={sil:.3f} < 0.5 → retrying geography-only clustering...")
        cluster_points(n_clusters=None, use_waste=False, k_min=2, k_max=10)
        sil = evaluate_silhouette(use_waste=False)

        if sil < 0.5:
            print(f"\n⚠️ Still weak separation (Silhouette={sil:.3f}) → switching to DBSCAN fallback...")
            dbscan_clustering(eps=0.03, min_samples=5)
            sil = evaluate_silhouette(use_waste=False)
            if sil >= 0.5:
                print(f"✅ DBSCAN improved clustering: Silhouette={sil:.3f}")
            else:
                print(f"⚠️ DBSCAN also below threshold (Silhouette={sil:.3f}) – consider tuning eps/min_samples manually.")
        else:
            print(f"✅ Geography-only clustering successful: Silhouette={sil:.3f}")
    else:
        print(f"✅ KMeans clustering successful: Silhouette={sil:.3f}")

except Exception as e:
    print("\n❌ Clustering step failed:", e)

# Step 3: Route Optimization
print("\n🚀 Running route_optimization.py ...")
try:
    subprocess.run([sys.executable, "src/route_optimization.py"], check=True)
except subprocess.CalledProcessError as e:
    print("\n⚠️ Error in route optimization:\n", e)

# Step 4: Visualization
print("\n🚀 Running route_visualization.py ...")
try:
    subprocess.run([sys.executable, "src/route_visualization.py"], check=True)
except subprocess.CalledProcessError as e:
    print("\n⚠️ Error in visualization:\n", e)

# Step 5: Generate Report
print("\n🚀 Running generate_report.py ...")
try:
    subprocess.run([sys.executable, "src/generate_report.py"], check=True)
    print("\n📊 Step 3.1 Complete — Beautified report generated!")
except subprocess.CalledProcessError as e:
    print("\n⚠️ Error in report generation:\n", e)

print("\n✅ Project completed successfully! Check 'outputs/' and 'data/' folders for results.\n")
