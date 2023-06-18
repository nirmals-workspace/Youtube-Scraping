# YouTube Data Harvesting and Warehousing
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://youtube-data-harvesting.streamlit.app/)

This web app is designed to fetch data from YouTube using their YouTube's Data API v3 based on user input for a channel username. The fetched data is stored in my personal MongoDB Atlas Database and provides facilities for users to migrate the channel data to their local MySQL database. The project also includes custom-made queries for basic data analysis and visualization using Streamlit.

## Prerequisites
Before you begin, you will need to have a few tools and libraries installed on your machine:
* Python 3.7 or higher
    [Note: Streamlit only supports .py files as of now. So, notebook(.ipynb) files are not recommended]
* Git software
* MySQL software
* MongoDB Atlas account
* The streamlit, google-api-client-python, pymongo, mysql-connector-python packages, pandas, plotly, altair, wordcloud and few other packages

#### Python
Python is a versatile programming language known for its simplicity and readability. In this project, Python is the core language used for developing the entire application, including data fetching, processing, analysis, and visualization.

#### MongoDB Atlas
MongoDB Atlas is a fully managed cloud database service for MongoDB. In this project, MongoDB Atlas is used to store the fetched data from YouTube's Data API v3. It provides a reliable and scalable database solution for efficient data storage and retrieval.

#### MySQL
MySQL is an open-source relational database management system. In this project, MySQL is used to store the migrated channel data from MongoDB Atlas. It offers a structured and efficient way to store and query data, ensuring data integrity and scalability.

#### Streamlit
Streamlit is a Python library used for building interactive web applications. In this project, Streamlit is utilized to create a user-friendly interface for users to interact with the fetched YouTube data, select channels, playlists, and visualize data using various charts and plots.

#### Pandas
Pandas is a popular Python library used for data manipulation and analysis. We used pandas to clean and preprocess the data, create new features, and perform data analysis. It provides a wide range of functions and methods for working with data.

#### Visualization libraries such as Plotly, Altair, Matplotlib
These visualization libraries in Python are used to create various charts, plots, and visualizations based on the fetched YouTube data. Plotly, Altair, and Matplotlib offer a wide range of options for visualizing data, making it easier to understand patterns, trends, and insights.

#### Wordcloud
Wordcloud is a Python library used to create visual representations of text data, where the size of each word is proportional to its frequency. In this project, the Wordcloud library is used to generate word clouds based on the tags or comments associated with the YouTube videos, providing a visual summary of the most commonly used terms.

#### Pymongo
pymongo is a Python library that provides tools for working with MongoDB databases. In this project, pymongo is used to establish a connection to the MongoDB Atlas database and perform operations such as inserting, updating, and querying data.

#### MySQL Connector
mysql.connector is a Python library used to connect and interact with MySQL databases. In this project, mysql.connector is used to establish a connection to the local MySQL database and execute SQL queries to migrate the channel data from MongoDB Atlas.

#### Google API Client
googleapiclient is a Python library that enables interaction with various Google APIs. In this project, googleapiclient is used to make requests to YouTube's Data API v3 and fetch the required data, such as channel details, video details, and comments. It provides a convenient interface to access YouTube's vast collection of data programmatically.

## Ethical Perspective of scraping youtube data
From an ethical standpoint, it is essential to approach the scraping of YouTube content with caution and responsibility. It is important to respect the terms and conditions set by YouTube, obtain proper authorization, and adhere to data protection regulations. The collected data should be used responsibly, ensuring privacy and confidentiality, and avoiding misuse or misrepresentation. Additionally, considering the potential impact on the platform and its community is crucial to ensure a fair and sustainable scraping process. By following these ethical guidelines, we can maintain integrity while harnessing YouTube data for valuable insights.

## Project Structure

### Fetching and Storing Data

The YouTube Data API v3 is utilized to retrieve channel details, video details, and comments. The fetched data is structured as follows:

    "_id": "UC7cs8q-gJRlGwj4A8OmCmXg",
      "Channel_Details": {
        "Channel_Id": "UC7cs8q-gJRlGwj4A8OmCmXg",
        "Channel_Name": "Alex The Analyst",
        "Uploads_Playlist_Id": "UU7cs8q-gJRlGwj4A8OmCmXg",
        "Subscription_Count": 478000,
        "Channel_Views": 3652,
        "Channel_Description": "My name is Alex Freberg and on this channel I will be going over everything you need to know to become a Data Analyst. If you are wanting to make a career change or learn the skills needed to become a Data Analyst, be sure to subscribe to stay up to date on all my latest content.\n\nYou can find me on LinkedIn at:\nhttps://www.linkedin.com/in/alex-freberg/\n\nAlexTheAnalyst.com\nhttps://www.alextheanalyst.com/\n\nDiscord Channel:\nhttps://discord.gg/rxZUjNvRzR\n\nTwitter:\n@Alex_TheAnalyst\n\nSend Me Something:\n431 Saint James Avenue Suite L #318, Goose Creek, SC, 29445\n",
        "Channel_Status": "public"
      },
      "Video_Details": {
        "Video_1": {
          "Playlist_Id": "PLUaB-1hjhk8GZOuylZqLz-Qt9RIdZZMBE",
          "Video_Id": "dUpyC40cF6Q",
          "Playlist_Name": "Pandas for Beginners",
          "Video_Name": "Reading in Files in Pandas | Python Pandas Tutorials",
          "Video_Description": "In this series we will be walking through everything you need to know to get started in Pandas! In this video, we learn about Reading in Files in Pandas.\n\nDatasets in GitHub: \nCSV -  https://bit.ly/3CH1h8E\nTXT - https://bit.ly/3RGqm7X\nJSON - https://bit.ly/3RMvJTk\nEXCEL - https://bit.ly/3ClvRmW\n\nCode in GitHub: https://github.com/AlexTheAnalyst/PandasYouTubeSeries/blob/main/Pandas%20101%20-%20Reading%20in%20Files.ipynb\n\nFavorite Pandas Course:\nData Analysis with Pandas and Python - https://bit.ly/3KHMLlu\n____________________________________________ \n\nSUBSCRIBE!\nDo you want to become a Data Analyst? That's what this channel is all about! My goal is to help you learn everything you need in order to start your career or even switch your career into Data Analytics. Be sure to subscribe to not miss out on any content!\n____________________________________________ \n\nRESOURCES:\n\nCoursera Courses:\n📖Google Data Analyst Certification: https://coursera.pxf.io/5bBd62\n📖Data Analysis with Python - https://coursera.pxf.io/BXY3Wy\n📖IBM Data Analysis Specialization - https://coursera.pxf.io/AoYOdR\n📖Tableau Data Visualization - https://coursera.pxf.io/MXYqaN\n\nUdemy Courses:\n📖Python for Data Analysis and Visualization- https://bit.ly/3hhX4LX\n📖Statistics for Data Science - https://bit.ly/37jqDbq\n📖SQL for Data Analysts (SSMS) - https://bit.ly/3fkqEij\n📖Tableau A-Z - http://bit.ly/385lYvN\n\n*Please note I may earn a small commission for any purchase through these links - Thanks for supporting the channel!*\n____________________________________________ \n\nBECOME A MEMBER - \n\nWant to support the channel? Consider becoming a member! I do Monthly Livestreams and you get some awesome Emoji's to use in chat and comments!\n\nhttps://www.youtube.com/channel/UC7cs8q-gJRlGwj4A8OmCmXg/join\n____________________________________________ \n\nWebsites: \n💻Website: AlexTheAnalyst.com\n💾GitHub: https://github.com/AlexTheAnalyst\n📱Instagram: @Alex_The_Analyst\n____________________________________________\n\n0:00 Intro\n0:58 Read in CSV File\n7:39 Read in Txt File\n8:53 Read in JSON File\n9:32 Read in Excel File \n11:30 Looking at Max Rows/Columns\n13:35 Looking at Data in DataFrame\n18:05 Outro\n\n*All opinions or statements in this video are my own and do not reflect the opinion of the company I work for or have ever worked for*",
          "Tags": [
            "Data Analyst",
            "Data Analyst job",
            "Data Analyst Career",
            "Data Analytics",
            "Alex The Analyst",
            "Pandas",
            "pandas python",
            "python pandas",
            "pandas tutorials",
            "pandas tutorial",
            "reading in files",
            "python read in files",
            "pandas read in file"
          ],
          "PublishedAt": "2023-02-28 12:30:18",
          "View_Count": 12544,
          "Like_Count": 352,
          "Dislike_Count": 0,
          "Favorite_Count": 0,
          "Comment_Count": 29,
          "Duration": "00:19:17",
          "Thumbnail": "https://i.ytimg.com/vi/dUpyC40cF6Q/default.jpg",
          "Caption_Status": "Not available",
          "Comments": {
            "Comment_1": {
              "Comment_Id": "UgxKaleBkd1lMGC7bBp4AaABAg",
              "Comment_Text": "Great videos MAN , one thing i struggled with was no module named panda , would have helped if you told us how to download the library  or maybe its because i am doing it in vs code : still great vidoes man u are G.O.A.T",
              "Comment_Author": "srijan rawat",
              "Comment_PublishedAt": "2023-05-20 10:43:15"
            },
            "Comment_2": {
              "Comment_Id": "Ugys9exSnZqaXTKmkQl4AaABAg",
              "Comment_Text": "You teach in the most simple way. Thank you for zooming the screen so one can see the text clearly.  God bless you.  Keep up the good work",
              "Comment_Author": "Kpeyi Alale",
              "Comment_PublishedAt": "2023-05-06 05:55:40"
            },
            "Comment_3": {
              "Comment_Id": "UgwVLiMpt2QvvYBR-4h4AaABAg",
              "Comment_Text": "getting error pd is not define",
              "Comment_Author": "Nitish Lakhanpal",
              "Comment_PublishedAt": "2023-04-12 14:58:31"
            }
          }
        }


The fetched data includes channel details, video details (including comments), and associated metadata.

### SQL Tables

The project involves creating and using the following SQL tables:

**Channels Table**

    Channels (
        channel_id VARCHAR(255) PRIMARY KEY,
        channel_name VARCHAR(255),
        subscription_count INT,
        channel_views INT,
        channel_description MEDIUMTEXT,
        channel_status VARCHAR(255)
    )

**Playlists Table**

    Playlists (
        channel_id VARCHAR(255),
        playlist_id VARCHAR(255),
        playlist_name VARCHAR(255),
        PRIMARY KEY (channel_id, playlist_id),
        FOREIGN KEY (channel_id) REFERENCES Channels(channel_id)
    )

**Videos Table**

    Videos (
        video_order VARCHAR(10),
        channel_id VARCHAR(255),
        playlist_id VARCHAR(255),
        video_id VARCHAR(255) PRIMARY KEY,
        video_name VARCHAR(255),
        video_description MEDIUMTEXT,
        published_at DATETIME,
        view_count INT,
        like_count INT,
        dislike_count INT,
        favorite_count INT,
        comment_count INT,
        duration VARCHAR(10),
        thumbnail MEDIUMTEXT,
        caption_status VARCHAR(50),
        FOREIGN KEY (channel_id) REFERENCES Channels(channel_id),
        FOREIGN KEY (channel_id, playlist_id) REFERENCES Playlists(channel_id, playlist_id)
    )

**Comments Table**

    Comments (
        channel_id VARCHAR(255),
        playlist_id VARCHAR(255),
        video_id VARCHAR(255),
        comment_id VARCHAR(255) PRIMARY KEY,
        comment_text LONGTEXT,
        comment_author VARCHAR(255),
        comment_published_at DATETIME,
        FOREIGN KEY (channel_id) REFERENCES Channels(channel_id),
        FOREIGN KEY (channel_id, playlist_id) REFERENCES Playlists(channel_id, playlist_id),
        FOREIGN KEY (video_id) REFERENCES Videos(video_id)
    )


These tables store the channel, playlist, video, and comment data, enabling efficient storage and retrieval.

## Features
* ##### YouTube Data Fetching: Utilizes YouTube's Data API v3 to fetch channel details, video details, and comments.
* ##### MongoDB Atlas Integration: Stores the fetched data in MongoDB Atlas for reliable and scalable data storage.
* ##### MySQL Migration: Allows users to migrate channel data from MongoDB Atlas to their local MySQL database.
* ##### Data Analysis with Pandas: Performs custom queries and provides basic analysis of the fetched data using Pandas.
* ##### Interactive User Interface: Offers a user-friendly interface using Streamlit for easy data selection and display.
* ##### Visualization Capabilities: Enables users to generate visualizations such as Animated Bubble Plot, Word Cloud, Donut Chart, Bar Chart, and Histogram.
* ##### Word Cloud Generation: Utilizes the Wordcloud library to generate visual representations of text data based on tags or comments associated with YouTube videos.

These features collectively allow users to fetch, store, analyze, and visualize YouTube data, providing insights and facilitating better understanding of channel information.

## User Guide
    1. Click on the badge provided at the top of this file and it will take you to the app in your web browser.
    2. Explore the different features and functionalities available on each section of the app.
    3. Utilize the user-friendly interface to provide inputs, such as channel name and visualization selection, and obtain insightful data analysis and visualizations.

## Developer Guide:
To run the app, follow these steps:

    1. Clone the repository to your local machine using the command: `git clone [https://github.com/Nirmal-Data-Scientist/Youtube_Data_Harvesting.git]`.
    2. Install the required libraries by running: `pip install -r requirements.txt`.
    3. Set up a MongoDB Atlas account and obtain the connection details.
    4. Create a MySQL database and define the necessary tables using the provided SQL statements.
    5. Configure the app by providing your MongoDB Atlas and MySQL connection details in the appropriate sections of the code.
    6. Open a terminal and navigate to the directory where the app is located.
    7. Run the Streamlit app using the command: `streamlit run app.py`.
    8. Access the app through the provided local URL in your web browser.
    9. Explore the different sections of the app, customize queries, and interact with the visualizations to gain insights from the YouTube data.

To modify the app, you can:

    1. Add new visualizations or analysis functions to provide additional insights into the YouTube data.
    2. Extend the app's functionality to support more advanced querying options or filtering criteria.
    3. Incorporate additional data sources or APIs to enhance the data fetching capabilities.
    4. Customize the user interface by modifying the existing components or adding new ones to match your specific requirements.
    5. Implement additional database integrations, such as PostgreSQL or SQLite, to provide more options for data storage and retrieval.
    6. Optimize the code by improving query efficiency or implementing caching mechanisms to enhance performance.
    7. Implement user authentication and authorization features to ensure secure access to the app and data.
 
## Potential Applications
1. **Content Creator Analysis**: Gain insights into a specific YouTube channel's performance, including video views, likes, and comments, to assess audience engagement and optimize content creation strategies.

2. **Competitive Analysis**: Compare multiple YouTube channels to understand their subscriber counts, video trends, and audience demographics, helping businesses identify their competitors' strengths and weaknesses.

3. **Marketing and Advertising**: Use the app to gather data on popular video topics, keywords, and tags to inform marketing campaigns and target specific audience segments effectively.

4. **Influencer Research**: Analyze channel and video metrics to evaluate potential influencers' reach and engagement levels before partnering with them for promotional activities.

5. **Trend Identification**: Monitor popular video categories, view trends, and emerging content creators to identify new opportunities and stay ahead in the dynamic YouTube landscape.

6. **Performance Tracking**: Track the performance of specific playlists and videos over time, enabling content creators and marketers to measure the success of their strategies and make data-driven decisions.

7. **Audience Insights**: Analyze comments and engagement patterns to understand audience sentiment, preferences, and feedback, allowing for targeted content creation and audience interaction.

These applications demonstrate how the app can be utilized by content creators, marketers, businesses, and researchers to leverage YouTube data for strategic decision-making and audience engagement.

## Web App Snap
![Screenshot (8)](https://github.com/Nirmal-Data-Scientist/Youtube_Data_Harvesting/assets/123751119/f7446674-615b-49da-81d8-63e985b89eb2)

![Screenshot (9)](https://github.com/Nirmal-Data-Scientist/Youtube_Data_Harvesting/assets/123751119/7cf675e0-f475-4f5a-a250-8a25855ea03b)

![Screenshot (10)](https://github.com/Nirmal-Data-Scientist/Youtube_Data_Harvesting/assets/123751119/70ba2ac0-6293-44cc-9a05-d43f8e247103)

![Screenshot (11)](https://github.com/Nirmal-Data-Scientist/Youtube_Data_Harvesting/assets/123751119/c9b11860-c9a7-40a0-b8f6-3ecc8182be39)

## Web App Demo Video

<a href="https://www.linkedin.com/posts/nirmal-kumar-data-scientist_youtubedata-dataharvesting-datawarehousing-activity-7068697509958742016-5yi2?utm_source=share&utm_medium=member_desktop" target="_blank">Demo Video</a>

## Streamlit web URL

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://youtube-data-harvesting.streamlit.app/)

## Disclaimer
This application is intended for educational and research purposes only and should not be used for any commercial or unethical activities.

## Contact
If you have any questions, comments, or suggestions for the app, please feel free to contact me at [nirmal.works@outlook.com]
