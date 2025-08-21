import asyncio
# 修正 #1: 导入正确的类名 CrawlerHub
from crawl4ai import CrawlerHub

def get_meaningful_html(url: str) -> str:
    """
    使用 crawl4ai 库获取给定URL加载完全后的、有意义的HTML内容。

    该函数会自动处理JavaScript渲染，并清洗掉页面中的广告、导航栏、
    页脚等非核心内容，返回对语言模型友好的干净HTML。

    Args:
        url (str): 需要抓取的目标网站URL。

    Returns:
        str: 清洗和处理后的HTML内容字符串。如果抓取失败，
             则返回一个包含错误信息的字符串。
    """
    print(f"[*] 正在使用 crawl4ai 抓取并解析URL: {url}")
    
    # 修正 #2: 实例化正确的类 CrawlerHub
    crawler = CrawlerHub()

    try:
        # 修正 #3: 使用 .run() 方法，它会自动处理事件循环
        result = crawler.run(url=url)
        
        # result.html 包含了清洗后的HTML内容
        if result and result.html:
            print(f"[+] 成功获取并清洗了URL: {url}")
            return result.html
        else:
            return f"错误: 抓取URL '{url}' 后未能提取到有效HTML内容。"
            
    except Exception as e:
        # 捕获所有可能的异常，如网络超时、无效URL等
        error_message = f"错误: 抓取URL '{url}' 时发生异常. 详情: {e}"
        print(f"[-] {error_message}")
        return error_message

# --- 使用示例 (无需修改) ---
if __name__ == "__main__":
    # 示例1: 抓取一个有大量动态内容和模板代码的博客文章
    test_url_success = "https://www.deeplearning.ai/the-batch/a-roadmap-for-building-trustworthy-ai/"
    
    meaningful_content = get_meaningful_html(test_url_success)
    
    print("\n" + "="*50)
    print("抓取到的有意义HTML内容 (前1000个字符):")
    print("="*50)
    if meaningful_content.startswith("错误:"):
        print(meaningful_content)
    else:
        print(meaningful_content[:1000])
        print("\n...")
        print(f"\n[i] 总内容长度: {len(meaningful_content)} 字符")
        
    print("\n" + "="*50)
    
    # 示例2: 抓取一个不存在的URL来测试错误处理
    test_url_fail = "https://this-is-an-invalid-domain-12345.com"
    error_content = get_meaningful_html(test_url_fail)
    
    print("\n" + "="*50)
    print("测试错误处理:")
    print("="*50)
    print(error_content)