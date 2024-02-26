from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import string

extractor = URLExtract()


def stats(user, df):
    if user != 'overall':
        df = df[df['users'] == user]

    total_messages = df.shape[0]

    number_of_words = 0
    for i in df[df['msg'] != '<Media omitted>\n']['msg'].values:

        if not extractor.has_urls(i):
            i = i.split()
            number_of_words = number_of_words + len(i)

    number_of_media_messages = df[df['msg'] == '<Media omitted>\n'].shape[0]

    number_of_urls = 0
    for i in df['msg'].values:
        if extractor.has_urls(i):
            number_of_urls = number_of_urls + 1

    return total_messages, number_of_words, number_of_media_messages, number_of_urls


def active_users(df):
    df2 = pd.DataFrame(df['users'].value_counts())
    df2.columns = ['Messages']
    return df2


def create_wordcloud(user, df):
    if user != 'overall':
        df = df[df['users'] == user]
    # cleaning the dataframe
    cln_df = df[df['msg'] != '<Media omitted>\n']

    sw = open('stop_hinglish.txt', encoding='utf-8').read()
    sw = sw.replace('\n', ' ')

    s1 = ''
    for i in cln_df['msg'].values:
        # Removing URL
        if not extractor.has_urls(i):
            for word in i.split():
                if word not in sw:
                    s1 = s1 + ' ' + word.split(sep='\n')[0]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    return wc.generate(s1)

def most_fequent_words(user, df):
    if user != 'overall':
        df = df[df['users'] == user]
    # cleaning the dataframe
    cln_df = df[df['msg'] != '<Media omitted>\n']

    sw = open('stop_hinglish.txt', encoding='utf-8').read()
    sw = sw.replace('\n', ' ')

    s1 = ''
    for i in cln_df['msg'].values:
        # Removing URL
        if not extractor.has_urls(i):
            for word in i.split():
                if word not in sw:
                    s1 = s1 + ' ' + word.split(sep='\n')[0]

    df_temp = pd.DataFrame(Counter(s1.split(sep = ' ')).most_common(25))
    df_temp.columns = ['word', 'count']
    return df_temp

def emoji_used(user, df):
    if user != 'overall':
        df = df[df['users'] == user]
    emo = list()
    for i in df['msg']:
        for j in i.split():
            if emoji.is_emoji(j):
                emo.append(j)

    list_of_emoji_used = list()
    for i in emo:
        if i == '😶\u200d🌫':
            list_of_emoji_used.append('😶')
        elif i == '🤦\u200d♂':
            list_of_emoji_used.append('🤦')
        elif i == '🙆\u200d♂':
            list_of_emoji_used.append('🙆')
        else:
            list_of_emoji_used.append(i)

    temp = pd.DataFrame(Counter(list_of_emoji_used).most_common(15))
    temp.columns = ['emoji', 'count']
    return temp

def month_wise_msg_stats(user, df, year):
    if user != 'overall':
        df = df[df['users'] == user]

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_wise_num_of_message = list()

    temp = df[df['year'] == year]

    for month in months:
        month_wise_num_of_message.append(temp[temp['month'] == month].shape[0])

    ans = pd.DataFrame({'Month': months, 'Num of Messages': month_wise_num_of_message})
    return ans

def monthly_timeline(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['msg'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['msg'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

