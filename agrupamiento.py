# Imports 
import pandas as pd
import numpy as np
import pickle

# Leer usuario 
respuesta = pd.read_csv('./static/zodiacN.csv')
X = np.array(respuesta)

features = ["confianza","optimista","atencion","afecto","extrovertida","inteligente","fiesta","fisico","ejercicio","solitaria","viajar","estacion","emprendedor","pesimista","introvertida","elemento"]

respuesta = respuesta.dropna(subset=features)

data = respuesta[features].copy()

data = (data - data.min()) / (data.max() - data.min()) * 9 + 1

def random_centroids(data, k):
    centroids = []
    for i in range(k):
        centroid = data.apply(lambda x: float(x.sample()))
        centroids.append(centroid)
    return pd.concat(centroids, axis=1) 

centroids = random_centroids(data, 4)

def get_labels(data, centroids):
    distances = centroids.apply(lambda x: np.sqrt(((data - x)**2).sum(axis=1)))
    return distances.idxmin(axis=1)

labels = get_labels(data, centroids)

def new_centroids(data, labels, k):
    return data.groupby(labels).apply(lambda x: np.exp(np.log(x).mean())).T

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from IPython.display import clear_output

def plot_clusters(data, labels, centroids, iteration):
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(data)
    centroids_2d = pca.transform(centroids.T)
    clear_output(wait=True)
    plt.title(f'Número de iteración: {iteration}')
    plt.scatter(x=data_2d[:,0], y=data_2d[:,1], c=labels, label=labels )
    plt.scatter(x=centroids_2d[:,0], y=centroids_2d[:,1], c="red", marker ='*', label='centroides')
    plt.grid(True)
    plt.savefig(f'./static/images/imgAgrupamiento/pic{iteration}.png')

max_iterations = 10
k = 4
 
centroids = random_centroids(data, k)
old_centroids = pd.DataFrame()
iteration = 1

while iteration < max_iterations and not centroids.equals(old_centroids):
    old_centroid = centroids
    
    labels = get_labels(data, centroids)
    centroids = new_centroids(data, labels, k)
    plot_clusters(data, labels, centroids, iteration)
    iteration += 1

print(centroids)
print(centroids.shape)

# Salvar los centroides como un archivo pickle localmente
with open('freezed_centroids.pkl','wb') as f:
    pickle.dump(centroids, f)
    print('Los centroides fueron guardados como un archivo pickle localmente.')
