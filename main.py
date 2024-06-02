import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("university.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Curso (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Disciplina (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            curso_id INTEGER,
            FOREIGN KEY (curso_id) REFERENCES Curso(id)
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Professor (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            curso_id INTEGER,
            disciplina_id INTEGER,
            FOREIGN KEY (curso_id) REFERENCES Curso(id),
            FOREIGN KEY (disciplina_id) REFERENCES Disciplina(id)
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Aluno (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            curso_id INTEGER,
            FOREIGN KEY (curso_id) REFERENCES Curso(id)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Matricula (
            aluno_id INTEGER,
            disciplina_id INTEGER,
            PRIMARY KEY (aluno_id, disciplina_id),
            FOREIGN KEY (aluno_id) REFERENCES Aluno(id),
            FOREIGN KEY (disciplina_id) REFERENCES Disciplina(id)
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Nota (
            id INTEGER PRIMARY KEY,
            aluno_id INTEGER,
            disciplina_id INTEGER,
            nota REAL,
            FOREIGN KEY (aluno_id) REFERENCES Aluno(id),
            FOREIGN KEY (disciplina_id) REFERENCES Disciplina(id)
        )""")
        
        self.conn.commit()

    def inserir_nota(self, aluno_id, disciplina_id, nota):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Nota (aluno_id, disciplina_id, nota) VALUES (?, ?, ?)", (aluno_id, disciplina_id, nota))
        self.conn.commit()

    def listar_notas_por_disciplina(self, disciplina_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Aluno.nome, Nota.nota FROM Nota
        JOIN Aluno ON Nota.aluno_id = Aluno.id
        WHERE Nota.disciplina_id = ?
        """, (disciplina_id,))
        return cursor.fetchall()

    def inserir(self, tabela, valores):
        cursor = self.conn.cursor()
        placeholders = ', '.join(['?'] * len(valores))
        cursor.execute(f"INSERT INTO {tabela} VALUES ({placeholders})", valores)
        self.conn.commit()

    def remover(self, tabela, id):
        cursor = self.conn.cursor()
        cursor.execute(f"DELETE FROM {tabela} WHERE id = ?", (id,))
        self.conn.commit()

    def atualizar(self, tabela, coluna, valor, id):
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE {tabela} SET {coluna} = ? WHERE id = ?", (valor, id))
        self.conn.commit()

    def listar(self, tabela):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {tabela}")
        return cursor.fetchall()

    def listar_disciplinas_por_curso(self, curso_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Disciplina WHERE curso_id = ?", (curso_id,))
        return cursor.fetchall()

    def listar_alunos_por_disciplina(self, disciplina_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT Aluno.id, Aluno.nome FROM Aluno
        JOIN Matricula ON Aluno.id = Matricula.aluno_id
        WHERE Matricula.disciplina_id = ?
        """, (disciplina_id,))
        return cursor.fetchall()

    def listar_professores_por_disciplina(self, disciplina_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Professor WHERE disciplina_id = ?", (disciplina_id,))
        return cursor.fetchall()

    def listar_professores_por_curso(self, curso_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Professor WHERE curso_id = ?", (curso_id,))
        return cursor.fetchall()
    
    def matricula_existe(self, aluno_id, disciplina_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Matricula WHERE aluno_id = ? AND disciplina_id = ?", (aluno_id, disciplina_id))
        return cursor.fetchone()[0] > 0


class BaseTab:
    def __init__(self, notebook, db, tab_name):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text=tab_name)
        self.db = db
        self.create_widgets()

    def create_widgets(self):
        pass

    def create_scrollable_listbox(self, row, col, rowspan=1, columnspan=1):
        frame = tk.Frame(self.frame)
        frame.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, padx=10, pady=5)
        scrollbar = tk.Scrollbar(frame)
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=listbox.yview)
        return listbox


class CursosTab(BaseTab):
    def __init__(self, notebook, db):
        super().__init__(notebook, db, "Cursos")

    def create_widgets(self):
        self.adicionar_curso_frame()
        self.remover_curso_frame()
        self.atualizar_curso_frame()
        self.listar_cursos_frame()
        self.listar_disciplinas_por_curso_frame()

    def adicionar_curso_frame(self):
        tk.Label(self.frame, text="Nome do Curso:").grid(row=0, column=0, padx=10, pady=5)
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Adicionar", command=self.inserir_curso).grid(row=1, column=0, columnspan=2, pady=5)

    def inserir_curso(self):
        nome = self.nome_entry.get()
        self.db.inserir("Curso", (None, nome))
        messagebox.showinfo("Sucesso", "Curso inserido com sucesso!")
        self.listar_cursos_frame()

    def remover_curso_frame(self):
        tk.Label(self.frame, text="ID do Curso:").grid(row=2, column=0, padx=10, pady=5)
        self.id_entry = tk.Entry(self.frame)
        self.id_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Remover", command=self.remover_curso).grid(row=3, column=0, columnspan=2, pady=5)

    def remover_curso(self):
        id_curso = self.id_entry.get()
        self.db.remover("Curso", int(id_curso))
        messagebox.showinfo("Sucesso", "Curso removido com sucesso!")
        self.listar_cursos_frame()

    def atualizar_curso_frame(self):
        tk.Label(self.frame, text="ID do Curso:").grid(row=4, column=0, padx=10, pady=5)
        self.id_update_entry = tk.Entry(self.frame)
        self.id_update_entry.grid(row=4, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Novo Nome:").grid(row=5, column=0, padx=10, pady=5)
        self.nome_update_entry = tk.Entry(self.frame)
        self.nome_update_entry.grid(row=5, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Atualizar", command=self.atualizar_curso).grid(row=6, column=0, columnspan=2, pady=5)

    def atualizar_curso(self):
        id_curso = self.id_update_entry.get()
        novo_nome = self.nome_update_entry.get()
        self.db.atualizar("Curso", "nome", novo_nome, int(id_curso))
        messagebox.showinfo("Sucesso", "Curso atualizado com sucesso!")
        self.listar_cursos_frame()

    def listar_cursos_frame(self):
        cursos = self.db.listar("Curso")
        if hasattr(self, 'cursos_listbox'):
            self.cursos_listbox.destroy()
        self.cursos_listbox = self.create_scrollable_listbox(7, 0, columnspan=2)
        for curso in cursos:
            self.cursos_listbox.insert(tk.END, f"ID: {curso[0]} - Nome: {curso[1]}")

    def listar_disciplinas_por_curso_frame(self):
        tk.Label(self.frame, text="ID do Curso:").grid(row=8, column=0, padx=10, pady=5)
        self.id_curso_entry = tk.Entry(self.frame)
        self.id_curso_entry.grid(row=8, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Listar Disciplinas", command=self.listar_disciplinas_por_curso).grid(row=9, column=0, columnspan=2, pady=5)

    def listar_disciplinas_por_curso(self):
        curso_id = self.id_curso_entry.get()
        disciplinas = self.db.listar_disciplinas_por_curso(int(curso_id))
        if hasattr(self, 'disciplinas_listbox'):
            self.disciplinas_listbox.destroy()
        self.disciplinas_listbox = self.create_scrollable_listbox(10, 0, columnspan=2)
        for disciplina in disciplinas:
            self.disciplinas_listbox.insert(tk.END, f"ID: {disciplina[0]} - Nome: {disciplina[1]} - Curso ID: {disciplina[2]}")

class DisciplinasTab(BaseTab):
    def __init__(self, notebook, db):
        super().__init__(notebook, db, "Disciplinas")

    def create_widgets(self):
        self.adicionar_disciplina_frame()
        self.remover_disciplina_frame()
        self.atualizar_disciplina_frame()
        self.listar_disciplinas_frame()

    def adicionar_disciplina_frame(self):
        tk.Label(self.frame, text="Nome da Disciplina:").grid(row=0, column=0, padx=10, pady=5)
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="ID do Curso:").grid(row=1, column=0, padx=10, pady=5)
        self.curso_id_entry = tk.Entry(self.frame)
        self.curso_id_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Adicionar", command=self.inserir_disciplina).grid(row=2, column=0, columnspan=2, pady=5)

    def inserir_disciplina(self):
        nome = self.nome_entry.get()
        curso_id = self.curso_id_entry.get()
        self.db.inserir("Disciplina", (None, nome, curso_id))
        messagebox.showinfo("Sucesso", "Disciplina inserida com sucesso!")
        self.listar_disciplinas_frame()

    def remover_disciplina_frame(self):
        tk.Label(self.frame, text="ID da Disciplina:").grid(row=3, column=0, padx=10, pady=5)
        self.id_entry = tk.Entry(self.frame)
        self.id_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Remover", command=self.remover_disciplina).grid(row=4, column=0, columnspan=2, pady=5)

    def remover_disciplina(self):
        id_disciplina = self.id_entry.get()
        self.db.remover("Disciplina", int(id_disciplina))
        messagebox.showinfo("Sucesso", "Disciplina removida com sucesso!")
        self.listar_disciplinas_frame()

    def atualizar_disciplina_frame(self):
        tk.Label(self.frame, text="ID da Disciplina:").grid(row=5, column=0, padx=10, pady=5)
        self.id_update_entry = tk.Entry(self.frame)
        self.id_update_entry.grid(row=5, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Novo Nome:").grid(row=6, column=0, padx=10, pady=5)
        self.nome_update_entry = tk.Entry(self.frame)
        self.nome_update_entry.grid(row=6, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Atualizar", command=self.atualizar_disciplina).grid(row=7, column=0, columnspan=2, pady=5)

    def atualizar_disciplina(self):
        id_disciplina = self.id_update_entry.get()
        novo_nome = self.nome_update_entry.get()
        self.db.atualizar("Disciplina", "nome", novo_nome, int(id_disciplina))
        messagebox.showinfo("Sucesso", "Disciplina atualizada com sucesso!")
        self.listar_disciplinas_frame()

    def listar_disciplinas_frame(self):
        disciplinas = self.db.listar("Disciplina")
        if hasattr(self, 'disciplinas_listbox'):
            self.disciplinas_listbox.destroy()
        self.disciplinas_listbox = self.create_scrollable_listbox(8, 0, columnspan=2)
        for disciplina in disciplinas:
            self.disciplinas_listbox.insert(tk.END, f"ID: {disciplina[0]} - Nome: {disciplina[1]} - Curso ID: {disciplina[2]}")

class ProfessoresTab(BaseTab):
    def __init__(self, notebook, db):
        super().__init__(notebook, db, "Professores")

    def create_widgets(self):
        self.adicionar_professor_frame()
        self.remover_professor_frame()
        self.atualizar_professor_frame()
        self.listar_professores_frame()

    def adicionar_professor_frame(self):
        tk.Label(self.frame, text="Nome do Professor:").grid(row=0, column=0, padx=10, pady=5)
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="ID do Curso:").grid(row=1, column=0, padx=10, pady=5)
        self.curso_id_entry = tk.Entry(self.frame)
        self.curso_id_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="ID da Disciplina:").grid(row=2, column=0, padx=10, pady=5)
        self.disciplina_id_entry = tk.Entry(self.frame)
        self.disciplina_id_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Adicionar", command=self.inserir_professor).grid(row=3, column=0, columnspan=2, pady=5)

    def inserir_professor(self):
        nome = self.nome_entry.get()
        curso_id = self.curso_id_entry.get()
        disciplina_id = self.disciplina_id_entry.get()
        self.db.inserir("Professor", (None, nome, curso_id, disciplina_id))
        messagebox.showinfo("Sucesso", "Professor inserido com sucesso!")
        self.listar_professores_frame()

    def remover_professor_frame(self):
        tk.Label(self.frame, text="ID do Professor:").grid(row=4, column=0, padx=10, pady=5)
        self.id_entry = tk.Entry(self.frame)
        self.id_entry.grid(row=4, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Remover", command=self.remover_professor).grid(row=5, column=0, columnspan=2, pady=5)

    def remover_professor(self):
        id_professor = self.id_entry.get()
        self.db.remover("Professor", int(id_professor))
        messagebox.showinfo("Sucesso", "Professor removido com sucesso!")
        self.listar_professores_frame()

    def atualizar_professor_frame(self):
        tk.Label(self.frame, text="ID do Professor:").grid(row=6, column=0, padx=10, pady=5)
        self.id_update_entry = tk.Entry(self.frame)
        self.id_update_entry.grid(row=6, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Novo Nome:").grid(row=7, column=0, padx=10, pady=5)
        self.nome_update_entry = tk.Entry(self.frame)
        self.nome_update_entry.grid(row=7, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Atualizar", command=self.atualizar_professor).grid(row=8, column=0, columnspan=2, pady=5)

    def atualizar_professor(self):
        id_professor = self.id_update_entry.get()
        novo_nome = self.nome_update_entry.get()
        self.db.atualizar("Professor", "nome", novo_nome, int(id_professor))
        messagebox.showinfo("Sucesso", "Professor atualizado com sucesso!")
        self.listar_professores_frame()

    def listar_professores_frame(self):
        professores = self.db.listar("Professor")
        if hasattr(self, 'professores_listbox'):
            self.professores_listbox.destroy()
        self.professores_listbox = self.create_scrollable_listbox(9, 0, columnspan=2)
        for professor in professores:
            self.professores_listbox.insert(tk.END, f"ID: {professor[0]} - Nome: {professor[1]} - Curso ID: {professor[2]} - Disciplina ID: {professor[3]}")

class AlunosTab(BaseTab):
    def __init__(self, notebook, db):
        super().__init__(notebook, db, "Alunos")

    def create_widgets(self):
        self.adicionar_aluno_frame()
        self.remover_aluno_frame()
        self.atualizar_aluno_frame()
        self.listar_alunos_frame()
        self.matricular_aluno_frame()
        self.listar_alunos_por_disciplina_frame()

    def adicionar_aluno_frame(self):
        tk.Label(self.frame, text="Nome do Aluno:").grid(row=0, column=0, padx=10, pady=5)
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="ID do Curso:").grid(row=1, column=0, padx=10, pady=5)
        self.curso_id_entry = tk.Entry(self.frame)
        self.curso_id_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Adicionar", command=self.inserir_aluno).grid(row=2, column=0, columnspan=2, pady=5)

    def inserir_aluno(self):
        nome = self.nome_entry.get()
        curso_id = self.curso_id_entry.get()
        self.db.inserir("Aluno", (None, nome, int(curso_id)))
        messagebox.showinfo("Sucesso", "Aluno inserido com sucesso!")
        self.listar_alunos_frame()

    def remover_aluno_frame(self):
        tk.Label(self.frame, text="ID do Aluno:").grid(row=3, column=0, padx=10, pady=5)
        self.id_entry = tk.Entry(self.frame)
        self.id_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Remover", command=self.remover_aluno).grid(row=4, column=0, columnspan=2, pady=5)

    def remover_aluno(self):
        id_aluno = self.id_entry.get()
        self.db.remover("Aluno", int(id_aluno))
        messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
        self.listar_alunos_frame()

    def atualizar_aluno_frame(self):
        tk.Label(self.frame, text="ID do Aluno:").grid(row=5, column=0, padx=10, pady=5)
        self.id_update_entry = tk.Entry(self.frame)
        self.id_update_entry.grid(row=5, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="Novo Nome:").grid(row=6, column=0, padx=10, pady=5)
        self.nome_update_entry = tk.Entry(self.frame)
        self.nome_update_entry.grid(row=6, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Atualizar", command=self.atualizar_aluno).grid(row=7, column=0, columnspan=2, pady=5)

    def atualizar_aluno(self):
        id_aluno = self.id_update_entry.get()
        novo_nome = self.nome_update_entry.get()
        self.db.atualizar("Aluno", "nome", novo_nome, int(id_aluno))
        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
        self.listar_alunos_frame()

    def listar_alunos_frame(self):
        alunos = self.db.listar("Aluno")
        if hasattr(self, 'alunos_listbox'):
            self.alunos_listbox.destroy()
        self.alunos_listbox = self.create_scrollable_listbox(8, 0, columnspan=2)
        for aluno in alunos:
            self.alunos_listbox.insert(tk.END, f"ID: {aluno[0]} - Nome: {aluno[1]}")

    def matricular_aluno_frame(self):
        tk.Label(self.frame, text="ID do Aluno:").grid(row=10, column=0, padx=10, pady=5)
        self.aluno_id_entry = tk.Entry(self.frame)
        self.aluno_id_entry.grid(row=10, column=1, padx=10, pady=5)
        tk.Label(self.frame, text="ID da Disciplina:").grid(row=11, column=0, padx=10, pady=5)
        self.disciplina_id_entry = tk.Entry(self.frame)
        self.disciplina_id_entry.grid(row=11, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Matricular", command=self.matricular_aluno).grid(row=12, column=0, columnspan=2, pady=5)

    def matricular_aluno(self):
        aluno_id = self.aluno_id_entry.get()
        disciplina_id = self.disciplina_id_entry.get()
        if self.db.matricula_existe(int(aluno_id), int(disciplina_id)):
            messagebox.showerror("Erro", "O aluno já está matriculado nesta disciplina.")
        else:
            self.db.inserir("Matricula", (int(aluno_id), int(disciplina_id)))
            messagebox.showinfo("Sucesso", "Aluno matriculado com sucesso!")

    def listar_alunos_por_disciplina_frame(self):
        tk.Label(self.frame, text="ID da Disciplina:").grid(row=13, column=0, padx=10, pady=5)
        self.id_disciplina_entry = tk.Entry(self.frame)
        self.id_disciplina_entry.grid(row=13, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Listar Alunos", command=self.listar_alunos_por_disciplina).grid(row=14, column=0, columnspan=2, pady=5)
        self.alunos_disciplina_listbox = self.create_scrollable_listbox(15, 0, columnspan=2)

    def listar_alunos_por_disciplina(self):
        id_disciplina = self.id_disciplina_entry.get()
        alunos = self.db.listar_alunos_por_disciplina(int(id_disciplina))
        self.alunos_disciplina_listbox.delete(0, tk.END)
        for aluno in alunos:
            self.alunos_disciplina_listbox.insert(tk.END, f"ID: {aluno[0]} - Nome: {aluno[1]}")

class NotasTab(BaseTab):
    def __init__(self, notebook, db):
        super().__init__(notebook, db, "Notas")

    def create_widgets(self):
        self.adicionar_nota_frame()
        self.gerar_grafico_frame()

    def adicionar_nota_frame(self):
        tk.Label(self.frame, text="ID do Aluno:").grid(row=0, column=0, padx=10, pady=5)
        self.aluno_id_entry = tk.Entry(self.frame)
        self.aluno_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.frame, text="ID da Disciplina:").grid(row=1, column=0, padx=10, pady=5)
        self.disciplina_id_entry = tk.Entry(self.frame)
        self.disciplina_id_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.frame, text="Nota:").grid(row=2, column=0, padx=10, pady=5)
        self.nota_entry = tk.Entry(self.frame)
        self.nota_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Button(self.frame, text="Adicionar Nota", command=self.inserir_nota).grid(row=3, column=0, columnspan=2, pady=5)

    def inserir_nota(self):
        aluno_id = self.aluno_id_entry.get()
        disciplina_id = self.disciplina_id_entry.get()
        nota = self.nota_entry.get()
        self.db.inserir_nota(int(aluno_id), int(disciplina_id), float(nota))
        messagebox.showinfo("Sucesso", "Nota inserida com sucesso!")

    def gerar_grafico_frame(self):
        tk.Label(self.frame, text="ID da Disciplina para Gráfico:").grid(row=4, column=0, padx=10, pady=5)
        self.disciplina_id_grafico_entry = tk.Entry(self.frame)
        self.disciplina_id_grafico_entry.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Button(self.frame, text="Gerar Gráfico", command=self.gerar_grafico).grid(row=5, column=0, columnspan=2, pady=5)

    def gerar_grafico(self):
        disciplina_id = self.disciplina_id_grafico_entry.get()
        notas = self.db.listar_notas_por_disciplina(int(disciplina_id))
        
        alunos = [nota[0] for nota in notas]
        notas_valores = [nota[1] for nota in notas]
        
        fig, ax = plt.subplots()
        ax.scatter(alunos, notas_valores)
        
        ax.set_xlabel('Alunos')
        ax.set_ylabel('Notas')
        ax.set_title('Notas dos Alunos por Disciplina')
        
        for i, txt in enumerate(notas_valores):
            ax.annotate(txt, (alunos[i], notas_valores[i]))
        
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().grid(row=6, column=0, columnspan=2)
        canvas.draw()

class App:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Sistema Universitário")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill="both")

        CursosTab(self.notebook, self.db)
        DisciplinasTab(self.notebook, self.db)
        ProfessoresTab(self.notebook, self.db)
        AlunosTab(self.notebook, self.db)
        NotasTab(self.notebook, self.db)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
