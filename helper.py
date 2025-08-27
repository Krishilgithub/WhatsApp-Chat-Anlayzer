from collections import Counter
from urlextract import URLExtract   #type: ignore
from wordcloud import WordCloud     #type: ignore
from collections import Counter
import pandas as pd
import emoji    #type: ignore

extractor = URLExtract()

def fetch_stats(selected_user, df):

  if selected_user != 'Overall':
    df = df[df['users'] == selected_user]
  
  # fetch the number of messages
  num_messages = df.shape[0]
  # fetch the number of words
  words = []
  # fetch the media messages
  num_media_messages = df[df['messages'].str.contains('<Media omitted>\n', na=False)].shape[0]
  # fetch the number of links shared
  links = []

  for message in df['messages']:
    try:
      if pd.notna(message) and isinstance(message, str):
        words.extend(message.split())
        links.extend(extractor.find_urls(message))
    except:
      continue

  return num_messages, len(words), num_media_messages, len(links)

def most_busy_user(df):
  x = df['users'].value_counts().head()
  df_busy = round(df['users'].value_counts().head()/df.shape[0]*100, 2).reset_index().rename(columns={'index': 'Name', 'users': 'Percent'})
  return x, df_busy

def create_wordcloud(selected_user, df):

  if selected_user != 'Overall':
    df = df[df['users'] == selected_user]

  temp = df[df['messages'] != 'group_notification']
  temp = temp[~temp['messages'].str.contains('<Media omitted>\n', na=False)]

  f = open('./stop_hinglish.txt', 'r')
  stopwords = f.read().split()  # Split into list for faster lookup
  f.close()

  def remove_stopwords(message):
    if pd.notna(message) and isinstance(message, str):
      words = [word for word in message.split() if word.lower() not in stopwords]
      return " ".join(words)
    return ""

  # Check if messages column exists and handle null values
  if 'messages' not in temp.columns:
    raise ValueError("DataFrame does not contain 'messages' column")
  
  # Apply stopword removal efficiently
  temp = temp.copy()  # Avoid SettingWithCopyWarning
  temp['messages'] = temp['messages'].apply(remove_stopwords)
  
  # Filter out empty messages and concatenate
  messages_text = temp['messages'][temp['messages'].str.len() > 0].str.cat(sep=" ")
  
  if not messages_text.strip():
    raise ValueError("No valid messages found after removing stopwords")

  wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
  df_wc = wc.generate(messages_text)

  return df_wc

def most_common_words(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['users'] == selected_user]

  temp = df[df['messages'] != 'group_notification']
  temp = temp[~temp['messages'].str.contains('<Media omitted>\n')]

  f = open('./stop_hinglish.txt', 'r')
  stopwords = f.read()
  f.close()

  words = []

  for message in temp['messages']:
    for word in message.split():
      if word not in stopwords:
        words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])
  return most_common_df


def emoji_helper(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['users'] == selected_user]

  emojis = []

  for message in df['messages']:
    emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

  return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


def monthly_timeline(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['users'] == selected_user]

  timeline = df.groupby(['month', 'year']).count()['messages'].reset_index()
  timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

  return timeline

def daily_timeline(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['users'] == selected_user]

  timeline = df.groupby(['only_date']).count()['messages'].reset_index()
  return timeline

def week_activity_map(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['users'] == selected_user]

  return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['users'] == selected_user]

  return df['month'].value_counts()

def activity_heatmap(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['users'] == selected_user]

  heatmap_data = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

  return heatmap_data
