from urlextract import URLExtract #it is a library to extract url from text
from wordcloud import WordCloud# wordcloud matplotlib
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract() #object


def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # total number of messages
    total_messages = df.shape[0]
    # total no. of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # total number of media messages
    total_media_msg = df[df['message']=='<Media omitted>\n'].shape[0]
    # fetch number of links
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return total_messages, len(words),total_media_msg,len(links)


def active_users(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'users','user':'percent'})
    return x,df

def create_cloud(selected_user,df):
    f = open('stopwords.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    w=WordCloud(width=500, height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stopwords)
    df_w=w.generate(temp['message'].str.cat(sep=" "))
    return df_w


def most_common_words(selected_user,df):
    f= open('stopwords.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']

    words= []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(25))
    return most_common_df

def emoji_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])


    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    dt = df.groupby('only_date').count()['message'].reset_index()

    return dt

def week_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_map = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_map