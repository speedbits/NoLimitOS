"""
auto_app.py

This module provides functionality for creating and running AI agents and tasks
using the CrewAI framework. It includes functions for loading data from JSON files,
creating Agent and Task objects, and running a Crew of agents to perform tasks.

The module uses configuration files (agents.json, input.json, and tools.json) to
set up the agents, tasks, and execution parameters.

Main functions:
- load_data_from_file: Loads JSON data from a file
- get_tasks_by_name: Retrieves tasks by their names
- create_agents_and_tasks: Creates Agent and Task objects from JSON configuration
- run_agents: Sets up and runs a Crew of agents to perform tasks

Dependencies:
- crewai: For Agent, Task, Crew, and Process classes
- utils: For getting OpenAI API key
- tools_repo: For accessing tool configurations
- llms.llms_instances: For accessing language model instances
"""

import json
import os
import importlib
from crewai import Agent, Task, Crew, Process
from utils import get_openai_api_key
from tools_repo import *
from llms import llms_instances

def load_data_from_file(filename):
    """
    Load JSON data from a file.

    Args:
        filename (str): Path to the JSON file.

    Returns:
        dict: Loaded JSON data, or None if the file doesn't exist.
    """
    file_exists = os.path.isfile(filename)
    if file_exists:
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return None
    
def get_tasks_by_name(crew_tasks_dict, task_name_list):
    """
    Retrieve tasks by their names from a dictionary of tasks.

    Args:
        crew_tasks_dict (dict): Dictionary of all available tasks.
        task_name_list (list): List of task names to retrieve.

    Returns:
        list: List of task objects corresponding to the given names.
    """
    my_tasks = {}
    if task_name_list and crew_tasks_dict:
        for task_name in task_name_list:
            if task_name in crew_tasks_dict.keys():
                my_tasks[task_name] = crew_tasks_dict[task_name]
                print(f"Added following task to context => {task_name}")
    else:
        print("Either tasks_name_list or tasks_instances or both are None.")
    return list(my_tasks.values())

def create_agents_and_tasks(app_folder, agents_json_file):
    """
    Create Agent and Task objects from JSON configuration files.

    Args:
        app_folder (str): Path to the application folder.
        agents_json_file (str): Path to the agents JSON file.

    Returns:
        tuple: Two dictionaries containing Agent and Task objects.
    """
    if agents_json_file is None:
       agents_json_file = app_folder + "agents.json"

    data = load_data_from_file(agents_json_file)
    agents_dict = {}
    tasks_dict = {}

    # Create Agent objects
    for agent_data in data['agents']:
        agent = Agent(
            role=agent_data['role'],
            goal=agent_data['goal'],
            backstory=agent_data['backstory']
        )
        # Set additional properties
        for key, value in agent_data.items():
            if key not in ['name', 'role', 'goal', 'backstory']:
                if key == 'allow_delegation' and value:
                    agent.allow_delegation = bool(value)
                if key == 'verbose' and value:
                    agent.verbose = bool(value)

        agents_dict[agent_data['name']] = agent

    # Create Task objects
    for task_data in data['tasks']:
        task = Task(
            description=task_data['description'],
            expected_output=task_data['expected_output'],
            agent=agents_dict[task_data['agent']] 
        )
        # Set additional properties
        for key, value in task_data.items():
            if key not in ['name', 'description', 'expected_output', 'agent']:
                if key == 'tools':
                    tools_json = app_folder+'tools.json'
                    tools_config = load_data_from_file(tools_json)
                    print("tools -> ")
                    print(tools_config)
                    my_tools = get_tools(task_data[key], tools_config) 
                    task.tools = my_tools 
                if key == 'human_input':
                    task.human_input = bool(value)
                if key == 'output_json':
                    # the class file-name should be same as the class name
                    # example if the class name is VenueDetails,then model class file name should be VenueDetails.py
                    models_module = importlib.import_module('models.'+value)
                    model_class = getattr(models_module, value)
                    task.output_json = model_class
                if key == 'output_file':
                    task.output_file = value
                if key == 'async_execution':
                    task.async_execution = bool(value)
                if key == 'context':
                    print("context -> ")
                    print(value)                    
                    context_tasks = get_tasks_by_name(tasks_dict, value) 
                    task.context = context_tasks

        tasks_dict[task_data['name']] = task

    return agents_dict, tasks_dict

def run_agents(app_folder, my_inputs=None):
    """
    Set up and run a Crew of agents to perform tasks.

    Args:
        app_folder (str): Path to the application folder.
        my_inputs (dict, optional): Input data for the agents. If None, loads from input.json.

    Returns:
        Any: Result of the Crew's execution.
    """
    openai_api_key = get_openai_api_key()
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo' 
    
    input_data = load_data_from_file(app_folder+'input.json')
    print(f"input data => {str(input_data)}")
    if my_inputs is None:
        print(f"input data file => {app_folder}input.json")
        inputs = input_data["inputs"]
    else:
        inputs = my_inputs

    agents_json_file_path = app_folder + input_data["agents_json_file"]
    print(f"agents_json_file_path => {agents_json_file_path}")

    # Use the function to load data and create objects
    agents, tasks = create_agents_and_tasks(app_folder, agents_json_file=agents_json_file_path)

    # Example output
    for agent_name, agent_obj in agents.items():
        print(f"Agent Name: {agent_name}, Role: {agent_obj.role}")

    for task_name, task_obj in tasks.items():
        print(f"Task Name: {task_name}, Description: {task_obj.description}")

    # Get crew config from the input.json and set it as part of the crew instantiation
    crew_config = input_data.get("crew_config", {})
    
    enable_crew_memory = crew_config.get("memory", False)
    print(f"crew memory => {enable_crew_memory}")

    crew_verbose_level = crew_config.get("verbose", 2)
    print(f"crew verbose => {crew_verbose_level}")
    
    crew_process_type = Process.sequential  # defaulting to sequential
    process_manager_llm = None
    if "process" in crew_config:
        if crew_config["process"] == "sequential":
            crew_process_type = Process.sequential
            print("crew crew_process_type => sequential")
        elif crew_config["process"] == "hierarchical":
            crew_process_type = Process.hierarchical
            print("crew crew_process_type => hierarchical")
            if "manager_llm" in crew_config:
                process_manager_llm = llms_instances.get_llm(crew_config["manager_llm"])
                print(f"crew process_manager_llm set. {crew_config['manager_llm']}")

    crew = Crew(
        agents=agents.values(),
        tasks=tasks.values(),
        memory=enable_crew_memory,
        process=crew_process_type,
        manager_llm=process_manager_llm,
        verbose=crew_verbose_level
    )
    
    result = crew.kickoff(inputs=inputs)
    return result
