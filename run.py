#!/usr/bin/env python3

print('preparing...')

import os,sys

root=os.path.dirname(__file__)

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, HSplit, FloatContainer, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout


print('generating applist...')
Applist=[]
for appfile in os.listdir(path=f"{root}/AppRegister")


# root_container = Window([
#     HSplit([
#         Window(content=FormattedTextControl(text="Vosjedev's application launcher")),
#         HSplit(Applist)
#     ])
# ])

# layout = Layout(root_container)

# app = Application(layout=layout, full_screen=True)
# app.run()