from argparse import ArgumentParser

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
                like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']
                snippet = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.add((like_count, snippet))

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
                # extract top level comment snippets (reply comments not included)
                for comment in comments_response['items']:
                    like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']
                    snippet = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments.add((like_count, snippet))

        except HttpError as e:
            print(f"An error occurred: {e}")
            
        comments_dict = {   str(index): {"like_count": like_count, "comment": comment} 
                            for index, (like_count, comment) in enumerate(comments)     }
        return comments_dict

def save_to_json(data, filename='comments.json'):
    with open(filename, 'w', encoding='utf-8') as json_file:
        dump(data, json_file, ensure_ascii=False, indent=4)

def main():
    parser = ArgumentParser(description="Command Line Utility to extract and save YouTube comments of a specified video to a json file")
    parser.add_argument('video_id', metavar='VIDEO_ID', type=str, help='a YouTube video\'s ID')
    parser.add_argument('json_path', metavar='JSON_PATH', type=str, help='relative path of json file to save the data')

    args = parser.parse_args()

    comments = get_video_comments(args.video_id, 100)
    save_to_json(comments, filename=args.json_path)

    print("\nComments Data saved successfully.\n")


if __name__ == '__main__':
    main()