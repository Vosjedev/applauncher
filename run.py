#!/usr/bin/env python3

print('preparing...')

import os,sys
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style

root=os.path.dirname(__file__)


def ParseAppFile(filename,skipargs=False):
    ParsingArgs=False
    file=open(filename,'r')
    data=file.read()
    data=data.split('\n')
    returndata=dict()
    args=list()
    for entry in data:
        if entry=="@args": # start argparsing if line is @args
            ParsingArgs=True
            if skipargs: # stop parsing if
                break
            continue
        if ParsingArgs: # parse args indexes
            if not ';' in entry:
                continue
            entry=entry.split(';')
            # undo split at escaped ;
            cnt=-1
            for i in entry:
                cnt=cnt+1
                while entry[cnt].endswith('\\'):
                    entry[cnt]=f"{entry[cnt][:-1]};{entry.pop(cnt+1)}"
            # 
            args.append(entry)
        else: # or continue making dictionary
            if not '=' in entry:
                continue
            entry=entry.split('=')
            # undo split at escaped =
            cnt=-1
            for i in entry:
                cnt=cnt+1
                while entry[cnt].endswith('\\'):
                    entry[cnt]=f"{entry[cnt][:-1]}={entry.pop(cnt+1)}"     
            returndata[entry[0]]=entry[1]
    returndata['ArgsData']=args
    returndata['Filename']=filename
    return returndata

print('generating applist...')
Applist=list()
for appfile in os.listdir(path=f"{root}/ClosedAppRegister"):
    infolist=ParseAppFile(f"{root}/ClosedAppRegister/{appfile}",skipargs=True)
    print(infolist['ID'],',',end='',flush=True)
    Applist.append((f"{root}/ClosedAppRegister/{appfile}",infolist["Name"]))
for appfile in os.listdir(path=f"{root}/AppRegister"):
    infolist=ParseAppFile(f"{root}/AppRegister/{appfile}",skipargs=True)
    print(infolist['ID'],',',end='',flush=True)
    Applist.append((f"{root}/AppRegister/{appfile}",infolist["Name"]))
print('')

print("done.")

# it would be appreciated if anyone can make the dialog have NO background at all, not even black. (terminal background color)

AppToStart=radiolist_dialog(
    title="Vosjedev's app launcher",
    text="Please select an app\nyou can do this by navigating using the arrow keys, then pressing space. You can also use the mouse.\nThen, press ok by either using tab to select it and then enter, or clicking it",
    values=Applist
).run()

if AppToStart==None:
    print("User canceled")
    exit(1)

AppData=ParseAppFile(AppToStart)
print("User chose the following app:")
print(AppData)
print("preparing configurator...")
import vosjedev_app_configurator as config

cmd=config.run(AppData)
if cmd==None:
    print('Error: Received None')
    exit(1)

if "@__root_vosje__@" in cmd:
    cmd=cmd.replace("@__root_vosje__@",root,1)

print(f"recieved command: {cmd}")
if "PWD" in AppData:
    os.chdir(AppData["PWD"])
print("running command...")
os.system("cls" if os.name=='nt' else "clear")
x=os.system(cmd)
print(f"Command exited with code {x},")
input("press enter to close...")