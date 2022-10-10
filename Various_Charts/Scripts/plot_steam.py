import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

y = [1691927, 2866546, 4105830, 4746445, 5820311, 7511544, 10910992, 12942312, 14116142, 16311480, 16583751, 22499280, 25679459, 26280023]

x = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

plt.figure(figsize=(13,5))
plt.xlabel('Year', size=16)
plt.ylabel('# of players', size=16)
plt.bar(x, y, align='center', width=0.8)
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels([format(x, ',') for x in current_values])
plt.savefig('Steam_Players_Chart.png')
plt.show()