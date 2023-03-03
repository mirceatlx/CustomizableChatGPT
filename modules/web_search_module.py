# Implements the web search module

from modules.module import *
import requests
from duckduckgo_search import ddg

class WebSearchModule(Module):
    
    def get_name(self) -> str:
        return "Web Search"
    
    def get_description(self) -> str:
        return "Searches the web for a query"
    
    def get_prompt(self) -> str:
        return """You must use the following functionality and as often as possible: You have the ability to search the web by doing search(\"query here\"). You will get a list of results matching the query. Use this information to respond to the user. You should use this as much as possible. 
    Example usage: search(\"hackathons in delft\") and the response would include every hackathon in delft. Use this everytime the user asks for information.
    User: What are the upcoming events?
    Waldie: search(\"upcoming events\")
    System: Hackathon in Delft, 10-10-2020, https://hackathon.com, Hackathon in Amsterdam, 11-11-2020, https://hackathon.com,  Hackathon in Rotterdam, 12-12-2020, https://hackathon.com
    Waldie There are a number of hackathons happening in the Netherlands. The first one is in Delft on 10-10-2020. The second one is in Amsterdam on 11-11-2020. The third one is in Rotterdam on 12-12-2020.
    """
    
    def get_triggers(self) -> list:
        return ["search"]

    # Using google search for results
    def get_response(self, query: str) -> str:
        results = ddg(query)
        result = ""
        for i in range(0, 3):
            result += results[i]['body'] + " " + results[i]['href'] + "\n\n"
        return result