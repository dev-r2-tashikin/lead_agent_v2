import os
from typing import List
from autogen_ext.models.openai import OpenAIChatCompletionClient

class AppSettings:
    NB_GEMINI_API_KEY = ['AIzaSyADbqWnOUP1hsXJbALzC2AYsFh3BkstjZU']
    GEMINI_APIKEYS: List[str] = [
    'AIzaSyBWPiNDni24gEzdZUzNUhVxws6prDHB4Yo',
    'AIzaSyBxVGph11TTLKKfGBXH3GVPIXriYaroV9E',
   ' AIzaSyCZ0aWliaCy2JteNdeIfvvJ4lZhf3-YYjI',
    'AIzaSyADbqWnOUP1hsXJbALzC2AYsFh3BkstjZU',
    'AIzaSyCiBhsJ7TYZpNNgAXM9OH0jHZiA7mG3VqA',
    'AIzaSyCuUDlC1PCcUR3gL3GMpUTwHmlIDb6S48A',
    'AIzaSyARZu1qOJ8KCGlOuuAJ7HDxyv9gmYigu4w'
    ]
    MODEL_LIST = {
        # 'flash': 'gemini-2.0-flash',
        'flash': 'gemini-2.5-flash',
        'pro': 'gemini-2.5-pro'
    }

settings = AppSettings()


def get_Clients():
    """
    Returns a list of OpenAIChatCompletionClient instances for Gemini.
    """
    flash_Client_list = [OpenAIChatCompletionClient(model = settings.MODEL_LIST['flash'], api_key = settings.GEMINI_APIKEYS[i]) for i in range(len(settings.GEMINI_APIKEYS))]
    # pro_clent_list = [get_model_client(settings.NB_GEMINI_API_KEY[i], settings.MODEL_LIST['pro']) for i in range(len(settings.NB_GEMINI_API_KEY))]
    pro_Client_list = [OpenAIChatCompletionClient(model = settings.MODEL_LIST['flash'], api_key = key) for key in settings.NB_GEMINI_API_KEY]
    return flash_Client_list , pro_Client_list


flash_Client_list, pro_Client_list = get_Clients()

# Import new tools for data_insight_agent
from src.tools.search_tools import search_ddgs, LLM_search
from src.tools.file_writer_tool import edit_file
from src.tools.file_reader_tool import read_multiple_files
from src.tools.search import process_and_cache_urls

search_agent_tool = [search_ddgs, edit_file, read_multiple_files]
exec_agent_tool = [edit_file, read_multiple_files, process_and_cache_urls]