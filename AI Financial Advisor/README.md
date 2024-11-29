# AI Personal Finance Planner

An AI-powered personal finance planner that generates personalized financial plans using OpenAI GPT-4o. This Streamlit app automates the process of researching, planning, and creating tailored budgets, investment strategies, and savings goals.

## Features

- Set your financial goals and provide details about your current financial situation
- Use GPT-4o to generate intelligent and personalized financial advice
- Receive customized budgets, investment plans, and savings strategies
- Web-based research integration using SerpAPI
- Modern, user-friendly interface

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and add your API keys:
   - Get OpenAI API key from: https://platform.openai.com/account/api-keys
   - Get SerpAPI key from: https://serpapi.com/

## Running the App

You can run the app using either of these commands:

```bash
python -m streamlit run app.py  # Recommended
# OR
streamlit run app.py
```

## Usage

1. Enter your OpenAI and SerpAPI keys (if not set in .env)
2. Input your financial goals
3. Describe your current financial situation
4. Click "Generate Financial Plan"
5. Review your personalized financial plan

## Note

This tool provides general financial advice and should not be considered as professional financial counsel. Always consult with a qualified financial advisor for important financial decisions.
