import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from uuid import uuid4
from faker import Faker
from PyPDF2 import PdfMerger

class AttendanceSystem:
    def __init__(self, root):
        self.fake = Faker('pt_BR')
        self.root = root
        self.root.title("Presence Merit 3.0")
        self.root.geometry("1200x800")
        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.output_folder = os.path.expanduser("~/Documents/PresenceMerit")
        self.daily_receipts = []
        self.cursos = self.criar_cursos_com_alunos()
        self.setup_ui()
        self.create_folders()
        self.configure_styles()

    def configure_styles(self):
        self.style.configure('TFrame', background='#f5f6fa')
        self.style.configure('TLabel', background='#f5f6fa', font=('Segoe UI', 10), foreground='#2d3436')
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'))
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#0984e3')
        self.style.configure('Accent.TButton', background='#0984e3', foreground='white')
        self.style.map('Accent.TButton', 
                      background=[('active', '#0873c4'), ('!active', '#0984e3')])

    def criar_cursos_com_alunos(self):
        return {
            "Tecnologia da Informação": [{'nome': self.fake.name(), 'id': f"TI{self.fake.unique.random_number(4)}"} for _ in range(15)],
            "Mecatrônica Industrial": [{'nome': self.fake.name(), 'id': f"MI{self.fake.unique.random_number(4)}"} for _ in range(18)],
            "Desenvolvimento Web": [{'nome': self.fake.name(), 'id': f"DW{self.fake.unique.random_number(4)}"} for _ in range(20)],
            "Redes de Computadores": [{'nome': self.fake.name(), 'id': f"RC{self.fake.unique.random_number(4)}"} for _ in range(16)],
            "Inteligência Artificial": [{'nome': self.fake.name(), 'id': f"IA{self.fake.unique.random_number(4)}"} for _ in range(17)]
        }

    def create_folders(self):
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(os.path.join(self.output_folder, 'comprovantes'), exist_ok=True)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(header_frame, text="Presence Merit - Controle de Frequência Digital", 
                style='Header.TLabel').pack(side=tk.LEFT)
        
        # Controles Superiores
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="Selecionar Pasta", 
                  command=self.select_output_folder).pack(side=tk.LEFT, padx=5)
        self.folder_label = ttk.Label(control_frame, text=f"Pasta: {self.output_folder}")
        self.folder_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(control_frame, text="Unificar Comprovantes", 
                  command=self.unificar_comprovantes).pack(side=tk.RIGHT, padx=5)
        ttk.Button(control_frame, text="Gerar Planilha", 
                  command=self.gerar_planilha).pack(side=tk.RIGHT, padx=5)

        # Corpo Principal
        body_frame = ttk.Frame(main_frame)
        body_frame.pack(fill=tk.BOTH, expand=True)

        # Painel de Cursos e Alunos
        left_frame = ttk.Frame(body_frame, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Label(left_frame, text="Selecione o Curso:").pack(anchor=tk.W)
        self.course_combo = ttk.Combobox(left_frame, values=list(self.cursos.keys()), 
                                       state="readonly")
        self.course_combo.pack(fill=tk.X, pady=5)
        self.course_combo.bind('<<ComboboxSelected>>', self.atualizar_alunos)
        self.course_combo.current(0)

        ttk.Label(left_frame, text="Alunos Matriculados:").pack(anchor=tk.W, pady=10)
        self.student_list = ttk.Treeview(left_frame, columns=('id', 'nome'), show='headings', height=15)
        self.student_list.heading('id', text='ID')
        self.student_list.column('id', width=100)
        self.student_list.heading('nome', text='Nome do Aluno')
        self.student_list.pack(fill=tk.BOTH, expand=True)

        # Painel de Registro
        right_frame = ttk.Frame(body_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        form_frame = ttk.Frame(right_frame)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Aluno Selecionado:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.selected_student = ttk.Combobox(form_frame, state='readonly', width=40)
        self.selected_student.grid(row=0, column=1, padx=5, pady=5)
        self.selected_student.bind('<<ComboboxSelected>>', self.preencher_dados)

        ttk.Label(form_frame, text="Data da Aula:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.date_entry = ttk.Entry(form_frame, width=25)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Button(form_frame, text="⌚ Data Atual", 
                 command=self.inserir_data_atual).grid(row=1, column=2, padx=5)

        # Botões de Ação
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="✅ Registrar Frequência", 
                  style='Accent.TButton', command=self.submit_attendance).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="🔄 Limpar Seleção", 
                  command=self.limpar_selecao).pack(side=tk.LEFT, padx=10)

        self.atualizar_alunos()

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.folder_label.config(text=f"Pasta: {folder}")
            self.create_folders()

    def inserir_data_atual(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def atualizar_alunos(self, event=None):
        curso = self.course_combo.get()
        alunos = self.cursos[curso]
        
        self.student_list.delete(*self.student_list.get_children())
        for aluno in alunos:
            self.student_list.insert('', tk.END, values=(aluno['id'], aluno['nome']))
        
        self.selected_student['values'] = [f"{aluno['id']} - {aluno['nome']}" for aluno in alunos]

    def preencher_dados(self, event):
        if self.selected_student.get():
            index = self.selected_student.current()
            self.student_list.selection_set(self.student_list.get_children()[index])

    def limpar_selecao(self):
        self.selected_student.set('')
        self.student_list.selection_remove(self.student_list.selection())

    def validate_inputs(self):
        if not self.selected_student.get():
            messagebox.showerror("Erro", "Selecione um aluno da lista")
            return False
        return True

    def generate_receipt(self, data):
        receipt_id = str(uuid4())[:8].upper()
        filename = os.path.join(self.output_folder, 'comprovantes', f"{data['date']}_{data['student_id']}_{receipt_id}.pdf")
        
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor('#0984e3')
        c.drawCentredString(width/2, height-50, "Presence Merit - Comprovante de Frequência")
        c.line(50, height-60, width-50, height-60)

        # Conteúdo
        c.setFont("Helvetica", 12)
        c.setFillColor('black')
        y_position = height-100
        
        content = [
            f"Curso: {data['course']}",
            f"Aluno: {data['name']}",
            f"ID do Aluno: {data['student_id']}",
            f"Data da Aula: {data['date']}",
            f"Registro realizado em: {data['timestamp']}",
            f"Código do Comprovante: {receipt_id}"
        ]

        for line in content:
            c.drawString(50, y_position, line)
            y_position -= 25

        c.save()
        self.daily_receipts.append(filename)
        return filename

    def save_to_csv(self, data):
        csv_path = os.path.join(self.output_folder, 'registros.csv')
        file_exists = os.path.isfile(csv_path)
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

    def unificar_comprovantes(self):
        if not self.daily_receipts:
            messagebox.showwarning("Aviso", "Nenhum comprovante gerado hoje!")
            return

        merger = PdfMerger()
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_file = os.path.join(self.output_folder, f"comprovantes_unificados_{date_str}.pdf")

        for pdf in self.daily_receipts:
            merger.append(pdf)

        merger.write(output_file)
        merger.close()
        messagebox.showinfo("Sucesso", f"Comprovantes unificados salvos em:\n{output_file}")
        self.daily_receipts = []

    def gerar_planilha(self):
        csv_path = os.path.join(self.output_folder, 'registros.csv')
        if not os.path.exists(csv_path):
            messagebox.showerror("Erro", "Nenhum registro encontrado!")
            return

        df = pd.read_csv(csv_path)
        excel_path = os.path.join(self.output_folder, 'registros.xlsx')
        
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
            worksheet = writer.sheets['Sheet1']
            
            # Formatação
            header_format = writer.book.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#0984e3',
                'font_color': 'white',
                'border': 1
            })
            
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, max(len(value), 12))

        messagebox.showinfo("Sucesso", f"Planilha gerada em:\n{excel_path}")

    def submit_attendance(self):
        if not self.validate_inputs():
            return

        aluno_id, aluno_nome = self.selected_student.get().split(' - ', 1)
        
        attendance_data = {
            'name': aluno_nome.strip(),
            'student_id': aluno_id.strip(),
            'course': self.course_combo.get(),
            'date': self.date_entry.get(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            receipt_path = self.generate_receipt(attendance_data)
            self.save_to_csv(attendance_data)
            
            messagebox.showinfo("Sucesso", 
                f"Registro realizado!\nComprovante: {receipt_path}")
            
            self.limpar_selecao()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no registro: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()