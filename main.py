import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt  
import plotly.express as px
import base64

CONST_URL_DATA = "https://zenodo.org/record/7339445/files/IMDB%20Selection%20Database.csv?download=1"
CONST_HISTOGRAM_PATH = "docs/histogram.png"
CONST_RADARCHAT_PATH = "docs/radarchat.png"
CONST_SPARKLINE_PATH = "docs/sparkline.html"


def calculate_mean(df, genre):

    sum_value = 0
    iterator = 0

    for index, row in df.iterrows():
        if genre in str(row['genres']):
            sum_value += float(row['score'])
            iterator += 1

    return sum_value/iterator

def get_score_by_genre(df, genre):

    score_genre = []

    for index, row in df.iterrows():
        if genre in str(row['genres']):
            score_genre.append(float(row['score']))

    return score_genre

def generate_histogram(values):

    plt.hist(x=values)
    plt.ylabel('Puntuaciones')
    plt.title('Histograma de puntuaciones de películas recogidos en IMDB')
    plt.savefig(CONST_HISTOGRAM_PATH)

def generate_radar_chat(values, description_values):
    data_frame = pd.DataFrame(dict(
        r=values,
        theta=description_values))
    fig = px.line_polar(data_frame, r='r', theta='theta', line_close=True)
    fig.show()
    fig.write_image(CONST_RADARCHAT_PATH)

def sparkline(data, figsize=(4, 0.25), **kwags):

    data = list(data)

    fig, ax = plt.subplots(1, 1, figsize=figsize, **kwags)
    ax.plot(data)
    for k,v in ax.spines.items():
        v.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.plot(len(data) - 1, data[len(data) - 1], 'r.')

    ax.fill_between(range(len(data)), data, len(data)*[min(data)], alpha=0.1)

    img = BytesIO()
    plt.savefig(img, transparent=True, bbox_inches='tight')
    img.seek(0)
    plt.close()

    return base64.b64encode(img.read()).decode("UTF-8")

def generate_sparkline(values):

    with open(CONST_SPARKLINE_PATH, "w") as file:
        for value in values:
            file.write('<div><img src="data:image/png;base64,{}"/></div>'.format(sparkline(value)))

if __name__ == "__main__":

    dataSet = pd.read_csv(CONST_URL_DATA)

    genres_list =[genre.replace("'", "") for genre in set(
        np.concatenate(
        dataSet['genres'].apply(lambda x: x[1:-1].split(', ')).values))]

    genre_means = []
    genre_scores = []

    for genre in genres_list:
        genre_means.append(calculate_mean(dataSet, genre))
        genre_scores.append(get_score_by_genre(dataSet, genre))
    
    generate_histogram(dataSet['score'])
    generate_radar_chat(genre_means, genres_list)
    generate_sparkline(genre_scores)
    

