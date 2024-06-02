import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class Database:
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

    def executar_query(self, query, parameters=()):
        cursor = self.conexao.cursor()
        cursor.execute(query, parameters)
        self.conexao.commit()
        return cursor

class CursoManager:
    def __init__(self, database):
        self.db = database

    def inserir_curso(self, nome):
        self.db.executar_query("INSERT INTO Curso (nome) VALUES (?)", (nome,))

    def retirar_curso(self, id):
        self.db.executar_query("DELETE FROM Curso WHERE id = ?", (id,))

    def listar_cursos(self):
        return self.db.executar_query("SELECT id, nome FROM Curso").fetchall()

class DisciplinaManager:
    def __init__(self, database):
        self.db = database

    def inserir_disciplina(self, nome, id_curso):
        self.db.executar_query("INSERT INTO Disciplina (nome, id_curso) VALUES (?, ?)", (nome, id_curso))

    def retirar_disciplina(self, id):
        self.db.executar_query("DELETE FROM Disciplina WHERE id = ?", (id,))

    def listar_disciplinas(self):
        return self.db.executar_query("SELECT id, nome FROM Disciplina").fetchall()

class AlunoManager:
    def __init__(self, database):
        self.db = database

    def inserir_aluno(self, nome, curso_id):
        self.db.executar_query("INSERT INTO Aluno (nome, curso_id) VALUES (?, ?)", (nome, curso_id))

    def retirar_aluno(self, id):
        self.db.executar_query("DELETE FROM Aluno WHERE id = ?", (id,))

    def listar_alunos(self):
        return self.db.executar_query("SELECT id, nome FROM Aluno").fetchall()

class ProfessorManager:
    def __init__(self, database):
        self.db = database

    def inserir_professor(self, nome, curso_id, disciplina_id):
        self.db.executar_query("INSERT INTO Professores (nome, curso_id, disciplina_id) VALUES (?, ?, ?)", (nome, curso_id, disciplina_id))

    def retirar_professor(self, id):
        self.db.executar_query("DELETE FROM Professores WHERE id = ?", (id,))

    def listar_professores(self):
        return self.db.executar_query("SELECT id, nome FROM Professores").fetchall()

class Interface:
    def __init__(self, nome):
        self.janela = tk.Tk()
        self.janela.title("Gerenciador da faculdade")
        self.centralizar_janela()
        self.janela.resizable(False, False)

        self.notebook = ttk.Notebook(self.janela)
        self.notebook.grid(row=0, column=0, padx=10, pady=10)

        self.db = Database(nome)
        self.curso_manager = CursoManager(self.db)
        self.disciplina_manager = DisciplinaManager(self.db)
        self.aluno_manager = AlunoManager(self.db)
        self.professor_manager = ProfessorManager(self.db)

        self.adicionar_frames()

        self.janela.mainloop()

    def centralizar_janela(self):
        screen_width = self.janela.winfo_screenwidth()
        screen_height = self.janela.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (800 / 2))
        y_cordinate = int((screen_height / 2) - (600 / 2))

        self.janela.geometry(f"800x600+{x_cordinate}+{y_cordinate}")

    def adicionar_frames(self):
        self.frame_cursos = ttk.Frame(self.notebook)
        self.frame_disciplinas = ttk.Frame(self.notebook)
        self.frame_alunos = ttk.Frame(self.notebook)
        self.frame_professores = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_cursos, text="Cursos")
        self.notebook.add(self.frame_disciplinas, text="Disciplinas")
        self.notebook.add(self.frame_alunos, text="Alunos")
        self.notebook.add(self.frame_professores, text="Professores")

        self.adicionar_widgets()

    def adicionar_widgets(self):
        # Adicione widgets para gerenciar cursos, disciplinas, alunos e professores aqui
        pass

if __name__ == "__main__":
    Interface("faculdade")
