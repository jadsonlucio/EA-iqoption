import tkinter as tk

import arquivo
from tkinter import ttk
from time import sleep
from thread_file import thread
from script import script
from janela_captura import janela_captura
from janela_trader import janela_trader,saldo

class frame_principal(tk.Frame):
    def __init__(self,janela,container):
        tk.Frame.__init__(self,container)
        self.nome='frame_principal'
        self.janela=janela
        self.script=script()
        self.macro_ativo=False

    def verificar_arquivo_informacoes(self):
        array=arquivo.ler_arquivo(self.janela.kwargs['infoativacao_url']+'/'+self.janela.kwargs['infoativacao_name'])
        kargs=arquivo.converter_array_to_dictonary(array)
        return kargs

    def ativar_macro(self):
        if(not self.macro_ativo):
            arquivo.limpar_arquivo(self.janela.kwargs['operacoes_url'] + '/' + self.janela.kwargs['operacoes_name'])
            self.saldo=saldo(self.janela)
            self.saldo.rodar_script_getsaldo()
            self.janela.wm_state('iconic')
            self.macro_ativo=True
            self.macro_time=self.box_times.current()
            self.script.carregar_mapeamento()
            self.script.criar_mapeamento()
            self.nova_thread = thread(self.run)
            self.nova_thread.start()
            self.confirm_button.config(text='Desativar macro')
        else:
            self.saldo.parar_script_getsaldo()
            self.macro_ativo=False
            self.confirm_button.config(text='Ativar macro')


    def run(self):
        while(self.macro_ativo):
            self.array_macros = arquivo.ler_arquivo(self.janela.kwargs['operacoes_url']+'/'+self.janela.kwargs['operacoes_name'])
            arquivo.limpar_arquivo(self.janela.kwargs['operacoes_url']+'/'+self.janela.kwargs['operacoes_name'])
            if(len(self.array_macros)>0):
                box_time=self.box_times.current()
                if(box_time==0):
                    macros_time=5
                elif(box_time==1):
                    macros_time=15
                for linha in self.array_macros:
                    self.script.criar_script(linha.decode('utf-8'),macros_time)
                    self.script.rodar_script()

            sleep(0.5)


    def iniciar_componentes(self):
        try:
            imagem_logo = tk.PhotoImage(file='files/iqoption-logo.png')
            self.div1 = tk.Frame(self)
            self.div1.pack_propagate(False)
            self.div1.config(width=100, height=10)
            self.div2 = tk.Frame(self)
            self.div2.pack_propagate(False)
            self.div2.config(width=100, height=5)
            self.label_logo = tk.Label(self, image=imagem_logo)
            self.label_logo.image = imagem_logo
            self.text_label=tk.Label(self,text='Selecione o tempo\ngráfico')
            self.text_label.config(font=('Arial',13),justify=tk.LEFT)
            self.box_times=ttk.Combobox(self)
            self.box_times.config(justify=tk.CENTER, width=6)
            self.confirm_button=tk.Button(self,text='Ativar Macro',font=("Arial",10),command=self.ativar_macro)
            self.confirm_button.config(relief=tk.GROOVE,width=15)
            self.captura_button=tk.Button(self,text='Mapear Coordenadas',font=("Arial",10),command=self.janela.abrir_janela_mapeamento)
            self.captura_button.config(relief=tk.GROOVE, width=15)
            text_times=['5 min','15 min']
            self.box_times['value']=text_times
            self.box_times['state'] = 'readonly'
            self.box_times.current(newindex=0)
            self.div1.grid(row=0, column=0, columnspan=2)
            self.label_logo.grid(row=1, column=0, columnspan=2, padx=20)
            self.div2.grid(row=2,column=0)
            self.text_label.grid(row=3,column=0,padx=20)
            self.box_times.grid(row=3,column=1)
            self.confirm_button.grid(row=4,column=0,columnspan=2,pady=10,padx=20)
            self.captura_button.grid(row=5,column=0,columnspan=2,pady=5,padx=10)
            if(not self.script.carregar_mapeamento()):
                self.confirm_button.config(state='disabled')
        except Exception as e:
            print(str(e))