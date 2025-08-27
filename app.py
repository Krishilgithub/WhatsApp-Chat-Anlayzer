import streamlit as st
import pickle
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
  bytes_data = uploaded_file.getvalue()
  data = bytes_data.decode('utf-8')

  # st.text(data)

  df = preprocessor.preprocess(data)
  st.dataframe(df)

  user_list = df['users'].unique().tolist()
  # if user_list.contains('group_notifications'):
  #   user_list.remove('group_notifications')
  user_list.sort()
  user_list.insert(0,  'Overall')

  selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

  if st.sidebar.button('Show Analysis'):
    st.title("Top Statistics")
    col1, col2, col3, col4 = st.columns(4)

    num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

    with col1:
      st.header("Total Messages")
      st.title(num_messages)

    with col2:
      st.header("Total Words")
      st.title(words)

    with col3:
      st.header("Media Shared")
      st.title(num_media_messages)

    with col4:
      st.header("Links Shared")
      st.title(num_links)


    # finding the busiest user from the group(Group level)
    if selected_user == 'Overall':
      st.title('Most Busy Users')
      x, df_busy = helper.most_busy_user(df)
      fig, ax = plt.subplots()

      col1, col2 = st.columns(2)
      
      with col1:
        ax.bar(x.index, x.values, color='red')
        ax.set_xlabel("Users")
        ax.set_ylabel("Number of Messages")
        plt.xticks(rotation=90)
        st.pyplot(fig)

      with col2:
        st.dataframe(df_busy)


    # WordCloud
    st.title("WordCloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    # most common words
    st.title("Most Common Words")
    col1, col2 = st.columns(2)
    most_common_df = helper.most_common_words(selected_user, df)

    with col2:
      st.dataframe(most_common_df)

    with col1:
      fig, ax = plt.subplots()
      ax.barh(most_common_df['Word'], most_common_df['Count'], color='green')
      plt.xlabel("Count")
      plt.ylabel("Words")
      st.pyplot(fig)

    # Emoji Analysis
    st.title("Emoji Analysis")
    col1, col2 = st.columns(2)

    with col2:
      emoji_df = helper.emoji_helper(selected_user, df)
      st.dataframe(emoji_df)

    with col1:
      fig, ax = plt.subplots()
      ax.barh(emoji_df[0], emoji_df[1], color='blue')
      plt.xlabel("Count")
      plt.ylabel("Emojis")
      st.pyplot(fig)

    # monthly timeline
    st.title("Monthly Timeline")

    col1, col2 = st.columns(2)

    with col1:
      timeline = helper.monthly_timeline(selected_user, df)
      fig, ax = plt.subplots()
      ax.plot(timeline['time'], timeline['messages'])
      plt.xticks(rotation=90)
      st.pyplot(fig)

    with col2:
      st.dataframe(timeline)

    # daily timeline
    st.title("Daily Timeline")

    col1, col2 = st.columns(2)

    with col1:
      timeline = helper.daily_timeline(selected_user, df)
      fig, ax = plt.subplots()
      ax.plot(timeline['only_date'].astype(str), timeline['messages'])
      plt.xticks(rotation=90)
      st.pyplot(fig)

    with col2:
      st.dataframe(timeline)

    # activity map
    st.title("Weekly Activity Map")

    col1, col2 = st.columns(2)

    with col1:
      timeline = helper.week_activity_map(selected_user, df)
      fig, ax = plt.subplots()
      ax.bar(timeline.index, timeline.values, color='purple')
      ax.set_xlabel("Days")
      ax.set_ylabel("Number of Messages")
      plt.xticks(rotation=90)
      st.pyplot(fig)

    with col2:
      st.dataframe(timeline)

    # month activity map

    st.title("Monthly Activity Map")

    col1, col2 = st.columns(2)

    with col1:
      timeline = helper.month_activity_map(selected_user, df)
      fig, ax = plt.subplots()
      ax.bar(timeline.index, timeline.values, color='orange')
      ax.set_xlabel("Months")
      ax.set_ylabel("Number of Messages")
      plt.xticks(rotation=90)
      st.pyplot(fig)

    with col2:
      st.dataframe(timeline)

    # activity map
    st.title("Activity Heatmap")

    col1, col2 = st.columns(2)

    with col1:
      timeline = helper.activity_heatmap(selected_user, df)
      fig, ax = plt.subplots()
      sns.heatmap(timeline, cmap='Blues', annot=True, ax=ax)
      plt.yticks(rotation='horizontal')
      plt.xticks(rotation='vertical')
      st.pyplot(fig)

    with col2:
      st.dataframe(timeline)
