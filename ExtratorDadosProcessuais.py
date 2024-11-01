# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 09:02:59 2024

@author: Alexandre Araújo Costa
"""

# Este programa realiza buscas na p√°gina de andamentos processuais do STF.

import urllib3
urllib3.disable_warnings()
import dsl
from dsl import ext, clean, clext, get
import pandas as pd
import time
lista = []

# Defina a classe a ser buscada
classe = "ADI"

# Defina o n√∫mero inicial e final dos processos
inicial = 7222
final = 7222

for n in range (final - inicial + 1):
    
    
    processo = n + inicial
    
    print (processo)

    url = 'https://portal.stf.jus.br/processos/listarProcessos.asp?classe=' + classe + '&numeroProcesso=' + str(processo)
    

    dados = get(url)
    
    incidente_id = ext(dados,'<input type="hidden" id="incidente" value="','"')
    classe_numero = clean(ext(dados,'<input type="hidden" id="classe-numero-processo" value="','"'))
    classe = ext(classe_numero, '', ' ')
    numero = ext(classe_numero, ' ', '')
    n_unico = ext(dados,'Número Único: ','<')
    classe_extenso = ext(dados,'<div class="processo-classe p-t-8 p-l-16">','<')
    relator_final = clext(dados,'<div class="processo-dados p-l-16">Relator: ','<')
    redator_acordao = clext(dados,'<div class="processo-dados p-l-16">Redator do acórdão:','<')
    relator_ultimo_incidente = clext(dados,'Relator do último incidente:','<')
    
# Processa informações
    dados_processo = get('https://portal.stf.jus.br/processos/abaInformacoes.asp?incidente='+incidente_id)
    assuntos = ext(dados_processo,'Assunto:','</ul').replace('</li>','')
    assuntos = assuntos.split('<li>')[1:]
    origem_orgao = ext(dados_processo,'Órgão de Origem:','<div class="col-md-7')
    origem_orgao = clean(clext(origem_orgao,'processo-detalhes">','<'))
    origem_orgao = clean(origem_orgao.replace('SUPREMO TRIBUNAL FEDERAL','STF').replace('\r',''))
    origem_numero = ext(dados_processo,'Número de Origem:','<div class="col-md-12')
    origem_numero = clean(ext(origem_numero,'processo-detalhes">','<').replace('\r',''))
    
    numeros = ext(dados_processo,'<div class="col-md-12 col-lg-6 processo-informacao__col m-t-8 m-b-8" style="display: flex;justify-content: space-between;">','<div id="partes" class="tab-pane">').split('<div class="numero">')
    for n in numeros[1:]:
        origem = clean(ext(n,'<span id="descricao-procedencia">','<').replace('\r',''))
        if 'Volumes' in n:
            volumes = (ext(n,'','<'))
        else:
            volumes = 'NA'
        if 'Folhas' in n:
            folhas = (ext(n,'','<'))
        else:
            folhas = 'NA'
        if 'Apensos' in n:
            apensos = (ext(n,'','<'))
        else:
            apensos = 'NA'

    

# Processa partes
    dados_partes = get('https://portal.stf.jus.br/processos/abaPartes.asp?incidente='+incidente_id)
    dados_partes = ext(dados_partes,'','div id="partes-resumidas">')
    partes0 = dados_partes.split('<div class="processo-partes lista-dados m-l-16 p-t-0">')[1:]
    partes = []
    index = -1
    for parte in partes0:
        parte_tipo = ext(parte,'<div class="detalhe-parte">','<')
        parte_nome = ext(parte,'<div class="nome-parte">','<')
        if 'ADV' in parte_tipo:
            index_adv = str(index)+'a'
            partes.append([index_adv,parte_tipo,parte_nome])
        else:
            index = (index+1)
            partes.append([str(index),parte_tipo,parte_nome])

# Processa andamentos
    andamentos_dados = get('https://portal.stf.jus.br/processos/abaAndamentos.asp?incidente=' + incidente_id)
    andamentos0 = andamentos_dados.split('<div class="andamento-item">')[1:]
    andamentos_lista = []
    decisoes = []
    index = len(andamentos0) + 1
    for item in andamentos0:
        index = index - 1
        andamento_data = ext(item,'<div class="andamento-data ">','<')
        andamento_nome =  ext(item,'<h5 class="andamento-nome ">','<')
        if '<a href="' in item:
            andamento_docs = 'https://portal.stf.jus.br/processos/' + ext(item,'<a href="','"')
        else:
            andamento_docs = 'NA'

        if 'andamento-julgador' in item:
            andamento_julgador = ext(item,'<span class="andamento-julgador badge bg-info ">','</')
        else:
            andamento_julgador = 'NA'
            
        andamento_complemento = dsl.clean(ext(item,'<div class="col-md-9 p-0','<'))
        if andamento_complemento == '':
            andamento_complemento = 'NA'

        andamento_dados = {'index': index,
                           'data': andamento_data,
                           'nome': andamento_nome,
                           'complemento': andamento_complemento,
                           'julgador': andamento_julgador,
                           'docs': andamento_docs,
                           'item': item.replace('\r\n','')
                            }

        andamentos_lista.append(andamento_dados)
        
    incidentes_processuais = get('https://sistemas.stf.jus.br/repgeral/votacao?oi='+ incidente_id)
        
    sessao_virtual_dados = get('https://portal.stf.jus.br/processos/abaSessao.asp?incidente=' + incidente_id)
    
    
    
    # Define os dados a gravar, criando uma lista com as variáveis

    dados_a_gravar = {"incidente_id": incidente_id,
                      "classe": classe,
                      "classe_extenso": classe_extenso,
                      "numero": numero,
                      "n_unico": n_unico,
                      "origem": origem,
                      "partes": partes,
                      "origem_orgao": origem_orgao,
                      "origem_numero": origem_numero,
                       "relator_final": relator_final,
                       "relator_ultimo_incidente": relator_ultimo_incidente,
                       "assuntos": assuntos,
                       "partes": partes,
                       "volumes": volumes,
                       "folhas": folhas,
                       "apensos": apensos,
                       "andamentos": andamentos_lista,
                       "decisoes": decisoes,
                       # "sessaovirtual": sessaovirtual,
                       # "deslocamentos": deslocamentos,
                       # "peticoes": peticoes,
                       # "recursos": recursos,
                       # "pautas": pautas
                       }
                      
                          
    lista.append(dados_a_gravar)




# # Acrescenta na lista os dados extra√≠dos de cada processo
#     lista.append(dados_a_gravar)
    
# # Define o nome das colunas a gravar. 
# # As colunas devem corresponder aos nomes das vari√°veis em dados_a_gravar
# colunas = ['incidente_id',
#                   'classe + str(processo)',
#                   'n_unico',
#                   'processo_titulo',
#                   'classe',
#                   'origem',
#                   'origem_orgao',
#                   'origem_numero',
#                   'relator',
#                   'assuntos',
#                   'partes',
#                   'processo_tipo',
#                   'processo_sigilo',
#                   'volumes',
#                   'folhas',
#                   'apensos',
#                   'andamentos',
#                   'decisoes',
#                   'sessaovirtual',
#                   'deslocamentos',
#                   'peticoes',
#                   'recursos',
#                   'pautas']

# df = pd.DataFrame(lista, columns = colunas)
# df.to_csv('Dados_processuais.csv', index=False)