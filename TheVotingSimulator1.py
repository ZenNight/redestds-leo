import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class VotingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Votação Segura")  # Corrected Portuguese characters
        self.root.geometry("500x400")
        self.style = ttk.Style()
        # ... rest of the code remains the same ...
        
        # Configurar cores e fontes
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.root.configure(bg=self.bg_color)
        
        self.current_frame = None
        self.nome_eleitor = ""
        self.id_eleitor = ""
        self.candidatos = [
            "Eleitor1",
            "Eleitor2",
            "Eleitor3"
        ]
        
        self.mostrar_tela_boas_vindas()

    def limpar_janela(self):
        if self.current_frame:
            self.current_frame.destroy()

    def mostrar_tela_boas_vindas(self):
        self.limpar_janela()
        self.current_frame = tk.Frame(self.root, bg=self.bg_color)
        self.current_frame.pack(pady=50, padx=30, fill='both', expand=True)

        tk.Label(self.current_frame, 
                text="Bem-vindo ao Sistema de Votação Segura",
                font=('Helvetica', 16, 'bold'),
                bg=self.bg_color,
                fg=self.primary_color).pack(pady=10)

        tk.Label(self.current_frame, 
                text="Por favor, verifique sua identidade",
                font=('Helvetica', 12),
                bg=self.bg_color).pack(pady=5)

        form_frame = tk.Frame(self.current_frame, bg=self.bg_color)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Nome Completo:", bg=self.bg_color).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Insira seu CPF ou RG :", bg=self.bg_color).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.id_entry = ttk.Entry(form_frame, width=30)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.current_frame, 
                 text="Prosseguir para Votação",
                 command=self.verificar_identidade,
                 style='Primary.TButton').pack(pady=20)

        # Configurar estilo do botão
        self.style.configure('Primary.TButton', 
                          foreground='white',
                          background=self.secondary_color,
                          font=('Helvetica', 10, 'bold'))

    def verificar_identidade(self):
        self.nome_eleitor = self.name_entry.get().strip()
        self.id_eleitor = self.id_entry.get().strip()

        if not self.nome_eleitor or not self.id_eleitor:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios")
            return

        self.mostrar_tela_votacao()

    def mostrar_tela_votacao(self):
        self.limpar_janela()
        self.current_frame = tk.Frame(self.root, bg=self.bg_color)
        self.current_frame.pack(pady=30, padx=20, fill='both', expand=True)

        tk.Label(self.current_frame, 
                text="Selecione Seu Candidato",
                font=('Helvetica', 14, 'bold'),
                bg=self.bg_color,
                fg=self.primary_color).pack(pady=10)

        self.candidato_selecionado = tk.StringVar()

        candidate_frame = tk.Frame(self.current_frame, bg=self.bg_color)
        candidate_frame.pack(pady=15)

        for index, candidato in enumerate(self.candidatos):
            rb = ttk.Radiobutton(candidate_frame,
                               text=candidato,
                               variable=self.candidato_selecionado,
                               value=candidato,
                               style='TRadiobutton')
            rb.grid(row=index, column=0, sticky='w', pady=5)

        ttk.Button(self.current_frame,
                 text="Confirmar Voto",
                 command=self.submeter_voto,
                 style='Primary.TButton').pack(pady=20)

    def submeter_voto(self):
        selecionado = self.candidato_selecionado.get()
        if not selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um candidato antes de confirmar")
            return

        confirmacao = messagebox.askyesno("Confirmar Voto",
                                         "Você tem certeza de que deseja confirmar seu voto?\n"
                                         "Esta ação não pode ser desfeita.")
        if confirmacao:
            self.gerar_recibo(selecionado)
            self.mostrar_tela_confirmacao()

    def gerar_recibo(self, candidato):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"recibo_votacao_{self.nome_eleitor.replace(' ', '_')}_{self.id_eleitor}.txt"
        
        conteudo_recibo = f"""=== RECIBO DE VOTAÇÃO ===
        
Nome no Documento: {self.nome_eleitor}
Documento de Identidade: {self.id_eleitor}
Data e Hora: {timestamp}
Candidato Selecionado: {candidato}

Este é seu recibo oficial de votação.
Por favor, mantenha-o para seus registros.
        
Obrigado por participar das eleições!
        """
        
        with open(filename, 'w') as file:
            file.write(conteudo_recibo)

    def mostrar_tela_confirmacao(self):
        self.limpar_janela()
        self.current_frame = tk.Frame(self.root, bg=self.bg_color)
        self.current_frame.pack(pady=50, padx=30, fill='both', expand=True)

        tk.Label(self.current_frame, 
                text="Voto Confirmado com Sucesso!",
                font=('Helvetica', 16, 'bold'),
                bg=self.bg_color,
                fg='green').pack(pady=10)

        tk.Label(self.current_frame, 
                text="Seu voto foi registrado.\nUm recibo foi gerado em seu diretório.",
                font=('Helvetica', 12),
                bg=self.bg_color,
                justify='center').pack(pady=20)

        ttk.Button(self.current_frame,
                 text="Sair do Sistema",
                 command=self.root.destroy,
                 style='Primary.TButton').pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = VotingSystem(root)
    root.mainloop()
