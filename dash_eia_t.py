import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# Verificar se o Streamlit está instalado
try:
    import streamlit as st
except ModuleNotFoundError:
    print("Erro: O módulo 'streamlit' não está instalado. Execute 'pip install streamlit' para instalá-lo.")
    exit()

# Configuração da página
st.set_page_config(page_title="AeroPos", layout="wide")

# Título do Dashboard
st.title("AeroPos")
st.markdown("### Análise e Registro de Operações da Pós-graduação em Infraestrutura Aeronáutica")

# Carregar a base de dados
try:
    df = pd.read_excel("base_de_dados_eia_t.ods", engine="odf")

except FileNotFoundError:
    st.error("Erro: O arquivo 'data/base_de_dados_eia_t.ods' não foi encontrado. Verifique o caminho do arquivo.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()
    
    
def obter_semestre_atual(ano_sem_ingresso):
    # Obtém a data atual
    hoje = datetime.now()
    ano_atual = hoje.year
    mes_atual = hoje.month
    sem_atual = 1 if mes_atual < 7 else 2
    
    # Calcula o semestre de ingresso
    ano_ingresso, sem_ingresso = map(int, ano_sem_ingresso.split('-'))
    
    # Calcula quantos semestres se passaram
    semestres_passados = (ano_atual - ano_ingresso) * 2 + (sem_atual - sem_ingresso) + 1
    return semestres_passados

def desenhar_linha_tempo_avancada(ano_sem_ingresso, modalidade):
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Definir número de semestres baseado na modalidade
    duracao = 4 if modalidade.lower() == "mestrado" else 8
    semestre_atual = obter_semestre_atual(ano_sem_ingresso)
    
    # Criar posições dos pontos
    x_pos = np.arange(duracao)
    y_pos = [1] * duracao
    
    # Desenhar linha base
    ax.plot(x_pos, y_pos, '-', color='#f1c40f', linewidth=2, zorder=1)
    
    # Definir marcos para cada modalidade
    if modalidade.lower() == "mestrado":
        marcos = ['Início', 'Pesquisa', 'Pesquisa', 'Defesa']
        cores = ['#f1c40f'] * 4  # Todas amarelas por padrão
    else:  # doutorado
        marcos = ['Início'] + ['Pesquisa']*3 + ['Qualificação'] + ['Pesquisa']*2 + ['Defesa']
        cores = ['#f1c40f'] * 8  # Todas amarelas por padrão
        cores[4] = '#e74c3c'  # Qualificação em vermelho
    
    # Adicionar pontos e rótulos
    legend_elements = []
    for i, (marco, cor) in enumerate(zip(marcos, cores)):
        # Determinar se este é o semestre atual
        is_current = (i + 1) == semestre_atual
        cor_ponto = '#3498db' if is_current else cor  # Semestre atual em azul
        
        # Desenhar círculo
        circle = ax.plot(x_pos[i], y_pos[i], 'o', markersize=25, color=cor_ponto, zorder=2)[0]
        
        # Adicionar rótulo do marco
        ax.annotate(marco,
                   xy=(x_pos[i], y_pos[i]),
                   xytext=(0, 25),
                   textcoords='offset points',
                   ha='center',
                   va='bottom',
                   bbox=dict(boxstyle='round,pad=0.5',
                           fc='white',
                           alpha=0.8),
                   fontsize=10,
                   fontweight='bold')
        
        # Adicionar semestre
        ano, sem = map(int, ano_sem_ingresso.split('-'))
        sem_atual = (sem + i - 1) % 2 + 1
        ano_atual = ano + (sem + i - 1) // 2
        semestre_texto = f"{ano_atual}-{sem_atual}\n({i+1}º SEM)"
        
        ax.annotate(semestre_texto,
                   xy=(x_pos[i], y_pos[i]),
                   xytext=(0, -30),
                   textcoords='offset points',
                   ha='center',
                   va='top',
                   fontsize=9)
    
    # Adicionar legenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#f1c40f', 
               markersize=15, label='Etapa Regular'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498db', 
               markersize=15, label='Semestre Atual'),
    ]
    
    if modalidade.lower() == "doutorado":
        legend_elements.append(
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c', 
                   markersize=15, label='Qualificação')
        )
    
    ax.legend(handles=legend_elements, 
             loc='upper center', 
             bbox_to_anchor=(0.5, -0.15),
             ncol=3,
             frameon=False,
             fontsize=10)
    
    # Configurações do gráfico
    ax.set_title(f'Fluxo do Programa de {modalidade}', pad=40, fontsize=14, fontweight='bold')
    ax.set_xlim(x_pos[0]-0.5, x_pos[-1]+0.5)
    ax.set_ylim(0, 2)
    
    # Remover eixos
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Ajustar layout para acomodar a legenda
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Ajuste para a legenda não ficar cortada
    
    return fig


# Adicionar selectbox na barra lateral para filtrar pelo 'Nome'
if 'nome' in df.columns:
    nomes = df['nome'].dropna().unique()
    nomes = sorted(nomes)
    nome_selecionado = st.sidebar.selectbox("Selecione um Nome", nomes)

    # Filtrar os dados com base no nome selecionado
    df_filtrado = df[df['nome'] == nome_selecionado]

    if not df_filtrado.empty:
        # Pegando os valores encontrados nas colunas relevantes
        ano_sem_ingresso = df_filtrado['ano_sem_ingresso'].iloc[0]
        modalidade = df_filtrado['modalidade'].iloc[0] if 'modalidade' in df_filtrado.columns else 'N/A'
        tipo = df_filtrado['tipo'].iloc[0] if 'tipo' in df_filtrado.columns and pd.notna(df_filtrado['tipo'].iloc[0]) else 'NA'
        orientador = df_filtrado['orientador'].iloc[0] if 'orientador' in df_filtrado.columns and pd.notna(df_filtrado['orientador'].iloc[0]) else 'NA'
        coorientador = df_filtrado['coorientador'].iloc[0] if 'coorientador' in df_filtrado.columns and pd.notna(df_filtrado['coorientador'].iloc[0]) else 'Sem coorientação'
        trancamento = df_filtrado['trancamento'].iloc[0] if 'trancamento' in df_filtrado.columns and pd.notna(df_filtrado['trancamento'].iloc[0]) else 'NA'
        bolsa_fomento = df_filtrado['bolsa_fomento'].iloc[0] if 'bolsa_fomento' in df_filtrado.columns and pd.notna(df_filtrado['bolsa_fomento'].iloc[0]) else 'NA'
        projetos_ext = df_filtrado['projetos_ext'].iloc[0] if 'projetos_ext' in df_filtrado.columns and pd.notna(df_filtrado['projetos_ext'].iloc[0]) else 'NA'
        ingles = df_filtrado['Inglês'].iloc[0] if 'Inglês' in df_filtrado.columns and pd.notna(df_filtrado['Inglês'].iloc[0]) else 'NA'
        qualificacao = df_filtrado['qualificacao'].iloc[0] if 'qualificacao' in df_filtrado.columns and pd.notna(df_filtrado['qualificacao'].iloc[0]) else 'NA'
        num_creditos = df_filtrado['num_creditos'].iloc[0] if 'num_creditos' in df_filtrado.columns and pd.notna(df_filtrado['num_creditos'].iloc[0]) else 'NA'
        titulo = df_filtrado['titulo'].iloc[0] if 'titulo' in df_filtrado.columns and pd.notna(df_filtrado['titulo'].iloc[0]) else 'NA'
        parecer = df_filtrado['parecer'].iloc[0] if 'parecer' in df_filtrado.columns and pd.notna(df_filtrado['parecer'].iloc[0]) else 'NA'


        
        # Exibir as informações formatadas
        st.markdown(f"""
        **📌 Dados do Aluno Selecionado**  
        - 🏫 **Ano de Ingresso e Semestre:** `{ano_sem_ingresso}`  
        - 🎓 **Modalidade:** `{modalidade}`  
        - 📖 **Tipo:** `{tipo}`  
        - 👨‍🏫 **Orientador:** `{orientador}`  
        - 👩‍🏫 **Coorientador:** `{coorientador}`  
        - 🔄 **Trancamento:** `{trancamento}`  
        - 💰 **Bolsa de Fomento:** `{bolsa_fomento}`  
        - 🔬 **Projetos Externos:** `{projetos_ext}`  
        - 🇬🇧 **Inglês:** `{ingles}`  
        - 🏅 **Qualificação:** `{qualificacao}`  
        - 📚 **Número de Créditos:** `{num_creditos}`  
        - 📜 **Título:** `{titulo}`  
        - 📝 **Parecer:** `{parecer}` 

        """)
    else:
        st.warning("Nenhum dado encontrado para o aluno selecionado.")
else:
    st.error("A coluna 'nome' não está presente no DataFrame. Verifique a base de dados.")

# Exibir gráfico da linha do tempo acadêmica
st.markdown(f"""🗺 **Linha do Tempo Acadêmica** """)
fig = desenhar_linha_tempo_avancada(ano_sem_ingresso, modalidade)
st.pyplot(fig)


