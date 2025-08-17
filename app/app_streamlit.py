
import re
import time
import streamlit as st
import auto_app
import sys

# Set the page configuration
st.set_page_config(page_title="SpeedLimit AI Apps", layout="wide")

# Function to display the main screen with panels
def main_screen():
    st.title("SpeedLimit AI Apps")

    # Create four columns for the panels
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    # col5, col6 = st.columns(2)

    # Function to display a panel with an image and a button
    def display_panel(column, image_path, description, button_label, key):
        with column:
            img_col, desc_col  = st.columns([2,3])
            with img_col:
                st.image(image_path)
            with desc_col:
                st.markdown(
                    f"""
                    <div style="width: 100%;">{description}</div>
                    """,
                    unsafe_allow_html=True
                )
            if st.button(button_label, key=key):
                if(key == 'button1'):
                    st.session_state.page = "input_screen1"
                    st.session_state.button_clicked = key
                if(key == 'button2'):
                    st.session_state.page = "input_screen2"
                    st.session_state.button_clicked = key

    # Descriptions
    col1_description = "Our agents will help you with creating a blog or article based on your topic.<br />Agents involved: Content Planner, Content Writer, Editor"
    col2_description = "Our agents will help with analysis on job posting and help Technology job applicants with updating their resume so it stands out. Additionally, helps job applicants with interview questions for their review and preparation. <br />Agents involved: Tech Job Researcher, Personal Profiler for Engineers, Resume Strategist for Engineers, Engineering Interview Preparer"
    col3_description = "Our agents will aid you in identifying high-value leads that match your ideal customer profile. Additionally, nurture leads with personalized, compelling communications. <br />Agents involved: Sales Representative, Lead Sales Representative"
    col4_description = "Our agents provides company's financial analysis to help you with trading strategy and advise. <br />Agents involved: Data Analyst, Trading Strategy Developer, Trade Advisor, Risk Advisor"
    # Display panels with images and buttons, each with a unique key
    display_panel(col1, "./app/images/ArticleWriter.jpg", col1_description, "Get Started", "button1")
    display_panel(col2, "./app/images/JobApplication.jpg", col2_description, "Get Started", "button2")
    display_panel(col3, "./app/images/CustomerOutreach.jpg", col3_description, "Get Started", "button3")
    display_panel(col4, "./app/images/FinancialAnalysis.jpg",col4_description, "Get Started", "button4")
    # display_panel(col5, "./app/images/Agents.jpg", "Description for image 1", "Get Started", "button5")
    # display_panel(col6, "./app/images/Agents.jpg", "Description for image 1", "Get Started", "button6")

#display the console processing on streamlit UI
class StreamToExpander:
    def __init__(self, expander, agent_roles=None):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange', 'gold', 'pink', 'indigo', 'peru', 'royalblue', 'sienna', 'palegreen']  # Define a list of colors
        self.color_index = 0  # Initialize color index
        self.agent_roles = agent_roles

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            # self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        # Dynamically highlights the role names showing up in the processing content to an assigned color
        for role in self.agent_roles:
            if role in cleaned_data:
                # Apply different color 
                # print("assigning color for role: "+role)
                self.color_index = (self.color_index + 1) % len(self.agent_roles)
                cleaned_data = cleaned_data.replace(role, f":{self.colors[self.color_index]}[{role}]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

# Function to display the input screen
def input_screen1():
    st.title("Article Writer")
    agent_roles = ["Content Planner", "Content Writer", "Editor"]
    # Sidebar for input fields
    with st.sidebar:
        st.header("Input Parameters")
        topic = st.text_input("topic")


    # Main section for displaying the inputs
    st.write("This interface takes 1 inputs: Topic for the article.")

    # Display the entered values
    st.subheader("Entered Values")
    st.write(f"**topic:** {topic}")

    # Example of processing the inputs
    if st.button("Submit"):
        if not topic:
            st.error("Please fill all the fields.")
        else:
            # Placeholder for stopwatch
            stopwatch_placeholder = st.empty()
        
            # Start the stopwatch
            start_time = time.time()
            with st.expander("Processing!"):
                sys.stdout = StreamToExpander(st, agent_roles)
                with st.spinner("Generating Results"):
                    #st.write("Processing your inputs...")
                    # Add your processing logic here
                    inputs = {"topic": topic}
                    results = auto_app.run_agents("./app/article_writer/", inputs)

            # Stop the stopwatch
            end_time = time.time()
            total_time = end_time - start_time
            stopwatch_placeholder.text(f"Total Time Elapsed: {total_time:.2f} seconds")
            st.subheader("Results from Article Writer:")
            # st.write(results)
            st.markdown(results)
            # st.success("Inputs processed successfully!")
    
    # Button to go back to the main screen
    if st.button("Back to Main Screen"):
        st.session_state.page = "main_screen"

# Function to display the input screen
def input_screen2():
    st.title("Job Application Helper")
    agent_roles = ["Tech Job Researcher", "Personal Profiler for Engineers", "Resume Strategist for Engineers", "Engineering Interview Preparer"]
    # Sidebar for input fields
    with st.sidebar:
        st.header("Input Parameters")
        job_posting_url = st.text_input("Job posting URL")
        github_url = st.text_input("Github URL to understand the Job application")
        personal_writeup = st.text_input("Personal write up of the job applicant")


    # Main section for displaying the inputs
    st.write("This interface takes 3 inputs: ")

    # Display the entered values
    st.subheader("Entered Values")
    st.write(f"**Job posting URL:** {job_posting_url}")
    st.write(f"**Github URL:** {github_url}")
    st.write(f"**Personal write up:** {personal_writeup}")

    # Example of processing the inputs
    if st.button("Submit"):
        if not job_posting_url and not personal_writeup and not github_url: 
            st.error("Please fill all the fields.")
        else:
            # Placeholder for stopwatch
            stopwatch_placeholder = st.empty()
        
            # Start the stopwatch
            start_time = time.time()
            with st.expander("Processing!"):
                sys.stdout = StreamToExpander(st, agent_roles)
                with st.spinner("Generating Results"):
                    #st.write("Processing your inputs...")
                    # Add your processing logic here
                    inputs = {"job_posting_url": job_posting_url, "github_url": github_url, "personal_writeup": personal_writeup}
                    results = auto_app.run_agents("./app/job_application/", inputs)

            # Stop the stopwatch
            end_time = time.time()
            total_time = end_time - start_time
            stopwatch_placeholder.text(f"Total Time Elapsed: {total_time:.2f} seconds")
            st.subheader("Results from Job Application Helper:")
            # st.write(results)
            st.markdown(results)
            # st.success("Inputs processed successfully!")
    
    # Button to go back to the main screen
    if st.button("Back to Main Screen"):
        st.session_state.page = "main_screen"

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "main_screen"

# Display the appropriate screen based on the session state
if st.session_state.page == "main_screen":
    main_screen()
elif st.session_state.page == "input_screen1":
    input_screen1()
elif st.session_state.page == "input_screen2":
    input_screen2()