import sqlite3
import matplotlib.pyplot as plt
import os

genres = ['Romance', 'Comedy', 'Animation', 'Mystery', 'Documentary', 'Crime', 'Family', \
          'Sport', 'Biography', 'History', 'Western', 'Sci-fi', 'Horror', 'Adventure', 'Drama', \
          'Fantasy', 'Thriller', 'Action']

if not os.path.exists('Genres'):
    os.makedirs('Genres')

with open(os.path.join('Genres', 'index.html'), 'w') as fp:
    fp.write('<h1>Genre releases by year of movies shown in more than 2000 theaters</h1>')

conn = sqlite3.connect('movies.db')
for genre in genres:
    sql = 'select year, count(distinct(title)) c from combined_boxoffice where genres like "%{}%" and theatersopen > 2000 group by year' .format(genre)
    x = [item[0] for item in conn.execute(sql)]
    y = [item[1] for item in conn.execute(sql)]

    plt.figure(figsize=(10, 5))
    plt.xlabel('Year', size = 16)
    plt.ylabel('{} titles' .format(genre), size = 16)

    plt.bar(x, y, align='center', width=0.8)
    plt.savefig(os.path.join('Genres', 'Theatrical_Wide_{}.png') .format(genre.replace('/', '_')))
    with open(os.path.join('Genres', 'index.html'), 'a') as fp:
        fp.write('<img src="Theatrical_Wide_{}.png" /><br>' .format(genre))