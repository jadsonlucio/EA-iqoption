import tkinter as tk
import arquivo
from tkinter import messagebox
from frame_principal import frame_principal
from janela_url import janela_url
from janela_captura import janela_captura,keyboard


class Janela_inicial(tk.Tk):

    def get_info(self):
        pos_x=self.winfo_x()
        pos_y=self.winfo_y()
        width=self.winfo_width()
        height=self.winfo_height()
        return [pos_x,pos_y,width,height]

    def __init__(self):
        tk.Tk.__init__(self)
        self.bind('<Key>',self.verificar_atalho)
        self.protocol("WM_DELETE_WINDOW", self.__on_close)
        self.string_digitada=''
        self.container=tk.Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.pack(fill='both', expand=1)
        self.frames={}

        new_frame=frame_principal(self,self.container)
        new_frame.grid(row=0,column=0,sticky='NSEW')
        self.frames[new_frame.nome]=new_frame

        self.iniciar_componentes()

    def verificar_atalho(self,event):
        self.string_digitada=self.string_digitada+event.char
        if(len(self.string_digitada)>2 and self.string_digitada[-3:]=='url'):
            self.abrir_janela_url()
        if (len(self.string_digitada) > 4 and self.string_digitada[-5:] == 'clear'):
            arquivo.resetar_configuracao()
            self.destroy()
        if(len(self.string_digitada) > 2 and self.string_digitada[-3:] == 'web'):
            pass

    def atualizar_frame(self,nome_class):
        self.current_frame=self.frames[nome_class]
        self.current_frame.tkraise()

    def abrir_janela_url(self):
        self.janela_url = janela_url(self)
        self.janela_url.show()

    def abrir_janela_mapeamento(self):
        frame=self.frames['frame_principal']
        if(frame.captura_button['text']=='Mapear Coordenadas'):
            frame.captura_button.config(text='Cancelar captura')
            self.wm_state('iconic')
            self.janela_mapeamento = janela_captura(self,frame)
        elif(frame.captura_button['text']=='Cancelar captura'):
            keyboard.remove_all_hotkeys()
            frame.captura_button.config(text='Mapear Coordenadas')
            self.janela_mapeamento.destroy()
    def iniciar_componentes(self):
        try:
            self.wm_geometry(str(396)+'x'+str(273))
            self.title('Janela principal')
            self.resizable(0,0)
            self.kwargs=arquivo.get_kwargs_informacoes()
            if(not arquivo.verificar_arquivo(self.kwargs['operacoes_url'],
                                          self.kwargs['operacoes_name'])):
                self.abrir_janela_url()

            self.atualizar_frame('frame_principal')
            self.current_frame.iniciar_componentes()
        except Exception as e:
            result=messagebox.askyesno('Erro','Não foi possivel encontra o arquivo de informações\n'
                                                ' por favor preencha as infomações a seguir')
            if(result==1):
                self.abrir_janela_url()

            elif(result==0):
                self.destroy()

    def __on_close(self):
        frame=self.frames['frame_principal']
        result=messagebox.askyesno('Sair','Tem certeza que deseja sair?')

        if(frame.confirm_button['text']=='Desativar macro' and result==1):
            frame.ativar_macro()
            self.destroy()
        elif(result==1):
            self.destroy()


