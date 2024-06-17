import pandas as pd
from math import log
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import text_preprocessing as tp
import time
from wordcloud import WordCloud

def process_data(json_path: str, csv_path: str):
    '''
    json_path: the json file to be processed
    csv_path: the path to save the processed data
    '''

    init = time.time()
    print("Reading data...")

    df = pd.read_json(json_path, orient="index")
    df.rename(columns={'comment': 'pre_clean'}, inplace=True) 

    print(f"Data read successfully ({time.time() - init:.2f}s)\n")


    init_c = time.time()
    print("Cleaning data...")

    df.insert(2, "post_clean", df["pre_clean"], False)

    for func in tp.PROCESSES:
        df["post_clean"] = df["post_clean"].apply(func)
    df = df.dropna(subset=['post_clean']).reset_index()
    
    print(f"Data cleaned successfully ({time.time() - init_c:.2f})s\n")


    init_p = time.time()
    print("Extracting features from cleaned data...")

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["post_clean"])

    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
    df = pd.concat([df, tfidf_df], axis=1)

    print(f"Feature extraction performed successfully ({time.time() - init_p:.2f}s)\n")


    init_c = time.time() 
    print(f"Clustering datapoints...")

    features = df.iloc[:, 3:]
    km = KMeans(n_clusters=5 if log(df.shape[0]) > 5 else log(df.shape[0]))
    clusters = km.fit_predict(features)
    df.insert(3, 'cluster', clusters)

    print(f"Datapoints clustered successfully ({time.time() - init_c:.2f}s)\n")


    init_w = time.time()
    print(f"Writing data to {csv_path} ...")

    df.to_csv(csv_path, index_label="idx")

    print(f"Data written to csv successfully ({time.time() - init_w:.2f}s)\n")

    print(f"Task complete ({time.time() - init:.2f}s)")

    return df

def display_word_clouds(df: pd.DataFrame):

    def generate_word_cloud(text, cluster_number):

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Word Cloud for Cluster {cluster_number}')
        plt.axis('off')
        plt.show()

    grouped_comments = df.groupby('cluster')['post_clean'].apply(lambda x: ' '.join(x)).reset_index()

    for _, row in grouped_comments.iterrows():
        cluster_number = row['cluster']
        text = row['post_clean']
        generate_word_cloud(text, cluster_number)

def plot_bar_graph(df: pd.DataFrame):

    result = df.groupby('cluster').agg(
                                        total_likes=('like_count', 'sum'),
                                        total_comments=('like_count', 'count')
                                        ).reset_index()
    
    positions = np.arange(len(result['cluster']))
    width = 0.35

    fig, ax = plt.subplots()
    bars1 = ax.bar(positions - width/2, result['total_likes'], width, label='Total Likes')
    bars2 = ax.bar(positions + width/2, result['total_comments'], width, label='Total Comments')

    ax.set_xlabel('Cluster')
    ax.set_ylabel('Magnitude/Number')
    ax.set_title('Total Likes and Comments per Cluster')
    ax.set_xticks(positions)
    ax.set_xticklabels(result['cluster'])
    ax.legend()

    def add_labels(bars):

        for bar in bars:
            height = bar.get_height()
            ax.annotate(str(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    add_labels(bars1)
    add_labels(bars2)

    plt.show()

def main():
    # process_data("raw-data/comments_1.json", "data/comments_1.csv")
    df = pd.read_csv("data/comments_1.csv", index_col="idx")

    display_word_clouds(df)
    plot_bar_graph(df)

if __name__ == "__main__":
    main()