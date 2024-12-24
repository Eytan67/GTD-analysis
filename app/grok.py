import requests
import json

# API key and endpoint
API_KEY = "xai-fKSWH7QYePJAo6EfNXQfhIbFwTYs4BOjiC37zu2ligEuqWDqtxamrUyfcXxMKzEvRReEi3vOj0VOT5iv"  # Replace with your Grok API key
API_URL = "https://api.x.ai/v1/chat/completions"

# Define the schema in Python as a dictionary
response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "news_classification",
        "schema": {
            "type": "object",
            "properties": {
                "classification": {
                    "type": "string",
                    "enum": [
                        "Current terrorism event",
                        "Past terrorism event",
                        "Other news event"
                    ]
                },
                "location": {
                    "type": "string",
                    "description": "The location where the event occurred"
                }
            },
            "required": ["classification", "location"],
            "additionalProperties": False
        },
        "strict": True
    }
}


# Function to send the request
def classify_news_article(article_content):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "messages": [
            {"role": "system",
             "content": "You are an assistant classifying news articles into categories and locations."},
            {"role": "user", "content": f"This is a news article: {article_content}"}
        ],
        "model": "grok-2-1212",
        "stream": False,
        "temperature": 0,
        "response_format": response_format
    }

    # Send the request
    response = requests.post(API_URL, headers=headers, json=payload)

    # Check for successful response
    if response.status_code == 200:
        try:
            response_json = response.json()
            return response_json
        except json.JSONDecodeError:
            print("Failed to decode JSON response")
            return None
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None


def extract_relevant_data(data):
    results = data.get("articles", {}).get("results", [])
    extracted = []
    for result in results:
        dt = result.get("dateTime")
        title = result.get("title")
        body = result.get("body", "")
        first_200_words = " ".join(body.split()[:200])
        extracted.append({"dt": dt, "title": title, "body_snippet": first_200_words})
    return extracted


artile_text1 = {
    "articles": {
        "page": 1,
        "pages": 2199,
        "totalResults": 2199,
        "results": [
            {
                "uri": "2024-12-583281968",
                "lang": "eng",
                "isDuplicate": False,
                "date": "2024-12-22",
                "time": "16:40:27",
                "dateTime": "2024-12-22T16:40:27Z",
                "dateTimePub": "2024-12-22T16:39:48Z",
                "dataType": "news",
                "sim": 0,
                "url": "https://www.infowars.com/posts/german-mother-mourns-loss-of-9-year-old-son-in-christmas-market-attack",
                "title": "German Mother Mourns Loss of 9-Year-Old Son in Christmas Market Attack",
                "body": "Germany continues to reel from a terror attack committed by Taleb A., a Saudi man who was granted German citizenship, after Taleb murdered five Germans and wounded over 200 on Friday night at the Magdeburg Christmas market. Now, the mother of the youngest victim, 9-year-old Andr\u00e9, has posted a heart-wrenching message on Facebook following the loss of her son.\n\n\"Andr\u00e9 didn't do anything to anyone -- why you, why?\" With these words, D\u00e9sir\u00e9e G. wrote her goodbyes to her son on Facebook. She also shared a photo of him.\n\n\"Let my little teddy bear fly around the world again,\" she begins her post. She wrote that Andr\u00e9 is now with his grandparents in heaven.\n\n\"They missed you very much, as much as we miss you here now.\" she added.\n\nTaleb A. drove a rented BMW into the crowd at full speed, killing five but also injuring another 200 people. There are still dozens fighting for their lives. So far, 41 people were seriously injured in the attack,\n\nOne woman, Anne, who was hit by the driver and knocked unconscious, told Bild newspaper: \"I woke up and thought I was in a dream.\" She still has a bloodshot eye from attack, however, her husband suffered a far worse injury to his thigh, saying that his flesh was \"literally ripped out.\" However, they were reunited when Anne regained consciousness when volunteers helped them find each other at the scene of the attack, and both expressed their happiness at being alive.\n\nNotably, German Christmas markets are already treated like fortresses, but Taleb A. found the only spot in the entire market that did not have a barrier, which was there to allow emergency vehicles and personnel to gain access to the market in the case of an emergency.\n\nThere is currently a debate raging about the man's motives, with a number on the right trying to claim Taleb A.is a secret Islamist. However, it appears from his own messages that he was furious that Germany was not granting asylum to Saudi refugees. He is on record threatening Germany and ethnic Germans with \"slaughter\" for not helping Saudi ex-Muslims.\n\nSome on the left are trying to tie him to the AfD, since he expressed support for the party in one of his posts. However, skeptics cite him saying he was a \"leftist\" in a video, that the AfD is strictly against mass immigration and granting asylum to those with a criminal record such as Taleb A., and that his multiple threats against Germans stands in complete contrast to the AfD's political platform, which seeks to block foreigners such as Taleb from entering the country entirely.\n\nRegardless of his motives, the man has a criminal history and had an open extradition request from Saudi Arabia -- yet he was still granted asylum and citizenship. In Germany, he faced a criminal complaint dating back to 2013 for threatening behavior. According to the Spiegel, Taleb A. had was found guilty in a district court in Rostock and sentenced to a fine of 90 daily rates on Sept. 4, 2013, for \"disturbing the public peace by threatening to commit criminal offenses\".\n\nIn addition, despite the German authorities at the BAMF being warned about his threatening statements against Germans by X users, no action was taken.\n\nIn short, it was a catastrophic failure in terms of migration and security policy from the German authorities. This failure has even caught the attention of Elon Musk, who shared a thread documenting the man's disturbing history in Germany and a lack of action from authorities.\n\nTaleb A. worked as a specialist in psychiatry and psychotherapy at a correctional facility in Bernberg. Shortly before the attack, he was on sick leave for several weeks.\n\nGermans have had their houses raided for calling Economic Minister Robert Habeck an \"idiot,\" and hundreds have faced prosecution for such insults. However, Taleb A. was saying just before the attack on X \"I assure you that revenge will 100 percent come soon. Even if it costs me my life.\"\n\nThere was no security response to his threats. In fact, police have been instead harassing grandmas at Christmas markets, a potential source of wasted resources that could have been put to work stopping an actual terror attack.\n\nTaleb A.is charged with five counts of murder and 205 counts of attempted murder. While Taleb A. is alive, Germans are mourning the deaths of their loved ones. Writing to her dead son Andr\u00e9, D\u00e9sir\u00e9e G. ends her farewell post by writing: \"You will always live on in our hearts. I promise you that.\"",
                "source": {
                    "uri": "infowars.com",
                    "dataType": "news",
                    "title": "Infowars"
                },
                "authors": [],
                "image": "https://imagedelivery.net/aeJ6ID7yrMczwy3WKNnwxg/3168c99d-690b-4b26-b635-721cf9089700/w=800,h=450",
                "eventUri": None,
                "sentiment": -0.1764705882352942,
                "wgt": 92912,
                "relevance": 18
            }
        ]
    }
}
artile_text2 =  {
 "uri": "8429097876",
 "lang": "eng",
 "isDuplicate": False,
 "date": "2024-11-26",
 "time": "05:50:27",
 "dateTime": "2024-11-26T05:50:27Z",
 "dateTimePub": "2024-11-26T05:49:25Z",
 "dataType": "news",
 "sim": 0,
 "url":
 "https://aninews.in/videos/national/2611-terror-attack-maha-cm-shinde-deputy-cms-fadnavis-ajit-pawar-pay-tribute-on-anniversary/",
 "title": "Asia's Leading News Site- India News, Business & Political, National & International, Bollywood, Sports | ANI News",
 "body": "Mumbai, Nov 26 (ANI): November 26, 2024 marked the 16th anniversary of the 26/11 Mumbai terror attack that shook the nation. Onthe occasion, Maharashtra Guv Radhakrishnan paid floral tributes to Bravehearts at Martyrs' Memorial on premises of Police Commissioner's Office. Maharashtra CM Eknath Shinde also paid tribute to the Bravehearts at the Memorial on the 16th anniversary. Further, Maharashtra Deputy CMs Devendra Fadnavis, Ajit Pawar paid homage to the Bravehearts.",
 "source": {
 "uri": "aninews.in",
 "dataType": "news",
 "title": "Asian News International (ANI)"
 }
}
# Example usage
if __name__ == "__main__":
    article = extract_relevant_data(artile_text2)
    result = classify_news_article(article)
    if result:
        print(json.dumps(result, indent=4))
        # חילוץ התוכן מתוך התשובה
        raw_content = result["choices"][0]["message"]["content"]

        # המרת התוכן מ-JSON למילון Python
        parsed_content = json.loads(raw_content)

        # הדפסת התוצאה
        print(f"Classification: {parsed_content['classification']}")
        print(f"Location: {parsed_content['location']}")
