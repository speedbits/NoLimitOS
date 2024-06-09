## NoLimitOS: Simplifying and unlocking the Potential of Crew AI

NoLimitOS, built upon the Crew AI Agentic system, introduces a powerful and intuitive way to manage AI agents and tasks through JSON configuration files. This innovative approach brings several possibilities to the Crew AI platform, including:

1. **User-Friendly Configuration**: Easily configure agents, tasks, and crews through a user-friendly interface.
2. **API Creation**: Seamlessly develop APIs for Crew AI-based applications.
3. **Simplified Application Development**: Empower business users and non-programmers to create Crew AI-based applications with ease.

With NoLimitOS, the complexities of AI management are streamlined, making advanced AI capabilities accessible to a broader audience.

### Installation
1. Clone the repository
2. `cd` (change directory) to the folder `nolimitos`
3. Run the following command to install all pre-requisite libraries:
   ```sh
   pip install -r requirements.txt
4. Update the .env-sample file with the tokens/keys and rename it to `.env`

### Runing the application
1. From the project root, run the following command
   ```sh
    python app/run_crew.py ./app/job_application/
- Where `./app/job_application/` is the folder of the appliation that contains crew configuration.