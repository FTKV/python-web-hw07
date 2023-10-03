import asyncio

import prettytable

from connect_db import AsyncDBSession
from my_select import select_statement
from window import make_window, window_update
    
        
def output_table(result):
    data = result.all()
    keys = list(result.keys())
    table = prettytable.PrettyTable(keys)
    for key in keys:
        if key.casefold().find("list") != -1:
            table.align[key] = "l"
    for row in data:
        line = []
        for el in row:
            if isinstance(el, list):
                line.append(", ".join(list(map(str, el))))
            else:
                line.append(el)
        table.add_row(line)
    return table


async def handle_db(session, aioqueue, aiocondition):
    async with session:
        while True:
            error_flag = False
            async with aiocondition:
                await aiocondition.wait()
                user_input = await aioqueue.get()
            if user_input.strip().casefold() == "exit":
                break
            try:
                user_input = int(user_input)
                if not 1 <= user_input <= 12:
                    result = "Try again"
                    error_flag = True
            except ValueError:
                result = "Try again"
                error_flag = True
            if not error_flag:
                stmt = select_statement(user_input)
                result = await session.execute(stmt)
                result = output_table(result)
            async with aiocondition:
                await aioqueue.put(result)
                aiocondition.notify()

async def main():
    session = AsyncDBSession()
    aioqueue = asyncio.Queue(maxsize=1)
    aiocondition = asyncio.Condition()
    root = make_window(aioqueue, aiocondition)
    window_task = asyncio.create_task(window_update(root))
    db_task = asyncio.create_task(handle_db(session, aioqueue, aiocondition))
    tasks = await asyncio.wait([window_task, db_task], return_when=asyncio.FIRST_COMPLETED)
    [task.cancel() for task in tasks[1]]
    await session.close()
    
    
if __name__ == "__main__":
    asyncio.run(main())
