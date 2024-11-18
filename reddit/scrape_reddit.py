import requests
import csv
import time
from datetime import datetime
import json

class RedditScraper:
    def __init__(self, access_token):
        self.headers = {
            'Authorization': f'bearer {access_token}',
            'User-Agent': 'travel-explorer by Immediate-Ship9951'
        }
        self.base_url = 'https://oauth.reddit.com'
    
    def get_posts(self, subreddit, sort_type='top', time_filter='all', max_posts=None):
        posts = []
        after = None
        
        while True:
            params = {
                'limit': 100,
                't': time_filter,
                'after': after
            }
            
            url = f'{self.base_url}/r/{subreddit}/{sort_type}'
            
            try:
                time.sleep(2)  # Respect rate limits
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                new_posts = data['data']['children']
                if not new_posts:
                    break
                    
                posts.extend(new_posts)
                print(f"Collected {len(posts)} posts...")
                
                if max_posts and len(posts) >= max_posts:
                    posts = posts[:max_posts]
                    break
                
                after = data['data'].get('after')
                if not after:
                    break
                    
            except Exception as e:
                print(f"Error fetching posts: {e}")
                break
                
        return posts
    
    def get_comments(self, subreddit, post_id, limit=None):
        url = f'{self.base_url}/r/{subreddit}/comments/{post_id}'
        params = {'limit': limit} if limit else {}
        
        try:
            time.sleep(1)  # Respect rate limits
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()[1]['data']['children']  # [1] contains comments
        except Exception as e:
            print(f"Error fetching comments for post {post_id}: {e}")
            return []

    def scrape_subreddit(self, subreddit, include_comments=True, max_posts=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        posts_file = f'{subreddit}_posts_{timestamp}.csv'
        comments_file = f'{subreddit}_comments_{timestamp}.csv'
        
        # Get posts from different sort types and time periods
        all_posts = []
        
        # Get posts from different sort types
        sort_types = ['top', 'hot', 'new']
        time_filters = ['all', 'year', 'month', 'week']
        
        for sort_type in sort_types:
            if sort_type == 'top':
                for time_filter in time_filters:
                    print(f"Fetching {sort_type} posts from {time_filter}...")
                    posts = self.get_posts(subreddit, sort_type, time_filter, max_posts)
                    all_posts.extend(posts)
            else:
                print(f"Fetching {sort_type} posts...")
                posts = self.get_posts(subreddit, sort_type, max_posts=max_posts)
                all_posts.extend(posts)
        
        # Remove duplicates based on post ID
        seen_posts = set()
        unique_posts = []
        for post in all_posts:
            if post['data']['id'] not in seen_posts:
                seen_posts.add(post['data']['id'])
                unique_posts.append(post)
        
        print(f"Found {len(unique_posts)} unique posts")
        
        # Save posts
        with open(posts_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Post ID', 'Title', 'URL', 'Score', 'Body Text', 
                           'Comments Count', 'Created UTC', 'Author', 'Upvote Ratio'])
            
            for post in unique_posts:
                post_data = post['data']
                writer.writerow([
                    post_data['id'],
                    post_data['title'],
                    post_data['url'],
                    post_data['score'],
                    post_data['selftext'],
                    post_data['num_comments'],
                    datetime.fromtimestamp(post_data['created_utc']).strftime('%Y-%m-%d %H:%M:%S'),
                    post_data['author'],
                    post_data['upvote_ratio']
                ])
        
        # Save comments if requested
        if include_comments:
            with open(comments_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Post ID', 'Comment ID', 'Parent ID', 'Author', 
                               'Body', 'Score', 'Created UTC', 'Depth'])
                
                for post in unique_posts:
                    post_id = post['data']['id']
                    print(f"Fetching comments for post {post_id}...")
                    comments = self.get_comments(subreddit, post_id)
                    self._process_comments(comments, writer, post_id)
        
        return posts_file, comments_file if include_comments else None
    
    def _process_comments(self, comments, writer, post_id, parent_id=None, depth=0):
        for comment in comments:
            if 'data' not in comment:
                continue
                
            comment_data = comment['data']
            
            # Skip deleted/removed comments
            if 'body' not in comment_data:
                continue
                
            writer.writerow([
                post_id,
                comment_data['id'],
                parent_id or '',
                comment_data['author'],
                comment_data['body'],
                comment_data['score'],
                datetime.fromtimestamp(comment_data['created_utc']).strftime('%Y-%m-%d %H:%M:%S'),
                depth
            ])
            
            # Process replies recursively
            if 'replies' in comment_data and comment_data['replies']:
                if isinstance(comment_data['replies'], dict):
                    self._process_comments(
                        comment_data['replies']['data']['children'],
                        writer,
                        post_id,
                        comment_data['id'],
                        depth + 1
                    )

# Usage example
if __name__ == "__main__":
    ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJsb2lkIiwiZXhwIjoxNzMxOTczNDMxLjY2MzA4NiwiaWF0IjoxNzMxODg3MDMxLjY2MzA4NiwianRpIjoiNnVMNDRiRE9qUmg4UXJwSVAtb1pLWmxCdEdlczJ3IiwiY2lkIjoiVWw2OVlUYkVCVjRWUndjQm9handyUSIsImxpZCI6InQyXzFkNnQ3NjVmcWkiLCJsY2EiOjE3MzE4ODcwMzE2NDgsInNjcCI6ImVKeUtWdEpTaWdVRUFBRF9fd056QVNjIiwiZmxvIjo2fQ.MeJ2SaRoLADLJlv3lkiQhHufGkii8IOozGPuE6dz_yTwfcoyT1jttvmkSIQHn4Sm-TkEzCSZuV8GAc4EeGiZ2T6MXKAGhKEz2yyto9uISNDLA-KfVrYFBsEnR8RxWigpINe1xA4mjQIasXCw27MMRuonRaaelnueNvWgjtti7QDi822R4yMd8y4KtXdXe6lypfLw5oTvgxgO7sHt6bz-ZrKO4yqIzBtmIGhfoMCsOgHAhtgddAHZVk_6YD9Y6KDYxUI66IxJwNkMtd4CFhxqr174r25WVbg_kK_ZEzw1VKCi1mkDTrWtgR8SiW1KYXJscMNtl8qP0pqWWN8P7Cpaag"
    SUBREDDIT = "travel_porn"
    
    scraper = RedditScraper(ACCESS_TOKEN)
    posts_file, comments_file = scraper.scrape_subreddit(
        SUBREDDIT,
        include_comments=True,
        max_posts=None  # Set to None to get as many posts as possible
    )
    
    print(f"Posts saved to: {posts_file}")
    if comments_file:
        print(f"Comments saved to: {comments_file}")

