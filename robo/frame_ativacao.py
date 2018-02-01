import tkinter as tk
import arquivo
from criptografia import instancia
from tkinter import ttk

class frame_ativacao(tk.Frame):
    def __init__(self,janela,container):
        tk.Frame.__init__(self,container)
        self.nome='frame_ativacao'
        self.janela=janela

    def salvar_arquivo_ativacao(self,tipo_ativacao,key):
        infoativacao_url=arquivo.get_value_informacoes('infoativacao_url')
        infoativacao_name=arquivo.get_value_informacoes('infoativacao_name')
        array_informacoes=[]
        array_informacoes.append('tipo_ativacao='+tipo_ativacao)
        array_informacoes.append('data_ativacao='+str(arquivo.getOnlineUTCTime()))
        array_informacoes.append('key_usada='+key)
        instancia.encrypt_array_to_file(infoativacao_url+'/'+infoativacao_name,array_informacoes)


    def salvar_arquivo_keys(self):
        if (not arquivo.verificar_arquivo(self.janela.kwargs['keys_url'],self.janela.kwargs['keys_name'])):
            array_keys = ['iqoption10', 'iqoptionpag1586', 'iqoptionpag1225', 'iqoptionpag1366', '40028922','1dia']
            instancia.encrypt_array_to_file(self.janela.kwargs['keys_url'] + '/' + self.janela.kwargs['keys_name'], array_keys)

    def ativar_programa(self):
        keys_url=self.janela.kwargs['keys_url']
        keys_name=self.janela.kwargs['keys_name']
        array_keys_descriptografas=instancia.decrypt_file_to_array(keys_url+'/'+keys_name)
        for key in array_keys_descriptografas:
            if(key==self.key_box.get()):
                array_keys_descriptografas.remove(key)
                instancia.encrypt_array_to_file(keys_url+'/'+keys_name,array_keys_descriptografas)
                if(key=='1dia'):
                    self.salvar_arquivo_ativacao('teste', key)
                elif(key=='40028922'):
                    self.salvar_arquivo_ativacao('vitalicia', key)
                else:
                    self.salvar_arquivo_ativacao('normal',key)
                self.janela.atualizar_frame('frame_principal')
                self.janela.iniciar_componentes()
                break


    def iniciar_componentes(self):
        imagem_logo=tk.PhotoImage(file='files//iqoption-logo.png')
        self.salvar_arquivo_keys()
        self.div1=tk.Frame(self)
        self.div1.pack_propagate(False)
        self.div1.config(width=100,height=20)
        self.label_logo=tk.Label(self,image=imagem_logo)
        self.label_logo.image=imagem_logo
        self.text_warning=ttk.Label(self,text="Você possui 0 dias de licença",font=("Arial",15))
        self.text_warning.config(foreground='red')
        self.text_key=ttk.Label(self,text="Inserir key:",font=("Arial",15))
        self.key_box=ttk.Entry(self,width=20,font=("Arial",15))
        self.confirm_buttom=tk.Button(self,text='Ativar key',font=("Arial",15),command=self.ativar_programa)
        self.confirm_buttom.config(relief=tk.GROOVE)

        self.div1.grid(row=0,column=0,columnspan=2)
        self.label_logo.grid(row=1,column=0,columnspan=2,padx=20)
        self.text_warning.grid(row=2,column=0,columnspan=2,sticky=tk.W,padx=20,pady=7)
        self.text_key.grid(row=3,column=0,padx=20)
        self.key_box.grid(row=3,column=1)
        self.confirm_buttom.grid(row=4,column=1,columnspan=2,pady=10,sticky=tk.W)