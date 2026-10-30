import xml.etree.ElementTree as ET

import requests


# The top 5 news stories, from the BBC News RSS feed (free, no API key)
# (the video used a free news API that has since shut down, so this now reads BBC's feed instead)
def get_top_news():
    url = "https://feeds.bbci.co.uk/news/rss.xml"
    response = requests.get(url, timeout=30)

    # RSS is XML, so we read it with Python's built-in XML parser
    root = ET.fromstring(response.content)

    # we take only the first 5 stories
    top_5 = root.findall("./channel/item")[:5]

    # we keep just the title and the summary of each story, so the LLM gets less to read
    stories = []
    for story in top_5:
        stories.append({
            "title": story.findtext("title"),
            "summary": story.findtext("description")
        })
    return stories


# What the LLM sees: a name, a description and the inputs
# schema
NEWS_TOOL = {
    "type": "function",
    "name": "get_top_news",
    "description": "Get the top 5 news stories right now.",
    "parameters": {
        "type": "object", 
        "properties": {}, 
        "required": []
    },
}

if __name__ == "__main__":
    print("Getting the top 5 news stories...")
    top_news = get_top_news()
    # we print just the title of each story
    for story in top_news:
        print("-", story["title"])