# utils/data_loader.py
import pandas as pd

def carregar_dados(arquivo):
    try:
        df = pd.read_excel(arquivo, engine="odf")
        return df
    except FileNotFoundError:
        return None

def extrair_info_aluno(df_filtrado):
    info = {}
    campos = [
        'ano_sem_ingresso', 'modalidade', 'tipo', 'orientador', 'coorientador',
        'trancamento', 'bolsa_fomento', 'projetos_ext', 'Inglês', 'qualificacao',
        'num_creditos', 'titulo', 'parecer'
    ]
    
    for campo in campos:
        if campo in df_filtrado.columns and not df_filtrado.empty:
            valor = df_filtrado[campo].iloc[0]
            info[campo] = valor if pd.notna(valor) else 'NA'
        else:
            info[campo] = 'NA'
            
    # Tratamento especial para coorientador
    if info.get('coorientador') == 'NA':
        info['coorientador'] = 'Sem coorientação'
        
    return info

