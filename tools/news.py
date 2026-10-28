import requests


# The top 5 news stories
def get_top_news():
    url = "https://actually-relevant-api.onrender.com/api/stories"
    data = requests.get(url, timeout=30).json()
    # we take only the first 5 stories
    top_5 = data["data"][:5]

    # we keep just the title and the summary of each story, so the LLM gets less to read
    stories = []
    for story in top_5:
        stories.append({
            "title": story["title"], 
            "summary": story["summary"]
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