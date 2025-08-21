from crawl4ai import AsyncWebCrawler, AdaptiveCrawler
from src.tools.search_tools import LLM_search
import asyncio
import time
from ddgs import DDGS
import psycopg2
from google import genai
from google.genai import types
from serpapi import GoogleSearch 
from pprint import pprint


def google_search(query):
    params = { "engine": "google", "num":5,"q": query, "api_key": "eb87362fbdcfafd5eccf8f821d9150cf328e14e6ef1c13e2571c2fe850aa24e8" } 
    search = GoogleSearch(params) 
    results = search.get_dict()

    organic_results = results.get('organic_results', [])
    return [r['link'] for r in organic_results]

def LLM_search(query: str):
    client = genai.Client(api_key='AIzaSyADbqWnOUP1hsXJbALzC2AYsFh3BkstjZU')

    # Define the grounding tool
    grounding_tool = types.Tool(url_context=types.UrlContext())
    search_tool = types.Tool(url_context=types.GoogleSearch())
    
    # Configure generation settings
    config = types.GenerateContentConfig(
        tools=[grounding_tool],
    )
    for i in range(3):
        try:
    # Configure and call the client
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=query,
                config=config,
            )

            return response.text
        except:
            time.sleep(20)
    return 'execution failed'



async def crawl(crawler, url):
    result = await crawler.arun(url=url)
    return result.markdown
    



import pandas as pd

df = pd.read_csv('./fip_query.csv')

name = list(df['title'])

from ddgs import DDGS

async def main():
    with open('./record.txt', 'a', encoding = 'utf-8') as f:
        with DDGS() as ddgs:
            for n in name[38:]:
                print(n)
                query = f"{n} mail"
                search_result = google_search(query)
                async with AsyncWebCrawler() as crawler:
                    exec_list = [crawl(crawler, url) for url in search_result]
                    exec_result = await asyncio.gather(*exec_list)
                    s = '\n'.join(exec_result)
                    q = f'''从以下内容获取给定医院邮箱，医院的名字是{n},只需要输出邮箱，如果没有，输出None：{s}'''
                result = LLM_search(q)
                print(result)
                f.write(f'{n} : {result}\n')

        
                

async def test():
    async with AsyncWebCrawler() as crawler:
        test_url =  'https://www.facebook.com/bangkokratchada/'
        result = await crawl(crawler, test_url)
        print(result)

asyncio.run(main())
# asyncio.run(test())
            

        