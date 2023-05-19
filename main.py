from pantalla import Pantalla
import ttkbootstrap as ttk

if __name__ == '__main__':
    screen = ttk.Window(themename = 'minty')
    custom_style = ttk.Style(theme='minty')
    custom_style.configure('.', font = ('DM Sans', 10))
    Pantalla(screen)
    screen.mainloop() 