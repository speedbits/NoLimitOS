"""
tools_repo.py

This module manages a repository of tools used in the CrewAI framework.
It provides functionality to create, store, and retrieve various tool instances
that can be used by AI agents in different tasks.

The module includes:
- Importing and instantiating various tool classes from crewai_tools
- A custom SentimentAnalysisTool class
- A dictionary (tool_repo) to store tool instances
- Functions to retrieve and configure tools based on configuration

Usage:
    Import this module to access the tool repository and utility functions
    for managing AI tools in your CrewAI applications.
"""

from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool, \
                         DirectoryReadTool, \
                         FileReadTool, \
                         MDXSearchTool

from crewai_tools import BaseTool
import numpy as np

# Dictionary to store tool instances
tool_repo = {}

# Website scrape tool
docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
)
tool_repo["docs_scrape_tool"] = docs_scrape_tool

# Sentimental analysis tool
class SentimentAnalysisTool(BaseTool):
    """
    A tool for analyzing the sentiment of text.

    This tool is designed to ensure positive and engaging communication
    by analyzing the sentiment of given text.
    """

    name: str = "Sentiment Analysis Tool"
    description: str = ("Analyzes the sentiment of text "
         "to ensure positive and engaging communication.")
    
    def _run(self, text: str) -> str:
        """
        Analyze the sentiment of the given text.

        Args:
            text (str): The text to analyze.

        Returns:
            str: The sentiment of the text (e.g., "positive").
        """
        # Your custom sentiment analysis code goes here
        return "positive"

# Create an instance of SentimentAnalysisTool
sentiment_analysis_tool = SentimentAnalysisTool()
# Add tool instance to the repo
tool_repo["sentiment_analysis_tool"] = sentiment_analysis_tool

# Directory read tool
directory_read_tool = DirectoryReadTool(directory='./temp')
tool_repo["directory_read_tool"] = directory_read_tool

# File read tool
file_read_tool = FileReadTool()
tool_repo["file_read_tool"] = file_read_tool

# Search tool
search_tool = SerperDevTool()
tool_repo["search_tool"] = search_tool

# Semantic search tool
semantic_search_mdx = MDXSearchTool(mdx=None)
tool_repo["semantic_search_mdx"] = semantic_search_mdx

def get_tools(tool_name_list, tool_config):
    """
    Retrieve and configure tool instances based on specified tool names and configuration.

    This function returns a list of tool instances based on the provided tool names.
    If a tool configuration is provided, it updates the tool's attributes accordingly.

    Args:
        tool_name_list (list): A list of tool names to retrieve.
        tool_config (dict): A dictionary containing tool configurations.

    Returns:
        list: A list of configured tool instances.

    Raises:
        Exception: If the class of a tool specified in agents.json does not match that in tools.json.
    """
    my_tools = {}
    for tool_name in tool_name_list:
        if tool_name in tool_repo.keys():
            a_tool = tool_repo[tool_name]
            print(f"tool_class_name: {a_tool.__class__.__name__}")

            if tool_config:
                print(f"tool config keys => {str(tool_config.keys())}")
            else: 
                print("tool config keys not provided.")

            # Update tool configuration if provided in tools.json
            if tool_config and tool_name in tool_config.keys():
                tool_detail = tool_config[tool_name]
                if tool_detail["class"] == a_tool.__class__.__name__:
                    tool_params = tool_detail["params"]
                    for param in tool_params:
                        setattr(a_tool, param["name"], param["value"])
                    print(a_tool)
                else:
                    raise Exception('Class of the tool specified in agents.json does not match that of in tools.json')

            my_tools[tool_name] = a_tool
            
    return list(my_tools.values())

# The following function is commented out, but kept for reference
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