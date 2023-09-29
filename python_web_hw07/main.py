import asyncio
from collections.abc import Iterable
import os

from connect_db import AsyncDBSession
from my_select import select_statement
    
        
def print_sql(result):
    data = result.all()
    keys = list(result.keys())

    widths = []
    columns = []
    tavnit = '|'
    separator = '+'

    try:
        terminal_width = int(str(os.get_terminal_size()).split(",")[0].split("columns=")[1])
    except ValueError:
        terminal_width = 150
    end_of_width = 1
    for index, cd in enumerate(keys):
        end_of_width += 3
        if end_of_width >= terminal_width:
            break
        max_col_length = max(list(map(lambda x: len(str(x[index])), data)))
        max_col_length = max(max_col_length, len(cd))
        if end_of_width + max_col_length > terminal_width:
            max_col_length = terminal_width - end_of_width
        end_of_width += max_col_length
        widths.append(max_col_length)
        columns.append(cd)

    for w in widths:
        #tavnit += " %-"+"%ss |" % (w,)
        tavnit += " %-"+"%s.%ss |" % (w,w)
        separator += '-'*w + '--+'

    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in data:
        line = []
        for el in row:
            if isinstance(el, list):
                line.append(", ".join(list(map(str, el))))
            else:
                line.append(el)
        print(tavnit % tuple(line))
    print(separator)


async def main():
    async with AsyncDBSession() as session:
        while True:
            user_input = input("Enter the number of query from 1 to 12 or 'exit': ")
            if user_input.strip().casefold() == "exit":
                exit(0)
            try:
                user_input = int(user_input)
            except ValueError:
                print("Try again")
                continue
            if not 1 <= user_input <= 12:
                print("Try again")
                continue

            stmt = select_statement(user_input)
            result = await session.execute(stmt)
            print_sql(result)
    
    
if __name__ == "__main__":
    asyncio.run(main())
