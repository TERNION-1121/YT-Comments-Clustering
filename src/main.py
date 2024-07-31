import matplotlib.pyplot as plt
import multiprocessing as mp
import numpy as np
import os
import pandas as pd
import text_preprocessing as tp
import time

from argparse import ArgumentParser
from math import ceil, log
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud


def preprocess_dataframe(df: pd.DataFrame):
    for func in tp.PROCESSES:
        df["post_clean"] = df["post_clean"].apply(func)
    return df


def process_data(json_path: str, csv_path: str) -> None:
    '''
    json_path: the json file to be processed
    csv_path: the path to save the processed data
    '''

    init = time.time()
    print("Reading data...", end=" ")

    df = pd.read_json(json_path, orient="index")
    df.rename(columns={'comment': 'pre_clean'}, inplace=True) 

    print("Data read successfully", end="\n\n")


    init_c = time.time()
    print("Cleaning data...", end=" ")

    df.insert(2, "post_clean", df["pre_clean"], False)

    num_partitions = mp.cpu_count()  # Number of partitions to split dataframe
    df_split = np.array_split(df, num_partitions)

    # Create a multiprocessing Pool
    pool = mp.Pool(num_partitions)

    # Process the dataframe in parallel
    df = pd.concat(pool.map(preprocess_dataframe, df_split))

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

    print(f"Data cleaned successfully ({time.time() - init_c:.2f})s\n")


    print("Extracting features from cleaned data...", end=" ")

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["post_clean"])

    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
    df = pd.concat([df, tfidf_df], axis=1)

    print(f"Feature extraction performed successfully", end="\n\n")


    init_c = time.time() 
    print(f"Clustering datapoints...", end=" ")

    features = df.iloc[:, 3:]
    # decide number of clusters for a given number of comments using some arbitrary math; max 5
    km = KMeans(n_clusters=5 if log(df.shape[0]) * 0.73 > 5 else ceil(log(df.shape[0]) * 0.73))
    clusters = km.fit_predict(features)
    df.insert(4, 'cluster', clusters)

    print(f"Datapoints clustered successfully", end="\n\n")


    print(f"Writing data to {csv_path}...", end=" ")

    df.to_csv(csv_path, index_label='idx')

    print(f"Data written to csv successfully", end="\n\n")


    print(f"Task complete ({time.time() - init:.2f}s)", end="\n\n")


def display_word_clouds(df: pd.DataFrame) -> None:
    '''
    Display a word cloud for each cluster
    '''
    def generate_word_cloud(text: str, cluster_number: int) -> None:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Word Cloud for Cluster {cluster_number}')
        plt.axis('off')
        plt.show()

    df = df.dropna(subset=['post_clean']).reset_index(drop=True)
    grouped_comments = df.groupby('cluster')['post_clean'].apply(lambda x: ' '.join(x)).reset_index()

    for _, row in grouped_comments.iterrows():
        cluster_number = row['cluster']
        text = row['post_clean']
        generate_word_cloud(text, cluster_number)


def plot_bar_graph(df: pd.DataFrame) -> None:
    '''
    Plot a graph to visualise cluster data
    '''
    result = df.groupby('cluster').agg(
                                        total_likes=('like_count', 'sum'),
                                        total_comments=('like_count', 'count')
                                        ).reset_index()
    df_total_likes = df['like_count'].sum()
    df_total_comments = len(df)
    
    positions = np.arange(len(result['cluster']))
    width = 0.35

    fig, ax = plt.subplots()
    plt.yscale('log')
    bars1 = ax.bar(positions - width/2, result['total_likes'], width, label='Total Likes')
    bars2 = ax.bar(positions + width/2, result['total_comments'], width, label='Total Comments')

    ax.set_xlabel('Cluster')
    ax.set_ylabel('Magnitude/Number')
    ax.set_title('Total Likes and Comments per Cluster')
    ax.set_xticks(positions)
    ax.set_xticklabels(result['cluster'])
    ax.legend()

    def add_labels(bars, percent_denom) -> None:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(str(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), 
                        textcoords="offset points",
                        ha='center', va='bottom')
            
            ax.annotate(f"{round(height / percent_denom * 100)}%",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, -10),  
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    add_labels(bars1, df_total_likes)
    add_labels(bars2, df_total_comments)

    plt.show()


def main():
    parser = ArgumentParser(description="Command Line Utility to cluster (pre-saved) YouTube comments and visualise the results")
    parser.add_argument('json_path', metavar='JSON_PATH', type=str, help='relative path of json file to be processed')
    parser.add_argument('csv_path', metavar='CSV_PATH', type=str, help='relative path of csv file to save the processed data')
    
    args= parser.parse_args()

    process_data(args.json_path, args.csv_path)
    df = pd.read_csv(args.csv_path, index_col='idx')


    input("\nPress Enter to view the visual results ")
    display_word_clouds(df)
    plot_bar_graph(df)


if __name__ == "__main__":
    main()