import asyncio
import datetime

import prettytable

from connect_db import AsyncDBSession
from my_select import select_statement
from window import make_window, window_update


def str_(arg):
    if isinstance(arg, datetime.datetime):
        return arg.date().isoformat()
    else:
        return str(arg)

        
def output_table(result):
    data = result.all()
    keys = [""] + list(result.keys())
    table = prettytable.PrettyTable(keys)
    table.align[keys[0]] = "r"
    for key in keys[1:]:
        if key.casefold().find("list") != -1:
            table.align[key] = "l"
    for i, row in enumerate(data):
        line = [i + 1]
        for el in row:
            if isinstance(el, list):
                line.append(", ".join(list(map(str_, el))))
            else:
                line.append(str_(el))
        table.add_row(line)
    return table


async def handle_db(session, aioqueue, aiocondition):
    async with session:
        while True:
            async with aiocondition:
                await aiocondition.wait()
                num = await aioqueue.get()
            if not num:
                break
            stmt = select_statement(num)
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
