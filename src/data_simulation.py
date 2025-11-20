import pandas as pd
import random
import os

def simulate_city_points(center_lat=28.7041, center_lon=77.1025, n=200, spread_km=5):
    os.makedirs('data', exist_ok=True)

    pts = []
    for i in range(1, n+1):
        lat = center_lat + random.uniform(-spread_km/111, spread_km/111)
        lon = center_lon + random.uniform(-spread_km/111, spread_km/111)
        waste = random.randint(3, 30)
        pts.append((i, lat, lon, waste))

    df = pd.DataFrame(pts, columns=['id', 'latitude', 'longitude', 'waste_kg'])
    df.to_csv('data/simulated_points.csv', index=False)
    print('Saved data/simulated_points.csv with', len(df), 'points')

if __name__ == '__main__':
    simulate_city_points(n=300)
