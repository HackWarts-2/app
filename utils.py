from apify_client import ApifyClient
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

apify_api_key = os.getenv('APIFY_TOKEN')
ai71_api_key = os.getenv('AI71_TOKEN')
google_api_key = os.getenv('GOOGLE_TOKEN')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

def userData(username):
  # Initialize the ApifyClient with your API token
  client = ApifyClient(apify_api_key)

  # Prepare the Actor input
  run_input = { "usernames": [username] }

  # Run the Actor and wait for it to finish
  run = client.actor("dSCLg0C3YEZ83HzYX").call(run_input=run_input)

  data = {}

  # Fetch and print Actor results from the run's dataset (if there are any)
  for item in client.dataset(run["defaultDatasetId"]).iterate_items():
      data.update(item)
      #print(item)

    # Function to extract relevant post information
  def extract_post_info(post):
      return {
          'type': post.get('type'),
          'caption': post.get('caption'),
          'hashtags': post.get('hashtags'),
          'mentions': post.get('mentions'),
          'url': post.get('url'),
          'commentsCount': post.get('commentsCount'),
          'displayUrl': post.get('displayUrl'),
          'images': post.get('images'),
          'videoUrl': post.get('videoUrl'),
          'alt': post.get('alt'),
          'likesCount': post.get('likesCount'),
          'videoViewCount': post.get('videoViewCount'),
          'timestamp': post.get('timestamp'),
          'latestComments': post.get('latestComments', []),
          'taggedUsers': [
              {
                  'full_name': tagged_user.get('full_name'),
                  'is_verified': tagged_user.get('is_verified'),
                  'profile_pic_url': tagged_user.get('profile_pic_url'),
                  'username': tagged_user.get('username'),
              }
              for tagged_user in post.get('taggedUsers', [])
          ],
          'ownerUsername': post.get('ownerUsername'),
          'productType': post.get('productType'),
      }

  # Extracting the required user information
  user_data = {
      'username': data.get('username'),
      'url': data.get('url'),
      'fullName': data.get('fullName'),
      'biography': data.get('biography'),
      'externalUrl': data.get('externalUrl'),
      'followersCount': data.get('followersCount'),
      'followsCount': data.get('followsCount'),
      'hasChannel': data.get('hasChannel'),
      'highlightReelCount': data.get('highlightReelCount'),
      'isBusinessAccount': data.get('isBusinessAccount'),
      'joinedRecently': data.get('joinedRecently'),
      'businessCategoryName': data.get('businessCategoryName'),
      'private': data.get('private'),
      'verified': data.get('verified'),
      'profilePicUrl': data.get('profilePicUrl'),
      'profilePicUrlHD': data.get('profilePicUrlHD'),
      'igtvVideoCount': data.get('igtvVideoCount'),
      'relatedProfiles': [
        {
            'id': profile.get('id'),
            'full_name': profile.get('full_name'),
            'is_private': profile.get('is_private'),
            'is_verified': profile.get('is_verified'),
            'profile_pic_url': profile.get('profile_pic_url'),
            'username': profile.get('username'),
        }
        for profile in data.get('relatedProfiles', []) if profile
          ] if data.get('relatedProfiles') else [],
      'latestIgtvVideos': data.get('latestIgtvVideos', []),
      'postsCount': data.get('postsCount'),
      'latestPosts': [extract_post_info(post) for post in data.get('latestPosts', [])],
  }

  # Output the extracted data
  #print(user_data)

  # Extracting required information
  user_info = f"""
    Username: {user_data['username']}
    Biography: {user_data['biography']}
    Followers Count: {user_data['followersCount']}
    Reels Count: {user_data['highlightReelCount']}
    Business Account? {user_data['isBusinessAccount']}
    Business Category Name: {user_data.get('businessCategoryName', 'N/A')}
    Related Profiles: {', '.join([profile['username'] for profile in user_data['relatedProfiles'][:5]])}
    Posts Count: {user_data['postsCount']}
    \nData for my last 5 posts:
    """

  # Extracting information from latestPosts
  for post in user_data['latestPosts'][-5:]:
      post_info = f"""
      Type: {post['type']}
      Caption: {post['caption']}
      Likes Count: {post['likesCount']}
      Comments Count: {post['commentsCount']}
      Video View Count: {post.get('videoViewCount', 'N/A')}
      """
      user_info += post_info
  
  # Calculate the length of user_info
  user_info_length = len(user_info)
  #print(f"Length of user_info: {user_info_length} characters")

  # Truncate if it's more than 3500 characters
  if user_info_length > 3500:
      user_info = user_info[:3500]
      print("user_info was truncated to 3500 characters.")

  #print(user_info)

      # Define the API endpoint
  url = "https://api.ai71.ai/v1/chat/completions"
  prompt = f"Instagram user data to analyze: {user_info}"

  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {ai71_api_key}",
  }
  payload = {
      "model": "tiiuae/falcon-180B-chat",
      "messages": [
          {"role": "system", "content": "Given the following Instagram account information and details about the user's last few posts, provide a summary and analysis of the account. The summary should include insights into the user's content focus, engagement levels, audience appeal, and any noticeable trends or patterns in their posts. Additionally, offer any observations about the style, themes, or branding present in their content. Answer using no more than 50 words."},
          {"role": "user", "content": prompt},
      ],
      "stream": False,
      "max_tokens": 300,
  }

  # Make the POST request
  response = requests.post(url, headers=headers, data=json.dumps(payload))

  # Check if the request was successful
  if response.status_code == 200:
      print("Success:")
      print(response.json())
      response_json = response.json()
      return response_json['choices'][0]['message']['content']
  else:
      print(f"Failed with status code {response.status_code}: {response.text}")

    
def getInsightsForProfile(user_data, profile_url):

    def getPosts(url):
        try:
            # Initialize the ApifyClient with API token
            client = ApifyClient(apify_api_key)

            # Prepare the Actor input
            run_input = {
                "addParentData": False,
                "directUrls": [url],
                "enhanceUserSearchWithFacebookPage": True,
                "isUserReelFeedURL": True,
                "isUserTaggedFeedURL": False,
                "resultsLimit": 5,
                "resultsType": "posts",
            }

            posts = []

            # Run the Actor and wait for it to finish
            run = client.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)

            # Fetch and process Actor results
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                posts.append(item)

            def extractPostData(original_dict):
                # Extract necessary information from the original dictionary
                extracted_info = {
                    'type': original_dict.get('type'),
                    'timestamp': original_dict.get('timestamp'),
                    'caption': original_dict.get('caption'),
                    'hashtags': original_dict.get('hashtags'),
                    'mentions': original_dict.get('mentions'),
                    'url': original_dict.get('url'),
                    'videoUrl': original_dict.get('videoUrl') if original_dict.get('type') == 'Video' else None,
                    'displayUrl': original_dict.get('displayUrl'),
                    'commentsCount': original_dict.get('commentsCount'),
                    'likesCount': original_dict.get('likesCount'),
                    'videoViewCount': original_dict.get('videoViewCount') if original_dict.get('type') == 'Video' else None,
                    'videoPlayCount': original_dict.get('videoPlayCount') if original_dict.get('type') == 'Video' else None,
                    'ownerUsername': original_dict.get('ownerUsername'),
                    'taggedUsers': ' '.join(['@' + user['username'] for user in original_dict.get('taggedUsers', [])]),
                    'latestComments': '\n'.join([comment['text'] for comment in original_dict.get('latestComments', [])])
                }

                # Create result string
                result_string = f"""type: {extracted_info['type']}
                timestamp: {extracted_info['timestamp']}
                caption: {extracted_info['caption']}
                hashtags: {' '.join(['#' + tag for tag in extracted_info['hashtags'] or []])}
                mentions: {' '.join(['@' + mention for mention in extracted_info['mentions'] or []])}
                commentsCount: {extracted_info['commentsCount']}
                likesCount: {extracted_info['likesCount']}
                videoViewCount: {extracted_info['videoViewCount']}
                videoPlayCount: {extracted_info['videoPlayCount']}
                ownerUsername: {extracted_info['ownerUsername']}
                taggedUsers: {extracted_info['taggedUsers']}
                latestComments: {extracted_info['latestComments']}
                """

                post_url = original_dict.get('url')  # Extract the post's URL
                return result_string, post_url

            extractedPosts = {}
            for post in posts:
                extractedPost, postUrl = extractPostData(post)
                extractedPosts[postUrl] = extractedPost

            return extractedPosts

        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return {}

    def generateInsights(user_data, user_posts):
        insights = {}

        # Define the API endpoint
        url = "https://api.ai71.ai/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ai71_api_key}",
        }

        for post_url, post_data in user_posts.items():
            # Define the prompt
            prompt = f"My account info:\n {user_data} \n Instagram post data to analyze:\n {post_data}"
            #print("Prompt for ", post_url, "\n", prompt)

            # API payload
            payload = {
                "model": "tiiuae/falcon-180B-chat",
                "messages": [
                    {"role": "system", "content": "You are an expert in social media analytics and growth. Given the information about an Instagram post and my own profile information, generate insights to help me understand why the post became popular and how I can improve my own account. Analyze the provided data and provide actionable recommendations on content strategy, engagement tactics, and audience interaction. Answer using no more than 50 words."},
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
                "max_tokens": 150,
            }

            # Make the POST request
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            # Process the response
            if response.status_code == 200:
                response_json = response.json()
                insight = response_json['choices'][0]['message']['content']
                insights[post_url] = insight
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
                insights[post_url] = "Failed to generate insight."

        return insights

    # Main function logic
    user_posts = getPosts(profile_url)
    if not user_posts:
        return {}

    insights = generateInsights(user_data, user_posts)
    return insights


def scrape_instagram_similar_profiles(query):

  def getSimilarProfiles(query):
      searchQuery = query
      url = "https://www.googleapis.com/customsearch/v1"
      params  = {
          "q": searchQuery,
          "key": google_api_key,
          "cx": search_engine_id,
          "num": 5
      }

      response = requests.get(url, params=params)
      results = response.json()
      links_array = [item['link'] for item in results['items']]
     
      return links_array # Added return statement to make links_array available outside the function

  apify_client = ApifyClient(apify_api_key)
  links_array = getSimilarProfiles(query) # Call getSimilarProfiles to get the links
  
  run_input = { # Indent this block one level further
    "addParentData": False,
    "directUrls":links_array,
    "enhanceUserSearchWithFacebookPage": False,
    "isUserReelFeedURL": False,
    "isUserTaggedFeedURL": False,
    "resultsType": "details",
    "resultsLimit": 1

  }

  actor_run = apify_client.actor('apify/instagram-scraper').call(run_input=run_input)

  data = []
  for item in apify_client.dataset(actor_run["defaultDatasetId"]).iterate_items():
      data.append({
          "inputUrl": item.get("inputUrl",'N/A'),
          "username": item.get("username",'N/A'),
          "followersCount": item.get("followersCount",0),
          "followsCount": item.get("followsCount",0),
          "postsCount": item.get("postsCount",0),
          "externalUrl": item.get("externalUrl",'N/A'),
          "biography": item.get("biography",'N/A'),
          "profilePicUrl": item.get("profilePicUrl",'N/A'),
          "highlightReelCount": item.get("highlightReelCount",0),
          "businessCategoryName": item.get("businessCategoryName",'N/A')
      })

  data_sorted = sorted(data, key=lambda x: x['followersCount'], reverse=True)
  #print(json.dumps(data_sorted))
  return json.dumps(data_sorted)    