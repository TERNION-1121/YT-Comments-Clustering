from API_KEY import API_KEY

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from json import dump

def get_video_comments(videoID: str, max_results: int = 20):
        assert isinstance(videoID, str), f"videoID should be a string, received {videoID.__class__.__name__}"
        assert isinstance(max_results, int) and 1 <= max_results <= 100, \
            f"max_results should be an unsigned integer in range [1, 100] inclusive, received {max_results} of type {max_results.__class__.__name__}"
        
        youtube = build(
                'youtube', 
                'v3', 
                developerKey=API_KEY
                )
        
        comments = set() 

        try:
            # initial request    
            comments_response = youtube.commentThreads().list(
                                    part='snippet',
                                    videoId=videoID,
                                    textFormat='plainText',
                                    maxResults=max_results,
                                    ).execute()
                                    
            # extract comment snippets
            for comment in comments_response['items']:
                snippet = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.add(snippet)

            # check for additional pages
            while 'nextPageToken' in comments_response:
                next_page_token = comments_response['nextPageToken']
                # make request
                comments_response = youtube.commentThreads().list(
                                        part='snippet',
                                        videoId=videoID,
                                        textFormat='plainText',
                                        maxResults=max_results,
                                        pageToken=next_page_token
                                    ).execute()
                # extract comment snippets
                for comment in comments_response['items']:
                    snippet = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments.add(snippet)

        except HttpError as e:
            print(f"An error occurred: {e}")
            
        return tuple(comments)

def save_to_json(data, filename='comments.json'):
    with open(filename, 'w', encoding='utf-8') as json_file:
        dump(data, json_file, ensure_ascii=False, indent=4)

def main():
    VIDEO_ID = 'sW9npZVpiMI'
    MAX_RESULTS = 100

    comments = get_video_comments(VIDEO_ID, MAX_RESULTS)
    save_to_json(comments, filename='data/comments_4.json')


if __name__ == '__main__':
    main()