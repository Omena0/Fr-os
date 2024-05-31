import engine as ui


root = ui.Root(
    'Test'
).show()

box = ui.Area(
    (100,100),
    100,
    100
).add(root)

sineInOut = ui.EasingOptions('sine')

opt = ui.AnimationOptions(300,sineInOut,(100,100),(400,200))

anim = ui.Animation(box,opt)

anim.start()

ui.mainloop()