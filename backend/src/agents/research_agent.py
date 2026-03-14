import json
import os
from typing import Dict, Any, List
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from src.agents.llm_utils import get_llm, get_text_content, clean_tool_args
from src.db.database import SQLALCHEMY_DATABASE_URL

def get_research_tools() -> List[Any]:
    """Initialize and return the tools for the Research Agent."""
    llm = get_llm(temperature=0)
    
    # 1. SQL Database Toolkit
    # Uses the unified database connection string (SQLite file or PostgreSQL)
    db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = sql_toolkit.get_tools()
    
    # 2. Web Search Tool
    # Only added if API key is present
    if os.getenv("TAVILY_API_KEY"):
        search = TavilySearchResults(k=3)
        tools.append(search)
        
    return tools

def invoke_research_agent(message: str) -> str:
    """
    Invokes the Research Agent to perform data analysis or web searches.
    Uses pre-built toolkits from LangChain.
    """
    tools = get_research_tools()
    llm = get_llm(temperature=0).bind_tools(tools)
    
    system_prompt = (
        "You are the specialized **Research Agent**. "
        "You have two main capabilities:\n"
        "1. **Data Analysis**: You can query the local SQL database to answer broad questions about the schema, "
        "table structures, or complex data relationships that simple tool calls can't handle.\n"
        "2. **Web Research**: You can search the internet for the latest news, market trends, or comparative information.\n\n"
        "Be thorough and cite your sources (database tables or search results)."
    )
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=message)
    ]
    
    # Simple ReAct-style loop for tool execution
    for i in range(5):
        response = llm.invoke(messages)
        messages.append(response)
        
        if not response.tool_calls:
            break
            
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = clean_tool_args(tool_call["args"])
            
            # Find the tool in our list (handling nested naming if necessary)
            tool_fn = next((t for t in tools if t.name == tool_name), None)
            
            if tool_fn:
                try:
                    tool_result = tool_fn.invoke(tool_args)
                    tool_msg = ToolMessage(
                        content=json.dumps(tool_result) if not isinstance(tool_result, str) else tool_result, 
                        tool_call_id=tool_call["id"], 
                        name=tool_name
                    )
                    messages.append(tool_msg)
                except Exception as e:
                    messages.append(ToolMessage(content=f"Error executing tool: {e}", tool_call_id=tool_call["id"], name=tool_name))
            else:
                messages.append(ToolMessage(content=f"Error: Tool {tool_name} not found", tool_call_id=tool_call["id"], name=tool_name))
                
    return get_text_content(messages[-1])
