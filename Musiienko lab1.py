import pandas as pd
import matplotlib.pyplot as plt

# Число К визначається днем народження студента та має бути визначено як змінна.
k = 10


print('1. Відкрити та зчитати файл з даними.')
data = pd.read_csv('Top100-2007.csv')

print('2. Визначити та вивести кількість записів та кількість полів у кожному записі.')
data_size = data.shape
print(f'К-сть записів: {data_size[0]}. К-сть полів: {data_size[1]}')

print('3. Вивести 5 записів, починаючи з К-ого.')
print(data.iloc[k-1:k+4])
print('3. Вивести 3К+2 останніх записів.')
print(data.tail(3*k+2))

print('4. Визначити та вивести тип полів кожного запису.')
print(data.dtypes)

print('5. Очистити текстові поля від зайвих пробілів.')
data['Name'] = data['Name'].str.strip()
data['Country'] = data['Country'].str.strip()
data['Singles Record (Career)'] = data['Singles Record (Career)'].str.strip()
data['Link to Wikipedia'] = data['Link to Wikipedia'].str.strip()

print('6. Визначити поля, які потрібно привести до числового вигляду та зробити це (продемонструвати підтвердження).')
data['Winning Percentage'] = data['Winning Percentage'].str.rstrip('%').astype(float)
data['Career Earnings'] = data['Career Earnings'].str.lstrip('$').astype(float)
print(data.dtypes)

print('7. Визначити записи із пропущеними даними та вивести їх на екран, після чого видалити з датафрейму.')
for index, row in data.iterrows():
    if row.isna().any():
        print(row)
data = data.dropna()

print('8. На основі поля Singles Record (Career) ввести нові поля:', 
      '\na.  Загальна кількість зіграних матчів Total',
      '\nb.  Кількість виграних матчів Win',
      '\nc.  Кількість програних матчів Lose')
data[['Win', 'Lose']] = data['Singles Record (Career)'].str.split('-', expand=True).astype('int64')
data['Total'] = data['Win'] + data['Lose']

print('9. Видалити з датафрейму поля Singles Record (Career) та Link to Wikipedia.')
data = data.drop(columns=['Singles Record (Career)', 'Link to Wikipedia'])

print('10. Змінити порядок розташування полів таким чином: Rank, Name, Country, Pts, Total, Win, Lose, Winning Percentage.')
data = data[['Rank', 'Name', 'Country', 'Pts', 'Total', 'Win', 'Lose', 'Winning Percentage', 'Career Earnings']]

print('11. Визначити та вивести:', 
      '\na.  Відсортований за абеткою перелік країн, тенісисти з яких входять у Топ-100')
data_sorted = data.sort_values(by='Country')
print(data_sorted.head(k))

print('b.  Гравця та кількість його очок із найменшою сумою призових')
min_player = data[data['Win'] == data['Win'].min()]
print(min_player[['Name', 'Pts']])

print('c.  Гравців та країну, яку вони представляють, кількість виграних матчів у яких дорівнює кількості програних')
equals = data[data['Win'] == data['Lose']]
print(equals[['Name', 'Country']])

print('12. Визначити та вивести:', 
      '\na.  Кількість тенісистів з кожної країни у Топ-100')
player_count =  data.groupby(['Country'])['Name'].count()
print(player_count)

print('b.   Середній рейтинг тенісистів з кожної країни')
player_mean =  data.groupby(['Country'])['Winning Percentage'].mean()
print(player_mean)

print('13. Побудувати діаграму кількості програних матчів по кожній десятці гравців з Топ-100.')
data['Group'] = 1 + data.index // 10
group10_lose = data.groupby('Group')['Lose'].sum()
plt.bar(group10_lose.index, group10_lose)
plt.xlabel('Group')
plt.ylabel('Total Loses')
plt.xticks(group10_lose.index)
plt.title('Total Loses for Each Group of 10 Players')
plt.show()

print('14. Побудувати кругову діаграму сумарної величини призових для кожної країни.')
country_win =  data.groupby(['Country'])['Win'].sum()
plt.pie(country_win, labels=country_win.values)
plt.title('Sum of Wins for Each Country')
plt.legend(country_win.index, loc="center left")
plt.show()

print('15. Побудувати на одному графіку:', 
      '\na.  Середню кількість очок для кожної країни',
      '\nb.  Середню кількість зіграних матчів тенісистами кожної країни')
mean_country = data.groupby('Country').agg({'Pts': 'mean', 'Total': 'mean'})
mean_country.plot(kind='bar', stacked=True)
plt.xlabel('Country')
plt.ylabel('Mean Value')
plt.title('Mean Points and Matches by Country')
plt.legend(['Points', 'Total Matches'], loc='upper right')
plt.show()
