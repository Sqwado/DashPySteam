from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

filename = 'games.csv'
# filename = 'testgame.csv'

df = pd.read_csv(filename, encoding = 'utf-8')
df = df.fillna('')
# df = df[df['Name'] != '' & df['Price'] != '' & df['Header image'] != '']

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

@app.route('/')
def home():
    
    df = get_data()

    args = request.args
    print(args)
    
    if 'search' in args:
        print('search')
        print(args['search'])
        df = get_games_by_name(args['search'], df)
        
    if 'category' in args:
        print('category')
        print(args.getlist('category'))
        df = get_games_by_category(args.getlist('category'), df)
    
    if 'genre' in args:
        print('genre')
        print(args.getlist('genre'))
        df = get_games_by_genre(args.getlist('genre'), df)
    
    if 'tag' in args:
        print('tag')
        print(args.getlist('tag'))
        df = get_games_by_tag(args.getlist('tag'), df)
    
    if 'platform' in args:
        print('platform')
        print(args['platform'])
        df = get_games_by_platform(args['platform'], df)
        
    if 'page' in args:
        print('page')
        print(args['page'])
        page = int(args['page'])
    else:
        page = 1
        
    if 'per_page' in args:
        print('per_page')
        print(args['per_page'])
        per_page = int(args['per_page'])
    else:
        per_page = 10
        
    if 'min_price' in args:
        print('min_price')
        print(args['min_price'])
        min_price = args['min_price']
    else:
        min_price = 0
    
    if 'max_price' in args:
        print('max_price')
        print(args['max_price'])
        max_price = args['max_price']
    else:
        max_price = 100000
        
    df = get_games_by_price_range(min_price, max_price, df)
        
    if 'min_metacritic' in args:
        print('min_metacritic')
        print(args['min_metacritic'])
        min_metacritic = args['min_metacritic']
    else:
        min_metacritic = 0
    
    if 'max_metacritic' in args:
        print('max_metacritic')
        print(args['max_metacritic'])
        max_metacritic = args['max_metacritic']
    else:
        max_metacritic = 100
        
    df = get_games_by_metacritic_range(min_metacritic, max_metacritic, df)
        
    if 'sort' in args:
        if args['sort'] == 'price-asc':
            print('price-asc')
            df = order_by_price(df)
        elif args['sort'] == 'price-desc':
            print('price-desc')
            df = order_by_price_reverse(df)
        elif args['sort'] == 'metacritic-asc':
            print('metacritic-asc')
            df = order_by_metacritic(df)
        elif args['sort'] == 'metacritic-desc':
            print('metacritic-desc')
            df = order_by_metacritic_reverse(df)
        elif args['sort'] == 'alpha-desc':
            print('alpha-desc')
            df = order_by_alphabetical_reverse(df)
        else:
            print('alpha-asc')
            df = order_by_alphabetical(df)
    else:
        df = order_by_alphabetical(df)
        
    total_games = len(df)
    
    min_price = get_min_price(df)
    max_price = get_max_price(df)
    
    min_metacritic = get_min_metacritic(df)
    max_metacritic = get_max_metacritic(df)

    df = get_data_page(page, per_page, df)
    
    # Convertir le DataFrame en dictionnaire pour le passer au template
    print(df)
    data = df.to_dict(orient='records')
    
    tag = get_tags()
    genre = get_genres()
    platform = get_platforms()
    category = get_categories()
    
    total_pages = total_games // per_page + 1
    
    return render_template('index.html', data=data, tag=tag, genre=genre, platform=platform, category=category, page=page, per_page=per_page, total_pages=total_pages, total_games=total_games, min_price=min_price, max_price=max_price, min_metacritic=min_metacritic, max_metacritic=max_metacritic)

@app.route('/game/<appid>')
def game(appid):
    df = get_data()
    game = get_game_by_id(appid, df)
    
    if game is None:
        return redirect(url_for('home'))
    
    return render_template('game.html', data=game)

@app.route('/create')
def create():
    
    args = request.args
    
    need_create = False
    
    if 'name' in args:
        name = args['name']
        need_create = True
    else:
        name = ''
        
    if 'price' in args:
        if args['price'] == '':
            price = 0
        else:
            price = float(args['price'])
        need_create = True
    else:
        price = 0
        
    if 'metacritic_score' in args:
        if args['metacritic_score'] == '':
            metacritic_score = 0
        else:
            metacritic_score = int(args['metacritic_score'])
        need_create = True
    else:
        metacritic_score = 0
        
    if 'genre' in args:
        genres = args.getlist('genre')
        need_create = True
    else:
        genres = []
        
    if 'category' in args:
        categories = args.getlist('category')
        need_create = True
    else:
        categories = []
        
    if 'tag' in args:
        tags = args.getlist('tag')
        need_create = True
    else:
        tags = []
        
    if 'platform' in args:
        windows = 'Windows' in args.getlist('platform')
        mac = 'Mac' in args.getlist('platform')
        linux = 'Linux' in args.getlist('platform')
        need_create = True
    else:
        windows = False
        mac = False
        linux = False
        
    if 'release_date' in args:
        if args['release_date'] == '':
            release_date = ''
        else:
            release_date = date_to_string(args['release_date'])
        need_create = True
    else:
        release_date = ''
        
    if 'header_image' in args:
        header_image = args['header_image']
        need_create = True
    else:
        header_image = ''
        
    if need_create:
        appid = add_game(name, price, metacritic_score, ','.join(genres), ','.join(categories), ','.join(tags), windows, mac, linux, release_date, header_image)
        if appid:
            set_data()
            print(url_for('game', appid=appid))
            return redirect(url_for('game', appid=appid))
    
    tag = get_tags()
    genre = get_genres()
    platform = get_platforms()
    category = get_categories()

    return render_template('create.html', tag=tag, genre=genre, platform=platform, category=category)


@app.route('/edit/<appid>')
def edit(appid):
    
    df = get_data()
    
    game = get_game_by_id(appid, df)
    
    if game is None:
        return redirect(url_for('home'))
    
    args = request.args
    
    need_update = False
    
    if 'name' in args:
        name = args['name']
        need_update = True
    else:
        name = game['Name']
        
    if 'price' in args:
        if args['price'] == '':
            price = game['Price']
        else:
            price = float(args['price'])
        need_update = True
    else:
        price = game['Price']
        
    if 'metacritic_score' in args:
        if args['metacritic_score'] == '':
            metacritic_score = game['Metacritic score']
        else:
            metacritic_score = int(args['metacritic_score'])
        need_update = True
    else:
        metacritic_score = game['Metacritic score']
        
    if 'genre' in args:
        genres = args.getlist('genre')
        need_update = True
    else:
        genres = game['Genres'].split(',')
        
    if 'category' in args:
        categories = args.getlist('category')
        need_update = True
    else:
        categories = game['Categories'].split(',')
        
    if 'tag' in args:
        tags = args.getlist('tag')
        need_update = True
    else:
        tags = game['Tags'].split(',')
        
    if 'platform' in args:
        windows = 'Windows' in args.getlist('platform')
        mac = 'Mac' in args.getlist('platform')
        linux = 'Linux' in args.getlist('platform')
        need_update = True
    else:
        windows = game['Windows']
        mac = game['Mac']
        linux = game['Linux']
        
    if 'release_date' in args:
        if args['release_date'] == '':
            release_date = game['Release date']
        else:
            release_date = date_to_string(args['release_date'])
        need_update = True
    else:
        release_date = game['Release date']
        
    if 'header_image' in args:
        header_image = args['header_image']
        need_update = True
    else:
        header_image = game['Header image']
        
    if need_update:
        updated = update_game(appid, name, price, metacritic_score, ','.join(genres), ','.join(categories), ','.join(tags), windows, mac, linux, release_date, header_image)
        if updated:
            return redirect(url_for('game', appid=appid))
    
    if game['Release date'] == '':
        date = ''
    else:
        date = to_date(game['Release date'])
    tag = get_tags()
    genre = get_genres()
    platform = get_platforms()
    category = get_categories()
    
    return render_template('edit.html', data=game, tag=tag, genre=genre, platform=platform, category=category, date=date)

@app.route('/delete/<appid>')
def delete(appid):
    if delete_game(appid):
        return redirect(url_for('home'))
    return redirect(url_for('game', appid=appid))

@app.route('/stats')
def stats():
    
    args = request.args
    
    df = get_data()
    
    if 'graph' in args:
        if args['graph'] == 'genre_hight_price':
            data = graph_genre_hight_price(df)
            values = data['Highest Price'].tolist()
            labels = data['Genre'].tolist()
            names = data['Game Name'].tolist()
            return render_template('stats.html', values=values, labels=labels, names=names)
        elif args['graph'] == 'best_score_platform_label_name':
            data = graph_best_score_platform_label_name(df)
            values = data['Best Score'].tolist()
            labels = data['Platform'].tolist()
            names = data['Game Name'].tolist()
            return render_template('stats.html', values=values, labels=labels, names=names)
        elif args['graph'] == 'best_score_year_platform_label_name':
            datawindows = graph_best_score_year_platform_label_name('Windows', df)
            datamac = (graph_best_score_year_platform_label_name('Mac', df))
            datalinux = (graph_best_score_year_platform_label_name('Linux', df))
            valueswindows = datawindows['Best Score'].tolist()
            labelswindows = datawindows['Year'].tolist()
            nameswindows = datawindows['Game Name'].tolist()
            valuesmac = datamac['Best Score'].tolist()
            labelsmac = datamac['Year'].tolist()
            namesmac = datamac['Game Name'].tolist()
            valueslinux = datalinux['Best Score'].tolist()
            labelslinux = datalinux['Year'].tolist()
            nameslinux = datalinux['Game Name'].tolist()
            return render_template('stats.html', valueswindows=valueswindows, labelswindows=labelswindows, nameswindows=nameswindows, valuesmac=valuesmac, labelsmac=labelsmac, namesmac=namesmac, valueslinux=valueslinux, labelslinux=labelslinux, nameslinux=nameslinux) 
        else:
            data = graph_prix_moyen_year(df)
            values = data['Average Price'].tolist()
            labels = data['Year'].tolist()
            return render_template('stats.html', values=values, labels=labels, names=[])
    else:
        data = graph_prix_moyen_year(df)
        values = data['Average Price'].tolist()
        labels = data['Year'].tolist()
        return render_template('stats.html', values=values, labels=labels)

if __name__ == '__main__':
    app.run(debug=True)
