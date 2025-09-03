import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('ChatLytics')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)

    # to get unique users
    user_list= df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")


    selected_user=st.sidebar.selectbox('User-centric Breakdown',user_list)

    if st.sidebar.button('Analysis'):

        total_messages,words,total_media_msg,total_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        c1,c2,c3,c4=st.columns(4)

        with c1:
            st.header("Total Messages")
            st.title(total_messages)
        with c2:
            st.header("Total words")
            st.title(words)
        with c3:
            st.header("Media exchanged")
            st.title(total_media_msg)
        with c4:
            st.header("Links Shared")
            st.title(total_links)

        #timeline
        # monthly
        st.title("Monthly Timeline")
        timeline=helper.monthly(selected_user, df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily
        st.title("Daily Timeline")
        dt = helper.daily(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(dt['only_date'], dt['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        c1,c2=st.columns(2)
        with c1:
            st.header("Most Busiest days")
            busy_day=helper.week_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with c2:
            st.header("Most Busy Month")
            busy_month=helper.month_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_map = helper.activity_map(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_map, cmap='YlGnBu')
        st.pyplot(fig)




        # Most active users
        if selected_user=='Overall':
            st.title("Most active users")
            x,new_df=helper.active_users(df)
            fig,ax=plt.subplots()

            c1,c2=st.columns(2)
            with c1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with c2:
                st.dataframe(new_df)




        # wordcloud
        st.title("Wordcloud")
        df_w=helper.create_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_w)
        st.pyplot(fig)

        # most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)


        # emoji info
        emoji_df=helper.emoji_analysis(selected_user,df)
        st.title('Emoji Analysis')
        c1,c2=st.columns(2)

        with c1:
            st.dataframe(emoji_df)
        with c2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
