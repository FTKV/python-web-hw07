import asyncio
import tkinter as tk

from async_tkinter_loop import async_handler


class ConsoleText(tk.Text):

    def __init__(self, master=None, aioqueue=None, aiocondition=None, **kw):
        tk.Text.__init__(self, master, **kw)
        self.is_run_enter_handler = False
        self.aioqueue = aioqueue
        self.aiocondition = aiocondition
        #self.insert('1.0', '0>>> ') # first prompt
        # create input mark
        self.mark_set('input', 'insert')
        self.mark_gravity('input', 'left')
        # create proxy
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        # binding to Enter key
        self.enter("first")
        self.bind("<Return>", self.enter)


    def _proxy(self, *args):
        largs = list(args)

        if args[0] == 'insert':
            if self.compare('insert', '<', 'input'):
                # move insertion cursor to the editable part
                self.mark_set('insert', 'end')  # you can change 'end' with 'input'
        elif args[0] == "delete":
            if self.compare(largs[1], '<', 'input'):
                if len(largs) == 2:
                    return # don't delete anything
                largs[1] = 'input'  # move deletion start at 'input'
        result = self.tk.call((self._orig,) + tuple(largs))
        return result

    @async_handler
    async def enter(self, event):
        if self.is_run_enter_handler:
            return
        else:
            self.is_run_enter_handler = True
        error_flag = False
        user_input = self.get('input', 'end')
        if event != "first":
            if user_input.strip().casefold() == "exit":
                user_input = 0
            else:
                try:
                    user_input = int(user_input)
                    if not 1 <= user_input <= 12:
                        result = "Try again"
                        error_flag = True
                except ValueError:
                    result = "Try again"
                    error_flag = True
            if not error_flag:
                async with self.aiocondition:
                    await self.aioqueue.put(user_input)
                    self.aiocondition.notify()
                async with self.aiocondition:
                    await self.aiocondition.wait()
                result = await self.aioqueue.get()
            self.insert('end', f'{result}\n\n')
        self.insert('end', "Enter the number of query from 1 to 12 or 'exit': ")
        # move input mark
        self.mark_set('input', 'insert')
        self.see("end")
        self.is_run_enter_handler = False
        return "break" # don't execute class method that inserts a newline


def make_window(aioqueue, aiocondition):
    root = tk.Tk()
    h = tk.Scrollbar(root, orient='horizontal')
    v = tk.Scrollbar(root)

    h.pack(side = tk.BOTTOM, fill = tk.X)
    v.pack(side = tk.RIGHT, fill = tk.Y)

    tfield = ConsoleText(root, wrap=tk.NONE, bg='black', fg='white', insertbackground='white', xscrollcommand = h.set, yscrollcommand = v.set, aioqueue=aioqueue, aiocondition=aiocondition)
    h.config(command=tfield.xview)
    v.config(command=tfield.yview)

    tfield.pack(expand=1, fill=tk.BOTH)

    return root


async def window_update(root):
    try:
        while root.state():
            root.update()
            await asyncio.sleep(0.01)
    except tk.TclError:
        pass