import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import helper
import preprocessor

st.sidebar.markdown("<h1 style='text-align: center; color: #FF4B4B;'>WhatsApp Chat Analyzer</h1>", unsafe_allow_html=True)
st.sidebar.write('\n')
st.sidebar.write('\n')

uploaded_file = st.sidebar.file_uploader("Choose a text file")
st.sidebar.write('\n')
st.sidebar.write('\n')

if "button1" not in st.session_state:
    st.session_state["button1"] = False

if "button2" not in st.session_state:
    st.session_state["button2"] = False

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # show different user
    all_users = df['users'].unique().tolist()
    if 'group_notification' in all_users :
        all_users.remove('group_notification')
    all_users.sort()
    all_users.insert(0, 'overall')
    selected_user = st.sidebar.selectbox(
        'Select The User From Below', all_users)
    
    st.sidebar.write('\n')
    st.sidebar.write("This year variable is used only for 'Year wise analysis' section.")
    year = st.sidebar.slider('Enter The Year, You Want to analysis', 2010, 2030)
    st.sidebar.write('\n')
    st.sidebar.write('\n')

    if st.sidebar.button('Show Analysis'):

        st.session_state["button1"] = not st.session_state["button1"]

        # Welcome text
        if selected_user == 'overall':
            st.title("WhatsApp Analysis Of Overall Group")
        else:
            st.title(f"WhatsApp Analysis Of : {selected_user}" )

        st.write('\n')
        st.write('\n')

        # Stats area
        num_messages, num_words, num_of_media_messages, num_of_url = helper.stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_of_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_of_url)

        st.write('\n')
        st.write('\n')
        st.write('\n')

        # activity map
        st.title('Activity Map')
        col11,col12 = st.columns(2)

        with col11:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='#b48e92')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col12:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='#5b7553')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Finding the Active user in the group
        if selected_user == 'overall':

            st.write('\n')
            st.write('\n')
            active_df = helper.active_users(df)
            st.header("Most Active Users :")

            # fig, ax = plt.subplot()
            col1, col2 = st.columns(2)

            with col1:
                # ax.bar(active_df.index, active_df.values)
                # plt.xticks(rotation = 'vertical')
                # st.pyplot(fig)
                plt.subplot(121)
                st.bar_chart(active_df.head())

            with col2:
                c1, c2 = st.columns(2)

                with c2 :
                    active_df['Messages'] = (active_df['Messages'].values / df.shape[0]) * 100
                    st.dataframe(active_df)

        # Ploting Word Cloud
        st.write('\n')
        st.write('\n')
        st.header("WordCloud")
        c1, c2 = st.columns(2)
        with c1 :
            img_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(img_wc)
            st.pyplot(fig)

        # Most frequently used words
        st.write('\n')
        st.write('\n')
        st.header("Most Frequently Used Words")
        df_most_frequent_words = helper.most_fequent_words(selected_user, df)
        colu1, colu2 = st.columns(2)
        fig, ax = plt.subplots()

        with colu1 :
            ax.bar(df_most_frequent_words['word'], df_most_frequent_words['count'], color = '#73683b')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with colu2 :
            st.dataframe(df_most_frequent_words)

        # Most frequently used emoji
        st.write('\n')
        st.write('\n')
        st.header("Most Frequently Used Emoji")
        df_most_frequent_emoji = helper.emoji_used(selected_user, df)
        col5, col6 = st.columns(2)
        fig, ax = plt.subplots()

        with col5:
            ax.bar(df_most_frequent_emoji['emoji'], df_most_frequent_emoji['count'], color = '#73683b')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col6:
            st.dataframe(df_most_frequent_emoji)

        # Your wise analysis
        st.write('\n')
        st.write('\n')
        st.header(f'Year wise analysis | Year : {year}')

        df_month_wise = helper.month_wise_msg_stats(selected_user, df, year)
        fig, ax = plt.subplots()

        col7, col8 = st.columns(2)

        with col7 :

            ax.bar(df_month_wise['Month'], df_month_wise['Num of Messages'], color = '#3e8989')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col8 :

            ax.plot(df_month_wise['Month'], df_month_wise['Num of Messages'], color = 'red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # monthly timeline
        st.write('\n')
        st.write('\n')
        st.header("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['msg'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.write('\n')
        st.write('\n')
        st.header("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['msg'], color='#472c4c')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

