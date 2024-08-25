import engine as ui
from classes import Application, size

if not 'settings' in globals(): settings = {'scale':1}

buttons = ['(','^','C','CE','7','8','9',' * ','4','5','6',' / ','1','2','3',' + ','.','0','=',' - ']

press = []

close = False
slash_button = None

for button in buttons:
    def action(b=button):
        global text, close
        if b == 'C': text.text = ''
        elif b == 'CE': text.text = text.text[:-1]
        elif b == '(':
            if close:
                text.text += ')'
                slash_button.text = ')'
            else:
                text.text += '('
                slash_button.text = '('
            close = not close
        elif b == '=':
            try: text.text = f'{eval(text.text.replace('^','**'))}'
            except Exception as e:
                text.text = f'{e}'
        else:
            text.text += b
        
        if len(text.text) == 0: return
        text.size = min(int(35/(len(text.text)/15)),area.height-5)

    press.append(action)

def open_app(app:Application):
    global buttons, press, text, area, slash_button
    w = ui.Window(
        position = (size[0]//2-size[0]//16,size[1]//2-size[1]//6),
        width = size[0]//8,
        height = size[1]//3,
        title=app.name,
        on_quit=app.quit,
        color = (45,45,45),
        bg_focused_color=(45,45,45)
    ).add(ui.root)
    app.windows.add(w)
    
    # Top Box
    ## Area
    area = ui.Area(
        position=(5,10),
        width=round(w.width-10),
        height=40,
        color=(60,60,60),
        corner_radius=5
    ).add(w)
    
    ## Text
    text = ui.Text(
        position=(10,20),
        text='',
        size=35
    ).add(w,2)
    
    
    # Buttons
    for y in range(5):
        for x in range(4):
            i = x+y*4
            
            a = ui.Button(
                (round(5+x*((w.width-50)/4+10)), round(57+y*(w.height-60)/5)),
                width = round((w.width-20)/4),
                height = round((w.height-75)/5),
                text = buttons[i],
                size = round(w.width/4),
                action = press[i],
                corner_radius = 5,
                color = (55,55,55),
                hover_color = (70,70,70)
            ).add(w,2)
            
            if press[i] == '(':
                slash_button = a



app = Application('calc','Calculator',open_app,ui.nothing,iconPath='assets/calc/calc_icon.png').pin()#add_to_taskbar=False)


