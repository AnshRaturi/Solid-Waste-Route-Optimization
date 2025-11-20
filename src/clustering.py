# src/clustering.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# Ensure output folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# ==============================================================
# 🔹 AUTO-OPTIMIZING KMEANS CLUSTERING
# ==============================================================
def find_best_k(X_scaled, k_min=2, k_max=10, random_state=42):
    results = []
    for k in range(k_min, k_max + 1):
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=20)
        labels = kmeans.fit_predict(X_scaled)
        if len(set(labels)) == 1:
            continue
        sil = silhouette_score(X_scaled, labels)
        db = davies_bouldin_score(X_scaled, labels)
        ch = calinski_harabasz_score(X_scaled, labels)
        results.append((k, sil, db, ch))
    return results


def cluster_points(n_clusters=None, use_waste=True, k_min=2, k_max=10):
    """
    Automatically clusters simulated waste collection points using KMeans.
    Selects optimal K based on Silhouette, DB, and CH scores.
    use_waste=True -> includes waste_kg as a feature.
    """
    # Load data
    if not os.path.exists("data/simulated_points.csv"):
        raise FileNotFoundError("❌ data/simulated_points.csv not found. Run data_simulation.py first.")
    df = pd.read_csv("data/simulated_points.csv")

    # Features for clustering
    features = ['latitude', 'longitude']
    if use_waste and 'waste_kg' in df.columns:
        features.append('waste_kg')

    X = df[features].copy()

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Auto-select K
    if n_clusters is None:
        results = find_best_k(X_scaled, k_min=k_min, k_max=k_max)
        if not results:
            raise RuntimeError("No valid clustering results found. Check your data.")

        results_sorted = sorted(results, key=lambda r: (r[1], r[3], -r[2]), reverse=True)
        best_k, best_sil, best_db, best_ch = results_sorted[0]

        print("k | Silhouette | Davies–Bouldin | Calinski–Harabasz")
        print("--|-------------|----------------|-------------------")
        for k, sil, db, ch in results:
            print(f"{k:2d} | {sil:0.3f}      | {db:0.3f}         | {ch:0.1f}")
        print(f"\n✅ Best K = {best_k} (Silhouette={best_sil:.3f}, DB={best_db:.3f}, CH={best_ch:.1f})")
        n_clusters = best_k

        # Save silhouette plot
        ks = [r[0] for r in results]
        sils = [r[1] for r in results]
        plt.figure(figsize=(6, 4))
        plt.plot(ks, sils, marker='o', linewidth=2)
        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Silhouette Score")
        plt.title("Silhouette Score vs k")
        plt.grid(True)
        plt.savefig("outputs/silhouette_vs_k.png", dpi=150)
        plt.close()
        print("📊 Saved silhouette plot: outputs/silhouette_vs_k.png")

    # Fit final model
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # Save results
    df.to_csv('data/clustered_points.csv', index=False)

    # Plot clusters
    plt.figure(figsize=(8, 6))
    plt.scatter(df['longitude'], df['latitude'], c=df['cluster'], cmap='tab10', s=40, edgecolor='k', linewidth=0.4)
    plt.title(f"Optimized City Waste Clusters (k={n_clusters})")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.savefig('data/cluster_map.png', dpi=150)
    plt.close()
    print("🗺️ Saved cluster map: data/cluster_map.png")

    # Compute metrics
    labels = df['cluster']
    sil = silhouette_score(X_scaled, labels)
    db = davies_bouldin_score(X_scaled, labels)
    ch = calinski_harabasz_score(X_scaled, labels)

    print("\n📈 Final Clustering Quality:")
    print(f"   Silhouette Score      : {sil:.3f}")
    print(f"   Davies–Bouldin Index  : {db:.3f}")
    print(f"   Calinski–Harabasz     : {ch:.3f}")
    print(f"📁 Results saved in: data/clustered_points.csv")

# ==============================================================
# 🔹 DBSCAN FALLBACK (non-spherical clusters)
# ==============================================================
def dbscan_clustering(eps=0.03, min_samples=5):
    from sklearn.cluster import DBSCAN

    df = pd.read_csv("data/simulated_points.csv")
    X = df[['latitude', 'longitude', 'waste_kg']]
    X_scaled = StandardScaler().fit_transform(X)

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X_scaled)
    df['cluster'] = labels
    df.to_csv('data/clustered_points.csv', index=False)

    if len(set(labels)) > 1:
        sil = silhouette_score(X_scaled, labels)
        db = davies_bouldin_score(X_scaled, labels)
        ch = calinski_harabasz_score(X_scaled, labels)
        print(f"\n🧭 DBSCAN Results — Silhouette={sil:.3f}, DB={db:.3f}, CH={ch:.1f}")
    else:
        print("⚠️ DBSCAN created only one cluster — try adjusting eps or min_samples.")

# ==============================================================
# 🔹 AGGLOMERATIVE FALLBACK (hierarchical)
# ==============================================================
def agglomerative_clustering(n_clusters=4):
    from sklearn.cluster import AgglomerativeClustering

    df = pd.read_csv("data/simulated_points.csv")
    X = df[['latitude', 'longitude', 'waste_kg']]
    X_scaled = StandardScaler().fit_transform(X)

    model = AgglomerativeClustering(n_clusters=n_clusters)
    labels = model.fit_predict(X_scaled)
    df['cluster'] = labels
    df.to_csv('data/clustered_points.csv', index=False)

    sil = silhouette_score(X_scaled, labels)
    db = davies_bouldin_score(X_scaled, labels)
    ch = calinski_harabasz_score(X_scaled, labels)
    print(f"\n🧭 Agglomerative Results — Silhouette={sil:.3f}, DB={db:.3f}, CH={ch:.1f}")

# ==============================================================
# 🔹 ENTRY POINT
# ==============================================================
if __name__ == "__main__":
    # Auto-optimized clustering: finds best k in range 2–10
    cluster_points(n_clusters=None, use_waste=False, k_min=2, k_max=14)
