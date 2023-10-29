# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import io
import json
import pathlib

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


from youtube_transcript_api import YouTubeTranscriptApi


scopes = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtubepartner"
        ]

# If modifying these scopes, delete the file token.json.
# scopes = ['https://www.googleapis.com/auth/admin.directory.user']

def get_credentials():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    client_secrets_file = "credentials_desktop_app.json"   
    client_authorized_file = "token.json"
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(client_authorized_file, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def build_youtube_service(creds):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, credentials=creds)

    try:
        if(test_youtube_service(youtube)):
            return youtube
        else:
            raise ValueError("Invalid Youtube service")
    except ValueError as e:
        print(e)


def test_youtube_service(service):
    # Call the Admin SDK Directory API
    print('Getting the first 10 users in the domain')
    # results = service.users().list(customer='my_customer', maxResults=10,
    #                                orderBy='email').execute()
    # users = results.get('users', [])

    # if not users:
    #     print('No users in the domain.')
    # else:
    #     print('Users:')
    #     for user in users:
    #         print(u'{0} ({1})'.format(user['primaryEmail'],
    #                                   user['name']['fullName']))
    return True

def json_parsed_response(response):
    s1 = json.dumps(response)
    parsed_response = json.loads(s1)
    return parsed_response

def get_videos_list(youtube, interviews_playlist_id, maxResults=10):

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=maxResults,
        playlistId=interviews_playlist_id
    )
    
    response = request.execute()
    response_parsed = json_parsed_response(response)

    # print(response_parsed["items"][0]["contentDetails"]["videoId"])
    # print(response_parsed["items"][0]["snippet"]["title"])
    # print(response_parsed["items"][0]["snippet"]["resourceId"]["videoId"])

    return response_parsed
    # return json_parsed_response(response)

def get_captions_list(youtube, video_list):
    captions = []
    n_downloads = 0
    try:
        for video in video_list["items"]:

            # if n_downloads >= 10:
            #     break

            # video_id = video["contentDetails"]["videoId"]
            video_id = video["snippet"]["resourceId"]["videoId"]
            video_title = video['snippet']['title']
            print(f"In captions {video_title}")
            # print(f"In captions {video_id}")

            # if "Private" not in video_title:
            #     request = youtube.captions().list(
            #                                     part="id",
            #                                     videoId=video_id
            #                                     )
            #     response = request.execute()
            #     response_parsed = json_parsed_response(response)
            #     captions.append(response_parsed)
            
            # srt = YouTubeTranscriptApi.get_transcript(video_id)
 
            # creating or overwriting a file "subtitles.txt" with 
            # the info inside the context manager
            # make a directory to download videos into
            # destination_folder = "./captions"
            # pathlib.Path(destination_folder).mkdir(parents=True, exist_ok=True)
            # d_file = destination_folder +"subtitles_" + video_title + ".txt"

            # with open(d_file, "w") as f:
            
            #         # iterating through each element of list srt
            #     for i in srt:
            #         # writing each element of srt on a new line
            #         f.write("{}\n".format(i))
            # captions.append(d_file)

            # Get the captions
            try:
                captions = YouTubeTranscriptApi.get_transcript(video_id)
                # Save the captions to a file
                with open(f"{video_title}.txt", "w", encoding="utf-8") as file:
                    for caption in captions:
                        file.write(caption["text"] + "\n")
                print(f"Captions saved for {video_title}")
            except Exception as e:
                print(f"Error fetching captions for {video_title}: {str(e)}")
            
            # n_downloads =  n_downloads + 1
    except ValueError:
        print(f"error download captions for {video_id}")
                
    # captions_d = dict(captions)
    # print(captions)
    return captions


def download_caption_id(youtube, captions_list):
    # make a directory to download videos into
    destination_folder = "./captions"
    pathlib.Path(destination_folder).mkdir(parents=True, exist_ok=True)
    # download captions
    try:
        for caption in captions_list:
            print(caption["items"][0]["id"])
            request = youtube.captions().download(
                            id=caption["items"][0]["id"]
            )
            # TODO: For this request to work, you must replace "YOUR_FILE"
            #       with the location where the downloaded content should be written.
            d_file = destination_folder + caption["items"][0]["id"] + "_ai.txt"
            fh = io.FileIO(d_file, "wb")

            download = MediaIoBaseDownload(fh, request)
            complete = False
            while not complete:
                status, complete = download.next_chunk()

    except KeyError:
            print(f"error download captions for {caption}")
    else:
            print(f"successfully download captions for {caption}")



def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.x
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    credentials = get_credentials()

    youtube = build_youtube_service(credentials)
    
    # Channel: 60 min youTube channel
    # Playlist: "Interviews"
    # URL: "https://www.youtube.com/playlist?list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL"
    # ID: "PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL"
    interviews_playlist = "PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL"
    num_videos = 10
    video_list = get_videos_list(youtube, interviews_playlist, num_videos)
    captions_list = get_captions_list(youtube, video_list)

    # print(captions_list)

    # download_caption_id(youtube, captions_list)

if __name__ == "__main__":
    main()