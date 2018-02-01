import arquivo
import pyautogui

from time import sleep



class script():
    def __init__(self):
        pass

    def carregar_mapeamento(self):
        try:
            self.resolucao=str(pyautogui.size()[0])+'x'+str(pyautogui.size()[1])
            self.kwars=arquivo.get_kwargs_mapeamento()
            self.kwars[self.resolucao],self.kwars['Config_mapeamento']
            return 1
        except:
            return 0

    def criar_mapeamento(self):
        array_coordenadas=[int(valor) for valor in self.kwars[self.resolucao].split(',')]
        array_config_mapeamento=[[int(valor) for valor in array.split(',')] for array in self.kwars['Config_mapeamento'].split('|')]
        self.array_coordenadas_mapeadas=[]
        cont=0
        for cont_janelas in range(4):
            linha=[]
            for valor in array_config_mapeamento[cont_janelas]:
                cell=[]
                for cont_opcoes in range(valor):
                    coordenada_x,coordenada_y=array_coordenadas[cont],array_coordenadas[cont+1]
                    cell.append([coordenada_x,coordenada_y])
                    cont=cont+2
                linha.append(cell)
            self.array_coordenadas_mapeadas.append(linha)

    def criar_script(self,array,macro_time):
        operacao,investimento,posicao_tela,posicao_bloco=array.split(';')
        self.posicao_tela=int(posicao_tela)-1
        self.investimento=investimento
        if(macro_time==5):
            self.posicao_bloco=int(posicao_bloco)-1
        if(macro_time==15):
            self.posicao_bloco=-1
        if(operacao=='PUT'):
            self.operacao=0
        if(operacao=='CALL'):
            self.operacao=1

    def tranformar_coordenadas(self,coordenada):
        return coordenada[0],coordenada[1]

    def rodar_script(self,janela_index=None,macro_time=None,valor_aposta=None,tipo_operacao=None):
        array_comandos=self.array_coordenadas_mapeadas[self.posicao_tela]
        pyautogui.click(self.tranformar_coordenadas(array_comandos[0][0]),duration=0.15)
        pyautogui.click(self.tranformar_coordenadas(array_comandos[1][self.posicao_bloco]),duration=0.15)
        pyautogui.click(self.tranformar_coordenadas(array_comandos[2][0]),duration=0.15)
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('del')
        pyautogui.typewrite(str(self.investimento))
        pyautogui.click(self.tranformar_coordenadas(array_comandos[3][self.operacao]),duration=0.15)

teste=script()


