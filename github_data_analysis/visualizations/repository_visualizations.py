import pandas as pd
import matplotlib.pyplot as plt

def boxplot_commits(csv_file):
    df = pd.read_csv(csv_file)
    df.boxplot(column='Commits', by='State')
    plt.title('Commits in Open vs Closed Pull Requests')
    plt.suptitle('')  # Removes the default title
    plt.xlabel('PR State')
    plt.ylabel('Number of Commits')
    plt.savefig('boxplot_commits.png')
    plt.show()
    
def boxplot_additions_deletions(csv_file):
    df = pd.read_csv(csv_file)
    df[['Additions', 'Deletions']].plot(kind='box')
    plt.title('Additions and Deletions in Pull Requests')
    plt.ylabel('Count')
    plt.savefig('boxplot_additions_deletions.png')
    plt.show()

def boxplot_changed_files_author(csv_file):
    df = pd.read_csv(csv_file)
    df.boxplot(column='Changed_Files', by='Author_Association')
    plt.title('Changed Files by Author Association')
    plt.suptitle('')
    plt.xlabel('Author Association')
    plt.ylabel('Number of Changed Files')
    plt.savefig('boxplot_changed_files_author.png')
    plt.show()

def scatterplot_additions_deletions(csv_file):
    df = pd.read_csv(csv_file)
    df.plot(kind='scatter', x='Additions', y='Deletions')
    plt.title('Relationship Between Additions and Deletions')
    plt.xlabel('Additions')
    plt.ylabel('Deletions')
    plt.savefig('scatterplot_additions_deletions.png')
    plt.show()

def line_graph_prs_per_day(csv_file):
    df = pd.read_csv(csv_file)
    df['Creation_Date'] = pd.to_datetime(df['Creation_Date'])
    df.groupby(df['Creation_Date'].dt.date).size().plot(kind='line')
    plt.title('Total Number of Pull Requests Per Day')
    plt.xlabel('Day')
    plt.ylabel('Number of Pull Requests')
    plt.savefig('line_graph_prs_per_day.png')
    plt.show()

def line_graph_open_closed_prs_per_day(csv_file):
    df = pd.read_csv(csv_file)
    df['Creation_Date'] = pd.to_datetime(df['Creation_Date'])
    pivot = df.pivot_table(index=df['Creation_Date'].dt.date, columns='State', aggfunc='size')
    pivot.plot(kind='line')
    plt.title('Open vs Closed Pull Requests Per Day')
    plt.xlabel('Day')
    plt.ylabel('Number of Pull Requests')
    plt.savefig('line_graph_open_closed_prs_per_day.png')
    plt.show()

