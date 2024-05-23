import pandas as pd
df = pd.read_csv('games.csv', encoding = 'utf-8')
# print(df.columns)
# print(df[['AppID','Name','Price','Metacritic score','Genres','Categories','Windows','Mac','Linux']].sort_values(by='Notes', ascending=False).head(10))
# print(df[['Name','Price','Metacritic score']].sort_values(by='Metacritic score', ascending=False).head(10))

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
    for i in range(len(df)):
        if type(df['Categories'][i]) != str:
            continue
        if set(category).issubset(set(df['Categories'][i].split(','))):
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_games_by_genre(genre, df=df):
    games = []
    for i in range(len(df)):
        if type(df['Genres'][i]) != str:
            continue
        if set(genre).issubset(set(df['Genres'][i].split(','))):
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_games_by_tag(tag, df=df):
    games = []
    for i in range(len(df)):
        if type(df['Tags'][i]) != str:
            continue
        if set(tag).issubset(set(df['Tags'][i].split(','))):
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def get_games_by_name(name, df=df):
    games = []
    for i in range(len(df)):
        if type(df['Name'][i]) != str:
            continue
        if name.lower() in df['Name'][i].lower():
            games.append(df.iloc[i].to_dict())
    return pd.DataFrame(games)

def order_by_alphabetical(df):
    return df.sort_values(by='Name')

def order_by_alphabetical_reverse(df):
    return df.sort_values(by='Name', ascending=False)

def order_by_price(df):
    return df.sort_values(by='Price')

def order_by_price_reverse(df):
    return df.sort_values(by='Price', ascending=False)



print(get_games_by_tag(['Local Multiplayer','Atmospheric','VR']))
# print(get_games_by_genre(['Action']))
# print(get_games_by_category(['LAN PvP']))
# print(get_games_by_name('the last of', get_games_by_genre([''],order_by_alphabetical(df)))[['Name','Genres']].values)

# print(get_all_categories())
# print(get_all_genres())
# print(get_all_tags())

# df = df.fillna('')
# print(df[df['Name'].str.contains('portal 2', case=False)]['Header image'].values)

