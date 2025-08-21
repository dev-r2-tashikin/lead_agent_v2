import time
from ddgs import DDGS
import psycopg2
from google import genai
from google.genai import types

# --- 常量定义 ---
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
MAX_RESULTS_PER_QUERY = 25 # 每个子查询返回的最大结果数

DB_CONFIG = {
    'dbname': 'land_agent',
    'user': 'postgres',  # PostgreSQL 的默认用户名通常是 'postgres'
    'password': 'root',
    'host': 'localhost', # 通常是 'localhost' 或 '127.0.0.1'
    'port': '5432'       # PostgreSQL 的默认端口
}


def log_search_to_db(company_name:str, query: str, result: str):
    """将搜索查询和结果记录到 PostgreSQL 数据库中。"""
    conn = None
    try:
        # 建立数据库连接
        conn = psycopg2.connect(**DB_CONFIG)
        # 创建一个游标对象
        with conn.cursor() as cur:
            # 定义 SQL 插入语句，使用占位符 (%s) 防止 SQL 注入
            sql = "INSERT INTO search_results (company_name,company_search_input,result) VALUES (%s, %s, %s);"
            # 执行插入操作
            cur.execute(sql, (company_name, query, result))
        # 提交事务，使更改生效
        conn.commit()
        print("--- 搜索结果已成功存入数据库。 ---")
    except psycopg2.Error as e:
        # 如果发生数据库错误，打印错误信息
        print(f"--- 数据库错误：无法写入搜索记录。原因: {e} ---")
    finally:
        # 无论成功与否，最后都关闭数据库连接
        if conn is not None:
            conn.close()


def search_ddgs(company_name:str, query: str, region: str = "wt-wt") -> str:
    """
    使用 DuckDuckGo 对一个或多个（以'|'分隔的）关键词执行网络搜索。

    该函数会分别查询每个关键词，然后将所有结果根据链接(href)进行去重合并。
    每个子查询都会独立进行最多3次的重试。

    Args:
        query (str): 需要搜索的关键词。如果是多个，请用逗号分隔。
                     例如: "Python asyncio, Python concurrency"
        region (str, optional): 搜索区域代码 (例如, 'us-en', 'cn-zh')。
                                默认为 'wt-wt' (全球，无地区限制)。

    Returns:
        str: 包含所有去重后搜索结果的格式化字符串。每个结果包含标题、链接和摘要，
             并由 '---' 分隔。如果所有查询都失败或无结果，则返回一条相应的错误或提示信息。

    Examples:
    query: "k-mara official website, k-mara"
    company_name: "k-mara"
    """
    # 1. 解析输入：拆分并清理查询词
    try:
        conn = psycopg2.connect(**DB_CONFIG)
            # 创建一个游标对象，用于执行SQL命令
        cur = conn.cursor()
        cur.execute("SELECT result FROM search_results WHERE company_name = %s", (company_name,))
        row = cur.fetchone() # 获取查询结果的第一行

        if row:
            # 如果查询到数据 (缓存命中)
            result = row[0]
            return result
    except:
        pass
        

    queries = [q.strip() for q in query.split('|') if q.strip()]
    if not queries:
        return "错误：查询输入为空或无效。"

    # 2. 结果聚合与去重：使用字典，以 href 为键，实现高效去重
    unique_results_by_href = {}

    # 3. 循环查询：为每个关键词执行搜索
    for single_query in queries:
        for attempt in range(MAX_RETRIES):
            try:
                with DDGS() as ddgs:
                    # 获取原始结果（字典列表）
                    raw_results = ddgs.text(
                        query=single_query,
                        region=region,
                        max_results=MAX_RESULTS_PER_QUERY
                    )
                    
                    # 将结果存入去重字典
                    for r in raw_results:
                        if r['href'] not in unique_results_by_href:
                            unique_results_by_href[r['href']] = r
                
                # 当前关键词搜索成功，跳出重试循环，进行下一个关键词的搜索
                break 
            
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY_SECONDS)

    # 检查是否收集到了任何结果
    if not unique_results_by_href:
        return "搜索完成，但所有关键词均未找到任何相关结果。"

    # 4. 格式化输出：将去重后的字典值转换为格式化字符串
    formatted_results = [
        (
            f"title: {r['title']}\n"
            f"href: {r['href']}\n"
            f"body: {r['body']}"
        )
        for r in unique_results_by_href.values()
    ]
    final_result = "\n---\n".join(formatted_results)
    log_search_to_db(company_name=company_name, query= query, result=final_result)
    return final_result


def LLM_search(query: str):
    """使用具备实时搜索能力的 Gemini 2.5 Pro 模型来回答问题。

    此函数通过将用户的问题与 Google 搜索工具集成，调用 Google 的 Gemini 2.5 Pro 模型。
    它不只是返回原始搜索链接，而是利用搜索到的实时信息来生成一个综合、准确、基于事实的回答。
    这使得它特别适合回答关于最新事件、特定事实或任何其答案在模型训练数据截止日期之后可能发生变化的问题。

    Args:
        query (str): 需要解答的问题或需要查询的信息。该问题应清晰明确，以便模型能有效利用搜索引擎。
                     例如："2024年夏季奥运会在哪里举办？" 或 "介绍一下 Gemini 2.5 Pro 的最新功能"。

    Returns:
        str: 由 Gemini 2.5 Pro 生成的、经过 Google 搜索结果增强和校验的文本答案。
             这是一个自然语言的回答，而非原始数据列表。
    example:
    query: '获取@https://www.mediclim.eu/about-us 中的内容， 返回该公司的信息
    result: Mediclim是一家实验室诊断分销公司，为公共和私营合作伙伴提供服务。 该公司是多个知名供应商的解决方案提供商，包括Biomerieux、Tosoh、Fujirebio、Randox、Microbiologics、Diagast和IDEXX。

Mediclim集团成立于2020年，由其三个子公司组成：Mediclim（罗马尼亚）、Mediclim Eood（保加利亚）和Mediclim AM（摩尔多瓦），是相关市场上的战略性区域 
分销商。 该公司的产品组合涵盖微生物学、免疫学、生物化学、输血、分子生物学、工业微生物学（食品、制药、水）、兽医免疫学和兽医诊断等领域。

Mediclim致力于质量（通过ISO:9001和ISO:13485认证），并致力于在各个专业领域提出最新的解决方案，为改善人口健康做出贡献，其口号是：“诊断的安全与勇气”。

**历史沿革**
*   **2000年：** Mediclim成为Biomerieux在罗马尼亚的独家经销商。
*   **2001-2002年：** 公司获得ISO 9001认证，并进入摩尔多瓦诊断市场。
*   **2009-2017年：** Randox Laboratories、Tosoh Bioscience、URIT、Fujirebio和Diagast等新的顶级供应商加入了Mediclim的产品组合。
*   **2018年：** 成立了保加利亚子公司Mediclim EOOD。
*   **2019-2020年：** 公司获得ISO 13485认证。Adaltis和Prognosis成为其合作伙伴，进一步完善了在分子生物学、ELISA测试和快速COVID-19测试方面的解决方 
案组合。

**联系信息**
*   **总部地址：** 罗马尼亚布加勒斯特第三区Matei Basarab街47号，邮编030671
*   **工作及通信地址：** 罗马尼亚伊尔福夫省奥托佩尼市Avram Iancu街32-34号，邮编075100
*   **电话：** +40 21 322.64.67 / +40 21 322.59.98
*   **传真：** +40 21 320.06.60
*   **电子邮件：** office@mediclim.eu
    """
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
                model="gemini-2.0-flash",
                contents=query,
                config=config,
            )

            return response.text
        except:
            time.sleep(20)
    return 'execution failed'


# --- 使用示例 ---
if __name__ == '__main__':
    # 确保你已经安装了库: pip install -U duckduckgo-search
    
    # 使用包含逗号的复合查询
    composite_query = '''
"kmara healthcare srl" official website | site:linkedin.com/company "kmara healthcare srl" | site:linkedin.com "kmara healthcare srl" | "kmara healthcare srl" contact us | "kmara healthcare srl" email | "kmara healthcare srl" address | "kmara healthcare srl" about us | "kmara healthcare srl" profile | "kmara healthcare srl" news OR "press release" | "kmara healthcare srl" competitors | companies like "kmara healthcare srl" | "kmara healthcare srl" products OR services | "kmara healthcare srl" customer reviews | "kmara healthcare srl" partners | "kmara healthcare srl" exhibitor list | "kmara healthcare srl" partita IVA | "kmara healthcare srl" careers OR hiring | site:linkedin.com/jobs "kmara healthcare srl" | site:linkedin.com "kmara healthcare srl" CEO OR founder | "kmara healthcare srl" management team | "kmara healthcare srl" product catalog filetype:pdf | "kmara healthcare srl" certifications OR "ISO 13485"
'''
    print(f"=== 开始执行复合查询: '{composite_query}' ===")
    final_response = search_ddgs(company_name='k-mara', query=composite_query, region='us-en')
    print("\n=== 最终合并去重后的结果 ===")
    print(final_response)