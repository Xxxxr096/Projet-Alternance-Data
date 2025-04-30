# Importation des bibliothèques nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import re
import os


# Fonction  conversion du poids
def convert_weight(cond):
    cond = str(cond).lower()
    match = re.search(r"\d+(?:[\.,]\d+)?", cond)
    if match:
        number = float(match.group().replace(",", "."))
        if "kg" in cond:
            return number * 1000
        elif "g" in cond:
            return number
    return None


# Chargement et nettoyage des données
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    df = df.rename(
        columns={
            "ia_product": "interpretation_product",
            "conditioning_unit": "conditioning",
            "unit_price_without_tax": "price",
        }
    )
    # Supprimer les lignes sans produit, conditionnement ou prix
    df = df.dropna(subset=["interpretation_product", "conditioning", "price"])
    df = df[(df["price"] > 0) & (df["price"] <= 150)]
    return df


# Préparation des données pour clustering
def prepare_clustering_data(df):
    cluster_df = (
        df.groupby(["interpretation_product", "conditioning"])
        .agg({"price": "mean"})
        .reset_index()
    )
    cluster_df["weight_in_g"] = cluster_df["conditioning"].apply(
        lambda x: convert_weight(str(x))
    )
    cluster_df = cluster_df.dropna(subset=["weight_in_g"])
    return cluster_df


# Clustering avec KMeans
def run_kmeans_clustering(cluster_df, n_clusters=3):
    """
    Applique l’algorithme KMeans sur les données standardisées (prix et poids).
    Retourne les clusters et les centroïdes.
    """
    X = cluster_df[["price", "weight_in_g"]]
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(normalized_data)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    # Ajouter les étiquettes aux données
    cluster_df["cluster"] = labels
    # Revenir aux valeurs originales (non standardisées)
    original_values = scaler.inverse_transform(normalized_data)
    cluster_df["price_original"] = original_values[:, 0]
    cluster_df["weight_original"] = original_values[:, 1]

    return cluster_df, centroids


# Visualisation des clusters
def plot_clusters(data, centroids):
    """
    Affiche les points clusterisés et les centroïdes sur un scatterplot.
    Sauvegarde le graphique dans 'clusters.png'.
    """
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        data["weight_in_g"], data["price"], c=data["cluster"], cmap="tab10", s=50
    )
    for i, center in enumerate(centroids):
        plt.scatter([], [], color=scatter.cmap(scatter.norm(i)), label=f"Cluster {i}")
    plt.xlabel("Poids (g)")
    plt.ylabel("Prix unitaire moyen (HT)")
    plt.title("Clustering des produits")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("clusters.png")
    plt.show()


# ----------- EXECUTION PRINCIPALE -----------
def main():
    file_path = "extrait_produits.csv"
    if not os.path.exists(file_path):
        print(f"Erreur : fichier '{file_path}' non trouvé.")
        return

    print("Chargement et nettoyage des données...")
    data = load_and_clean_data(file_path)

    print("Préparation des données pour le clustering...")
    cluster_data = prepare_clustering_data(data)

    print("Application de KMeans clustering...")
    cluster_data, centroids = run_kmeans_clustering(cluster_data, n_clusters=3)

    print("Génération du graphique de clusters...")
    plot_clusters(cluster_data, centroids)

    output_file = "resultats_clusters.csv"
    cluster_data.to_csv(output_file, index=False)
    print(f"Résultats enregistrés dans : {output_file}")


if __name__ == "__main__":
    main()
