import streamlit as st
import sqlite3 
import pandas as pd

def inicializar_banco():
    conexao = sqlite3.connect('safra.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          tipo TEXT,
          categoria TEXT,
          descricao TEXT,
          valor REAL,
          data TEXT
          )
    ''')
    conexao.commit()
    conexao.close()

def salvar_transacao(tipo, categoria, descricao, valor, data):
   conexao = sqlite3.connect('safra.db')
   cursor = conexao.cursor()
   cursor.execute('''
      INSERT INTO transacoes (tipo, categoria, descricao, valor, data)
      VALUES (?, ?, ?, ?, ?) 
    ''',(tipo, categoria, descricao, valor, data))

   conexao.commit()
   conexao.close()

def buscar_transacoes():
   conexao = sqlite3.connect('safra.db')
   tabela = pd.read_sql_query("SELECT * FROM transacoes", conexao)
   conexao.close()
   return tabela

def deletar_transacao(id):
    conexao = sqlite3.connect('safra.db')
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM transacoes WHERE id = ?', (id,))
    conexao.commit()
    conexao.close()

inicializar_banco()

st.title("Caderno de Campo")
st.write("Registre os custos e o apurado da sua safra abaixo:")

with st.form("meu_formulario"):

    tipo = st.selectbox("Tipo de movimentação", ["Custo", "Apurado"])
    categoria = st.selectbox("Categoria", ["Adubo", "Veneno", "Trator", "Trabalhador", "Semente", "Venda", "Outros"])
    descricao = st.text_input("Descrição, (Ex: 2 sacos de adubo)")
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    data = st.date_input("Data da movimentação")
    botao_salvar = st.form_submit_button("Salvar")

    if botao_salvar:
        data_texto = data.strftime("%Y-%m-%d")
        salvar_transacao(tipo, categoria, descricao, valor, data_texto)

        st.success("Transação salva com sucesso!")


st.divider()
st.subheader("Painel de Controle")

dados = buscar_transacoes()
if not dados.empty:
    total_custo = dados[dados['tipo'] == 'Custo']['valor'].sum()
    total_apurado = dados[dados['tipo'] == 'Apurado']['valor'].sum()
    lucro = total_apurado - total_custo

    coluna1, coluna2, coluna3 = st.columns(3)

    coluna1.metric("Total gasto", f"R$ {total_custo:.2f}")
    coluna2.metric("Total faturado", f"R$ {total_apurado:.2f}")
    coluna3.metric("Lucro", f"R$ {lucro:.2f}")

else:
    st.info("Nenhuma transação registrada ainda.")


st.divider()
st.subheader("Histórico de Transações")

dados = buscar_transacoes()
st.dataframe(dados, hide_index=True)

st.divider()
st.subheader("Deletar Transação")

coluna1, coluna2 = st.columns(2)

with coluna1:
    id_deletar = st.number_input("Digite o ID da transação que deseja deletar", min_value=0, step=1)
with coluna2:
    st.write("")
    st.write("")
    botao_deletar = st.button("Deletar")

if botao_deletar:
    deletar_transacao(id_deletar)
    st.rerun()