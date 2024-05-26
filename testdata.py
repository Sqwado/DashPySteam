import pandas as pd
import random
import re
df = pd.read_csv('games.csv', encoding = 'utf-8')
df = df.fillna('')
# df = df[df['Name'] != '' & df['Price'] != '' & df['Header image'] != '']
print(df.columns)
# print(df[['AppID','Name','Price','Metacritic score','Genres','Categories','Windows','Mac','Linux']].sort_values(by='Notes', ascending=False).head(10))
# print(df[['Name','Price','Metacritic score']].sort_values(by='Metacritic score', ascending=False).head(10))

def get_data():
    return df

def to_date(datein):
    if type(datein) != str:
        return datein
    print(datein)
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
    return f"{date}/{month}/{year}"

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
        if type(df['Genres'][i]) != str:
            continue
        if set(genre).issubset(set(df['Genres'][i].split(','))):
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
    print(bool_platform)
    for i in range(len(df)):                
        if bool_platform[0] and not df['Windows'][i]:
            continue
        if bool_platform[1] and not df['Mac'][i]:
            continue
        if bool_platform[2] and not df['Linux'][i]:
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
        if price >= min_price and price <= max_price:
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_min_price(df=df):
    df = order_by_price(df)
    return df.head(1)['Price'].values[0]

def get_max_price(df=df):
    df = order_by_price_reverse(df)
    return df.head(1)['Price'].values[0]

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

print(get_min_price(df))
print(get_max_price(df))

# print(df[['Name','Price']].sort_values(by='Price', ascending=False))

