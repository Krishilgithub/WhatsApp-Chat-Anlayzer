import re
import pandas as pd

def preprocess(data):
  pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'  # DD/MM/YY, HH:MM - 

  messages = re.split(pattern, data)
  dates = re.findall(pattern, data)

  if messages and not messages[0].strip():
    messages = messages[1:]

  dates = [str.split('-')[0] for str in dates]

  df = pd.DataFrame({'message_date': dates, 'user_message': messages})

  df['message_date'] = df['message_date'].str.strip()
  df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %H:%M")

  df.rename(columns={'message_date': 'date'}, inplace=True)

  x = 'Messages and calls are end-to-end encrypted. Only people in this chat can read, listen to, or share them. Learn more.'
  df = df[~df['user_message'].str.contains(x, na=False)]

  users = []
  messages = []
  group_notifications = []

  for i in df['user_message']:
    users.append(i.split(':')[0])
    messages.append(i.split(':')[1])
    if i.split(':') == '':
      messages.append(i)

  df['users'] = users
  df['messages'] = messages
  df.drop('user_message', axis=1, inplace=True)

  df['year'] = df['date'].dt.year
  df['month'] = df['date'].dt.month_name()
  df['only_date'] = df['date'].dt.date
  df['month_num'] = df['date'].dt.month
  df['day_name'] = df['date'].dt.day_name()
  df['day'] = df['date'].dt.day
  df['hour'] = df['date'].dt.hour
  df['minute'] = df['date'].dt.minute

  period = []

  for hour in df[['day_name', 'hour']]['hour']:
    if hour == 23:
      period.append(str(hour) + "-" + str(00))
    elif hour == 0:
      period.append(str('00') + "-" + str(hour + 1))
    else:
      period.append(str(hour) + "-" + str(hour + 1))

  df['period'] = period

  return df