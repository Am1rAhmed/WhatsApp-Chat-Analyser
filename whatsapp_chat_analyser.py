import streamlit as st
import preprocessor as ppr
import helper
import json
import matplotlib.pyplot as plt
import seaborn as sn
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="WhatsApp Chat Analyser",
    page_icon="https://static.vecteezy.com/system/resources/previews/023/986/631/non_2x/whatsapp-logo-whatsapp-logo-transparent-whatsapp-icon-transparent-free-free-png.png",
    layout = "wide"
)

with open("Animation - 1711349086623.json",'r') as file:
    animation = json.load(file)
st.lottie(animation,width=550,height=550)
st.sidebar.title(":violet[Whatsapp Chat Analyser]")
uploaded_file = st.sidebar.file_uploader(":green[Upload your file here] ",type=['txt'])
if uploaded_file is not None:
    # Converting the uploaded file whic is a byte stream into string 
    bytes_data = uploaded_file.getvalue()
    # Converting data into string
    data = bytes_data.decode("utf-8")
    df = ppr.preprocess(data)


    #fetch unique user
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")
        selected_user = st.sidebar.selectbox(":blue[Show Analysis] ",user_list)

    if st.sidebar.button("Show Analysis"):
        st.snow()
        num_msgs,words,num_media_msg,links = helper.fetch_stats(selected_user,df)
        st.markdown("<h1 style='text-align:center';>Whatsapp Statistics</h1>",unsafe_allow_html=True)
        st.markdown("---")
        col1,col2,col3,col4,col5 = st.columns(5)
        if selected_user == "Overall":
            with col1:
                st.header("Total Persons")
                st.title(len(user_list))
        with col2:
            st.header("Total Message ")
            st.title(num_msgs)
        with col3:
            st.header("Total Words")
            st.title(words)
        with col4:
            st.header("Total Media")
            st.title(num_media_msg)
        with col5:
            st.header("Total Links")
            st.title(links)
        
        # finding the most busy users in the group
        if selected_user == "Overall":
            st.markdown("<h1 style='text-align:center';>Most Busy Users</h1>",unsafe_allow_html=True)
            x,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Creating WordCloud
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Word Cloud</h1>",unsafe_allow_html=True)
        st.markdown("---")
        df_wc = helper.create_wordCloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Most Common Words</h1>",unsafe_allow_html=True)
        st.markdown("---")
        most_common_df = helper.most_commonWords(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

                
        # Emoji analysis
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Emoji Analysis</h1>",unsafe_allow_html=True)
        st.markdown("---")
        emoji_df = helper.emoji_helper(selected_user, df)
        if len(emoji_df) != 0:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df.head())
            
            with col2:
                # The 'Segoe UI Emoji' font family includes emojis and other Unicode symbols, making it suitable for displaying emoji characters in plots.

                plt.rcParams['font.family'] = 'Segoe UI Emoji'
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct="%0.1f%%")
                st.pyplot(fig)
            
        else:
            st.write(f"{selected_user} have not send any emoji right now...")


        #Monthly timeline
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Monthly Timeline Analysis</h1>",unsafe_allow_html=True)
        st.markdown("---")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="red")
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


        #Daily Timeline
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Daily Timeline</h1>",unsafe_allow_html = True)
        st.markdown("---")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['daily_timeline'],daily_timeline['message'],color="magenta")
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


        # Activity map
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Activity Map</h1>",unsafe_allow_html = True)
        st.markdown("---")
        col1,col2 = st.columns(2)
        with col1:
            st.subheader("**Most Busy Day**")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="green")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader("**Most Busy Month**")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="black")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # User Activity Heatmap
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Weekly Activity Heatmap</h1>",unsafe_allow_html = True)
        st.markdown("---")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots(figsize=(20,8))
        ax = sn.heatmap(user_heatmap,annot=True, cmap=sn.cubehelix_palette(as_cmap=True))
        st.pyplot(fig)

