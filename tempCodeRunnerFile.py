import json
import tkinter as tk
from tkinter import messagebox, simpledialog

def adicionar_item(lista, tree):
    nome = simpledialog.askstring("Adicionar Item", "Digite o nome do produto:")
    if not nome or not nome.strip():
        messagebox.showerror("Erro", "O nome do produto não pode estar vazio.")
        return

    try:
        quantidade = int(simpledialog.askstring("Adicionar Item", "Digite a quantidade:"))
        if quantidade <= 0:
            raise ValueError
    except (ValueError, TypeError):
        messagebox.showerror("Erro", "A quantidade deve ser um número maior que 0.")
        return

    try:
        preco = float(simpledialog.askstring("Adicionar Item", "Digite o preço:"))
        if preco < 0:
            raise ValueError
    except (ValueError, TypeError):
        messagebox.showerror("Erro", "O preço deve ser um número maior ou igual a 0.")
        return

    lista.append({"nome": nome, "quantidade": quantidade, "preco": preco})
    tree.insert("", "end", values=(nome, quantidade, f"R${preco:.2f}"))
    messagebox.showinfo("Sucesso", f"{nome} adicionado com sucesso!")

def exibir_lista(lista, tree):
    for item in tree.get_children():
        tree.delete(item)

    total = 0
    for item in lista:
        tree.insert("", "end", values=(item['nome'], item['quantidade'], f"R${item['preco']:.2f}"))
        total += item['quantidade'] * item['preco']

    return total

def remover_item(lista, tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Nenhum item selecionado para remoção.")
        return

    for item in selected_item:
        item_index = tree.index(item)
        tree.delete(item)
        lista.pop(item_index)

    messagebox.showinfo("Sucesso", "Item removido com sucesso!")

def salvar_lista(lista, arquivo="lista_compras.json"):
    with open(arquivo, "w") as f:
        json.dump(lista, f)
    messagebox.showinfo("Sucesso", "Lista salva com sucesso!")

def carregar_lista(arquivo="lista_compras.json"):
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def limpar_lista(lista, tree):
    lista.clear()
    for item in tree.get_children():
        tree.delete(item)
    messagebox.showinfo("Sucesso", "Lista apagada com sucesso!")

def criar_interface():
    lista_compras = carregar_lista()

    def atualizar_total():
        total = exibir_lista(lista_compras, tree)
        label_total["text"] = f"Total: R${total:.2f}"

    root = tk.Tk()
    root.title("Lista de Compras")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tree = tk.ttk.Treeview(frame, columns=("Nome", "Quantidade", "Preço"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço", text="Preço")
    tree.pack()

    label_total = tk.Label(root, text="Total: R$0.00", font=("Arial", 14))
    label_total.pack(pady=10)

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=10)

    btn_adicionar = tk.Button(frame_buttons, text="Adicionar Item", command=lambda: [adicionar_item(lista_compras, tree), atualizar_total()])
    btn_adicionar.grid(row=0, column=0, padx=5)

    btn_remover = tk.Button(frame_buttons, text="Remover Item", command=lambda: [remover_item(lista_compras, tree), atualizar_total()])
    btn_remover.grid(row=0, column=1, padx=5)

    btn_limpar = tk.Button(frame_buttons, text="Limpar Lista", command=lambda: [limpar_lista(lista_compras, tree), atualizar_total()])
    btn_limpar.grid(row=0, column=2, padx=5)

    btn_salvar = tk.Button(frame_buttons, text="Salvar Lista", command=lambda: salvar_lista(lista_compras))
    btn_salvar.grid(row=0, column=3, padx=5)

    atualizar_total()
    root.mainloop()

criar_interface()
