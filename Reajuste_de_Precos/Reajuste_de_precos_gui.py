# Exercício 5: Reajuste Geral de Preços (Setor Comercial) - Interface Gráfica
# Versão com interface Tkinter do script Reajuste_de_preços.py

import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

# Catálogo padrão, usado quando ainda não existe arquivo salvo
PRECOS_ORIGINAIS = {"celular": 1500.0, "tablet": 2500.0, "notebook": 5000.0}

# Arquivo de persistência (fica na mesma pasta deste script)
ARQUIVO_CATALOGO = Path(__file__).resolve().parent / "catalogo.json"


def carregar_catalogo() -> dict:
    """Lê o catálogo do JSON; se não existir ou estiver corrompido, usa o padrão."""
    try:
        with open(ARQUIVO_CATALOGO, encoding="utf-8") as f:
            dados = json.load(f)
        return {str(k).lower(): float(v) for k, v in dados.items()}
    except (FileNotFoundError, json.JSONDecodeError, ValueError, AttributeError):
        return dict(PRECOS_ORIGINAIS)


def salvar_catalogo(precos: dict) -> None:
    with open(ARQUIVO_CATALOGO, "w", encoding="utf-8") as f:
        json.dump(precos, f, ensure_ascii=False, indent=2)

# Paleta de cores
BG = "#0f172a"        # fundo da janela
CARD = "#1e293b"      # fundo do cartão
CARD_ALT = "#243044"  # linha alternada da tabela
ACCENT = "#38bdf8"    # azul de destaque
GREEN = "#4ade80"
RED = "#f87171"
TEXT = "#f1f5f9"
MUTED = "#94a3b8"


def formatar_moeda(valor: float) -> str:
    """Formata no padrão brasileiro: R$ 1.234,56"""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


class AppReajuste(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reajuste Geral de Preços")
        self.configure(bg=BG)
        self.resizable(False, False)

        # Catálogo carregado do arquivo (ou padrão, na primeira execução)
        self.precos = carregar_catalogo()
        self.percentual_atual = 0.0

        self._configurar_estilos()
        self._montar_interface()
        self._preencher_tabela(percentual=0.0)
        self._centralizar()

        self.entrada.focus_set()
        self.bind("<Return>", lambda _e: self.aplicar_reajuste())

    # ---------- construção ----------
    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure("Treeview",
                         background=CARD, fieldbackground=CARD, foreground=TEXT,
                         rowheight=34, borderwidth=0, font=("Segoe UI", 11))
        estilo.configure("Treeview.Heading",
                         background="#334155", foreground=TEXT, relief="flat",
                         font=("Segoe UI Semibold", 11), padding=8)
        estilo.map("Treeview.Heading", background=[("active", "#334155")])
        estilo.map("Treeview", background=[("selected", "#0ea5e9")],
                   foreground=[("selected", BG)])

    def _montar_interface(self):
        card = tk.Frame(self, bg=CARD, padx=32, pady=28,
                        highlightbackground="#334155", highlightthickness=1)
        card.pack(padx=40, pady=40)

        # Cabeçalho
        tk.Label(card, text="Reajuste Geral de Preços", bg=CARD, fg=TEXT,
                 font=("Segoe UI Semibold", 20)).pack(anchor="w")
        tk.Label(card, text="Setor Comercial · aplique um percentual a todo o catálogo",
                 bg=CARD, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 20))

        # Linha de entrada
        linha = tk.Frame(card, bg=CARD)
        linha.pack(fill="x", pady=(0, 18))

        tk.Label(linha, text="Percentual de aumento (%)", bg=CARD, fg=TEXT,
                 font=("Segoe UI", 11)).pack(side="left")

        self.var_percentual = tk.StringVar(value="10")
        self.entrada = self._entry(linha, self.var_percentual, width=10, justify="center", tamanho=13)
        self.entrada.pack(side="left", padx=12, ipady=6)

        self._botao(linha, "Aplicar reajuste", ACCENT, BG, self.aplicar_reajuste).pack(side="left")
        self._botao(linha, "Gravar reajuste", "#a78bfa", BG, self.gravar_reajuste).pack(side="left", padx=(8, 0))
        self._botao(linha, "Restaurar", "#334155", TEXT, self.restaurar).pack(side="left", padx=(8, 0))

        # Cadastro de produtos
        cadastro = tk.Frame(card, bg=CARD_ALT, padx=16, pady=12)
        cadastro.pack(fill="x", pady=(0, 18))

        tk.Label(cadastro, text="Cadastrar produto", bg=CARD_ALT, fg=TEXT,
                 font=("Segoe UI Semibold", 11)).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 8))

        tk.Label(cadastro, text="Nome", bg=CARD_ALT, fg=MUTED,
                 font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
        self.var_nome = tk.StringVar()
        self.entrada_nome = self._entry(cadastro, self.var_nome, width=22, justify="left")
        self.entrada_nome.grid(row=1, column=1, padx=(8, 16), ipady=5)

        tk.Label(cadastro, text="Preço (R$)", bg=CARD_ALT, fg=MUTED,
                 font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w")
        self.var_preco = tk.StringVar()
        self.entrada_preco = self._entry(cadastro, self.var_preco, width=12, justify="right")
        self.entrada_preco.grid(row=1, column=3, padx=(8, 16), ipady=5)

        self._botao(cadastro, "Adicionar", GREEN, BG, self.adicionar_produto).grid(row=1, column=4)
        self._botao(cadastro, "Remover selecionado", RED, BG,
                    self.remover_produto).grid(row=1, column=5, padx=(8, 0))

        # "break" impede que o Enter também dispare o reajuste (binding global da janela)
        self.entrada_nome.bind("<Return>", lambda _e: (self.entrada_preco.focus_set(), "break")[1])
        self.entrada_preco.bind("<Return>", lambda _e: (self.adicionar_produto(), "break")[1])

        # Tabela
        colunas = ("produto", "atual", "novo", "diferenca")
        self.tabela = ttk.Treeview(card, columns=colunas, show="headings",
                                   height=len(PRECOS_ORIGINAIS), selectmode="browse")
        titulos = {"produto": "Produto", "atual": "Preço atual",
                   "novo": "Novo preço", "diferenca": "Diferença"}
        larguras = {"produto": 160, "atual": 150, "novo": 150, "diferenca": 150}
        for col in colunas:
            self.tabela.heading(col, text=titulos[col])
            self.tabela.column(col, width=larguras[col],
                               anchor="w" if col == "produto" else "e")
        self.tabela.tag_configure("par", background=CARD)
        self.tabela.tag_configure("impar", background=CARD_ALT)
        self.tabela.pack(fill="x")

        # Rodapé com totais
        rodape = tk.Frame(card, bg=CARD)
        rodape.pack(fill="x", pady=(18, 0))

        self.lbl_total_atual = self._info(rodape, "Total atual")
        self.lbl_total_novo = self._info(rodape, "Total reajustado")
        self.lbl_variacao = self._info(rodape, "Variação")

        self.lbl_status = tk.Label(card, text="", bg=CARD, fg=MUTED, font=("Segoe UI", 10))
        self.lbl_status.pack(anchor="w", pady=(14, 0))

    def _entry(self, pai, variavel, width, justify, tamanho=11):
        return tk.Entry(pai, textvariable=variavel, width=width,
                        font=("Segoe UI", tamanho), bg=BG, fg=TEXT,
                        insertbackground=TEXT, relief="flat", justify=justify,
                        highlightthickness=2, highlightbackground="#334155",
                        highlightcolor=ACCENT)

    def _botao(self, pai, texto, cor_fundo, cor_texto, comando):
        return tk.Button(pai, text=texto, command=comando, bg=cor_fundo, fg=cor_texto,
                         activebackground=cor_fundo, activeforeground=cor_texto,
                         relief="flat", cursor="hand2", padx=16, pady=7,
                         font=("Segoe UI Semibold", 10), bd=0)

    def _info(self, pai, titulo):
        bloco = tk.Frame(pai, bg=CARD_ALT, padx=16, pady=10)
        bloco.pack(side="left", expand=True, fill="x", padx=4)
        tk.Label(bloco, text=titulo, bg=CARD_ALT, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w")
        valor = tk.Label(bloco, text="—", bg=CARD_ALT, fg=TEXT,
                         font=("Segoe UI Semibold", 13))
        valor.pack(anchor="w")
        return valor

    def _centralizar(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    # ---------- lógica ----------
    def _preencher_tabela(self, percentual: float):
        self.percentual_atual = percentual
        self.tabela.delete(*self.tabela.get_children())
        # A tabela cresce conforme a quantidade de produtos (mínimo 3, máximo 12 visíveis)
        self.tabela.config(height=max(3, min(len(self.precos), 12)))

        total_atual = total_novo = 0.0
        for i, (produto, preco) in enumerate(self.precos.items()):
            # Mesma fórmula do script original
            novo = preco * (1 + percentual / 100)
            diferenca = novo - preco
            total_atual += preco
            total_novo += novo

            sinal = "+" if diferenca >= 0 else "−"
            self.tabela.insert("", "end", iid=produto, values=(
                produto.capitalize(),
                formatar_moeda(preco),
                formatar_moeda(novo),
                f"{sinal}{formatar_moeda(abs(diferenca))}",
            ), tags=("par" if i % 2 == 0 else "impar",))

        variacao = total_novo - total_atual
        self.lbl_total_atual.config(text=formatar_moeda(total_atual))
        self.lbl_total_novo.config(text=formatar_moeda(total_novo))
        self.lbl_variacao.config(
            text=f"{'+' if variacao >= 0 else '−'}{formatar_moeda(abs(variacao))}",
            fg=GREEN if variacao > 0 else RED if variacao < 0 else TEXT)

    def aplicar_reajuste(self):
        texto = self.var_percentual.get().strip().replace("%", "").replace(",", ".")
        try:
            percentual = float(texto)
        except ValueError:
            messagebox.showerror("Valor inválido",
                                 "Digite um número válido para o percentual.\nEx.: 10 para 10%")
            self.entrada.focus_set()
            return

        self._preencher_tabela(percentual)
        self.lbl_status.config(
            text=f"Reajuste de {percentual:g}% aplicado com sucesso.", fg=GREEN)

    def restaurar(self):
        self.var_percentual.set("0")
        self._preencher_tabela(0.0)
        self.lbl_status.config(text="Reajuste removido (0%). Produtos cadastrados foram mantidos.", fg=MUTED)
        self.entrada.focus_set()

    def adicionar_produto(self):
        nome = " ".join(self.var_nome.get().split())  # remove espaços extras
        texto_preco = self.var_preco.get().strip().replace("R$", "").replace(".", "").replace(",", ".")

        if not nome:
            messagebox.showwarning("Nome obrigatório", "Informe o nome do produto.")
            self.entrada_nome.focus_set()
            return
        try:
            preco = float(texto_preco)
            if preco < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Preço inválido",
                                 "Digite um preço válido (número maior ou igual a zero).\nEx.: 1299,90")
            self.entrada_preco.focus_set()
            return

        chave = nome.lower()
        ja_existe = chave in self.precos
        if ja_existe and not messagebox.askyesno(
                "Produto já cadastrado",
                f"'{nome.capitalize()}' já existe no catálogo.\nDeseja atualizar o preço?"):
            return

        self.precos[chave] = preco
        self._salvar()
        self._preencher_tabela(self.percentual_atual)
        self.tabela.see(chave)

        self.var_nome.set("")
        self.var_preco.set("")
        self.entrada_nome.focus_set()
        acao = "atualizado" if ja_existe else "cadastrado"
        self.lbl_status.config(
            text=f"Produto '{nome.capitalize()}' {acao} por {formatar_moeda(preco)}.", fg=GREEN)

    def remover_produto(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showinfo("Nenhum produto selecionado",
                                "Clique em um produto na tabela para removê-lo.")
            return
        chave = selecao[0]
        if not messagebox.askyesno("Remover produto",
                                   f"Remover '{chave.capitalize()}' do catálogo?"):
            return
        del self.precos[chave]
        self._salvar()
        self._preencher_tabela(self.percentual_atual)
        self.lbl_status.config(text=f"Produto '{chave.capitalize()}' removido.", fg=RED)

    def gravar_reajuste(self):
        """Consolida os novos preços como base do catálogo e salva (como o script original fazia)."""
        if self.percentual_atual == 0:
            messagebox.showinfo("Nada a gravar",
                                "Aplique um percentual diferente de zero antes de gravar.")
            return
        if not messagebox.askyesno(
                "Gravar reajuste",
                f"Os novos preços (reajuste de {self.percentual_atual:g}%) passarão a ser "
                f"os preços atuais do catálogo.\n\nEsta ação não pode ser desfeita. Continuar?"):
            return
        self.precos = {p: round(v * (1 + self.percentual_atual / 100), 2)
                       for p, v in self.precos.items()}
        self._salvar()
        self.var_percentual.set("0")
        self._preencher_tabela(0.0)
        self.lbl_status.config(text="Reajuste gravado. Novos preços salvos no catálogo.", fg=GREEN)

    def _salvar(self):
        try:
            salvar_catalogo(self.precos)
        except OSError as erro:
            messagebox.showerror("Erro ao salvar",
                                 f"Não foi possível gravar o arquivo:\n{ARQUIVO_CATALOGO}\n\n{erro}")


if __name__ == "__main__":
    AppReajuste().mainloop()
