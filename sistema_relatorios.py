import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Título do sistema
st.title('Sistema de Geração de Relatórios Logísticos - Análises Diversificadas')

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Faça o upload do arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(uploaded_file)

        # Mostrar uma amostra dos dados
        st.write("Amostra dos Dados:", df.head())

        # Identificar automaticamente as colunas relevantes
        colunas_disponiveis = df.columns.tolist()

        # Menu de seleção para as análises disponíveis
        analise = st.selectbox("Selecione a análise desejada:", [
            "Filial que mais vendeu",
            "Capacidade Utilizada por Tipo de Veículo",
            "Distribuição do Status das Entregas",
            "Mês com Maior Receita Total",
            "Cliente que Gerou Maior Receita",
            "Região com Maior Peso Transportado",
            "Evolução do Status das Entregas ao Longo do Tempo"
        ])

        # Variável para armazenar o gráfico (caso precise exportar)
        fig = None

        # Análise 1: Filial que mais vendeu
        if analise == "Filial que mais vendeu":
            if 'FILIAL' in colunas_disponiveis and 'VALOR TOTAL' in colunas_disponiveis:
                valor_total_por_filial = df.groupby('FILIAL')['VALOR TOTAL'].sum().sort_values(ascending=False)
                filial_mais_vendeu = valor_total_por_filial.idxmax()
                valor_mais_vendeu = valor_total_por_filial.max()
                st.write(f"A filial que mais vendeu é: {filial_mais_vendeu} com um valor total de R$ {valor_mais_vendeu:,.2f}")

                fig, ax = plt.subplots(figsize=(10, 6))
                valor_total_por_filial.plot(kind='bar', ax=ax, color='royalblue', edgecolor='black')
                ax.set_title('Valor Total por Filial', fontsize=16, weight='bold')
                ax.set_xlabel('Filial', fontsize=14)
                ax.set_ylabel('Valor Total (R$)', fontsize=14)
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                for bar in ax.patches:
                    ax.annotate(f'{bar.get_height():,.0f}', (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                                ha='center', va='bottom', fontsize=12, weight='bold', color='black')
                st.pyplot(fig)

        # Análise 2: Capacidade Utilizada por Tipo de Veículo
        elif analise == "Capacidade Utilizada por Tipo de Veículo":
            if 'TIPO' in colunas_disponiveis and 'PESO REAL (tonelada)' in colunas_disponiveis:
                capacidade_tipo = df.groupby('TIPO')['PESO REAL (tonelada)'].sum().sort_values(ascending=False)
                fig, ax = plt.subplots(figsize=(10, 6))
                capacidade_tipo.plot(kind='bar', ax=ax, color='orange', edgecolor='black')
                ax.set_title('Capacidade Utilizada por Tipo de Veículo', fontsize=16, weight='bold')
                ax.set_xlabel('Tipo de Veículo', fontsize=14)
                ax.set_ylabel('Peso Real (Tonelada)', fontsize=14)
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                for bar in ax.patches:
                    ax.annotate(f'{bar.get_height():,.1f}', (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                                ha='center', va='bottom', fontsize=12, weight='bold', color='black')
                st.pyplot(fig)

        # Análise 3: Distribuição do Status das Entregas
        elif analise == "Distribuição do Status das Entregas":
            if 'Status' in colunas_disponiveis:
                status_counts = df['Status'].value_counts()
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'},
                       colors=['#66b3ff', '#99ff99', '#ffcc99'], shadow=True, explode=(0.1, 0))
                ax.set_title('Distribuição do Status das Entregas', fontsize=16, weight='bold')
                st.pyplot(fig)

        # Análise 4: Mês com Maior Receita Total
        elif analise == "Mês com Maior Receita Total":
            if 'DATA' in colunas_disponiveis and 'VALOR TOTAL' in colunas_disponiveis:
                df['MÊS'] = df['DATA'].dt.to_period('M')
                receita_por_mes = df.groupby('MÊS')['VALOR TOTAL'].sum().sort_values(ascending=False)
                mes_maior_receita = receita_por_mes.idxmax()
                valor_maior_receita = receita_por_mes.max()
                st.write(f"O mês com maior receita foi: {mes_maior_receita} com um valor total de R$ {valor_maior_receita:,.2f}")

                fig, ax = plt.subplots(figsize=(10, 6))
                receita_por_mes.plot(kind='bar', ax=ax, color='green', edgecolor='black')
                ax.set_title('Receita Total por Mês', fontsize=16, weight='bold')
                ax.set_xlabel('Mês', fontsize=14)
                ax.set_ylabel('Valor Total (R$)', fontsize=14)
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                st.pyplot(fig)

        # Análise 5: Cliente que Gerou Maior Receita
        elif analise == "Cliente que Gerou Maior Receita":
            if 'CLIENTES' in colunas_disponiveis and 'VALOR TOTAL' in colunas_disponiveis:
                receita_por_cliente = df.groupby('CLIENTES')['VALOR TOTAL'].sum().sort_values(ascending=False)
                cliente_maior_receita = receita_por_cliente.idxmax()
                valor_maior_receita = receita_por_cliente.max()
                st.write(f"O cliente que gerou maior receita foi: {cliente_maior_receita} com um valor total de R$ {valor_maior_receita:,.2f}")

                fig, ax = plt.subplots(figsize=(10, 6))
                receita_por_cliente.plot(kind='bar', ax=ax, color='purple', edgecolor='black')
                ax.set_title('Receita Total por Cliente', fontsize=16, weight='bold')
                ax.set_xlabel('Cliente', fontsize=14)
                ax.set_ylabel('Valor Total (R$)', fontsize=14)
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                st.pyplot(fig)

        # Análise 6: Região com Maior Peso Transportado
        elif analise == "Região com Maior Peso Transportado":
            if 'REGIÃO' in colunas_disponiveis and 'PESO REAL (tonelada)' in colunas_disponiveis:
                peso_por_regiao = df.groupby('REGIÃO')['PESO REAL (tonelada)'].sum().sort_values(ascending=False)
                regiao_maior_peso = peso_por_regiao.idxmax()
                peso_maior = peso_por_regiao.max()
                st.write(f"A região com maior peso transportado foi: {regiao_maior_peso} com um total de {peso_maior:,.1f} toneladas")

                fig, ax = plt.subplots(figsize=(10, 6))
                peso_por_regiao.plot(kind='bar', ax=ax, color='teal', edgecolor='black')
                ax.set_title('Peso Transportado por Região', fontsize=16, weight='bold')
                ax.set_xlabel('Região', fontsize=14)
                ax.set_ylabel('Peso Total (Tonelada)', fontsize=14)
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                st.pyplot(fig)

        # Análise 7: Evolução do Status das Entregas ao Longo do Tempo
        elif analise == "Evolução do Status das Entregas ao Longo do Tempo":
            if 'DATA' in colunas_disponiveis and 'Status' in colunas_disponiveis:
                df['MÊS'] = df['DATA'].dt.to_period('M')
                status_mes = df.groupby(['MÊS', 'Status']).size().unstack().fillna
