# utils/timeline.py
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def obter_semestre_atual(ano_sem_ingresso):
    hoje = datetime.now()
    ano_atual = hoje.year
    mes_atual = hoje.month
    sem_atual = 1 if mes_atual < 7 else 2
    
    ano_ingresso, sem_ingresso = map(int, ano_sem_ingresso.split('-'))
    semestres_passados = (ano_atual - ano_ingresso) * 2 + (sem_atual - sem_ingresso) + 1
    return semestres_passados

def desenhar_linha_tempo_avancada(ano_sem_ingresso, modalidade):
    fig, ax = plt.subplots(figsize=(12, 4))
    
    duracao = 4 if modalidade.lower() == "mestrado" else 8
    semestre_atual = obter_semestre_atual(ano_sem_ingresso)
    
    x_pos = np.arange(duracao)
    y_pos = [1] * duracao
    
    ax.plot(x_pos, y_pos, '-', color='#f1c40f', linewidth=2, zorder=1)
    
    if modalidade.lower() == "mestrado":
        marcos = ['Início', 'Pesquisa', 'Pesquisa', 'Defesa']
        cores = ['#f1c40f'] * 4
    else:
        marcos = ['Início'] + ['Pesquisa']*3 + ['Qualificação'] + ['Pesquisa']*2 + ['Defesa']
        cores = ['#f1c40f'] * 8
        cores[4] = '#e74c3c'
    
    for i, (marco, cor) in enumerate(zip(marcos, cores)):
        is_current = (i + 1) == semestre_atual
        cor_ponto = '#3498db' if is_current else cor
        
        circle = ax.plot(x_pos[i], y_pos[i], 'o', markersize=25, color=cor_ponto, zorder=2)[0]
        
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
    
    ax.set_title(f'Fluxo do Programa de {modalidade}', pad=40, fontsize=14, fontweight='bold')
    ax.set_xlim(x_pos[0]-0.5, x_pos[-1]+0.5)
    ax.set_ylim(0, 2)
    
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)
    
    return fig
