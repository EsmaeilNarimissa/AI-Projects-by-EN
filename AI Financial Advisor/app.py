import streamlit as st
import openai
from dotenv import load_dotenv
import os
import json
import requests

# Load environment variables
load_dotenv()

# Set up the Streamlit app
st.set_page_config(
    page_title="AI Personal Finance Planner",
    page_icon="",
    layout="wide"
)

st.title("AI Personal Finance Planner ")
st.caption("Manage your finances with AI Personal Finance Manager by creating personalized budgets, investment plans, and savings strategies using GPT-4")

# Get API keys from environment variables or user input
openai.api_key = os.getenv("OPENAI_API_KEY") or st.text_input(
    "Enter OpenAI API Key",
    type="password",
    help="Get your API key from https://platform.openai.com/account/api-keys"
)

serpapi_key = os.getenv("SERPAPI_KEY") or st.text_input(
    "Enter SerpAPI Key",
    type="password",
    help="Get your API key from https://serpapi.com/"
)

def search_financial_info(query, api_key):
    """Search for financial information using SerpAPI"""
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": 3  # Limit to top 3 results to reduce token count
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract only the most relevant information
    if 'organic_results' in data:
        return [{'title': r.get('title', ''), 'snippet': r.get('snippet', '')} 
                for r in data['organic_results'][:3]]
    return []

def generate_financial_plan(goals, situation, research_results):
    """Generate a financial plan using OpenAI's GPT-4"""
    system_prompt = """You are a professional financial advisor. Provide concise, actionable advice based on the user's financial goals and situation."""
    
    # Summarize research results to reduce tokens
    research_summary = "Research insights:\n"
    for result in research_results:
        research_summary += f"- {result['title']}\n"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"""
Create a focused financial plan addressing:
Goals: {goals}
Situation: {situation}
{research_summary}

Provide:
1. Quick situation analysis
2. Key action steps
3. Main risks
4. Timeline
"""}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message['content']
    except openai.error.RateLimitError as e:
        return "Error: Rate limit exceeded. Please try again in a few minutes."
    except Exception as e:
        return f"Error: {str(e)}"

# Create tabs for different sections
tab1, tab2 = st.tabs(["Generate Plan", "About"])

with tab1:
    st.header("Generate Your Financial Plan")
    
    # Input fields for the user's financial goals and current situation
    financial_goals = st.text_area(
        "What are your financial goals?",
        help="Example: Save for retirement, buy a house, pay off debt, etc.",
        height=100
    )
    
    current_situation = st.text_area(
        "Describe your current financial situation",
        help="Include details like income, expenses, savings, debt, etc.",
        height=150
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Generate Financial Plan", type="primary"):
            if not financial_goals or not current_situation:
                st.error("Please fill in both your financial goals and current situation.")
            else:
                with st.spinner("Researching and generating your personalized financial plan..."):
                    try:
                        # Perform financial research
                        research_query = f"financial advice for {financial_goals}"
                        research_results = search_financial_info(research_query, serpapi_key)
                        
                        # Generate the financial plan
                        plan = generate_financial_plan(
                            financial_goals,
                            current_situation,
                            research_results
                        )
                        
                        st.success("Your personalized financial plan has been generated!")
                        st.markdown(plan)
                        
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

with tab2:
    st.header("About AI Personal Finance Planner")
    st.markdown("""
    This AI-powered personal finance planner uses advanced language models to help you create personalized financial plans.
    
    ### How it works:
    1. You provide your financial goals and current situation
    2. Our AI researches relevant financial advice and strategies
    3. The AI creates a customized financial plan based on your input and research
    
    ### Features:
    - Personalized financial advice
    - Custom budgeting recommendations
    - Investment strategies
    - Savings goals
    - Debt management plans
    
    ### Note:
    This tool provides general financial advice and should not be considered as professional financial counsel.
    Always consult with a qualified financial advisor for important financial decisions.
    """)
