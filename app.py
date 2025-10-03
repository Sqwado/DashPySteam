from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random
import re
import os
import time

# Accélération GPU optionnelle via cuDF
try:
    import cudf as _gd
    CUDF_AVAILABLE = True
except Exception:
    _gd = None
    CUDF_AVAILABLE = False

# Flag runtime (peut être modifié par requête/env)
USE_CUDF = CUDF_AVAILABLE

def _resolve_engine(args):
    global USE_CUDF
    env_force = os.getenv('DASPYSTEAM_GPU', '')  # '1' pour GPU, '0' pour CPU
    if 'gpu' in args:
        use_gpu = args.get('gpu') in ['1', 'true', 'True', 'yes']
        USE_CUDF = CUDF_AVAILABLE and use_gpu
    elif env_force != '':
        USE_CUDF = CUDF_AVAILABLE and (env_force in ['1', 'true', 'True', 'yes'])
    else:
        USE_CUDF = CUDF_AVAILABLE
    return 'cuDF' if USE_CUDF else 'pandas'

app = Flask(__name__)

# filename = 'games.csv'
filename = 'games.csv'

def _read_csv(path):
    if USE_CUDF:
        return _gd.read_csv(path)
    return pd.read_csv(path, encoding='utf-8')

def _to_pandas(frame):
    try:
        if _gd is not None and isinstance(frame, _gd.DataFrame):
            return frame.to_pandas()
    except Exception:
        pass
    return frame

def _ensure_series_numeric(series):
    if USE_CUDF:
        # cuDF: astype with null handling
        try:
            return series.astype('float32')
        except Exception:
            return series
    # pandas
    return pd.to_numeric(series, errors='coerce')

def _safe_fillna_frame(frame):
    if not USE_CUDF:
        return frame.fillna('')
    # cuDF: éviter de remplir les colonnes numériques avec des chaînes
    for c in frame.columns:
        col = frame[c]
        try:
            kind = getattr(col.dtype, 'kind', None)
            if kind == 'b':
                frame[c] = col.fillna(False)
            elif kind in ('i', 'u', 'f'):
                # Laisser NaN; les filtres numériques gèrent NaN via isna/notna
                frame[c] = col
            else:
                frame[c] = col.fillna('')
        except Exception:
            try:
                frame[c] = col.fillna('')
            except Exception:
                pass
    return frame

def _string_contains(series, pattern):
    if USE_CUDF:
        return series.fillna('').str.contains(pattern, regex=True)
    return series.str.contains(pattern, regex=True, na=False)

def _ensure_engine_frame(frame):
    # Convertit le DataFrame vers le moteur choisi
    if USE_CUDF:
        if CUDF_AVAILABLE and isinstance(frame, pd.DataFrame):
            return _gd.from_pandas(frame)
        return frame
    else:
        # Forcer pandas même si frame est cuDF
        return _to_pandas(frame)

df = _read_csv(filename)
df = _safe_fillna_frame(df)
# df = df[df['Name'] != '' & df['Price'] != '' & df['Header image'] != '']

def set_data():
    global df
    df = _read_csv(filename)
    df = _safe_fillna_frame(df)

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
    if USE_CUDF:
        unique_vals = set()
        for val in categories.fillna('').to_pandas().tolist():
            if isinstance(val, str) and val:
                unique_vals.update([v for v in val.split(',') if v])
        return sorted(list(unique_vals))
    all_categories = []
    for val in categories:
        if type(val) != str:
            continue
        for item in val.split(','):
            if item not in all_categories and item != '':
                all_categories.append(item)
    all_categories.sort()
    return all_categories

def get_all_genres():
    genres = df['Genres']
    if USE_CUDF:
        unique_vals = set()
        for val in genres.fillna('').to_pandas().tolist():
            if isinstance(val, str) and val:
                unique_vals.update([v for v in val.split(',') if v])
        return sorted(list(unique_vals))
    all_genres = []
    for val in genres:
        if type(val) != str:
            continue
        for item in val.split(','):
            if item not in all_genres and item != '':
                all_genres.append(item)
    all_genres.sort()
    return all_genres

def get_all_tags():
    tags = df['Tags']
    if USE_CUDF:
        unique_vals = set()
        for val in tags.fillna('').to_pandas().tolist():
            if isinstance(val, str) and val:
                unique_vals.update([v for v in val.split(',') if v])
        return sorted(list(unique_vals))
    all_tags = []
    for val in tags:
        if type(val) != str:
            continue
        for item in val.split(','):
            if item not in all_tags and item != '':
                all_tags.append(item)
    all_tags.sort()
    return all_tags

def get_all_platforms():
    return ['Windows', 'Mac', 'Linux']
    

def get_games_by_category(category, df=df):
    if len(category) < 1:
        return df
    mask = None
    for cat in category:
        pattern = rf"(^|,){re.escape(cat)}(,|$)"
        col = df['Categories']
        curr = _string_contains(col, pattern)
        mask = curr if mask is None else (mask & curr)
    return df[mask]

def get_games_by_genre(genre, df=df):
    if len(genre) < 1:
        return df
    mask = None
    for g in genre:
        pattern = rf"(^|,){re.escape(g)}(,|$)"
        col = df['Genres']
        curr = _string_contains(col, pattern)
        mask = curr if mask is None else (mask & curr)
    return df[mask]

def get_games_by_tag(tag, df=df):
    if len(tag) < 1:
        return df
    mask = None
    for t in tag:
        pattern = rf"(^|,){re.escape(t)}(,|$)"
        col = df['Tags']
        curr = _string_contains(col, pattern)
        mask = curr if mask is None else (mask & curr)
    return df[mask]

def get_games_by_platform(platform, df=df):
    platforms = set(platform if isinstance(platform, (list, tuple, set)) else [platform])
    mask = None
    if 'Windows' in platforms:
        curr = df['Windows'] == True
        mask = curr if mask is None else (mask & curr)
    if 'Mac' in platforms:
        curr = df['Mac'] == True
        mask = curr if mask is None else (mask & curr)
    if 'Linux' in platforms:
        curr = df['Linux'] == True
        mask = curr if mask is None else (mask & curr)
    return df if mask is None else df[mask]

def get_games_by_name(name, df=df):
    if len(name) < 1:
        return df
    pattern = re.escape(name.lower())
    name_series = df['Name']
    if USE_CUDF:
        lower_series = name_series.fillna('').str.lower()
        mask = lower_series.str.contains(pattern, regex=True)
        return df[mask]
    # S'assurer d'être sur pandas si besoin
    ps = _to_pandas(name_series)
    return df[ps.str.lower().str.contains(pattern, regex=True, na=False)]

def get_game_by_id(id, df=df):
    data = df[df['AppID'] == int(id)]
    if (USE_CUDF and len(data) == 0) or (not USE_CUDF and data.empty):
        return None
    return _to_pandas(data).to_dict(orient='records')[0]

def order_by_alphabetical(df=df):
    if (not USE_CUDF and df.empty) or (USE_CUDF and len(df) == 0):
        return df
    return df.sort_values(by='Name')

def order_by_alphabetical_reverse(df=df):
    if (not USE_CUDF and df.empty) or (USE_CUDF and len(df) == 0):
        return df
    return df.sort_values(by='Name', ascending=False)

def order_by_price(df=df):
    if (not USE_CUDF and df.empty) or (USE_CUDF and len(df) == 0):
        return df
    return df.sort_values(by='Price')

def order_by_price_reverse(df=df):
    if (not USE_CUDF and df.empty) or (USE_CUDF and len(df) == 0):
        return df
    return df.sort_values(by='Price', ascending=False)

def order_by_metacritic(df=df):
    if (not USE_CUDF and df.empty) or (USE_CUDF and len(df) == 0):
        return df
    return df.sort_values(by='Metacritic score')

def order_by_metacritic_reverse(df=df):
    if (not USE_CUDF and df.empty) or (USE_CUDF and len(df) == 0):
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
    try:
        sampled = df.sample(n=n)
        return sampled
    except Exception:
        games = []
        indices = random.sample(range(len(df)), n)
        for i in indices:
            games.append(_to_pandas(df.iloc[[i]]) .to_dict(orient='records')[0])
        return pd.DataFrame(games)

def get_data_page(page, per_page, df=df):
    page = page - 1
    return df.iloc[page*per_page:(page+1)*per_page]

def get_games_by_price_range(min_price, max_price, df=df):
    price_series = df['Price']
    price_series = _ensure_series_numeric(price_series)
    return df[(price_series >= float(min_price)) & (price_series <= float(max_price))]

def get_games_by_metacritic_range(min_metacritic, max_metacritic, df=df):
    score_series = df['Metacritic score']
    score_series = _ensure_series_numeric(score_series)
    return df[(score_series >= float(min_metacritic)) & (score_series <= float(max_metacritic))]

def get_min_price(df=df):
    df_sorted = order_by_price(df)
    if (USE_CUDF and len(df_sorted) == 0) or (not USE_CUDF and df_sorted.empty):
        return 0
    if USE_CUDF:
        return float(df_sorted.head(1)['Price'].to_pandas().values[0])
    return df_sorted.head(1)['Price'].values[0]

def get_max_price(df=df):
    df_sorted = order_by_price_reverse(df)
    if (USE_CUDF and len(df_sorted) == 0) or (not USE_CUDF and df_sorted.empty):
        return 0
    if USE_CUDF:
        return float(df_sorted.head(1)['Price'].to_pandas().values[0])
    return df_sorted.head(1)['Price'].values[0]

def get_min_metacritic(df=df):
    df_sorted = order_by_metacritic(df)
    if (USE_CUDF and len(df_sorted) == 0) or (not USE_CUDF and df_sorted.empty):
        return 0
    if USE_CUDF:
        return float(df_sorted.head(1)['Metacritic score'].to_pandas().values[0])
    return df_sorted.head(1)['Metacritic score'].values[0]

def get_max_metacritic(df=df):
    df_sorted = order_by_metacritic_reverse(df)
    if (USE_CUDF and len(df_sorted) == 0) or (not USE_CUDF and df_sorted.empty):
        return 0
    if USE_CUDF:
        return float(df_sorted.head(1)['Metacritic score'].to_pandas().values[0])
    return df_sorted.head(1)['Metacritic score'].values[0]

def get_new_appid():
    while True:
        appid = random.randint(0, 9999999)
        if appid not in df['AppID'].values:
            return appid
        
def add_game(name, price, metacritic_score, genres, categories, tags, windows, mac, linux, release_date, header_image):
    global df
    appid = get_new_appid()
    new_row = [[appid, name, release_date, '', '', '', price, '', '', '', '', '', header_image, '', '', '', windows, mac, linux, metacritic_score, '', '', '', '', '', '', '', '', '', '', '', '', '', '', categories, genres, tags, '', '']]
    if USE_CUDF:
        new_game = _gd.DataFrame(new_row, columns=_to_pandas(df).columns)
        df = _gd.concat([df, new_game], ignore_index=True)
        _to_pandas(df).to_csv(filename, index=False, encoding='utf-8')
    else:
        new_game = pd.DataFrame(new_row, columns=df.columns)
        df = df._append(new_game, ignore_index=True)
        df.to_csv(filename, index=False, encoding='utf-8')
    return appid

def update_game(appid, name, price, metacritic_score, genres, categories, tags, windows, mac, linux, release_date, header_image):
    global df
    data = df[df['AppID'] == int(appid)]
    if (USE_CUDF and len(data) == 0) or (not USE_CUDF and data.empty):
        return False
    index = int(_to_pandas(data).index[0])
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
    _to_pandas(df).to_csv(filename, index=False, encoding='utf-8')
    return True

def delete_game(appid):
    global df
    data = df[df['AppID'] == int(appid)]
    if (USE_CUDF and len(data) == 0) or (not USE_CUDF and data.empty):
        return False
    index = int(_to_pandas(data).index[0])
    df = df.drop(index)
    _to_pandas(df).to_csv(filename, index=False, encoding='utf-8')
    return True

def graph_prix_moyen_year(df=df):
    price_series = _ensure_series_numeric(df['Price'])
    gdf = df[(price_series != 0.0) & price_series.notna()]
    pdf = _to_pandas(gdf).copy()
    pdf['__year__'] = pdf['Release date'].apply(to_date).str.slice(0, 4)
    grouped = pdf.groupby('__year__')['Price'].mean().reset_index()
    grouped.columns = ['Year', 'Average Price']
    grouped['Average Price'] = grouped['Average Price'].round(2)
    return grouped

def graph_genre_hight_price(df=df):
    genres = get_all_genres()
    price_series = _ensure_series_numeric(df['Price'])
    df2 = df[(price_series != 0.0) & price_series.notna() & (df['Genres'] != '')]
    prices = []
    games_names = []
    for genre in genres:
        genre_games = get_games_by_genre([genre], df2)
        pdf = _to_pandas(genre_games)
        if pdf.empty:
            prices.append(0)
            games_names.append('')
        else:
            max_price = pdf['Price'].max()
            prices.append(max_price)
            games_names.append(pdf[pdf['Price'] == max_price]['Name'].values[0])
    return pd.DataFrame({'Genre': genres, 'Highest Price': prices, 'Game Name': games_names})

def graph_best_score_platform_label_name(df=df):
    platforms = get_all_platforms()
    score_series = _ensure_series_numeric(df['Metacritic score'])
    df2 = df[(score_series != 0) & score_series.notna()]
    scores = []
    games_names = []
    for platform in platforms:
        platform_games = get_games_by_platform([platform], df2)
        pdf = _to_pandas(platform_games)
        if pdf.empty:
            scores.append(0)
            games_names.append('')
        else:
            max_score = pdf['Metacritic score'].max()
            scores.append(max_score)
            games_names.append(pdf[pdf['Metacritic score'] == max_score]['Name'].values[0])
    return pd.DataFrame({'Platform': platforms, 'Best Score': scores, 'Game Name': games_names})

def graph_best_score_year_platform_label_name(platform, df=df):
    score_series = _ensure_series_numeric(df['Metacritic score'])
    df2 = df[(score_series != 0) & score_series.notna()]
    df2 = get_games_by_platform([platform], df2)
    pdf = _to_pandas(df2).copy()
    years_unique = pdf['Release date'].dropna().apply(to_date).str.slice(0, 4).unique().tolist()
    years_unique.sort()
    scores = []
    games_names = []
    dates = pdf['Release date'].dropna().apply(to_date)
    for year in years_unique:
        year_mask = dates.str.contains(year)
        year_games = pdf[year_mask]
        if year_games.empty:
            scores.append(0)
            games_names.append('')
        else:
            max_score = year_games['Metacritic score'].max()
            scores.append(max_score)
            games_names.append(year_games[year_games['Metacritic score'] == max_score]['Name'].values[0])
    return pd.DataFrame({'Year': years_unique, 'Best Score': scores, 'Game Name': games_names})

@app.route('/')
def home():
    t0 = time.perf_counter()
    engine_name = _resolve_engine(request.args)

    df = _ensure_engine_frame(get_data())

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
    data = _to_pandas(df).to_dict(orient='records')
    
    tag = get_tags()
    genre = get_genres()
    platform = get_platforms()
    category = get_categories()
    
    total_pages = total_games // per_page + 1

    process_ms = int((time.perf_counter() - t0) * 1000)
    return render_template('index.html', data=data, tag=tag, genre=genre, platform=platform, category=category, page=page, per_page=per_page, total_pages=total_pages, total_games=total_games, min_price=min_price, max_price=max_price, min_metacritic=min_metacritic, max_metacritic=max_metacritic, process_ms=process_ms, engine_name=engine_name, gpu_enabled=(engine_name=='cuDF'))

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
    t0 = time.perf_counter()
    args = request.args
    engine_name = _resolve_engine(args)

    df = _ensure_engine_frame(get_data())
    
    if 'graph' in args:
        if args['graph'] == 'genre_hight_price':
            data = graph_genre_hight_price(df)
            values = data['Highest Price'].tolist()
            labels = data['Genre'].tolist()
            names = data['Game Name'].tolist()
            process_ms = int((time.perf_counter() - t0) * 1000)
            return render_template('stats.html', values=values, labels=labels, names=names, process_ms=process_ms, engine_name=engine_name, gpu_enabled=(engine_name=='cuDF'))
        elif args['graph'] == 'best_score_platform_label_name':
            data = graph_best_score_platform_label_name(df)
            values = data['Best Score'].tolist()
            labels = data['Platform'].tolist()
            names = data['Game Name'].tolist()
            process_ms = int((time.perf_counter() - t0) * 1000)
            return render_template('stats.html', values=values, labels=labels, names=names, process_ms=process_ms, engine_name=engine_name, gpu_enabled=(engine_name=='cuDF'))
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
            process_ms = int((time.perf_counter() - t0) * 1000)
            return render_template('stats.html', valueswindows=valueswindows, labelswindows=labelswindows, nameswindows=nameswindows, valuesmac=valuesmac, labelsmac=labelsmac, namesmac=namesmac, valueslinux=valueslinux, labelslinux=labelslinux, nameslinux=nameslinux, process_ms=process_ms, engine_name=engine_name, gpu_enabled=(engine_name=='cuDF')) 
        else:
            data = graph_prix_moyen_year(df)
            values = data['Average Price'].tolist()
            labels = data['Year'].tolist()
            process_ms = int((time.perf_counter() - t0) * 1000)
            return render_template('stats.html', values=values, labels=labels, names=[], process_ms=process_ms, engine_name=engine_name, gpu_enabled=(engine_name=='cuDF'))
    else:
        data = graph_prix_moyen_year(df)
        values = data['Average Price'].tolist()
        labels = data['Year'].tolist()
        process_ms = int((time.perf_counter() - t0) * 1000)
        return render_template('stats.html', values=values, labels=labels, process_ms=process_ms, engine_name=engine_name, gpu_enabled=(engine_name=='cuDF'))

@app.route('/settings')
def settings():
    # Page de paramètres front uniquement (le choix est géré via localStorage côté client)
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
