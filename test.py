from src.agent_factory import create_search_agent, create_exec_agent
import asyncio
from pprint import  pprint
from autogen_agentchat.messages import ToolCallSummaryMessage, ToolCallExecutionEvent, ToolCallRequestEvent, ToolCallExecutionEvent
import time
async def main():
    with open('./output/task.md', 'w', encoding='utf-8') as f:
        pass
    running = '''
K-MARA Healthcare Corporation
'''
    # running = running.strip('\n').split('\n')
    running = [running]
    
    for t in running:
        for r in range(2):
            search_agent = create_search_agent()
            exec_agent_list = [create_exec_agent(i) for i in range(3)]
            root = './log.txt'
            try:
                task = f'公司名称：{t}' 
                st = search_agent.run_stream(task = task)
                i = 0
                with open(root, 'w', encoding='utf-8') as f:
                    async for r in st:
                        if isinstance(r, ToolCallSummaryMessage):
                            continue
                        elif isinstance(r, ToolCallExecutionEvent):
                            print('ToolCallExecutionEvent:', file = f)
                            print(r.content[0].name, file = f)
                        else:
                            print(type(r), file= f)
                            print(r.model_dump_json(), file = f)
                        print('-' * 90, file = f)
                        if i % 3== 0:
                            time.sleep(30)
                        i += 1
            except:
                pass
            with open('./output/task.md', 'r', encoding='utf-8') as task_doc:
                task = task_doc.read()
            for j in range(3):
                agent = exec_agent_list[j]
                temp_task = f'''你是负责完成第{j + 1}部分的agent， 整体的任务清单如下所示：
                {task}'''
                st = agent.run_stream(task = temp_task)
                with open(root, 'a', encoding='utf-8') as f:
                    async for r in st:
                        if isinstance(r, ToolCallSummaryMessage):
                            continue
                        elif isinstance(r, ToolCallExecutionEvent):
                            print('ToolCallExecutionEvent:', file = f)
                            print(r, file = f)
                        else:
                            print(type(r), file= f)
                            print(r.model_dump_json(), file = f)
                        print('-' * 90, file = f)
            return
        time.sleep(30)


asyncio.run(main())