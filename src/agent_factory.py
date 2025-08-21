from src.settings import flash_Client_list, search_agent_tool, exec_agent_tool
from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from prompt_manager import PromptManager

model_client_1 = flash_Client_list[0]
termination = TextMentionTermination("TERMINATION")


prompt = PromptManager()
search_agent_prompt = prompt.get_prompts('search_agent')['system'].format()
exec_agent_prompt = prompt.get_prompts('exec_agent')['system'].format()

def create_search_agent() -> AssistantAgent:
    agent = AssistantAgent(
        name="search_agent",
        system_message=search_agent_prompt,
        model_client= flash_Client_list[-1],
        tools = search_agent_tool  # Reuse the same tools as data_insight_agent
    )

    # The group chat will alternate between the writer and the critic.
    team = RoundRobinGroupChat(
        participants = [agent],
        termination_condition=termination,  # Use specialized termination condition
        max_turns=200 # Allow sufficient turns for plan execution
    )
    agent = SocietyOfMindAgent("search_agent", team = team, model_client = flash_Client_list[-1])
    return agent


def create_exec_agent(i) -> AssistantAgent:
    agent = AssistantAgent(
        name="exec_agent",
        system_message=exec_agent_prompt,
        model_client= flash_Client_list[i],
        tools = exec_agent_tool  # Reuse the same tools as data_insight_agent
    )

    # The group chat will alternate between the writer and the critic.
    team = RoundRobinGroupChat(
        participants = [agent],
        termination_condition=termination,  # Use specialized termination condition
        max_turns=200 # Allow sufficient turns for plan execution
    )
    agent = SocietyOfMindAgent("search_agent", team = team, model_client = flash_Client_list[i])
    return agent

