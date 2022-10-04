import sqlite3
import matplotlib.pyplot as plt
import os

genres = ['Disaster', 'Terrorism', 'Sci-Fi - Adventure', 'Horror - Terror in the Water', 'Horror - R-Rated', \
         'Horror - Torture', 'Horror Remake', 'Fantasy - Live Action', 'Shark', 'Western', 'Horror - Slasher', 'Heist / Caper', \
        'Superhero', 'Sci-Fi - Based on Book', 'Sci-Fi Remake', 'Action Heroine', 'Sci-Fi Horror', 'Prequel', 'Horror - Supernatural', \
        'War - World War 2', 'Adventure - Desert', 'Future - Near', 'Post-Apocalypse', 'Comedy - Spy', 'Sci-Fi Chase', \
        'Thriller - Erotic', 'Thriller - Serial Killer', 'Pilot / Aircraft', 'Con Artist / Hustler', 'Time Travel', 'Action - Martial Arts', \
        'Adventure Remake', 'Pop Star Debuts', 'President', 'Mindbender', 'Medieval Times', 'Sword and Sorcery', 'Werewolf', \
        'Thriller - Psycho / Stalker / Blank from Hell', 'Spy', 'Thriller - Political', 'War - World War I', 'Treasure Hunt', \
        'Hitman / Assassin', 'Cyborg / Android / Robot', 'Adventure - Period', 'Action - Wire-Fu', 'Zombie', 'Young-Adult Book Adaptations', \
        'Action - Buddy Comedy', 'Vampire', 'Man vs. Machine', 'Creature Feature', 'Virtual Reality', 'Fire / Firefighter', \
        'Action Remake', 'Remake - Asian', 'Remake - Foreign Thrills', 'Thriller - On the Run', 'Dinosaur', 'Memory Loss / Amnesia', \
        'Hostage', 'Horror - Period', 'Found Footage', 'Witch', 'Sci-Fi - Alien Invasion', 'Underwater', 'Video Game Adaptation', 'Global Warming', 'CGI Star']


if not os.path.exists('Subgenres'):
    os.makedirs('Subgenres')

with open(os.path.join('Subgenres', 'index.html'), 'w') as fp:
    fp.write('<h1>Genre releases by year of movies shown in more than 2000 theaters</h1>')

conn = sqlite3.connect('movies.db')
for genre in genres:
    sql = 'select year, count(distinct(imdb_id)) c from combined_oldgenres where oldgenre like "%{}%" and theatersopen > 2000 group by year' .format(genre)
    x = [item[0] for item in conn.execute(sql)]
    y = [item[1] for item in conn.execute(sql)]

    plt.figure(figsize=(10, 5))
    plt.xlabel('Year', size = 16)
    plt.ylabel('{} titles' .format(genre), size = 16)

    plt.bar(x, y, align='center', width=0.8)
    plt.savefig(os.path.join('Subgenres', 'Theatrical_Wide_{}.png') .format(genre.replace('/', '_')))
    with open(os.path.join('Subgenres', 'index.html'), 'a') as fp:
        fp.write('<img src="Theatrical_Wide_{}.png" /><br>' .format(genre.replace('/', '_')))