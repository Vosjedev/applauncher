
def run(appdata: dict):
    print("conf: starting configurator...")
    from prompt_toolkit import Application
    from prompt_toolkit.buffer import Buffer
    from prompt_toolkit.layout.containers import  VSplit, HSplit, Window
    from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
    from prompt_toolkit.layout import ScrollablePane, Layout, FloatContainer, Float
    from prompt_toolkit.widgets import Frame, TextArea, Box, Checkbox, Button, Dialog, Label
    from prompt_toolkit.application.current import get_app
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.key_binding.bindings import focus
    from prompt_toolkit.validation import Validator
    from time import sleep
    
    global Cancel
    Cancel=False
    
    # validators for arg types
    class _validators():
        def _intfn(self,text):
            return type(text)==int
        int=Validator.from_callable(_intfn,error_message="Error: not a number: This option requires an integer as input")
    validators=_validators()
    
    class _buttons():
        class _handelers():
            def start(self):
                # make sure all inputs are correct
                errors=dict()
                for arg in args.names:
                    if args.types[arg]=='int':
                        if not args.inputs[arg].text.isnumeric():
                            errors[arg]="argument requires an integer, but a non-integer input was given"
                for arg in args.rpositionals:
                    if args.inputs[arg].text=='':
                        errors[arg]="Required argument"
                if len(errors)>0:
                    message="The following errors where found in the config:"
                    for error in errors:
                        message=f"{message}\n{error}: {errors[error]}"
                    PopUp(title="Errors where found",message=message)
                    return
                get_app().exit()
            def cancel(self):
                global Cancel
                Cancel=True
                get_app().exit()
            def PopUpAccept(event):
                floatcontainer.floats.clear()
                layout.focus(root_container)
        handelers=_handelers()
        
        start=Button(text="start",handler=handelers.start)
        cancel=Button(text="cancel",handler=handelers.cancel)
        
    buttons=_buttons()
    
    def PopUp(title,message):
        popup_layout=Dialog(
            title=title,
            body=HSplit([
                Label(text=title),
                Window(FormattedTextControl(text=message))
            ]),
            buttons=[Button(text="Ok",handler=buttons.handelers.PopUpAccept)]
        )
        float=Float(popup_layout)
        floatcontainer.floats.append(float)
        layout.focus(popup_layout)
        float.attach_to_window=root_container
        # while float in floatcontainer.floats:
        #     sleep(.1)
    
    print(f"conf: configuring app {appdata['ID']}")
    
    def start_button():
        get_app().exit()
    
    print('conf: sorting args...')
    class _args():
        names=list()
        positionals=list()
        rpositionals=list()
        inputs=dict()
        types=dict()
        descriptions=dict()       
    args=_args()
    
    for arg in appdata['ArgsData']:
        if arg[0] in args.names:
            print(f"conf: Error: arg already present: {arg[0]}, skipping")
            continue
        args.names.append(arg[0])
        if arg[2].startswith("pos:") or arg[2].startswith("rpos:"):
            args.types[arg[0]]=arg[2].split(":")[1]
            args.positionals.append(arg[0])
            if arg[2].startswith("rpos:"):
                args.rpositionals.append(arg[0])
        else:
            args.types[arg[0]]=arg[2]
        args.descriptions[arg[0]]=arg[1]
    
    print("conf: generating arg inputs...")
    x=0
    while x<=len(args.names)-1: # custom 'for' loop to fix issues when removing parts from loop
        arg=args.names[x]
        if args.types[arg]=='str':
            args.inputs[arg]=TextArea(height=1,name='> ', focus_on_click=True, multiline=False)
        elif args.types[arg]=='int':
            args.inputs[arg]=TextArea(height=1,name='> ', focus_on_click=True, validator=validators.int, multiline=False)
        elif args.types[arg]=='switch':
            args.inputs[arg]=Checkbox("Enable")
        else:
            print(f"conf: Error: invalid arg type {args.types[arg]} for arg {arg}")
            args.names.remove(arg)
            x=x-1
        x=x+1
    
    print('conf: generating layout...')

    ConfigLayout=list()
    
    for arg in args.names:
        ConfigLayout.append(
            Frame(
                body=HSplit([
                    Window(FormattedTextControl(text=f"{arg}"),height=1),
                    Window(FormattedTextControl(text=args.descriptions[arg]),height=1),
                    Frame(args.inputs[arg])
                    ])
            )
        )
    
    root_container=HSplit([
        Frame(
            title=f"Config for {appdata['Name']}",
            body=VSplit([
                Window(FormattedTextControl(
                    text="Here you can configure the options for this application.\n"\
                        "Navigate by clicking or using tab and shift-tab.\n"\
                        "when done, press Start, and the app will start. Or, press control-c to cancel.\n"
                ),height=3),
                HSplit([
                    buttons.start,
                    buttons.cancel
                ])
               
            ])
        ),
        Box(
            body=ScrollablePane(HSplit(ConfigLayout)),
            padding=1
        )
    ])
    
    floatcontainer=FloatContainer(root_container,floats=[]) # put root in a floatcontainer to be able to handel pop-ups later
    
    layout = Layout(container=floatcontainer)
    
    print("conf: preparing keybinds...")
    kb = KeyBindings()
    @kb.add("c-c")
    def exit(event) -> None:
        global Cancel
        Cancel=True
        get_app().exit()

    kb.add("tab")(focus.focus_next)
    kb.add("s-tab")(focus.focus_previous)
    
    print("conf: starting...")
    
    cmd=None
    
    application = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True)
    application.run()
    
    if Cancel:
        print('conf: user canceled')
        return None
    
    print("conf: composing command...")
    
    cmd=f"{appdata['Exec']}"
    for arg in args.names:
        if arg in args.positionals:
            continue
        if args.types[arg]=='str':
            if args.inputs[arg].text=='':
                print(f"arg {arg} empty")
                continue
            else:
                print(f"arg {arg} set to {args.inputs[arg].text}")
                cmd=f"{cmd} {arg} '{args.inputs[arg].text}'"
        elif args.types[arg]=='switch':
            if args.inputs[arg].checked:
                cmd=f"{cmd} {arg}"
        elif args.types[arg]=='int':
            if args.inputs[arg].text.isnumeric() and not args.inputs[arg].text=='':
                cmd=f"{cmd} {arg} {args.inputs[arg].text}"
                
    for arg in args.positionals:
        if arg in args.rpositionals:
            cmd=f"{cmd} '{args.inputs[arg].text}'"
        elif not args.inputs[arg].text=='':
                cmd=f"{cmd} '{args.inputs[arg].text}'"
            
    
    return cmd