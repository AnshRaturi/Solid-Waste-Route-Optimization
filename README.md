Solid Waste Collection Route Optimization using Cluster Analysis
Student Details
• Name: Ansh Raturi
• College: Lovely Professional University
• Project Title: Solid Waste Collection Route Optimization using Cluster Analysis

1. Problem Statement
Urban waste collection systems often suffer from inefficient routing, leading to
increased fuel consumption, higher operational costs, traffic congestion, and greater
carbon emissions. Municipal vehicles frequently follow static or poorly optimized routes
that do not adapt to waste distribution patterns.
This project addresses the problem by designing an intelligent system that optimizes
garbage truck routes based on geographic waste distribution using machine learning
and clustering techniques.

2. Proposed Solution
The solution uses unsupervised Machine Learning (Clustering) to divide waste
collection points into optimized zones. Each zone is then assigned an optimized route
for vehicle traversal using a nearest-neighbor routing heuristic.
This approach ensures:
• Reduced travel distance per vehicle
• Balanced load distribution
• Lower fuel consumption
• Decreased CO2 emissions
Simulation-based data generation allows scalability testing for real-world adaptation.

3. Tech Stack
Languages
• Python 3.13
Libraries & Frameworks

• pandas – Data handling
• numpy – Numerical processing
• scikit-learn – Clustering algorithms
• matplotlib – Route visualization
• networkx – Graph-based routing
• plotly – Interactive efficiency visualisation
• fpdf – PDF generation
• geopy – Geographical distance calculation
Tools
• VS Code
• PowerShell
• Git

4. System Architecture
Workflow Overview
Simulated Data → Clustering Engine → Route Optimizer → Efficiency Analyzer →
Visualization Engine → Report Generator
Architecture Explanation
1. Data Simulation Module
Generates synthetic waste collection coordinates and waste volumes.
2. Clustering Engine
Applies K-Means clustering to group locations into zones.
3. Route Optimization Module
Uses graph traversal logic to compute shortest collection routes.
4. Efficiency Analysis Module
Calculates fuel usage, cost, emissions, and efficiency score.
5. Visualization Engine
Generates 2D maps and browser-based performance dashboards.
6. Report Generator
Exports results in both Excel and PDF formats.

5. Core Features
Feature Purpose User Value
Zone-based
clustering

Divides city into efficient garbage
zones

Balanced workload & time
saving

Route optimization Minimizes distance per cluster

Reduced fuel & operational
cost

Emission tracking Displays CO2 output per route

Environmental impact
awareness

Efficiency scoring Evaluates route productivity

Helps optimize future
planning

Automated
reporting

Generates Excel + PDF reports Professional documentation

Trade-offs
• Nearest-neighbor routing is faster but may not be globally optimal compared to
TSP solvers.
• Synthetic data simplifies real-world noise.

6. Setup & Run Guide
Prerequisites
• Python 3.10+
• pip
Installation
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Run Full Project
python src/main.py
This will auto-generate:

• Simulated waste data
• Clustered maps
• Optimized routes
• Performance dashboard
• PDF & Excel reports

7. Environment Variables (.env.example)
PROJECT_NAME=Solid Waste Route Optimization
DATA_PATH=data/
OUTPUT_PATH=outputs/
N_CLUSTERS=4
MAX_K=10

8. ML Components
Algorithms Used
• K-Means (Primary)
• DBSCAN (Experimental)
Metrics Used
• Silhouette Score
• Davies-Bouldin Index
• Calinski-Harabasz Index
Best Observed Results
• Silhouette Score: 0.415
• Davies-Bouldin Index: 0.761
• Calinski-Harabasz: 311.065

9. Impact & Metrics

Metric Value
Total Distance Reduced ~35%
Fuel Saved ~28%
CO2 Reduction ~30%
Clustering Accuracy Medium-Good
System tested on 300 simulated points representing a small urban ward.

10. Deployment
Currently runs as a local ML system.
Planned deployment options include:
• Streamlit Web App
• Cloud hosting via Azure / AWS

11. Demo Video Guide
Video covers:
1. Problem explanation
2. Code walkthrough
3. Live run of pipeline
4. Result interpretation
5. Output report demonstration

12. Limitations
• Does not account for traffic conditions
• No real-time GPS integration
• Synthetic dataset only
• Routing heuristic not globally optimal

13. Future Improvements

• Real-time IoT sensor data integration
• Smart bin fill detection
• Dynamic traffic-aware routing
• AI-powered adaptive clustering
• Web-based decision dashboard

14. Conclusion
This project demonstrates how machine learning combined with route optimization can
significantly improve urban waste collection systems. It showcases practical AI
integration for sustainable city planning.
