# -*- coding: utf-8 -*-
"""Netflix User Behavior.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1c-YXGr4urNBZ8Er8eicW75CMp-R2PmU7
"""

# ------------------ INSTALL DEPENDENCIES ------------------
!pip install pandas matplotlib seaborn --quiet

# ------------------ IMPORT LIBRARIES ------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta, datetime
import random

# Set plot style and random seed
sns.set(style='whitegrid')
np.random.seed(42)

# ------------------ CONTENT METADATA ------------------

hollywood_movies = [
    'Inception', 'The Dark Knight', 'Avengers: Endgame', 'Titanic', 'Interstellar',
    'Avatar', 'Joker', 'The Matrix', 'Forrest Gump', 'Gladiator'
]

bollywood_movies = [
    '3 Idiots', 'Dangal', 'PK', 'Bajrangi Bhaijaan', 'Sholay',
    'Zindagi Na Milegi Dobara', 'Bahubali', 'Lagaan', 'Gully Boy', 'Kahaani'
]

web_series = [
    'Stranger Things', 'Breaking Bad', 'Money Heist', 'Sacred Games', 'Mirzapur',
    'The Witcher', 'Game of Thrones', 'The Family Man', 'Dark', 'Friends'
]

all_titles = hollywood_movies + bollywood_movies + web_series

genres = {
    'Inception': 'Sci-Fi', 'The Dark Knight': 'Action', 'Avengers: Endgame': 'Action',
    'Titanic': 'Romance', 'Interstellar': 'Sci-Fi', 'Avatar': 'Sci-Fi', 'Joker': 'Drama',
    'The Matrix': 'Sci-Fi', 'Forrest Gump': 'Drama', 'Gladiator': 'Action',
    '3 Idiots': 'Comedy', 'Dangal': 'Drama', 'PK': 'Comedy', 'Bajrangi Bhaijaan': 'Drama',
    'Sholay': 'Action', 'Zindagi Na Milegi Dobara': 'Drama', 'Bahubali': 'Action',
    'Lagaan': 'Historical', 'Gully Boy': 'Musical', 'Kahaani': 'Thriller',
    'Stranger Things': 'Thriller', 'Breaking Bad': 'Crime', 'Money Heist': 'Thriller',
    'Sacred Games': 'Crime', 'Mirzapur': 'Crime', 'The Witcher': 'Fantasy',
    'Game of Thrones': 'Fantasy', 'The Family Man': 'Action', 'Dark': 'Mystery', 'Friends': 'Comedy'
}

content_types = {title: 'Web Series' if title in web_series else 'Movie' for title in all_titles}
languages = {title: 'Hindi' if title in bollywood_movies or title in ['Sacred Games', 'Mirzapur', 'The Family Man'] else 'English' for title in all_titles}
countries = {title: 'India' if languages[title] == 'Hindi' else 'USA' for title in all_titles}
durations = {title: random.randint(40, 180) for title in all_titles}

# ------------------ SYNTHETIC LOG GENERATION ------------------

n_users = 1000
n_logs = 30000

users = [f'user_{i}' for i in range(1, n_users + 1)]
devices = ['Mobile', 'TV', 'Laptop', 'Tablet']
subscriptions = ['Basic', 'Standard', 'Premium']

data = {
    'user_id': np.random.choice(users, n_logs),
    'title': np.random.choice(all_titles, n_logs),
    'device_used': np.random.choice(devices, n_logs),
    'subscription_type': np.random.choice(subscriptions, n_logs),
    'is_rewatch': np.random.choice([0, 1], n_logs, p=[0.7, 0.3]),
    'rating': np.random.randint(1, 6, n_logs),
    'timestamp': [],
    'watch_time': [],
}

for i in range(n_logs):
    title = data['title'][i]
    full_duration = durations[title]
    watch_time = random.randint(10, full_duration)
    timestamp = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 180), hours=random.randint(0, 23), minutes=random.randint(0, 59))

    data['watch_time'].append(watch_time)
    data['timestamp'].append(timestamp)

df = pd.DataFrame(data)
df['genre'] = df['title'].map(genres)
df['duration'] = df['title'].map(durations)
df['completion_ratio'] = df['watch_time'] / df['duration']
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day_name()
df['content_type'] = df['title'].map(content_types)
df['language'] = df['title'].map(languages)
df['country'] = df['title'].map(countries)

# ------------------ ANALYSIS & VISUALIZATION ------------------

# Top Titles
top_titles = df['title'].value_counts().head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=top_titles.values, y=top_titles.index, palette='coolwarm')
plt.title("Top 10 Watched Titles")
plt.xlabel("Views")
plt.ylabel("Title")
plt.tight_layout()
plt.show()

# Genre Distribution
plt.figure(figsize=(10,6))
sns.countplot(data=df, y='genre', order=df['genre'].value_counts().index, palette='Set3')
plt.title("Genre Popularity")
plt.tight_layout()
plt.show()

# Device Usage
plt.figure(figsize=(8,6))
sns.countplot(data=df, x='device_used', palette='pastel')
plt.title("Devices Used for Watching")
plt.tight_layout()
plt.show()

# Completion by Subscription Type
plt.figure(figsize=(10,6))
sns.boxplot(data=df, x='subscription_type', y='completion_ratio', palette='Blues')
plt.title("Completion Ratio by Subscription")
plt.tight_layout()
plt.show()

# Language Distribution
plt.figure(figsize=(6,6))
df['language'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightgreen'])
plt.title("Language Distribution of Content Watched")
plt.ylabel('')
plt.tight_layout()
plt.show()

# Hourly Viewing Pattern
plt.figure(figsize=(12,5))
sns.histplot(data=df, x='hour', bins=24, kde=True, color='teal')
plt.title("Hourly Viewing Pattern")
plt.xlabel("Hour of Day")
plt.tight_layout()
plt.show()

# Heatmap by Day and Hour
heatmap_data = df.groupby(['day', 'hour']).size().unstack().fillna(0)
plt.figure(figsize=(14,6))
sns.heatmap(heatmap_data, cmap='YlOrRd', linewidths=0.5)
plt.title('View Count Heatmap (Day vs Hour)')
plt.xlabel('Hour')
plt.ylabel('Day')
plt.tight_layout()
plt.show()

# Correlation Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(df[['watch_time', 'rating', 'completion_ratio', 'is_rewatch']].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()

# Content Type vs Views
plt.figure(figsize=(6,6))
sns.countplot(data=df, x='content_type', palette='autumn')
plt.title("Content Type Distribution")
plt.tight_layout()
plt.show()