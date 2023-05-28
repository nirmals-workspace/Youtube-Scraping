from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.mention import mention
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from streamlit_lottie import st_lottie
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime
import plotly.express as px
import streamlit as st
import altair as alt
import pandas as pd
import requests
import isodate
import json
import math


# Page Configuration

st.set_page_config("Youtube Data Harvesting", layout = "wide", page_icon=r'Related Images and Videos/youtube.png')

page_title, lottie, buff= st.columns([65, 40, 5])

page_title.title('Youtube Data Harvesting')

with open (r"Related Images and Videos/youtube.json") as f:
    lottie_json = json.load(f)
with lottie:
    st_lottie(lottie_json, height= 100, width=200)


# MongoDB connection

mongo_client = MongoClient(st.secrets['mongo_db']['URI'])
db = mongo_client['youtube_db']
collection = db['youtube_collection']


# Loading API

api_key = st.secrets['api_key']['key']


# App Chapter 1

# 1.1 - Defining Functions

@st.cache_data
def convert_datetime(published_at):
    datetime_obj = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

@st.cache_data
def format_duration(duration):
    duration_obj = isodate.parse_duration(duration)
    hours = duration_obj.total_seconds() // 3600
    minutes = (duration_obj.total_seconds() % 3600) // 60
    seconds = duration_obj.total_seconds() % 60

    formatted_duration = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    return formatted_duration


@st.cache_data
def get_channel_id(api_key, channel_username):
    try:
        _youtube = build('youtube', 'v3', developerKey=api_key)
        response = _youtube.search().list(
            part="snippet",
            q=channel_username,
            type="channel",
            maxResults=1
        ).execute()

        if 'items' in response and response['items']:
            channel_item = response['items'][0]
            return channel_item['snippet']['channelId']
        else:
            page_source = requests.get(f'https://www.youtube.com/{channel_username}').text
            channel_id_start_index = page_source.find('"channelId":"') + len('"channelId":"')
            channel_id_end_index = page_source.find('"', channel_id_start_index)
            channel_id = page_source[channel_id_start_index:channel_id_end_index]
            return channel_id
    except HttpError as e:
        if e.resp.status == 403 and b"quotaExceeded" in e.content:
            st.write("API Quota exhausted... Try using after 24 hours")
        else:
            raise Exception('Channel ID not found.')

@st.cache_data                
def fetch_video_comments(_youtube, video_id, max_results=3):
    try:
        comments_response = _youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=max_results
        ).execute()
    except HttpError as e:
        if e.resp.status == 403:
            return {}
        else:
            raise

    comments = comments_response['items']
    
    video_comments = {}
    
    for idx, comment in enumerate(comments):
        comment_id = comment['snippet']['topLevelComment']['id']
        comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        comment_author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comment_published_at = convert_datetime(comment['snippet']['topLevelComment']['snippet']['publishedAt'])

        video_comments[f'Comment_{idx+1}'] = {
            'Comment_Id': comment_id,
            'Comment_Text': comment_text,
            'Comment_Author': comment_author,
            'Comment_PublishedAt': comment_published_at
        }
    
    return video_comments

channel_name = None

@st.cache_data
def fetch_channel_data(api_key, channel_id):
    global channel_name
    
    status_text = st.empty()
    try:
        _youtube = build('youtube', 'v3', developerKey=api_key)

        channel_response = _youtube.channels().list(part='snippet, statistics, contentDetails, status', id=channel_id).execute()
        channel_items = channel_response.get('items', [])
        
        if channel_items:
            channel_item = channel_items[0]
            channel_name = channel_item['snippet']['title']
            st.session_state['channel_name'] = channel_name
            subscription_count = int(channel_item['statistics']['subscriberCount'])
            view_count = int(channel_item['statistics']['viewCount'])
            if channel_item['snippet']['description'] == '':
                channel_description = 'NA'
            else:
                channel_description = channel_item['snippet']['description']
            uploads_playlist_id = channel_item['contentDetails']['relatedPlaylists']['uploads']
            channel_status = channel_item['status']['privacyStatus']
        else:
            channel_name = 'NA'
            subscription_count = 0
            view_count = 0
            channel_description = 'NA'
            uploads_playlist_id = 'NA'
            channel_status = 'NA'
            
        playlists = []
        next_page_token = None

        while True:
            playlists_response = _youtube.playlists().list(
                part='snippet',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            playlists.extend(playlists_response.get('items', []))

            next_page_token = playlists_response.get('nextPageToken')

            if next_page_token is None:
                break

        video_details = {}
        video_index = 1
        added_video_ids = set()

        for playlist in playlists:
            playlist_id = playlist['id']
            playlist_name = playlist['snippet']["title"]

            next_page_token = None
            videos = []

            while True:
                playlist_items_response = _youtube.playlistItems().list(
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()

                videos.extend(playlist_items_response.get('items', []))

                next_page_token = playlist_items_response.get('nextPageToken')

                if next_page_token is None:
                    break

            for item in videos:
                video_id = item['snippet']['resourceId']['videoId']

                if video_id in added_video_ids:
                    continue

                video_response = _youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=video_id
                ).execute()
                video_items = video_response.get('items', [])

                if video_items:
                    video_snippet = video_items[0]['snippet']
                    video_stats = video_items[0]['statistics']
                    video_name = video_snippet['title']
                    video_description = video_snippet['description']
                    video_tags = video_snippet.get('tags', [])
                    published_at = convert_datetime(video_snippet['publishedAt'])
                    view_count = int(video_stats.get('viewCount', 0))
                    like_count = int(video_stats.get('likeCount', 0))
                    dislike_count = int(video_stats.get('dislikeCount', 0))
                    favorite_count = int(video_stats.get('favoriteCount', 0))
                    comment_count = int(video_stats.get('commentCount', 0))
                    duration = format_duration(video_items[0]['contentDetails']['duration'])
                    thumbnail = video_snippet['thumbnails']['default']['url']
                    caption_status = video_snippet.get('caption', 'Not available')
                else:
                    continue

                video_key = f'Video_{video_index}'
                video_comments = fetch_video_comments(_youtube, video_id)
                    
                video_details[video_key] = {
                    'Playlist_Id': playlist_id,
                    'Video_Id': video_id,
                    'Playlist_Name': playlist_name,
                    'Video_Name': video_name,
                    'Video_Description': video_description,
                    'Tags': video_tags,
                    'PublishedAt': published_at,
                    'View_Count': view_count,
                    'Like_Count': like_count,
                    'Dislike_Count': dislike_count,
                    'Favorite_Count': favorite_count,
                    'Comment_Count': comment_count,
                    'Duration': duration,
                    'Thumbnail': thumbnail,
                    'Caption_Status': caption_status,
                    'Comments': video_comments
                }

                added_video_ids.add(video_id)
                video_index += 1

        next_page_token = None
        remaining_videos = []

        while True:
            remaining_videos_response = _youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=50,
                type='video',
                pageToken=next_page_token
            ).execute()

            remaining_videos.extend(remaining_videos_response.get('items', []))

            next_page_token = remaining_videos_response.get('nextPageToken')

            if next_page_token is None:
                break

        for item in remaining_videos:
            video_id = item['id']['videoId']

            if video_id in added_video_ids:
                continue

            video_response = _youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            ).execute()
            video_items = video_response.get('items', [])

            if video_items:
                video_snippet = video_items[0]['snippet']
                video_stats = video_items[0]['statistics']
                video_name = video_snippet['title']
                video_description = video_snippet['description']
                video_tags = video_snippet.get('tags', [])
                published_at = convert_datetime(video_snippet['publishedAt'])
                view_count = int(video_stats.get('viewCount', 0))
                like_count = int(video_stats.get('likeCount', 0))
                dislike_count = int(video_stats.get('dislikeCount', 0))
                favorite_count = int(video_stats.get('favoriteCount', 0))
                comment_count = int(video_stats.get('commentCount', 0))
                duration = format_duration(video_items[0]['contentDetails']['duration'])
                thumbnail = video_snippet['thumbnails']['default']['url']
                caption_status = video_snippet.get('caption', 'Not available')
            else:
                continue

            video_key = f'Video_{video_index}'
            video_comments = fetch_video_comments(_youtube, video_id)

            video_details[video_key] = {
                'Playlist_Id': 'NA',
                'Video_Id': video_id,
                'Playlist_Name': 'NA',
                'Video_Name': video_name,
                'Video_Description': video_description,
                'Tags': video_tags,
                'PublishedAt': published_at,
                'View_Count': view_count,
                'Like_Count': like_count,
                'Dislike_Count': dislike_count,
                'Favorite_Count': favorite_count,
                'Comment_Count': comment_count,
                'Duration': duration,
                'Thumbnail': thumbnail,
                'Caption_Status': caption_status,
                'Comments': video_comments
            }

            added_video_ids.add(video_id)
            video_index += 1

        channel_details = {
            'Channel_Id': channel_id,
            'Channel_Name': channel_name,
            'Uploads_Playlist_Id': uploads_playlist_id,
            'Subscription_Count': subscription_count,
            'Channel_Views': view_count,
            'Channel_Description': channel_description,
            'Channel_Status': channel_status
        }
        
        data = {
            '_id': channel_id,
            'Channel_Details': channel_details,
            'Video_Details': video_details
        }

        return data

    except HttpError as e:
        if e.resp.status == 403 and b"quotaExceeded" in e.content:
            status_text.write("API Quota exhausted... Try using after 24 hours")
        else:
            raise Exception('API request broke...Try again...')

# 1.2 - Streamlit Part

st.subheader('Fetch data and push into Atlas')

add_vertical_space(2)

col1, buff = st.columns([3,7])
channel_username = col1.text_input('Enter channel username:', value='@TechwithLucy')

but,ref = st.columns(2)

if but.button('Fetch and Push into MongoDB Atlas', key = 'push'):
    
    channel_id = get_channel_id(api_key, channel_username)
    channel_data = fetch_channel_data(api_key, channel_id)
    
    channel_details = channel_data['Channel_Details']
    df = pd.DataFrame.from_dict([channel_details]).rename(columns={
                                                                   "Channel_Name": "Channel Name",
                                                                   "Channel_Id": "Channel ID",
                                                                   "Uploads_Playlist_Id": "Channel Playlist ID",
                                                                   "Subscription_Count": "Subscription Count",
                                                                   "Channel_Views": "Channel View Count",
                                                                   "Channel_Description": "Channel Description",
                                                                   "Channel_Status": "Channel Status"
                                                                   }
                                                          )
    df.index = [1]
    st.dataframe(df)
    
    existing_doc = collection.find_one({"_id": channel_data["_id"]})

    if existing_doc:
        collection.replace_one({"_id": channel_data["_id"]}, channel_data)
    else:
        collection.insert_one(channel_data)
        
    st.write(f"Data related to the channel - '{df['Channel_Name']}' pushed successfully into MongoDB Atlas...")


# 1.3 - Youtube reference


with ref:
    mention(
    label="Go to YouTube",
    icon="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/brands/youtube.svg",
    url="https://youtube.com"
    )

add_vertical_space(2)


# 1.4 - Channel Username Reference

with st.expander('Wait! But where can you get channel username from ?'):
    
    image = st.image(r'Related Images and Videos/Username.png')
    
    if 'image' not in st.session_state:
        st.session_state["image"] = image

# App Chapter 2

# 2.1 - Defining Functions

def fetch_document(_collection, channel_name):
    document = _collection.find_one({"Channel_Details.Channel_Name": channel_name})
    return document

def fetch_channel_names(_collection):
    channel_names = _collection.distinct("Channel_Details.Channel_Name")
    return channel_names

if "channel_names" not in st.session_state:
    channel_names = fetch_channel_names(collection)
    st.session_state["channel_names"] = channel_names
    
existing_channel_count = len(st.session_state["channel_names"])
new_channel_count = collection.estimated_document_count()

if existing_channel_count != new_channel_count:
    existing_channels = set(st.session_state["channel_names"])
    new_channel_names = [name for name in fetch_channel_names(collection) if name not in existing_channels]
    st.session_state["channel_names"].extend(new_channel_names)


# 2.1 - Defining Function

def fetch_video_dataframe(document):
    
    video_details = document["Video_Details"]

    video_df_data = []
    for video_key, video_info in video_details.items():
        video_df_entry = {
            "Video_Name": video_info.get("Video_Name", ""),
            "Playlist_Id": video_info.get("Playlist_Id", ""),
            "Playlist_Name": video_info.get("Playlist_Name", ""),
            "PublishedAt": video_info.get("PublishedAt", ""),
            "View_Count": video_info.get("View_Count", ""),
            "Like_Count": video_info.get("Like_Count", ""),
            "Dislike_Count": video_info.get("Dislike_Count", ""),
            "Favorite_Count": video_info.get("Favorite_Count", ""),
            "Comment_Count": video_info.get("Comment_Count", ""),
            "Duration": video_info.get("Duration", "")
        }
        video_df_data.append(video_df_entry)

    video_df = pd.DataFrame(video_df_data)
    return video_df


# 2.2 - Streamlit Part


add_vertical_space(2)

st.subheader('Know about any video')

add_vertical_space(2)

col1, col2, col3 = st.columns(3)
selected_channel = col1.selectbox("Select Channel", list(st.session_state["channel_names"]), key="channel")

if selected_channel:
    
    selected_document = fetch_document(collection, selected_channel)

    if selected_document:
        
        selected_video_df = fetch_video_dataframe(selected_document)

        if not selected_video_df.empty:
            
            selected_video_df = selected_video_df[["Video_Name", "Playlist_Name", "PublishedAt", "View_Count", "Like_Count", "Dislike_Count", "Favorite_Count", "Comment_Count", "Duration"]]

            playlist_names = selected_video_df["Playlist_Name"].unique()
            playlist_names = [playlist for playlist in playlist_names if playlist != "NA"]

            videos_not_in_playlist = selected_video_df[selected_video_df["Playlist_Name"] == "NA"]
            
            if not videos_not_in_playlist.empty:
                
                playlist_names = ["Videos not in Playlists"] + playlist_names

            selected_playlist = col2.selectbox("Select Playlist", playlist_names, key="playlist")

            if selected_playlist:
                
                if selected_playlist == "Videos not in Playlists":
                    filtered_videos = videos_not_in_playlist
                else:
                    filtered_videos = selected_video_df[selected_video_df["Playlist_Name"] == selected_playlist]

                if not filtered_videos.empty:
                    
                    video_names = filtered_videos["Video_Name"].tolist()
                    video_names.insert(0, "Select Video")
                    
                    selected_video = col3.selectbox("Select Video", video_names, key="video")
                    

                    if selected_video != "Select Video":
                        
                        video_details = filtered_videos[filtered_videos["Video_Name"] == selected_video].iloc[0]
                        video_details = pd.DataFrame(video_details)
                        video_details.columns = ["Details"]
                        video_details.rename({
                            "Video_Name": "Video Name", "Playlist_Name": "Playlist Name",
                            "PublishedAt": "Published at", "View_Count": "View Count",
                            "Like_Count": "Like Count", "Dislike_Count": "Dislike Count",
                            "Favorite_Count": "Favorite Count", "Comment_Count": "Comment Count",
                        }, axis=0, inplace=True)
                        
                        st.dataframe(video_details, width=600)
                    else:
                        st.write("")
                else:
                    st.write("No videos available for the selected playlist.")
            else:
                st.write("Select a playlist.")
        else:
            st.write("No videos available for the selected channel.")
    else:
        st.write("Selected channel document not found.")
else:
    st.write("Select a channel.")


# App Chapter 3

# 3.1 - Streamlit Part and Visualizations


side_bar = st.sidebar

side_bar.subheader('Youtube Analytics')
side_bar.image(r'Related Images and Videos/youtube.gif')


selected_channel = side_bar.selectbox("Select Channel", st.session_state['channel_names'], key='channels')

channel_data = collection.find_one({"Channel_Details.Channel_Name": selected_channel})
video_details = channel_data["Video_Details"]

viz_options = ['Animated Bubble Plot', 'Word Cloud', 'Donut Chart', 'Bar Chart', 'Histogram']


if 'viz_options' not in st.session_state:
    st.session_state['viz_options'] = viz_options

selected_viz = side_bar.selectbox("Select Visualization", st.session_state['viz_options'], key = 'selected_viz')
viz_button = side_bar.button("Show Visualization",key='viz')


# Viz-1


if selected_viz == 'Animated Bubble Plot' and viz_button:
    
    st.subheader(f'Video view count trend in {selected_channel} channel')
    data = []

    for video_key, video_data in video_details.items():
        view_count = video_data.get('View_Count', 0)
        published_time = video_data.get('PublishedAt', '')

        published_time = pd.to_datetime(published_time)

        data.append({'View_Count': view_count, 'Published_Time': published_time, 'Video_Key': video_key})

    df = pd.DataFrame(data)

    df = df.sort_values('Published_Time')
    
    df['Video Number'] = range(1, len(df) + 1)

    fig = px.scatter(df, x='Published_Time', y='View_Count', size='View_Count', animation_frame='Video Number',
                    range_x=[df['Published_Time'].min(), df['Published_Time'].max()],
                    range_y=[df['View_Count'].min(), df['View_Count'].max()])

    fig.update_layout(xaxis_title='Published Time', yaxis_title='View Count')

    frame_duration = 1000  # Adjust the value to control the frame rate (e.g., 1000 milliseconds = 1 second)

    st.plotly_chart(fig, use_container_width=True, config={'plotly': {'animation': {'frame': {'duration': frame_duration}}}})


# Viz-2


elif selected_viz == 'Word Cloud' and viz_button:
    
    st.subheader(f'Video Titles Word Cloud for {selected_channel} channel')
    
    video_titles = [video_details[key]['Video_Name'] for key in video_details]
    text = ' '.join(video_titles)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt, use_container_width=True)


# Viz-3


elif selected_viz == 'Donut Chart' and viz_button:

    st.subheader(f'Top Playlists by view count in {selected_channel} channel')
  
    playlist_views = {}

    for video_key in video_details:
        playlist_name = video_details[video_key]['Playlist_Name']
        if playlist_name == 'NA':
            continue
        view_count = video_details[video_key]['View_Count']
        if playlist_name not in playlist_views:
            playlist_views[playlist_name] = view_count
        else:
            playlist_views[playlist_name] += view_count

    sorted_playlists = sorted(playlist_views, key=lambda x: playlist_views[x], reverse=True)
    sorted_counts = [playlist_views[x] for x in sorted_playlists]

    top_playlists = sorted_playlists[:6]
    other_count = sum(sorted_counts[6:])
    top_counts = sorted_counts[:6] + [other_count]

    data = pd.DataFrame({'Playlist': top_playlists + ['Others'], 'View_Count': top_counts})

    fig = px.pie(data, values='View_Count', names='Playlist', hole=0.6)
    fig.update_traces(textposition='inside', textinfo='percent')

    fig.update_layout(
        showlegend=True,
        legend_title='Playlist',
        height=500,
        width=800
    )

    playlist_counts = [len([v for v in video_details.values() if v['Playlist_Name'] == playlist]) for playlist in top_playlists]
    playlist_counts.append(len([v for v in video_details.values() if v['Playlist_Name'] not in top_playlists]))
    fig.update_traces(hovertemplate='<b>%{label}</b><br>View Count: %{value}<br>Number of Videos: %{text}<extra></extra>',
                    text=playlist_counts)

    st.plotly_chart(fig, use_container_width = True)


# Viz-4


elif selected_viz == 'Bar Chart' and viz_button:
    
    st.subheader(f'Top 10 Videos by like counts in {selected_channel} channel')

    top_videos = sorted(video_details.keys(), key=lambda x: video_details[x]['Like_Count'], reverse=True)[:10]

    data = pd.DataFrame({'Video Name': [video_details[key]['Video_Name'] for key in top_videos],
                        'Like Count': [video_details[key]['Like_Count'] for key in top_videos]})

    axis_format = '~s'
    
    chart = alt.Chart(data).mark_bar(size=18).encode(
                                                x=alt.X(
                                                        "Like Count",
                                                        axis=alt.Axis(format=axis_format)
                                                        ),
                                                y=alt.Y(
                                                        "Video Name",
                                                        sort= '-x',
                                                        title=None
                                                        ),
                                                tooltip=[
                                                         'Video Name', 'Like Count'
                                                         ]
                                                ).properties(width=600,height=400).configure_axis(grid=False)

    st.altair_chart(chart, use_container_width=True)
 

# Viz-5


elif selected_viz == 'Histogram' and viz_button:
    
    st.subheader(f'Video Duration Histogram of {selected_channel} channel')
    
    durations = [video_details[key]['Duration'] for key in video_details]
    durations_min = [int(duration.split(':')[1]) + int(duration.split(':')[2])/60 for duration in durations]

    max_duration = math.ceil(max(durations_min))
    num_bins = min(max_duration, 10)

    bins = [i * max_duration / num_bins for i in range(num_bins + 1)]
    bin_labels = [f"{bins[i]:.0f}-{bins[i+1]:.0f}" for i in range(len(bins)-1)]
    bin_labels[-1] = f"{bins[-2]:.0f}+"

    fig_hist = go.Figure(data=[go.Histogram(x=durations_min, xbins=dict(start=bins[0], end=bins[-1], size=(bins[-1]-bins[0])/num_bins))])
    fig_hist.update_layout(
        xaxis_title='Duration (in minutes)',
        yaxis_title='Number of Videos',
        showlegend=False,
        height=500,
        width=800
    )

    fig_hist.update_traces(hovertemplate='Duration: %{x:.0f} minutes<br>Count: %{y}')
    fig_hist.update_xaxes(ticktext=bin_labels, tickvals=bins[:-1])


    st.plotly_chart(fig_hist, use_container_width = True)

# Miscellaneous
    
with side_bar:
    add_vertical_space(1)
    button('nirmal.datageek', emoji='🕮', text = 'Buy me a book', floating = False)
