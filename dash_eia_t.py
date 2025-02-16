# app.py
import streamlit as st
from utils.data_loader import carregar_dados, extrair_info_aluno
from utils.timeline import desenhar_linha_tempo_avancada

def main():
    st.set_page_config(page_title="AeroPos", layout="wide")
    
    st.title("AeroPos")
    st.markdown("### Análise e Registro de Operações da Pós-graduação em Infraestrutura Aeronáutica")
    
    df = carregar_dados("base_de_dados_eia_t.ods")
    if df is None:
        st.error("Arquivo 'base_de_dados_eia_t.ods' não encontrado. Verifique se o arquivo está na mesma pasta do script.")
        st.stop()
    
    if 'nome' in df.columns:
        nomes = df['nome'].dropna().unique()
        nomes = sorted(nomes)
        nome_selecionado = st.sidebar.selectbox("Selecione um Nome", nomes)
        
        df_filtrado = df[df['nome'] == nome_selecionado]
        
        if not df_filtrado.empty:
            info_aluno = extrair_info_aluno(df_filtrado)
            
            st.markdown(f"""
            **📌 Dados do Aluno Selecionado**  
            - 🏫 **Ano de Ingresso e Semestre:** `{info_aluno['ano_sem_ingresso']}`  
            - 🎓 **Modalidade:** `{info_aluno['modalidade']}`  
            - 📖 **Tipo:** `{info_aluno['tipo']}`  
            - 👨‍🏫 **Orientador:** `{info_aluno['orientador']}`  
            - 👩‍🏫 **Coorientador:** `{info_aluno['coorientador']}`  
            - 🔄 **Trancamento:** `{info_aluno['trancamento']}`  
            - 💰 **Bolsa de Fomento:** `{info_aluno['bolsa_fomento']}`  
            - 🔬 **Projetos Externos:** `{info_aluno['projetos_ext']}`  
            - 🇬🇧 **Inglês:** `{info_aluno['Inglês']}`  
            - 🏅 **Qualificação:** `{info_aluno['qualificacao']}`  
            - 📚 **Número de Créditos:** `{info_aluno['num_creditos']}`  
            - 📜 **Título:** `{info_aluno['titulo']}`  
            - 📝 **Parecer:** `{info_aluno['parecer']}`
            """)
            
            st.markdown(f"""🗺 **Linha do Tempo Acadêmica** """)
            fig = desenhar_linha_tempo_avancada(info_aluno['ano_sem_ingresso'], info_aluno['modalidade'])
            st.pyplot(fig)
        else:
            st.warning("Nenhum dado encontrado para o aluno selecionado.")
    else:
        st.error("A coluna 'nome' não está presente no DataFrame. Verifique a base de dados.")

if __name__ == "__main__":
    main()
