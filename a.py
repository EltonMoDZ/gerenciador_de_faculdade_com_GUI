import tkinter as tk
from tkinter import messagebox
import sqlite3

class BancoDeDados:
    def __init__(self, nome: str):
        self.conexao = sqlite3.connect("{}.db".format(nome))
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Curso (id INTEGER PRIMARY KEY, nome TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Disciplina (id INTEGER PRIMARY KEY, nome TEXT, id_curso INTEGER, FOREIGN KEY(id_curso) REFERENCES Curso(id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Aluno (id INTEGER PRIMARY KEY, nome TEXT, curso_id INTEGER, FOREIGN KEY(curso_id) REFERENCES Curso(id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Professores (id INTEGER PRIMARY KEY, nome TEXT, curso_id INTEGER, disciplina_id INTEGER, FOREIGN KEY(curso_id) REFERENCES Curso(id), FOREIGN KEY(disciplina_id) REFERENCES Disciplina(id))")
        self.conexao.commit()

    def inserir_curso(self, nome: str):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO Curso (nome) VALUES (?)", (nome,))
        self.conexao.commit()

    def inserir_disciplina(self, nome: str, id_curso: int):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO Disciplina (nome, id_curso) VALUES (?, ?)", (nome, id_curso))
        self.conexao.commit()

    def inserir_aluno(self, nome: str, curso_id: int):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO Aluno (nome, curso_id) VALUES (?, ?)", (nome, curso_id))
        self.conexao.commit()
    
    def inserir_professor(self, nome: str, curso_id: int, disciplina_id: int):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO Professores (nome, curso_id, disciplina_id) VALUES (?, ?, ?)", (nome, curso_id, disciplina_id))
        self.conexao.commit()

    def retirar_curso(self, id: int):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM Curso WHERE id = ?", (id,))
        self.conexao.commit()

    def retirar_disciplina(self, id: int):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM Disciplina WHERE id = ?", (id,))
        self.conexao.commit()

    def retirar_aluno(self, id: int):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM Aluno WHERE id = ?", (id,))
        self.conexao.commit()

    def retirar_professor(self, id: int):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM Professores WHERE id = ?", (id,))
        self.conexao.commit()

    def atualizar_curso(self, id: int, novo_nome: str):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT nome FROM Curso WHERE id = ?", (id,))
        curso_atual = cursor.fetchone()
        if curso_atual is None:
            print("Curso não encontrado")
            return
        nome_atual = curso_atual[0]
        nome = novo_nome if novo_nome else nome_atual
        cursor.execute("UPDATE Curso SET nome = ? WHERE id = ?", (nome, id))
        self.conexao.commit()

    def atualizar_disciplina(self, id: int, novo_nome: str, novo_id_curso: int):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT nome, id_curso FROM Disciplina WHERE id = ?", (id,))
        disciplina_atual = cursor.fetchone()
        if disciplina_atual is None:
            print("Disciplina não encontrada")
            return
        nome_atual, id_curso_atual = disciplina_atual
        nome = novo_nome if novo_nome else nome_atual
        id_curso = novo_id_curso if novo_id_curso else id_curso_atual
        cursor.execute("UPDATE Disciplina SET nome = ?, id_curso = ? WHERE id = ?", (nome, id_curso, id))
        self.conexao.commit()

    def atualizar_aluno(self, id: int, novo_nome: str, novo_curso_id: int):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT nome, curso_id FROM Aluno WHERE id = ?", (id,))
        aluno_atual = cursor.fetchone()
        if aluno_atual is None:
            print("Aluno não encontrado")
            return
        nome_atual, curso_id_atual = aluno_atual
        nome = novo_nome if novo_nome else nome_atual
        curso_id = novo_curso_id if novo_curso_id else curso_id_atual
        cursor.execute("UPDATE Aluno SET nome = ?, curso_id = ? WHERE id = ?", (nome, curso_id, id))
        self.conexao.commit()

    def atualizar_professor(self, id: int, novo_nome: str, novo_curso_id: int, novo_disciplina_id: int):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT nome, curso_id, disciplina_id FROM Professores WHERE id = ?", (id,))
        professor_atual = cursor.fetchone()
        if professor_atual is None:
            print("Professor não encontrado")
            return
        nome_atual, curso_id_atual, disciplina_id_atual = professor_atual
        nome = novo_nome if novo_nome else nome_atual
        curso_id = novo_curso_id if novo_curso_id else curso_id_atual
        disciplina_id = novo_disciplina_id if novo_disciplina_id else disciplina_id_atual
        cursor.execute("UPDATE Professores SET nome = ?, curso_id = ?, disciplina_id = ? WHERE id = ?", (nome, curso_id, disciplina_id, id))
        self.conexao.commit()
    

def centralizar_janela(root, width=800, height=600):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x_cordinate = int((screen_width/2) - (width/2))
    y_cordinate = int((screen_height/2) - (height/2))
    
    root.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")

janela = tk.Tk()
janela.title("Gerenciador da faculdade")
centralizar_janela(janela)
janela.resizable(False, False)
banco = BancoDeDados(nome="faculdade")

def abrir_janela_inserir_curso():
    janela_inserir = tk.Toplevel(janela)
    janela_inserir.title("Inserir Curso")
    centralizar_janela(janela_inserir, 400, 200)
    tk.Label(janela_inserir, text="Nome do Curso:").grid(row=0, column=0, padx=10, pady=10)
    nome_entry = tk.Entry(janela_inserir)
    nome_entry.grid(row=0, column=1, padx=10, pady=10)
    def inserir_curso():
        nome = nome_entry.get()
        banco.inserir_curso(nome)
        messagebox.showinfo("Sucesso", "Curso inserido com sucesso!")
        janela_inserir.destroy()
    tk.Button(janela_inserir, text="Inserir", command=inserir_curso).grid(row=1, column=0, columnspan=2, pady=10)

def abrir_janela_atualizar_curso():
    janela_atualizar = tk.Toplevel(janela)
    janela_atualizar.title("Atualizar Curso")
    centralizar_janela(janela_atualizar, 400, 400)

    cursos = banco.listar_cursos()
    cursos_str = "\n".join(f"ID: {id} - Nome: {nome}" for id, nome in cursos)

    tk.Label(janela_atualizar, text="ID do Curso:").grid(row=0, column=0, padx=10, pady=10)
    id_entry = tk.Entry(janela_atualizar)
    id_entry.grid(row=0, column=1, padx=10, pady=10)
    tk.Label(janela_atualizar, text="Novo Nome do Curso:").grid(row=1, column=0, padx=10, pady=10)
    nome_entry = tk.Entry(janela_atualizar)
    nome_entry.grid(row=1, column=1, padx=10, pady=10)

    cursos_listbox = tk.Listbox(janela_atualizar)
    cursos_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    for curso in cursos:
        cursos_listbox.insert(tk.END, f"ID: {curso[0]} - Nome: {curso[1]}")

tk.Button(janela, text="Inserir Curso", command=abrir_janela_inserir_curso).grid(row=0, column=0, padx=10, pady=10)
tk.Button(janela, text="Atualizar Curso", command=abrir_janela_atualizar_curso).grid(row=1, column=0, padx=10, pady=10)

janela.mainloop()
