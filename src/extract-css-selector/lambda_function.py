import requests
import json
import os

def lambda_handler(event, context):
    google_api_key = os.environ.get('GOOGLE_API_KEY')

    cleaned_html_with_bs4 = event.get('body', '')
    url = event.get('url')

    response = requests.post(
        url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={google_api_key}",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": "extract the class name of pagination next page button of review section, author of review, text of review, and rating classname from this codebase. Just return a comma seperated value of classnames, if multiple class name is found for the same section, use the most relevant one which is unique. if not present then add 'null' at it's place. Don't return any other text than that. Here is the code: " + cleaned_html_with_bs4
                        }
                    ]
                }
            ]
        }
    )

    if response.status_code == 200:
        data = response.json()
        message_content = data['candidates'][0]['content']['parts'][0]['text']
        message_content = message_content.strip("\n")
        review_paginate_next, review_author, review_text, review_rating = message_content.split(",")  
        return {
            'statusCode': 200,
            'url': url,
            'reviewPaginateNext': review_paginate_next,
            'reviewAuthor': review_author,
            'reviewText': review_text,
            "reviewRating": review_rating
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': json.dumps({
                "error": response.text
            })
        }
