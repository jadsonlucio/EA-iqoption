import tkinter as tk
import pytesseract.pytesseract as pt
import pyautogui
import arquivo

from time import sleep
from PIL import Image
from thread_file import thread

class janela_trader(tk.Toplevel):
    def __init__(self,janela_inicial):
        tk.Toplevel.__init__(self,janela_inicial)

        self.pos_ini = '+0+0'
        self.resolucao = str(pyautogui.size()[0]) + 'x' + str(pyautogui.size()[1])
        self.macro_ativo=False

        self.janela_inicial = janela_inicial
        self.geometry(self.resolucao + self.pos_ini)
        self.wm_attributes("-topmost", True)
        self['background'] = 'white'
        self.wm_attributes("-transparentcolor", "white")
        self.winfo_toplevel()
        self.overrideredirect(True)
        self.iniciar_componentes()

    def iniciar_componentes(self):
        pt.tesseract_cmd = r'Tesseract-OCR/tesseract.exe'
        self.kwargs=arquivo.get_kwargs_posicao_preco()
        self.url_saldo=self.janela_inicial.kwargs['saldo_url']+'/'+self.janela_inicial.kwargs['saldo_name']
        self.macro_ativo=True
        self.array_precos=[]
        self.cont_segundos=0

        self.text_saldo_inicial=tk.StringVar()
        self.text_saldo_atual=tk.StringVar()
        self.text_lucro=tk.StringVar()
        self.text_tempo=tk.StringVar()

        self.text_saldo_inicial.set('Saldo inicial:$00.00')
        self.text_saldo_atual.set('Saldo atual:$00.00')
        self.text_lucro.set("Lucro:$00.00")


        self.frame_infos=tk.Frame(self,width=200,height=150)
        self.frame_infos.pack_propagate(False)
        self.frame_infos.config(borderwidth=3,highlightbackground='#3E4149')
        self.frame_infos.pack(anchor=tk.NW)

        self.saldo_inicial_label = tk.Label(self.frame_infos, textvariable=self.text_saldo_inicial, font=("Arial", 14))
        self.saldo_inicial_label.config(background='whitesmoke')
        self.saldo_inicial_label.pack(anchor=tk.NW)

        self.saldo_atual_label=tk.Label(self.frame_infos,textvariable=self.text_saldo_atual,font=("Arial",14))
        self.saldo_atual_label.config(background='whitesmoke')
        self.saldo_atual_label.pack(anchor=tk.NW)

        self.lucro_label=tk.Label(self.frame_infos,textvariable=self.text_lucro,font=("Arial",14))
        self.lucro_label.config(background='whitesmoke')
        self.lucro_label.pack(anchor=tk.NW)

        self.text_tempo_label = tk.Label(self.frame_infos, textvariable=self.text_tempo, font=("Arial", 14))
        self.text_tempo_label.config(background='whitesmoke')
        self.text_tempo_label.pack(anchor=tk.NW)


        thread_main=thread(self.main_function)
        thread_main.start()

    def main_function(self):
        while(self.macro_ativo):

            if(self.cont_segundos%10==0 or self.cont_segundos==0):
                self.atualizar_saldo()
                self.cont_segundos=self.cont_segundos+4
            self.cont_segundos=self.cont_segundos+1
            self.atualizar_textos()
            sleep(1)


    def adcionar_saldo(self,string=None):
        string_numero=""
        linha_escolhida=""
        for linha in string.split('\n'):
            for char in linha:
                if(char=='$' or char=='s' or char=='S'):
                    linha_escolhida=linha
            if(linha_escolhida):
                break
        for char in linha_escolhida:
            if (char.isnumeric()):
                string_numero = string_numero + char
            elif (char == 'o' or char == 'O'):
                string_numero = string_numero + '0'
        if(len(string_numero)>2):
            self.array_precos.append(float(string_numero[:-2]+'.'+string_numero[-2:]))
            arquivo.salvar_arquivo(self.url_saldo,[self.array_precos[-1]])

    def atualizar_saldo(self):

        self.pontos_saldo=[int(valor) for valor in self.kwargs[self.resolucao].split(',')]

        pos_x1=self.pontos_saldo[0]
        pos_y1=self.pontos_saldo[1]
        pos_x2=self.pontos_saldo[2]
        pos_y2=self.pontos_saldo[3]

        self.print_screen=pyautogui.screenshot(region=(pos_x1,pos_y1,pos_x2,pos_y2))
        self.print_screen_resize=self.print_screen.resize((int(pos_x2-pos_x1)*4,int(pos_y2-pos_y1)*4),Image.ANTIALIAS)
        self.saldo_string=pt.image_to_string(self.print_screen_resize)
        self.adcionar_saldo(self.saldo_string)

    def atualizar_textos(self):
        self.text_saldo_inicial.set("Saldo inicial:$"+str(self.array_precos[0]))
        self.text_saldo_atual.set("Saldo atual:$"+str(self.array_precos[-1]))
        self.text_lucro.set("Lucro:$"+str(self.array_precos[-1]-self.array_precos[0])[:5])



class saldo():
    def __init__(self,janela_inicial):
        self.janela_inicial=janela_inicial
        self.iniciar_variaveis()

    def iniciar_variaveis(self):
        pt.tesseract_cmd = r'Tesseract-OCR/tesseract.exe'
        self.kwargs=arquivo.get_kwargs_posicao_preco()
        self.url_saldo=self.janela_inicial.kwargs['saldo_url']+'/'+self.janela_inicial.kwargs['saldo_name']
        self.array_precos=[]
        self.resolucao = str(pyautogui.size()[0]) + 'x' + str(pyautogui.size()[1])
        self.cont_seconds=0
        self.macro_ativo=False

    def rodar_script_getsaldo(self):
        self.macro_ativo=True
        script=thread(self.run)
        script.start()

    def parar_script_getsaldo(self):
        self.macro_ativo=False

    def run(self):
        while(self.macro_ativo):
            if(self.cont_seconds%5==0):
                self.atualizar_saldo()
            self.cont_seconds=self.cont_seconds+1
            sleep(1)

    def adcionar_saldo(self,string=None):
        string_numero=""
        linha_escolhida=""
        for linha in string.split('\n'):
            for char in linha:
                if(char=='$' or char=='s' or char=='S'):
                    linha_escolhida=linha
            if(linha_escolhida):
                break
        for char in linha_escolhida:
            if (char.isnumeric()):
                string_numero = string_numero + char
            elif (char == 'o' or char == 'O'):
                string_numero = string_numero + '0'
        if(len(string_numero)>2):
            self.array_precos.append(float(string_numero[:-2]+'.'+string_numero[-2:]))
            arquivo.salvar_arquivo(self.url_saldo,[self.array_precos[-1]])

    def atualizar_saldo(self):
        self.pontos_saldo=[int(valor) for valor in self.kwargs[self.resolucao].split(',')]

        pos_x=self.pontos_saldo[0]
        pos_y=self.pontos_saldo[1]
        width=self.pontos_saldo[2]
        heigth=self.pontos_saldo[3]

        self.print_screen=pyautogui.screenshot(region=(pos_x,pos_y,width,heigth))
        self.print_screen_resize=self.print_screen.resize((width*3,heigth*3),Image.ANTIALIAS)
        self.saldo_string=pt.image_to_string(self.print_screen_resize)
        self.adcionar_saldo(self.saldo_string)

