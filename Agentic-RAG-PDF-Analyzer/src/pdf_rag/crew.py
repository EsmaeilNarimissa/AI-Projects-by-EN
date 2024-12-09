from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Get the directory where the script is located
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
PDF_DIR = PROJECT_ROOT / "input_pdf"

def get_pdf_path(pdf_name=None):
    """Get the path to the PDF file to process.
    If pdf_name is provided, look for that specific file.
    Otherwise, return the first PDF found in the input_pdf directory."""
    if pdf_name:
        pdf_path = PDF_DIR / pdf_name
        if pdf_path.exists():
            return str(pdf_path)
        raise FileNotFoundError(f"PDF file {pdf_name} not found in {PDF_DIR}")
    
    # If no specific PDF requested, use the first PDF found
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {PDF_DIR}")
    return str(pdf_files[0])

# Use the resolved path for the PDFSearchTool
pdf_search_tool = None  # Initialize as None

@CrewBase
class PdfRag():
    """PdfRag crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        global pdf_search_tool
        if pdf_search_tool is None:
            pdf_path = get_pdf_path()  # Default to first PDF if not specified
            pdf_search_tool = PDFSearchTool(pdf=pdf_path)

    @agent
    def pdf_rag_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_rag_agent'],
            tools=[pdf_search_tool],
            verbose=True
        )

    @agent
    def pdf_summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_summary_agent'],
            verbose=True
        )

    @task
    def pdf_rag_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_rag_task'],
        )

    @task
    def pdf_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_summary_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PdfRag crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )