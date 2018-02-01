import tkinter as tk
import pyautogui
import arquivo
import keyboard

from tkinter import messagebox
from time import sleep
from thread_file import thread


class janela_captura(tk.Toplevel):

    def criar_janela_warning(self):
        self.janela_warning=tk.Toplevel(self)
        self.janela_warning.geometry('300x300+0+0')
        self.janela_warning.grab_set()
        self.janela_warning.wm_attributes("-topmost", True)

    def __on_close(self):
        self.frame_principal.captura_button.config(text='Mapear Coordenadas')
        self.destroy()

    def __init__(self, janela_inicial, frame_principal):
        tk.Toplevel.__init__(self, janela_inicial)
        self.pos_ini = '+0+0'
        self.resolucao = str(pyautogui.size()[0]) + 'x' + str(pyautogui.size()[1])

        self.janela_inicial = janela_inicial
        self.frame_principal = frame_principal

        self.protocol("WM_DELETE_WINDOW", self.__on_close)
        self.geometry(self.resolucao + self.pos_ini)
        self.wm_attributes("-topmost", True)
        self['background'] = 'white'
        self.wm_attributes("-transparentcolor", "white")
        self.winfo_toplevel()
        self.overrideredirect(True)

        self.cont_click = 0
        self.iniciar_componentes()

    def iniciar_componentes(self):

        self.frame_textos = tk.Frame(self)
        self.frame_textos.config(background='white')
        self.frame_textos.pack(side=tk.TOP, fill=tk.X)

        self.text_var = tk.StringVar()
        self.text_var.set('0,Coordenadas=0,0')
        self.text_label = tk.Label(self.frame_textos, textvariable=self.text_var, font="-weight bold -size 15")
        self.text_label.config(background='white', foreground='red')
        self.text_label.pack(side=tk.RIGHT, anchor=tk.N)

        self.text_var_alert = tk.StringVar()
        self.text_var_alert.set("Pressione esc para salvar")
        self.text_alert = tk.Label(self.frame_textos, textvariable=self.text_var_alert, font="-weight bold -size 15")
        self.text_alert.config(background='white', foreground='red')
        self.text_alert.pack(side=tk.LEFT, anchor=tk.N)

        self.text_var_objeto = tk.StringVar()
        self.text_var_objeto.set("Mapeando o objeto 1,\npressione espaço para ir pra próxima janela")
        self.text_janela = tk.Label(self.frame_textos, textvariable=self.text_var_objeto)
        self.text_janela.config(font="-weight bold -size 15", background='white', foreground='red')
        self.text_janela.pack(anchor=tk.CENTER)

        self.current_mouse_x = self.winfo_pointerx()
        self.current_mouse_y = self.winfo_pointery()
        self.coordenadas_mapeadas = str(pyautogui.size()[0]) + 'x' + str(pyautogui.size()[1]) + '='
        self.configuracao_mepeamento = 'Config_mapeamento='
        self.ponto_inicial = 0
        self.cont_janela = 1

        self.criar_evento_hotkey()

    def on_closing(self):
        array = []
        array.append(self.coordenadas_mapeadas[:-1])
        array.append(self.configuracao_mepeamento[:-1])
        arquivo.salvar_arquivo('files//mapeamento.txt', array)
        if ('x' in dir(self) and 'y' in dir(self) and 'width' in dir(self) and 'height' in dir(self)):
            array = []
            array.append(self.resolucao + '=' + str(self.x) + ',' + str(self.y) + ',' +
                         str(self.width) + ',' + str(self.height))
            arquivo.salvar_arquivo('files//posições_saldo.txt', array)

        keyboard.remove_all_hotkeys()
        self.destroy()
        self.frame_principal.confirm_button.config(state='normal')
        self.frame_principal.captura_button.config(text='Mapear Coordenadas')


    def add_coordenada(self):
        mouse_x = self.janela_inicial.winfo_pointerx()
        mouse_y = self.janela_inicial.winfo_pointery()
        if (mouse_x != self.current_mouse_x or mouse_y != self.current_mouse_y):
            self.current_mouse_x = mouse_x
            self.current_mouse_y = mouse_y
            self.coordenadas_mapeadas = self.coordenadas_mapeadas + str(mouse_x) + ',' + str(mouse_y) + ','
            self.cont_click = self.cont_click + 1
            self.text_var.set(str(self.cont_click) + ',' + 'Coordenadas' + '=' + str(mouse_x) + ',' + str(mouse_y))

    def add_tela(self):
        if (self.cont_click - self.ponto_inicial - 4 <= 0 and self.cont_janela < 5):
            pass
        elif (self.cont_janela < 5):
            if (self.cont_janela != 4):
                self.configuracao_mepeamento = self.configuracao_mepeamento + '1' + ',' + \
                                               str(
                                                   self.cont_click - self.ponto_inicial - 4) + ',' + '1' + ',' + '2' + '|'
                self.cont_janela = self.cont_janela + 1
                self.ponto_inicial = self.cont_click
                self.text_var_objeto.set(
                    'Mapeando o objeto ' + str(self.cont_janela) + ',\npressione espaço para ir pra próxima janela')
            else:
                self.configuracao_mepeamento = self.configuracao_mepeamento + '1' + ',' + \
                                               str(
                                                   self.cont_click - self.ponto_inicial - 4) + ',' + '1' + ',' + '2' + '|'
                self.cont_janela = self.cont_janela + 1
                if (arquivo.verificar_kwargs('files//posições_saldo.txt', self.resolucao)):
                    self.text_var_objeto.set('Aperte espaço para iniciar o mapeamento do saldo')
                    keyboard.add_hotkey('esc', lambda: self.on_closing())
                else:
                    self.text_var_objeto.set('Você ainda não mapeou o saldo\npressione espaço para mapear')
                    self.text_alert.destroy()
                    self.text_label.destroy()
                keyboard.remove_hotkey('enter')
        else:

            self.frame_textos.destroy()
            self.frame_preencher = tk.Frame(self)
            self.frame_preencher.config(background='gray')
            self.frame_preencher.pack_propagate(False)
            self.frame_preencher.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH, expand=True)
            self.wm_attributes('-alpha', 0.3)

            self.frame_captura = tk.Frame(self)
            self.frame_captura.config(background='white')
            self.frame_captura.pack_propagate(False)

            self.criar_evento_saldo()
            keyboard.remove_hotkey('space')

    def saldo_click_event(self, event):
        if (self.motion_event == False):
            self.motion_event = True
            self.click1_x = event.x
            self.click1_y = event.y
            keyboard.remove_all_hotkeys()
        else:
            self.motion_event = False
            keyboard.add_hotkey('space',lambda :self.on_closing())

    def atualizar_frame_captura(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        if (self.motion_event == True):
            if (self.mouse_x > self.click1_x and self.mouse_y > self.click1_y):
                self.x = self.click1_x
                self.y = self.click1_y
                self.width = abs(self.mouse_x - self.click1_x)
                self.height = abs(self.mouse_y - self.click1_y)
                self.frame_captura.place(x=self.x, y=self.y)
                self.frame_captura.config(width=self.width,
                                          height=self.height)

            if (self.mouse_x < self.click1_x and self.mouse_y < self.click1_y):
                self.x = self.mouse_x
                self.y = self.mouse_y
                self.width = abs(self.mouse_x - self.click1_x)
                self.height = abs(self.mouse_y - self.click1_y)
                self.frame_captura.place(x=self.x, y=self.y)
                self.frame_captura.config(width=self.width,
                                          height=self.height)

            if (self.mouse_x > self.click1_x and self.mouse_y < self.click1_y):
                self.x = self.click1_x
                self.y = self.mouse_y
                self.width = abs(self.mouse_x - self.click1_x)
                self.height = abs(self.mouse_y - self.click1_y)
                self.frame_captura.place(x=self.x, y=self.y)
                self.frame_captura.config(width=self.width,
                                          height=self.height)

            if (self.mouse_x < self.click1_x and self.mouse_y > self.click1_y):
                self.x = self.mouse_x
                self.y = self.click1_y
                self.width = abs(self.mouse_x - self.click1_x)
                self.height = abs(self.mouse_y - self.click1_y)
                self.frame_captura.place(x=self.x, y=self.y)
                self.frame_captura.config(width=self.width,
                                          height=self.height)

    def criar_evento_saldo(self):
        self.frame_preencher.bind('<Button-1>', self.saldo_click_event)
        self.frame_preencher.bind('<Motion>', self.atualizar_frame_captura)
        self.motion_event = False

    def criar_evento_hotkey(self):
        keyboard.add_hotkey('enter', lambda: self.add_coordenada())
        keyboard.add_hotkey('space', lambda: self.add_tela())

if __name__ == '__main__':
    janela_cap = janela_captura()
    janela_cap.mainloop()


