from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool, \
                         DirectoryReadTool, \
                        FileReadTool, \
                        MDXSearchTool

from crewai_tools import BaseTool
import numpy as np

tool_repo = {}

# Website scrape tool
docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
)
tool_repo["docs_scrape_tool"] = docs_scrape_tool

# Sentimental analysis tool
class SentimentAnalysisTool(BaseTool):
    name: str ="Sentiment Analysis Tool"
    description: str = ("Analyzes the sentiment of text "
         "to ensure positive and engaging communication.")
    
    def _run(self, text: str) -> str:
        # Your custom code tool goes here
        return "positive"
# create an instance
sentiment_analysis_tool = SentimentAnalysisTool()
# add tool instance to the repo
tool_repo["sentiment_analysis_tool"] = sentiment_analysis_tool


directory_read_tool = DirectoryReadTool(directory='./temp')
# add tool instance to the repo
tool_repo["directory_read_tool"] = directory_read_tool

file_read_tool = FileReadTool()
# add tool instance to the repo
tool_repo["file_read_tool"] = file_read_tool

search_tool = SerperDevTool()
# add tool instance to the repo
tool_repo["search_tool"] = search_tool

semantic_search_mdx = MDXSearchTool(mdx=None)
# add tool instance to the repo
tool_repo["semantic_search_mdx"] = semantic_search_mdx

# This returns the list of tools instances based on specified tool names
# tool_config the JSON object of the tools.json
# Note: we add tool instances to the 'tool_repo', so the name provided should match the names in the repo.
def get_tools(tool_name_list, tool_config):
    my_tools = {}
    for tool_name in tool_name_list:
        if tool_name in tool_repo.keys():
            a_tool = tool_repo[tool_name]
            print("tool_class_name: "+str(a_tool.__class__.__name__))

            if(tool_config):
                print("tool config keys => "+str(tool_config.keys()))
            else: 
                print("tool config keys not provided.")

            # If the tool exists in the tools.json, then we may have to change the configuration of the tool per the json
            if (tool_config and tool_name in tool_config.keys()):
                tool_detail = tool_config[tool_name]
                if(tool_detail["class"] == a_tool.__class__.__name__):
                    tool_params = tool_detail["params"]
                    for param in tool_params:
                        setattr( a_tool, param["name"], param["value"])
                    print(a_tool)
                else:
                    raise Exception('Class of the tool specified in agents.json does not match that of in tools.json')

            my_tools[tool_name] = a_tool
            
    return list(my_tools.values())

# tool_list is the list of tool instances (output from get_tools() )
# tool_config the JSON object of the tools.json
# def update_tools_config(tool_list, tool_config):
#     if (tool_config and tool_list):
#         my_tool_list = {}
#         for tool in tool_list:
#             tool_class_name = tool.__class__.__name__
#             print("tool_class_name: "+str(tool_class_name))
#             if (tool_config[])
#         return tool_list
#     else: 
#         return tool_list