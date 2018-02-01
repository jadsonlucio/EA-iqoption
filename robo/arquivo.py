import urllib.request as read_url
from datetime import datetime
from os import listdir


informacoes_licensa=['tipo_licensa','data_ativacao']

def getOnlineUTCTime():
    webpage = read_url.urlopen("http://just-the-time.appspot.com/")
    internettime = webpage.read().decode('utf-8')
    OnlineUTCTime = datetime.strptime(internettime.strip(), '%Y-%m-%d %H:%M:%S')
    return OnlineUTCTime

def getTime():
    return datetime.now().strftime('%H:%M:%S')

def subtrair_datas(data_inicial=datetime,data_final=datetime):
    resultado=data_final-data_inicial
    return resultado.days

def subtrair_tempos(tempo_inicial,tempo_final):
    hora_inicial,minuto_inicial,segundo_inicial=[float(result) for result in tempo_inicial.split(':')]
    hora_final,minuto_final,segundo_final=[float(result) for result in tempo_final.split(':')]
    tempo_to_seconds_inicial=hora_inicial*3600+minuto_inicial*60+segundo_inicial
    tempo_to_seconds_final=hora_final*3600+minuto_final*60+segundo_inicial
    return tempo_to_seconds_final-tempo_to_seconds_inicial

def converter_string_to_date(string,format='%Y-%m-%d %H:%M:%S'):
    data=datetime.strptime(string,format)
    return data

def list_files(url):
    list_files = listdir(url)
    return list_files

def ler_arquivo(url_arquivo):
    file=open(url_arquivo,'rb')
    array=file.readlines()
    file.close()
    return array

def salvar_arquivo(url_arquivo,array):
    file=open(url_arquivo,'w+')
    file.writelines([str(linha)+'\n' for linha in array])
    file.close()

def resetar_configuracao():
    try:
        limpar_arquivo('files//informações.txt')
        limpar_arquivo('files//mapeamento.txt')
        limpar_arquivo('files//posições_saldo.txt')
    except:
        pass

def limpar_arquivo(url_arquivo):
    try:
        open(url_arquivo, 'w').close()
    except Exception as e:
        pass

def verificar_arquivo(url, nome_arquivo):
    files_names = list_files(url)
    for file_name in files_names:
        if (file_name == nome_arquivo):
            return True
    return False


def converter_array_to_dictonary(array):
    dicionario={}
    for line in array:
        key,arg=str(line).split('=')
        dicionario[str(key)]=str(arg)
    return dicionario


def get_kwargs_posicao_preco():
    array = ler_arquivo('files//posições_saldo.txt')
    new_array = [linha.decode('utf-8').replace('\n', '').replace('\r', '') for linha in array]
    kwargs = converter_array_to_dictonary(new_array)
    return kwargs

def get_kwargs_mapeamento():
    array=ler_arquivo('files//mapeamento.txt')
    new_array = [linha.decode('utf-8').replace('\n', '').replace('\r', '') for linha in array]
    kwargs = converter_array_to_dictonary(new_array)
    return kwargs

def get_kwargs_informacoes():
    array = ler_arquivo('files//informações.txt')
    new_array=[linha.decode('utf-8').replace('\n','').replace('\r','') for linha in array]
    dirct = converter_array_to_dictonary(new_array)
    return dirct

def verificar_kwargs(url_arquivo,key):
    try:
        array=ler_arquivo(url_arquivo)
        new_array=[linha.decode('utf-8').replace('\n','').replace('\n','') for linha in array]
        kwargs=converter_array_to_dictonary(new_array)
        for key_arquivo in kwargs.keys():
            if(key_arquivo==key):
                return 1
        return 0
    except:
        return 0


