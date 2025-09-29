import asyncio
import os
import time
from datetime import datetime  # <--- 1. 导入 datetime 模块
from pprint import pprint

# 假设你的 agent factory 和消息类型在这里
# 如果路径不同，请相应修改
from src.agent_factory import create_search_agent, create_exec_agent
from autogen_agentchat.messages import (
    ToolCallSummaryMessage,
    ToolCallExecutionEvent,
    ToolCallRequestEvent,
)

# --- 配置常量 ---
# 输入文件
COMPANY_LIST_FILE = 'company.txt'

# 输出目录
OUTPUT_DIR = './output'
LOG_DIR = './logs'

# 每个公司运行的次数
RUNS_PER_COMPANY = 2

# --- 辅助函数 ---

def read_companies_from_file(filepath: str) -> list[str]:
    """从文件中读取公司列表，每行一个，忽略空行。"""
    if not os.path.exists(filepath):
        print(f"错误: 公司文件 '{filepath}' 不存在。")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        companies = [line.strip() for line in f if line.strip()]
    return companies

async def log_stream_events(stream, log_file_path: str, mode: str = 'w'):
    """将 agent 运行的事件流写入日志文件。"""
    i = 0
    with open(log_file_path, mode, encoding='utf-8') as f:
        async for event in stream:
            if isinstance(event, ToolCallSummaryMessage):
                continue
            
            f.write(f"--- Event Start ---\n")
            if isinstance(event, ToolCallExecutionEvent):
                f.write(f"EventType: ToolCallExecutionEvent\n")
                if event.content and hasattr(event.content[0], 'name'):
                     f.write(f"Tool Name: {event.content[0].name}\n")
                else:
                    f.write(f"Content: {event.model_dump_json(indent=2)}\n")
            else:
                f.write(f"EventType: {type(event).__name__}\n")
                f.write(f"{event.model_dump_json(indent=2)}\n")
            
            f.write(f"--- Event End ---\n\n")
            f.flush()

            if i > 0 and i % 3 == 0:
                time.sleep(10)
            i += 1

async def process_company(company_name: str, run_number: int):
    """
    对单个公司执行完整的调查和任务拆分流程。
    
    Args:
        company_name (str): 要调查的公司名称。
        run_number (int): 当前是第几次运行（用于日志打印）。
    """
    print(f"--- 开始处理: {company_name} (第 {run_number} 次) ---")

    # --- 主要修改部分在这里 ---
    # 2. 生成一个格式化的时间戳字符串，例如 '20231027_153000'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 清理公司名称中的非法字符，使其适合做文件名
    sanitized_company_name = company_name.replace(' ', '_').replace('/', '-').replace('\\', '-')
    
    # 3. 使用时间戳来构建独一无二的文件名
    #    示例: Tashikin_task_20231027_153000.md
    log_filename = f"{sanitized_company_name}_log_{timestamp}.log"
    task_filename = f"{sanitized_company_name}_task_{timestamp}.md"
    
    log_filepath = os.path.join(LOG_DIR, log_filename)
    task_filepath = os.path.join(OUTPUT_DIR, task_filename)
    # --- 修改结束 ---

    # 1. 初始化 Agent
    try:
        search_agent = create_search_agent()
        exec_agent_list = [create_exec_agent(i) for i in range(3)]
    except Exception as e:
        print(f"错误: 初始化 Agent 失败 - {e}")
        return

    # 2. 运行 Search Agent 进行初步调查和任务拆分
    try:
        print(f"  [1/2] 运行 Search Agent 进行任务拆分...")
        search_task = f'公司名称：{company_name}'
        
        # 确保 search_agent 使用的临时 task 文件被清空
        # 注意: 理想情况下, search_agent 应该接受一个输出路径参数
        temp_task_file = './output/task.md'
        with open(temp_task_file, 'w', encoding='utf-8') as f:
            pass

        stream_search = search_agent.run_stream(task=search_task)
        await log_stream_events(stream_search, log_filepath, mode='w')
        
        # 读取 search_agent 生成的任务清单
        with open(temp_task_file, 'r', encoding='utf-8') as f:
            generated_task_list = f.read()

        # 将生成的任务清单保存到本次运行的专属时间戳文件中
        with open(task_filepath, 'w', encoding='utf-8') as f:
            f.write(generated_task_list)
        
        print(f"  任务清单已生成并保存至: {task_filepath}")

    except Exception as e:
        print(f"  错误: Search Agent 运行时发生错误 - {company_name}: {e}")
        return

    # 3. 运行 Execution Agents 执行具体任务
    if not generated_task_list.strip():
        print("  警告: 生成的任务清单为空，跳过 Execution Agents。")
        return

    print(f"  [2/2] 运行 Execution Agents 执行子任务...")
    for i, agent in enumerate(exec_agent_list):
        try:
            print(f"    - Agent {i+1} 开始执行...")
            exec_task = f'''你是负责完成第{i + 1}部分的agent， 整体的任务清单如下所示：
            {generated_task_list}'''
            
            stream_exec = agent.run_stream(task=exec_task)
            await log_stream_events(stream_exec, log_filepath, mode='a')
            print(f"    - Agent {i+1} 执行完成。")

        except Exception as e:
            print(f"  错误: Execution Agent {i+1} 运行时发生错误 - {company_name}: {e}")
            continue

    print(f"--- 完成处理: {company_name} (第 {run_number} 次) ---")
    print(f"详细日志请查看: {log_filepath}\n")


async def main():
    """主函数，负责读取公司列表并分发任务。"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    companies = read_companies_from_file(COMPANY_LIST_FILE)
    if not companies:
        print("公司列表为空或文件不存在，程序退出。")
        return

    print(f"成功读取 {len(companies)} 家公司，准备开始处理...")
    
    for company in companies:
        for i in range(RUNS_PER_COMPANY):
            await process_company(company, run_number=i + 1)
            
            if i < RUNS_PER_COMPANY - 1:
                print(f"  在下一次运行前等待 10 秒...")
                time.sleep(10)
        
        print(f"处理完公司 '{company}' 的所有运行，等待 30 秒...")
        time.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())