import tkinter as tk
from os.path import split
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from arquivo import salvar_arquivo

class janela_url(tk.Toplevel):
    def __init__(self,janela_inicial):
        tk.Toplevel.__init__(self,janela_inicial)
        self.title('Janela urls')
        self.resizable(0, 0)
        info=janela_inicial.get_info()
        self.geometry(str(int(info[2]*0.86))+'x'+str(int(info[3]/2))+''
                                  '+'+str(info[0]+30)+'+'+str(info[1]+30))
        self.janela_inicial=janela_inicial
        self.iniciar_componenetes()
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        result=messagebox.askyesno('Sair','Tem certeza que deseja sair')
        if(result==1):
            self.janela_inicial.destroy()

    def show(self):
        self.deiconify()
        self.transient(self.janela_inicial)
        self.grab_set()

    def choice_file(self,func):
        if(func=='operacoes'):
            self.url_operacoes = split(filedialog.askopenfile().name)
            self.text_box_var.set(self.url_operacoes[1])
        if(func=='saldo'):
            self.url_saldo = filedialog.askdirectory()
            self.text_box_var2.set('saldos.txt')
            open(self.url_saldo+'/'+'saldos.txt','w')

    def salvar_urls(self):
        if(len(self.url_operacoes)):
            array=[]
            array.append('operacoes_url='+self.url_operacoes[0])
            array.append('operacoes_name='+self.url_operacoes[1])
            array.append('saldo_url=' + self.url_operacoes[0])
            array.append('saldo_name=' + 'saldo.txt')
            salvar_arquivo('files//informações.txt',array)
            self.janela_inicial.iniciar_componentes()
            self.janela_inicial.focus_force()
            self.destroy()
        else:
            pass

    def iniciar_componenetes(self):
        self.url_operacoes=''
        self.text_box_var=tk.StringVar()
        self.text_box_var2=tk.StringVar()

        self.text_info_opc=tk.Label(self,text="Arquivo de operacões:")
        self.text_info_opc.config(font=('Arial',12))
        self.text_box_opc=tk.Label(self,textvariable=self.text_box_var)
        self.text_box_opc.config(justify=tk.RIGHT)
        self.botao_select_opc=ttk.Button(self,text="Selecionar")

        self.botao_confirmar=ttk.Button(self,text="Comfirmar",command=self.salvar_urls)

        self.text_info_opc.grid(row=0, column=0)
        self.text_box_opc.grid(row=0,column=2)
        self.botao_select_opc.grid(row=0,column=1)

        self.botao_confirmar.place(x=260,y=110)

        self.botao_select_opc.bind('<Button-1>',lambda event:self.choice_file('operacoes'))

