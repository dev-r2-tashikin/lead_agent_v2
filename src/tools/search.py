import asyncio
from crawl4ai import AsyncWebCrawler, AdaptiveCrawler
import psycopg2
from src.tools.search_tools import LLM_search
DB_CONFIG = {
    'dbname': 'land_agent',
    'user': 'postgres',  # PostgreSQL 的默认用户名通常是 'postgres'
    'password': 'root',
    'host': 'localhost', # 通常是 'localhost' 或 '127.0.0.1'
    'port': '5432'       # PostgreSQL 的默认端口
}






async def crawl_url(crawler,url: str) -> str:
    result = await crawler.arun(
        url=url,

    )
    return {url:result.markdown}

async def process_and_cache_urls(urls_string: str):
    """
    处理一个逗号分隔的URL字符串，为每个URL获取内容。
    - 首先检查数据库缓存。
    - 如果缓存未命中，则从网络获取，并存入数据库。
    - 返回一个字典，键是URL，值是其内容。
    """
    # 分割字符串并去除首尾空格
    urls = [url.strip() for url in urls_string.split(',') if url.strip()]
    if not urls:
        print("输入的URL字符串为空或无效。")
        return {}

    results = {}
    conn = None
    try:
        # 连接到PostgreSQL数据库
        conn = psycopg2.connect(**DB_CONFIG)
        # 创建一个游标对象，用于执行SQL命令
        cur = conn.cursor()

        for url in urls:
            cur.execute("SELECT content FROM url_content WHERE url = %s", (url,))
            row = cur.fetchone() # 获取查询结果的第一行

            results[url] = row[0] if row else None
        

        exec_list = []
        async with AsyncWebCrawler() as crawler:
            for url in urls:
                if not results[url]:
                    exec_list.append(crawl_url(crawler, url))
        
            exec_result = await asyncio.gather(*exec_list)

        for result in exec_result:
            url = list(result.keys())[0]  
            content = result[url]
            LLM_content = LLM_search(f'''我将提供三段html内容，你需要总结这些内容，不要遗漏任何可能有用的信息，我们是一个IVD行业b2b品牌，正在寻找分销商的线索及其上下文，请你以markdown格式返回清洗后的文本，不需要返回其其他东西：
                                        {content}
    ''')
            if content is not None:
                cur.execute(
                    "INSERT INTO url_content (url, content,llmcontent) VALUES (%s, %s, %s)",
                    (url, content, LLM_content)
                )
                # 提交事务，使插入操作生效
                conn.commit()
                print(" - 结果: 成功写入数据库。")
            else:
                # 如果获取内容失败，记录下来
                print(" - 结果: 未能获取内容，跳过数据库写入。")
            
            results[url] = LLM_content

    except psycopg2.Error as e:
        print(f"数据库错误: {e}")
        if conn:
            conn.rollback() # 如果发生错误，回滚事务
        return {} # 或者可以抛出异常
    finally:
        # 无论成功与否，最后都要关闭数据库连接
        if conn:
            cur.close()
            conn.close()
            print("\n数据库连接已关闭。")
    
    return results



if __name__ == "__main__":
    asyncio.run(process_and_cache_urls("https://www.legal.io/articles/5428730/Community-Spotlight-Mara-Senn-Executive-Global-Compliance-Lead-at-GE-Healthcare"))