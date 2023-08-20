#!/usr/bin/python3
import os,sys,shutil
url=sys.argv[1]

if url=="do-update":
    print("entering app dir")
    os.chdir(os.path.dirname(__file__)+"/AppDir")
    appnotupdatedcnt=0
    for app in os.listdir():
        if os.path.isdir(app):
            print(f"updating {app} if possible")
            os.chdir(app)
            x=os.system("git pull")
            if not x==0:
                print(f"git failed with code {x}! Is it installed?")
                appnotupdatedcnt=appnotupdatedcnt+1
                continue
            if os.path.isdir("AppRegister"):
                for file in os.listdir("AppRegister"):
                    if file.endswith(".app") and os.path.isfile("AppRegister/"+file):
                        print(f"copying entry {file}")
                        shutil.copyfile("AppRegister/"+file,f"../../AppRegister/{file}")
                    elif file=="LivingDirectory":
                        print("Found file living directory, copying...")
                        f=open("LivingDirectory","r")
                        dest=f.read().split("\n")[0]
                        shutil.copytree(".",dest)
                        print("done")
                print("done")
            os.chdir('..')
    if appnotupdatedcnt>0:
        print(f"{appnotupdatedcnt} apps not updated!")
    exit()

print("entering app dir")
os.chdir(os.path.dirname(__file__)+"/AppDir")
print("find name...")
name=url.split('/')[-1]
print("cloning...")
x=os.system(f"git clone '{url}' '{name}'")
if not x==0:
    print(f"git failed with code {x}! Is it installed?")
    exit(x)
print("entering app dir...")
os.chdir(name)
print("finding app files...")
if os.path.isdir("AppRegister"):
    for file in os.listdir("AppRegister"):
        if file.endswith(".app") and os.path.isfile("AppRegister/"+file):
            print(f"copying entry {file}")
            shutil.copyfile("AppRegister/"+file,f"../../AppRegister/{file}")
        elif file=="LivingDirectory":
            print("Found file living directory, copying...")
            f=open("LivingDirectory","r")
            dest=f.read().split("\n")[0]
            shutil.copytree(".",dest)
            print("done")
    print("done")
else:
    print("not found, generating them instead")
    print("currently not implemented... come back later, or implement yourself.")