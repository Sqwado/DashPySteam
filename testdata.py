import pandas as pd
import random
import re

# filename = 'games.csv'
filename = 'testgame.csv'

df = pd.read_csv(filename, encoding = 'utf-8')
df = df.fillna('')
# df = df[df['Name'] != '' & df['Price'] != '' & df['Header image'] != '']
print(df.columns)
# print(df[['AppID','Name','Price','Metacritic score','Genres','Categories','Windows','Mac','Linux']].sort_values(by='Notes', ascending=False).head(10))
# print(df[['Name','Price','Metacritic score']].sort_values(by='Metacritic score', ascending=False).head(10))

def set_data():
    global df
    df = pd.read_csv(filename, encoding = 'utf-8')
    df = df.fillna('')

def get_data():
    return df

def to_date(datein):
    if type(datein) != str:
        return datein
    month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    datein = datein.replace(',', '')
    datein = datein.split(' ')
    date = datein[1]
    month = datein[0]
    if len(date) > 2:
        year = date
        date = '01'
    else:
        year = datein[2]
    
    if len(date) == 1:
        date = '0' + date
    month = month_dict[month]
    return f"{year}-{month}-{date}"

def date_to_string(datein):
    month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    datein = datein.split('-')
    year = datein[0]
    month = list(month_dict.keys())[list(month_dict.values()).index(datein[1])]
    date = datein[2]
    return f"{month} {date}, {year}"

def get_all_categories():
    categories = df['Categories']
    all_categories = []
    for i in range(len(categories)):
        if type(categories[i]) != str:
            continue
        this_categories = categories[i].split(',')
        for j in range(len(this_categories)):
            if this_categories[j] not in all_categories:
                all_categories.append(this_categories[j])
    all_categories.sort()
    all_categories = [category for category in all_categories if category != '']
    return all_categories

def get_all_genres():
    genres = df['Genres']
    all_genres = []
    for i in range(len(genres)):
        if type(genres[i]) != str:
            continue
        this_genres = genres[i].split(',')
        for j in range(len(this_genres)):
            if this_genres[j] not in all_genres:
                all_genres.append(this_genres[j])
    all_genres.sort()
    all_genres = [genre for genre in all_genres if genre != '']
    return all_genres

def get_all_tags():
    tags = df['Tags']
    all_tags = []
    for i in range(len(tags)):
        if type(tags[i]) != str:
            continue
        this_tags = tags[i].split(',')
        for j in range(len(this_tags)):
            if this_tags[j] not in all_tags:
                all_tags.append(this_tags[j])
    all_tags.sort()
    all_tags = [tag for tag in all_tags if tag != '']
    return all_tags

def get_all_platforms():
    return ['Windows', 'Mac', 'Linux']
    

def get_games_by_category(category, df=df):
    games = []
    if len(category) < 1:
        return df
    for i in range(len(df)):
        if type(df['Categories'][i]) != str:
            continue
        if set(category).issubset(set(df['Categories'][i].split(','))):
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_games_by_genre(genre, df=df):
    games = []
    if len(genre) < 1:
        return df
    for i in range(len(df)):
        if type(df['Genres'].values[i]) != str:
            continue
        if set(genre).issubset(set(df['Genres'].values[i].split(','))):
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_games_by_tag(tag, df=df):
    games = []
    if len(tag) < 1:
        return df
    for i in range(len(df)):
        if type(df['Tags'][i]) != str:
            continue
        if set(tag).issubset(set(df['Tags'][i].split(','))):
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_games_by_platform(platform, df=df):
    bool_platform = [False] * 3
    for j in platform:
        if j in ['Windows', 'Mac', 'Linux']:
            bool_platform[['Windows', 'Mac', 'Linux'].index(j)] = True
    games = []
    for i in range(len(df)):                
        if bool_platform[0] and not df['Windows'].values[i]:
            continue
        if bool_platform[1] and not df['Mac'].values[i]:
            continue
        if bool_platform[2] and not df['Linux'].values[i]:
            continue
        games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_games_by_name(name, df=df):
    games = []
    if len(name) < 1:
        return df
    for i in range(len(df)):
        if type(df['Name'][i]) != str:
            continue
        if name.lower() in df['Name'][i].lower():
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_game_by_id(id, df=df):
    print(df['AppID'])
    data = df[df['AppID'] == int(id)]
    if data.empty:
        return None
    return data.to_dict(orient='records')[0]

def order_by_alphabetical(df=df):
    if df.empty:
        return df
    return df.sort_values(by='Name')

def order_by_alphabetical_reverse(df=df):
    if df.empty:
        return df
    return df.sort_values(by='Name', ascending=False)

def order_by_price(df=df):
    if df.empty:
        return df
    return df.sort_values(by='Price')

def order_by_price_reverse(df=df):
    if df.empty:
        return df
    return df.sort_values(by='Price', ascending=False)

def order_by_metacritic(df=df):
    if df.empty:
        return df
    return df.sort_values(by='Metacritic score')

def order_by_metacritic_reverse(df=df):
    if df.empty:
        return df
    return df.sort_values(by='Metacritic score', ascending=False)

def write_categories():
    categories = get_all_categories()
    with open('filterdata/categories.txt', 'w') as f:
        f.write('\n'.join(categories))

def write_genres():
    genres = get_all_genres()
    with open('filterdata/genres.txt', 'w') as f:
        f.write('\n'.join(genres))
            
def write_tags():
    tags = get_all_tags()
    with open('filterdata/tags.txt', 'w') as f:
        f.write('\n'.join(tags))
            
def write_platforms():
    platforms = get_all_platforms()
    with open('filterdata/platforms.txt', 'w') as f:
        f.write('\n'.join(platforms))
        
def get_categories():
    with open('filterdata/categories.txt', 'r') as f:
        return f.read().split('\n')
    
def get_genres():
    with open('filterdata/genres.txt', 'r') as f:
        return f.read().split('\n')
    
def get_tags():
    with open('filterdata/tags.txt', 'r') as f:
        return f.read().split('\n')
    
def get_platforms():
    with open('filterdata/platforms.txt', 'r') as f:
        return f.read().split('\n')
    
def random_games(n=10, df=df):
    games = []
    indices = random.sample(range(len(df)), n)
    for i in indices:
        games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_data_page(page, per_page, df=df):
    page = page - 1
    return df.iloc[page*per_page:(page+1)*per_page]

def get_games_by_price_range(min_price, max_price, df=df):
    games = []
    for i in range(len(df)):
        if df['Price'][i] == '':
            continue
        price = df['Price'][i]
        if price >= float(min_price) and price <= float(max_price):
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_games_by_metacritic_range(min_metacritic, max_metacritic, df=df):
    games = []
    for i in range(len(df)):
        if df['Metacritic score'][i] == '':
            continue
        metacritic = df['Metacritic score'][i]
        if metacritic >= float(min_metacritic) and metacritic <= float(max_metacritic):
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_min_price(df=df):
    df = order_by_price(df)
    if df.empty:
        return 0
    return df.head(1)['Price'].values[0]

def get_max_price(df=df):
    df = order_by_price_reverse(df)
    if df.empty:
        return 0
    return df.head(1)['Price'].values[0]

def get_min_metacritic(df=df):
    df = order_by_metacritic(df)
    if df.empty:
        return 0
    return df.head(1)['Metacritic score'].values[0]

def get_max_metacritic(df=df):
    df = order_by_metacritic_reverse(df)
    if df.empty:
        return 0
    return df.head(1)['Metacritic score'].values[0]

def get_new_appid():
    while True:
        appid = random.randint(0, 9999999)
        if appid not in df['AppID'].values:
            return appid
        
def add_game(name, price, metacritic_score, genres, categories, tags, windows, mac, linux, release_date, header_image):
    global df
    appid = get_new_appid()
    new_game = pd.DataFrame([[appid, name, release_date, '', '', '', price, '', '', '', '', '', header_image, '', '', '', windows, mac, linux, metacritic_score, '', '', '', '', '', '', '', '', '', '', '', '', '', '', categories, genres, tags, '', '']], columns=df.columns)
    df = df._append(new_game, ignore_index=True)
    df.to_csv(filename, index=False, encoding='utf-8')
    return appid

def update_game(appid, name, price, metacritic_score, genres, categories, tags, windows, mac, linux, release_date, header_image):
    global df
    data = df[df['AppID'] == int(appid)]
    if data.empty:
        return False
    index = data.index[0]
    df.at[index, 'Name'] = name
    df.at[index, 'Price'] = price
    df.at[index, 'Metacritic score'] = metacritic_score
    df.at[index, 'Genres'] = genres
    df.at[index, 'Categories'] = categories
    df.at[index, 'Tags'] = tags
    df.at[index, 'Windows'] = windows
    df.at[index, 'Mac'] = mac
    df.at[index, 'Linux'] = linux
    df.at[index, 'Release date'] = release_date
    df.at[index, 'Header image'] = header_image
    df.to_csv(filename, index=False, encoding='utf-8')
    return True

def delete_game(appid):
    global df
    data = df[df['AppID'] == int(appid)]
    if data.empty:
        return False
    index = data.index[0]
    df.drop(index, inplace=True)
    df.to_csv(filename, index=False, encoding='utf-8')
    return True

def graph_prix_moyen_year(df=df):
    df = df[df['Price'] != 0.0]
    years = []
    for i in range(len(df)):
        if type(df['Release date'].values[i]) != str:
            continue
        date = to_date(df['Release date'].values[i])
        year = date.split('-')[0]
        if year not in years:
            years.append(year)
    years.sort()
    moyennes = []
    for year in years:
        total = 0
        count = 0
        for i in range(len(df)):
            if type(df['Release date'].values[i]) != str:
                continue
            date = to_date(df['Release date'].values[i])
            if date.split('-')[0] == year:
                total += df['Price'].values[i]
                count += 1
        if count == 0:
            moyennes.append(0)
        else:
            moyennes.append(round((total/count), 2))
    return pd.DataFrame({'Year': years, 'Average Price': moyennes})

def graph_genre_hight_price(df=df):
    genres = get_all_genres()
    df = df[df['Price'] != 0.0]
    df = df[df['Genres'] != '']
    prices = []
    games_names = []
    for genre in genres:
        genre_games = get_games_by_genre([genre], df)
        if genre_games.empty:
            prices.append(0)
            games_names.append('')
        else:
            prices.append(genre_games['Price'].max())
            games_names.append(genre_games[genre_games['Price'] == genre_games['Price'].max()]['Name'].values[0])
    return pd.DataFrame({'Genre': genres, 'Highest Price': prices, 'Game Name': games_names})

def graph_best_score_platform_label_name(df=df):
    platforms = get_all_platforms()
    df = df[df['Metacritic score'] != '']
    df = df[df['Metacritic score'] != 0]
    scores = []
    games_names = []
    for platform in platforms:
        platform_games = get_games_by_platform([platform], df)
        if platform_games.empty:
            scores.append(0)
            games_names.append('')
        else:
            scores.append(platform_games['Metacritic score'].max())
            games_names.append(platform_games[platform_games['Metacritic score'] == platform_games['Metacritic score'].max()]['Name'].values[0])
    return pd.DataFrame({'Platform': platforms, 'Best Score': scores, 'Game Name': games_names})

def graph_best_score_year_platform_label_name(platform, df=df):
    df = df[df['Metacritic score'] != '']
    df = df[df['Metacritic score'] != 0]
    df = get_games_by_platform([platform], df)
    years = []
    scores = []
    games_names = []
    for i in range(len(df)):
        if type(df['Release date'].values[i]) != str:
            continue
        date = to_date(df['Release date'].values[i])
        year = date.split('-')[0]
        if year not in years:
            years.append(year)
    years.sort()
    for year in years:
        year_games = df[df['Release date'].apply(to_date).str.contains(year)]
        if year_games.empty:
            scores.append(0)
            games_names.append('')
        else:
            scores.append(year_games['Metacritic score'].max())
            games_names.append(year_games[year_games['Metacritic score'] == year_games['Metacritic score'].max()]['Name'].values[0])
    return pd.DataFrame({'Year': years, 'Best Score': scores, 'Game Name': games_names})
   
# write_categories()
# write_genres()
# write_tags()
# write_platforms()

# print(get_categories())
# print(get_genres())
# print(get_tags())
# print(get_platforms())
    

# print(df['Release date'].apply(to_date))

# print(order_by_price(get_games_by_tag(['Local Multiplayer','Atmospheric','VR'])))
# print(get_games_by_genre(['Action']))
# print(get_games_by_category(['LAN PvP']))
# print(get_games_by_name('the last of', get_games_by_genre([''],order_by_alphabetical(df)))[['Name','Genres']].values)

# print(get_all_categories())
# print(get_all_genres())
# print(get_all_tags())

# df = df.fillna('')
# data = df[df['Name'].str.contains('portal 2', case=False)]

# data = data.to_dict(orient='records')

# def get_game_by_id(id, df=df):
#     data = df[df['AppID'] == int(id)]
#     if data.empty:
#         return None
#     return data.to_dict(orient='records')[0]

# print(get_game_by_id('2293130'))

# df = df.head(25)

# df = random_games(25)

# print(get_data_page(2, 10, df))

# print(get_games_by_platform(['Linux'], df))

df = get_data()

# df = get_games_by_price_range(0, 10.11, df)

windowstopgames = graph_best_score_year_platform_label_name('Windows', df)
linuxtopgames = graph_best_score_year_platform_label_name('Linux', df)
mactopgames = graph_best_score_year_platform_label_name('Mac', df)

print(windowstopgames)
print(linuxtopgames)
print(mactopgames)

# print(get_min_price(df))
# print(get_max_price(df))

# print(df[['Name','Price']].sort_values(by='Price', ascending=False))

# print(add_game('Test Game', 0.0, 0, 'Action', 'Single-player', 'Test', True, False, False, 'Nov 9, 2020', 'https://steamcdn-a.akamaihd.net/steam/apps/271590/header.jpg?t=1604933843'))
# print(update_game(5960268, 'Test Game 2', 0.0, 0, 'Action', 'Single-player', 'Test', True, False, False, 'Nov 9, 2020', 'https://steamcdn-a.akamaihd.net/steam/apps/271590/header.jpg?t=1604933843'))
# print(delete_game(5960268))
