import json
from crewai import Agent, Task, Crew, Process

import os
from utils import get_openai_api_key
from tools_repo import *
import os.path
import importlib
from llms import llms_instances


def load_data_from_file(filename):
    file_exists = os.path.isfile(filename)
    if(file_exists):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return None
    
def get_tasks_by_name(crew_tasks_dict, task_name_list):
    my_tasks = {}
    if(task_name_list and crew_tasks_dict):
        for task_name in task_name_list:
            if(task_name in crew_tasks_dict.keys()):
                my_tasks[task_name] = crew_tasks_dict[task_name]
                print("Added following task to context => "+task_name)
    else:
        print("Either tasks_name_list or tasks_instances or both are None.")
    return list(my_tasks.values())

def create_agents_and_tasks(app_folder, agents_json_file):
    if(agents_json_file is None):
       agents_json_file = app_folder + "agents.json"

    data = load_data_from_file(agents_json_file)
    agents_dict = {}
    tasks_dict = {}

    # Create Agent objects
    for agent_data in data['agents']:
        agent = Agent(
            #name=agent_data['name'],
            role=agent_data['role'],
            goal=agent_data['goal'],
            backstory=agent_data['backstory']
        )
        # Set additional properties
        for key, value in agent_data.items():
            if key not in ['name', 'role', 'goal', 'backstory']:
                if (key == 'allow_delegation' and value):
                    agent.allow_delegation = bool(value)
                if (key == 'verbose' and value):
                    agent.verbose = bool(value)

        agents_dict[agent_data['name']] = agent

    # Create Task objects
    for task_data in data['tasks']:
        task = Task(
            #name=task_data['name'],
            description=task_data['description'],
            expected_output=task_data['expected_output'],
            agent=agents_dict[task_data['agent']] 
        )
        # Set additional properties
        for key, value in task_data.items():
            if key not in ['name', 'description', 'expected_output', 'agent']:
                if (key == 'tools'):
                    tools_json = app_folder+'tools.json'
                    tools_config = load_data_from_file(tools_json)
                    print("tools -> ")
                    print(tools_config)
                    # print(get_tools(task_data[key]))
                    my_tools = get_tools(task_data[key], tools_config) 
                    #my_tools = update_tools_config(my_tools, tools_config)
                    task.tools = my_tools 
                if (key == 'human_input'):
                    task.human_input = bool(value)
                if (key == 'output_json'):
                    # the class file-name should be same as the class name
                    # example if the class name is VenueDetails,then model class file name should be VenueDetails.py
                    models_module = importlib.import_module('models.'+value)
                    model_class = getattr(models_module, value)
                    # model_instance = model_class()
                    task.output_json = model_class
                if (key == 'output_file'):
                    task.output_file = value
                if (key == 'async_execution'):
                    task.async_execution = bool(value)
                if (key == 'context'):
                    print("context -> ")
                    print(value)                    
                    context_tasks = get_tasks_by_name(tasks_dict, value) 
                    task.context = context_tasks


        tasks_dict[task_data['name']] = task

    return agents_dict, tasks_dict


def run_agents(app_folder):
        
    openai_api_key = get_openai_api_key()
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo' 

    input_data = load_data_from_file(app_folder+'input.json')
    agents_json_file_path = app_folder + input_data["agents_json_file"]
    inputs = input_data["inputs"] #{"topic": "How Artificial Intelligence helps in field of bio chemistry"}
    print("agents_json_file_path => "+agents_json_file_path)

    # Use the function to load data and create objects
    agents, tasks = create_agents_and_tasks(app_folder, agents_json_file=agents_json_file_path)

    # Example output
    for agent_name, agent_obj in agents.items():
        print(f"Agent Name: {agent_name}, Role: {agent_obj.role}")

    for task_name, task_obj in tasks.items():
        print(f"Task Name: {task_name}, Description: {task_obj.description}")

    # get crew config from the input.json and set it as part of the crew instantiation
    crew_config = None
    if ("crew_config" in input_data.keys()):
        crew_config = input_data["crew_config"]
    
    enable_crew_memory = False
    if(crew_config and "memory" in crew_config.keys()):
        print("crew memory => "+str(crew_config["memory"]))
        enable_crew_memory = bool(crew_config["memory"])

    crew_verbose_level = 2
    if(crew_config and "verbose" in crew_config.keys()):
        print("crew verbose => "+str(crew_config["verbose"]))
        crew_verbose_level = crew_config["verbose"]
    
    crew_process_type = Process.sequential # defaulting to sequential because None was not an option it likes
    process_manager_llm = None
    if(crew_config and "process" in crew_config.keys()):
        if (crew_config["process"] == "sequential"):
            crew_process_type = Process.sequential
            print("crew crew_process_type => sequential")
        elif (crew_config["process"] == "hierarchical"):
            crew_process_type = Process.hierarchical
            print("crew crew_process_type => hierarchical")
            if ("manager_llm" in crew_config.keys()):
                process_manager_llm = llms_instances.get_llm(crew_config["manager_llm"])
                print("crew process_manager_llm set."+crew_config["manager_llm"])

    crew = Crew(
        agents=agents.values(),
        tasks=tasks.values(),
        memory=enable_crew_memory,
        process=crew_process_type,
        manager_llm=process_manager_llm,
        verbose=crew_verbose_level
    )
    
    result = crew.kickoff(inputs=inputs)


if __name__ == "__main__":
    app_folder = './app/job_application/'
    run_agents(app_folder)