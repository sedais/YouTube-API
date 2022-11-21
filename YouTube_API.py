# Import libraries
import requests
import pandas as pd
import time

# Keys
API_KEY = "AIzaSyD5_DJ3nv9CySefqkEZH3jVEzzzewuwKbw"
#CHANNEL_ID = "UCWN2FPlvg9r-LnUyepH9IaQ"
CHANNEL_ID = "UCQAHhPvAPfOtxWI6g7QJNUA"

def get_video_details(video_id):
        print("Video id here " + video_id)
        #make API call for statistics
        url_video_stats = "https://www.googleapis.com/youtube/v3/videos?key=" + API_KEY + "&part=statistics&id=" + video_id
        response_video_stats = requests.get(url_video_stats).json()
        view_count = response_video_stats['items'][0]['statistics']['viewCount']
        like_count = response_video_stats['items'][0]['statistics']['likeCount']
        favorite_count = response_video_stats['items'][0]['statistics']['favoriteCount']
        comment_count = 0

        if "commentCount" in response_video_stats['items'][0]['statistics']:
            print("The required key is present")
            comment_count = response_video_stats['items'][0]['statistics']['commentCount']
        else:
            print("The required key is absent")
        return view_count, like_count, favorite_count, comment_count

def make_search_api_call(url):
    response = requests.get(url).json()
    nextPageToken = response['nextPageToken']
    return response, nextPageToken 

def get_details_of_items(df, response):
    for video in response['items']:
            if(video['id']['kind'] == "youtube#video"):
                video_id = video['id']['videoId']
                video_title= video['snippet']['title']
                upload_date = video['snippet']['publishedAt']
                upload_day = str(upload_date).split("T")[0]
                upload_time = str(upload_date).split("T")[1]

                # Get video statistics
                view_count, like_count, favorite_count, comment_count = get_video_details(video_id)

                # Create the new row as its own dataframe        
                new_row = pd.DataFrame({
                    "video_id": video_id,
                    "video_title": video_title,
                    "upload_day": upload_day,
                    "upload_time": upload_time,
                    "view_count": view_count,
                    "like_count": like_count,
                    "favorite_count": favorite_count,
                    "comment_count": comment_count
                }, index=[0])
                #i+=1
                df = pd.concat([df, new_row], axis=0, ignore_index=True)
                #print(i)
    return df

def get_videos(df):
    # Make YouTube search API call
    # The max results you can get with 1 call is 50
    pageToken = ""
    url = "https://www.googleapis.com/youtube/v3/search?key=" + API_KEY + "&channelId=" + CHANNEL_ID + "&part=snippet,id&order=date&maxResults=50"+ "&pageToken=" +pageToken
    response = requests.get(url).json()
    nextPageToken = response['nextPageToken']
    
    while len(nextPageToken) != 0:
        time.sleep(3)
        print("I'm here")
        print(nextPageToken)
        df = get_details_of_items(df, response)
        url = "https://www.googleapis.com/youtube/v3/search?key=" + API_KEY + "&channelId=" + CHANNEL_ID + "&part=snippet,id&order=date&maxResults=50"+ "&pageToken=" +nextPageToken
        response = requests.get(url).json()
        if "nextPageToken" in response:
            nextPageToken = response['nextPageToken']
        else:
            nextPageToken = ""
    return df

def api_call():
    url = "https://www.googleapis.com/youtube/v3/search?key=" + API_KEY + "&channelId=" + CHANNEL_ID + "&part=snippet,id&order=date&maxResults=10000"
    response = requests.get(url).json()
    print(response)

def df_test():

    df = pd.DataFrame(columns= ["a", "b", "c"])
    for x in range(100):
        new_row = pd.DataFrame({
            "a": 1,
            "b": 2,
            "c": 3
        }, index=[0])
        df = pd.concat([df, new_row], axis=0, ignore_index=True)
    print(df)  

# Main method
if __name__ == '__main__':

    #df_test()
    #api_call()
    #build the pandas dataframe
    cols = ["video_id", "video_title", "upload_day", "upload_time", "view_count", "like_count", "favorite_count", "comment_count"]
    df = pd.DataFrame(columns= cols)
    print(df.head())
    df = get_videos(df)
    print(df)
    print(len(df))

