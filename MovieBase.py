import pandas as pd
import matplotlib.pyplot as plt

# Wczytaj bazę filmów
movies = pd.read_csv(r'C:\Users\leszek.stanislawski\Downloads\Kodilla\Python\Visual\tmdb_movies.csv')

# Wczytaj bazę gatunków
genres = pd.read_csv(r'C:\Users\leszek.stanislawski\Downloads\Kodilla\Python\Visual\tmdb_genres.csv')

# Konwertuj kolumnę 'genre_id' w bazie filmów na typ object
movies['genre_id'] = movies['genre_id'].astype('object')

# Połącz bazy filmów i gatunków
movies_with_genres = pd.merge(movies, genres, left_on='genre_id', right_on='Unnamed: 0', how='left')

# Usuń zbędne kolumny z ramki danych 'movies_with_genres'
# Drop the unnamed index columns from both DataFrames
movies_with_genres.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)
print(movies_with_genres.columns)
# movies_with_genres.drop('Unnamed: 0', axis=1, inplace=True)

# 1. Zwróć listę 10 najwyżej ocenianych filmów
filtered_movies = movies_with_genres[movies_with_genres['vote_count'] > movies_with_genres['vote_count'].quantile(0.75)]
top_rated_movies = filtered_movies.nlargest(10, ['vote_average', 'vote_count'])

print("1. 10 najwyżej ocenianych filmów:")
print(top_rated_movies[['title', 'vote_average', 'vote_count']])

# 2. Grupuj tabelę i stwórz wykres
movies_with_genres['release_year'] = pd.to_datetime(movies_with_genres['release_date']).dt.year  # Dodaj kolumnę 'release_year'
grouped_data = movies_with_genres[(movies_with_genres['release_year'] >= 2010) & (movies_with_genres['release_year'] <= 2016)].groupby('release_year').agg({'revenue': 'mean', 'budget': 'mean'})

# Wykres
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Rok')
ax1.set_ylabel('Średnie przychody', color=color)
ax1.bar(grouped_data.index, grouped_data['revenue'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Średni budżet', color=color)
ax2.plot(grouped_data.index, grouped_data['budget'], color=color, marker='o')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('2. Średnie przychody i średni budżet filmów (2010-2016)')
plt.legend(['Średnie przychody', 'Średni budżet'], loc='upper right')
plt.show()

# 4. Najczęstszy gatunek filmu i ilość filmów tego gatunku
most_common_genre = movies_with_genres['genres'].value_counts().idxmax() if not movies_with_genres['genres'].isnull().all() else None
count_most_common_genre = movies_with_genres[movies_with_genres['genres'] == most_common_genre].shape[0] if most_common_genre else 0

if most_common_genre:
    print("\n4. Najczęstszy gatunek filmu:")
    print(f"Nazwa gatunku: {most_common_genre}")
    print(f"Ilość filmów tego gatunku: {count_most_common_genre}")
else:
    print("\n4. Brak dostępnych danych na temat najczęstszego gatunku filmu, ze względu na brakujące wartości w kolumnie 'genres'.")

# 5. Gatunek filmu trwający średnio najdłużej
avg_runtime_by_genre = movies_with_genres.groupby('genres')['runtime'].mean()
genre_with_longest_runtime = avg_runtime_by_genre.idxmax() if not avg_runtime_by_genre.isnull().all() else None

if genre_with_longest_runtime:
    print("\n5. Gatunek filmu trwający średnio najdłużej:")
    print(f"Nazwa gatunku: {genre_with_longest_runtime}")
else:
    print("\n5. Brak dostępnych danych na temat gatunku filmu trwającego średnio najdłużej, ze względu na brakujące wartości w kolumnie 'runtime'.")

# 6. Histogram czasu trwania filmów z gatunku, który cechuje się największym średnim czasem trwania
if genre_with_longest_runtime:
    longest_runtime_genre_movies = movies_with_genres[movies_with_genres['genres'] == genre_with_longest_runtime]
    plt.hist(longest_runtime_genre_movies['runtime'], bins=20, edgecolor='black')
    plt.xlabel('Czas trwania (minuty)')
    plt.ylabel('Liczba filmów')
    plt.title(f'6. Histogram czasu trwania filmów z gatunku {genre_with_longest_runtime}')
    plt.show()
else:
    print("\n6. Brak dostępnych danych na temat gatunku filmu do stworzenia histogramu, ze względu na brakujące wartości w kolumnie 'runtime'.")
