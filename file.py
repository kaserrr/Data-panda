import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import pandas as pd

# Load the data
data_path = 'C:\\xampp\\htdocs\\Data-panda\\data.csv'  # Adjust this path to where your actual CSV file is located
data = pd.read_csv(data_path)

# Cleaning function to extract numeric values and convert to float
def clean_numeric(column):
    data[column] = data[column].astype(str).str.extract('(\d+\.?\d*)', expand=False)
    data[column] = pd.to_numeric(data[column], errors='coerce')

# Clean the 'Budget (in $)' and 'World Wide Sales (in $)' columns
clean_numeric('Budget (in $)')
clean_numeric('World Wide Sales (in $)')

# Create a 2x2 subplot grid
fig, axs = plt.subplots(2, 2, figsize=(20, 15))

# Adjust space between plots
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

# First Plot: Yearly Movie Counts (Line Plot)
yearly_movie_counts = data.groupby('Year').size()
axs[0, 0].plot(yearly_movie_counts.index, yearly_movie_counts.values, color='green', marker='o', linewidth=2, markersize=5)
axs[0, 0].set_title('Yearly Movie Counts')
axs[0, 0].set_xlabel('Year')
axs[0, 0].set_ylabel('Number of Movies')
axs[0, 0].grid(True)

# Second Plot: Budget vs. Worldwide Sales (Hexbin Plot)
hb = axs[0, 1].hexbin(data['Budget (in $)'], data['World Wide Sales (in $)'], gridsize=50, cmap='Blues', bins='log')
axs[0, 1].set_title('Budget vs. Worldwide Sales')
axs[0, 1].set_xlabel('Budget ($)')
axs[0, 1].set_ylabel('Worldwide Sales ($)')
axs[0, 1].set_xscale('log')
axs[0, 1].set_yscale('log')
fig.colorbar(hb, ax=axs[0, 1], label='log10(N)')

# Third Plot: Domestic vs. International Sales (Stacked Bar Chart)
data_short = data[['Title', 'Domestic Sales (in $)', 'International Sales (in $)']].head(5)
data_short.set_index('Title').plot(kind='bar', stacked=True, ax=axs[1, 0])
axs[1, 0].set_title('Domestic vs. International Sales')
axs[1, 0].set_ylabel('Sales ($)')
axs[1, 0].tick_params(labelrotation=45)

# Fourth Plot: Distribution of Genres (Word Cloud)
genre_string = ' '.join([' '.join(ast.literal_eval(genre)) for genre in data['Genre'] if pd.notnull(genre)])
wordcloud = WordCloud(width=400, height=200, background_color='white').generate(genre_string)
axs[1, 1].imshow(wordcloud, interpolation='bilinear')
axs[1, 1].axis('off')
axs[1, 1].set_title('Word Cloud of Movie Genres')

plt.show()
