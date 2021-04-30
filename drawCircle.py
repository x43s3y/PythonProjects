import turtle

turtle.colormode(255)

window = turtle.Screen()
window.title("circle motion")
window.bgcolor("pink")

red,green,blue = 100,255,0

draw = turtle.Turtle()
draw.color(red,green,blue)

radius = 150

for i in range(12):
    try:
        draw.circle(radius)
        draw.penup()
        draw.setposition(i*0, 10)
        draw.left(30)
        draw.pendown()
        green = green - 20
        blue = blue + 20
        draw.color(red,green,blue)
        turtle
    except Exception as e:
        print(e)

window.mainloop()