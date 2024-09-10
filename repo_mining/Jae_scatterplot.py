import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors

def prepare_data(file):
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
    return df

def plot_data(df):
    authors = df['Author'].unique()
    colors = list(mcolors.TABLEAU_COLORS.keys())
    color_map = {author: colors[i % len(colors)] for i, author in enumerate(authors)}

    plt.figure(figsize=(12, 8))
    for author in authors:
        author_data = df[df['Author'] == author]
        plt.scatter(author_data['Week'], author_data['Filename'], color=color_map[author], label=author, alpha=0.6)

    plt.xlabel('Week')
    plt.ylabel('Filename')
    plt.title('File Touches Over Time by Author')
    plt.legend()
    plt.grid(True)
    plt.show()

df = prepare_data('data/authors_dates.csv')
plot_data(df)

