from pathlib import Path
from datetime import datetime
import csv
from tkinter import messagebox
import customtkinter as ctk

pasta = Path.home() / "Registro de Ocorrencias"
pasta.mkdir(parents=True, exist_ok=True)

arquivo = pasta / "Ocorrencias.csv"
arquivo.touch(exist_ok=True)

COLUNAS = ["Categoria", "Protocolo", "Pessoa", "CPF", "Descrição", "Local", "Data", "Status"]
COLUNAS_EDITAVEIS = ["Categoria", "Pessoa", "CPF", "Descrição", "Local", "Data", "Status"]
STATUS_VALIDOS = ("Aberto", "Em andamento", "Concluído")

Lista_Categorias = {
    "Água": [],
    "Infraestrutura": [],
    "Saneamento": []
}

def carregar_chamados():
    """Lê todas as linhas do arquivo CSV e retorna uma lista de dicionários."""
    if not arquivo.exists() or arquivo.stat().st_size == 0:
        return []
    with arquivo.open("r", newline="", encoding="latin-1") as f:
        return list(csv.DictReader(f))


def salvar_chamados(linhas):
    """Sobrescreve o arquivo CSV com a lista atualizada de chamados."""
    with arquivo.open("w", newline="", encoding="latin-1") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(linhas)


def protocolo_existe(protocolo):
    """Verifica se um número de protocolo já está registrado no CSV."""
    linhas = carregar_chamados()
    return any(str(linha["Protocolo"]).strip() == str(protocolo).strip() for linha in linhas)


def gerar_proximo_protocolo():
    """Encontra o maior protocolo cadastrado no CSV e retorna o próximo número (+1)."""
    linhas = carregar_chamados()
    maior_protocolo = 0

    for row in linhas:
        prot_str = str(row.get("Protocolo", "")).strip()
        if prot_str.isdigit():
            protocolo_atual = int(prot_str)
            if protocolo_atual > maior_protocolo:
                maior_protocolo = protocolo_atual

    return maior_protocolo + 1


def validar_entrada(coluna, valor):
    """Valida e formata o dado digitado de acordo com a coluna."""
    valor = str(valor).strip()

    if not valor:
        return False, f"O campo '{coluna}' não pode ficar vazio."

    match coluna:
        case "Categoria":
            cat_formatada = valor.capitalize()
            if cat_formatada not in Lista_Categorias:
                opcoes = ", ".join(Lista_Categorias.keys())
                return False, f"Categoria inválida. Escolha entre: {opcoes}."
            return True, cat_formatada

        case "CPF":
            cpf_limpo = valor.replace(".", "").replace("-", "")
            if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
                return False, "CPF inválido. Digite exatamente 11 números."
            cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
            return True, cpf_formatado

        case "Data":
            data_limpa = valor.replace("/", "")
            if not data_limpa.isdigit() or len(data_limpa) != 8:
                return False, "Data inválida. Use o formato DD/MM/AAAA (8 dígitos)."
            data_formatada = f"{data_limpa[:2]}/{data_limpa[2:4]}/{data_limpa[4:]}"
            return True, data_formatada

        case "Status":
            status_formatado = valor.capitalize()
            if status_formatado not in STATUS_VALIDOS:
                return False, f"Status inválido. Escolha entre: {', '.join(STATUS_VALIDOS)}."
            return True, status_formatado

        case _:
            return True, valor


def criar_chamado(categoria, protocolo, pessoa, cpf, desc, local, data, status):
    """Cria o dicionário do chamado, armazena em memória e adiciona ao CSV."""
    if protocolo_existe(protocolo):
        return None

    categoria_formatada = categoria.strip().capitalize()
    if categoria_formatada not in Lista_Categorias:
        return None

    chamado = {
        "Categoria": categoria_formatada,
        "Protocolo": str(protocolo),
        "Pessoa": pessoa,
        "CPF": cpf,
        "Descrição": desc,
        "Local": local,
        "Data": data,
        "Status": status
    }

    Lista_Categorias[categoria_formatada].append(chamado)
    arquivo_vazio = not arquivo.exists() or arquivo.stat().st_size == 0

    with arquivo.open("a", newline="", encoding="latin-1") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUNAS)
        if arquivo_vazio:
            escritor.writeheader()
        escritor.writerow(chamado)

    return chamado


def atualizar_registro_csv(protocolo, coluna, novo_valor):
    """Valida e atualiza uma coluna específica de um protocolo no CSV."""
    valido, resultado = validar_entrada(coluna, novo_valor)
    if not valido:
        return False, resultado

    linhas = carregar_chamados()
    atualizado = False

    for row in linhas:
        if str(row["Protocolo"]).strip() == str(protocolo).strip():
            row[coluna] = resultado
            atualizado = True
            break

    if not atualizado:
        return False, f"Protocolo {protocolo} não encontrado."

    salvar_chamados(linhas)
    return True, f"Protocolo {protocolo} atualizado com sucesso!"


def deletar_registro_csv(protocolo):
    """Remove um chamado pelo número de protocolo e salva o CSV."""
    linhas = carregar_chamados()
    linhas_mantidas = [row for row in linhas if str(row["Protocolo"]).strip() != str(protocolo).strip()]

    if len(linhas_mantidas) == len(linhas):
        return False

    salvar_chamados(linhas_mantidas)
    return True


def primeira_vez():
    """Popula o CSV com chamados de exemplo caso o arquivo esteja vazio."""
    if arquivo.exists() and arquivo.stat().st_size > 0:
        return

    exemplos = [
        ("Água", 123458, "Carlos Eduardo", "333.444.555-67", "Vazamento de água limpa na calçada", "Tatuapé", "12/11/2026", "Aberto"),
        ("Água", 123459, "Fernanda Lima", "444.555.666-78", "Baixa pressão de água nas torneiras", "Ipiranga", "13/11/2026", "Em andamento"),
        ("Água", 123460, "Roberto Alves", "555.666.777-89", "Água saindo com coloração turva", "Santana", "13/11/2026", "Aberto"),
        ("Água", 123461, "Juliana Costa", "666.777.888-90", "Hidrômetro danificado vazando na rua", "Pinheiros", "14/11/2026", "Concluído"),
        ("Infraestrutura", 123462, "Marcos Paulo", "777.888.999-01", "Calçada cedendo próximo ao ponto de ônibus", "Belém", "14/11/2026", "Aberto"),
        ("Infraestrutura", 123463, "Patrícia Souza", "888.999.000-12", "Poste de iluminação pública apagado", "Vila Mariana", "14/11/2026", "Em andamento"),
        ("Infraestrutura", 123464, "Lucas Mendes", "999.000.111-23", "Asfalto afundando no cruzamento", "Penha", "15/11/2026", "Aberto"),
        ("Infraestrutura", 123465, "Aline Rocha", "101.202.303-44", "Sinalização de trânsito caída na via", "Lapa", "15/11/2026", "Concluído"),
        ("Saneamento", 123466, "Ricardo Gomes", "202.303.404-55", "Bueiro entupido causando alagamento", "Itaquera", "15/11/2026", "Aberto"),
        ("Saneamento", 123467, "Camila Dias", "303.404.505-66", "Vazamento de esgoto a céu aberto", "Jabaquara", "15/11/2026", "Em andamento"),
        ("Saneamento", 123468, "Felipe Nascimento", "404.505.606-77", "Mau cheiro forte vindo da galeria pluvial", "Casa Verde", "16/11/2026", "Aberto"),
        ("Saneamento", 123469, "Beatriz Martins", "505.606.707-88", "Tampa de poço de visita deslocada", "Butantã", "16/11/2026", "Concluído"),
    ]
    for item in exemplos:
        criar_chamado(*item)


# ==============================================================================
# 3. INTERFACE GRÁFICA MODERNA (CUSTOMTKINTER)
# ==============================================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SistemaChamadosApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão de Ocorrências")
        self.geometry("1120x680")
        self.minsize(960, 600)

        # Layout principal: Coluna 0 (Sidebar fixa) | Coluna 1 (Área de conteúdo expansível)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._construir_sidebar()
        self._construir_tela_consulta()
        self._construir_tela_criar()
        self._construir_tela_atualizar()

        # Inicia na tela de consulta e atualiza os dados
        self.mostrar_tela("consulta")
        self.atualizar_interface_geral()

    # --------------------------------------------------------------------------
    # MENU LATERAL E INDICADORES (KPIs)
    # --------------------------------------------------------------------------
    def _construir_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="Central de Chamados",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(25, 5), padx=20)

        ctk.CTkLabel(
            self.sidebar,
            text="Gestão de Ocorrências CSV",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        ).pack(pady=(0, 25), padx=20)

        # Botões de navegação
        self.btn_nav_consulta = ctk.CTkButton(
            self.sidebar, text="Consultar Chamados", height=40, anchor="w",
            command=lambda: self.mostrar_tela("consulta")
        )
        self.btn_nav_consulta.pack(fill="x", padx=18, pady=6)

        self.btn_nav_criar = ctk.CTkButton(
            self.sidebar, text="+ Novo Chamado", height=40, anchor="w",
            command=lambda: self.mostrar_tela("criar")
        )
        self.btn_nav_criar.pack(fill="x", padx=18, pady=6)

        self.btn_nav_atualizar = ctk.CTkButton(
            self.sidebar, text="Atualizar Chamado", height=40, anchor="w",
            command=lambda: self.mostrar_tela("atualizar")
        )
        self.btn_nav_atualizar.pack(fill="x", padx=18, pady=6)

        # Painel de resumo (KPIs) no rodapé da barra lateral
        self.kpi_frame = ctk.CTkFrame(self.sidebar, fg_color=("gray85", "gray17"))
        self.kpi_frame.pack(side="bottom", fill="x", padx=18, pady=20)

        ctk.CTkLabel(
            self.kpi_frame, text="Resumo Operacional",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=(10, 8))

        self.lbl_kpi_total = ctk.CTkLabel(self.kpi_frame, text="Total: 0", anchor="w")
        self.lbl_kpi_total.pack(fill="x", padx=15, pady=2)

        self.lbl_kpi_abertos = ctk.CTkLabel(self.kpi_frame, text="Abertos: 0", text_color="#FF6B6B", anchor="w")
        self.lbl_kpi_abertos.pack(fill="x", padx=15, pady=2)

        self.lbl_kpi_andamento = ctk.CTkLabel(self.kpi_frame, text="Em andamento: 0", text_color="#FFD166", anchor="w")
        self.lbl_kpi_andamento.pack(fill="x", padx=15, pady=2)

        self.lbl_kpi_concluidos = ctk.CTkLabel(self.kpi_frame, text="Concluídos: 0", text_color="#06D6A0", anchor="w")
        self.lbl_kpi_concluidos.pack(fill="x", padx=15, pady=(2, 12))

    # --------------------------------------------------------------------------
    # TELA 1: CONSULTAR / LISTAR / EXCLUIR CHAMADOS
    # --------------------------------------------------------------------------
    def _construir_tela_consulta(self):
        self.frame_consulta = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_consulta.grid_columnconfigure(0, weight=1)
        self.frame_consulta.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.frame_consulta, text="Consultar Ocorrências",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(22, 12))

        # Barra de busca e filtro
        barra_filtro = ctk.CTkFrame(self.frame_consulta)
        barra_filtro.grid(row=1, column=0, sticky="ew", padx=25, pady=(0, 15))
        barra_filtro.grid_columnconfigure(1, weight=1)

        self.combo_filtro_coluna = ctk.CTkOptionMenu(
            barra_filtro,
            values=["Todos"] + COLUNAS,
            width=160,
            command=lambda _: self.renderizar_lista_chamados()
        )
        self.combo_filtro_coluna.set("Todos")
        self.combo_filtro_coluna.grid(row=0, column=0, padx=12, pady=12)

        self.entry_busca = ctk.CTkEntry(
            barra_filtro,
            placeholder_text="Digite para filtrar por protocolo, nome, bairro, descrição..."
        )
        self.entry_busca.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=12)
        self.entry_busca.bind("<KeyRelease>", lambda _: self.renderizar_lista_chamados())

        ctk.CTkButton(
            barra_filtro, text="Limpar", width=90, fg_color="gray35", hover_color="gray25",
            command=self._limpar_filtros
        ).grid(row=0, column=2, padx=(0, 12), pady=12)

        # Lista rolável de cartões
        self.scroll_chamados = ctk.CTkScrollableFrame(self.frame_consulta)
        self.scroll_chamados.grid(row=2, column=0, sticky="nsew", padx=25, pady=(0, 20))
        self.scroll_chamados.grid_columnconfigure(0, weight=1)

    def _limpar_filtros(self):
        self.combo_filtro_coluna.set("Todos")
        self.entry_busca.delete(0, "end")
        self.renderizar_lista_chamados()

    def renderizar_lista_chamados(self):
        for widget in self.scroll_chamados.winfo_children():
            widget.destroy()

        linhas = carregar_chamados()
        coluna_filtro = self.combo_filtro_coluna.get()
        termo = self.entry_busca.get().strip().lower()

        filtradas = []
        for row in linhas:
            if not termo:
                filtradas.append(row)
            elif coluna_filtro == "Todos":
                if any(termo in str(v).lower() for v in row.values()):
                    filtradas.append(row)
            else:
                valor_campo = str(row.get(coluna_filtro, "")).lower()
                if termo in valor_campo:
                    filtradas.append(row)

        if not filtradas:
            ctk.CTkLabel(
                self.scroll_chamados,
                text="Nenhum chamado encontrado com os filtros atuais.",
                text_color="gray65",
                font=ctk.CTkFont(size=14)
            ).pack(pady=40)
            return

        cores_status = {
            "Aberto": "#C0392B",
            "Em andamento": "#D68910",
            "Concluído": "#1E8449"
        }

        for row in reversed(filtradas):  # Mais recentes primeiro
            card = ctk.CTkFrame(self.scroll_chamados, corner_radius=10)
            card.pack(fill="x", padx=6, pady=6)
            card.grid_columnconfigure(0, weight=1)

            # Linha superior: Protocolo, Categoria, Data e Badge de Status
            topo = ctk.CTkFrame(card, fg_color="transparent")
            topo.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(12, 4))

            ctk.CTkLabel(
                topo,
                text=f"#{row['Protocolo']}  •  {row['Categoria']}  •  {row['Data']}",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left")

            cor_badge = cores_status.get(row["Status"], "gray40")
            badge = ctk.CTkLabel(
                topo,
                text=f"  {row['Status']}  ",
                fg_color=cor_badge,
                corner_radius=6,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            badge.pack(side="right")

            # Detalhes do solicitante e descrição
            info_texto = (
                f"Solicitante: {row['Pessoa']} (CPF: {row['CPF']})   |   Local: {row['Local']}\n"
                f"Descrição: {row['Descrição']}"
            )
            ctk.CTkLabel(
                card,
                text=info_texto,
                justify="left",
                anchor="w",
                text_color="gray85",
                wraplength=650
            ).grid(row=1, column=0, sticky="w", padx=15, pady=(2, 12))

            # Botões de ação rápida no cartão
            acoes = ctk.CTkFrame(card, fg_color="transparent")
            acoes.grid(row=1, column=1, sticky="e", padx=15, pady=(2, 12))

            prot = row["Protocolo"]
            ctk.CTkButton(
                acoes, text="Editar", width=75, height=30,
                command=lambda p=prot: self._atalho_editar(p)
            ).pack(side="left", padx=(0, 6))

            ctk.CTkButton(
                acoes, text="Excluir", width=75, height=30,
                fg_color="#A93226", hover_color="#922B21",
                command=lambda p=prot: self._confirmar_exclusao(p)
            ).pack(side="left")

    def _atalho_editar(self, protocolo):
        self.mostrar_tela("atualizar")
        self._selecionar_protocolo_atualizacao(protocolo)

    def _confirmar_exclusao(self, protocolo):
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir permanentemente o chamado #{protocolo}?"
        )
        if resposta:
            if deletar_registro_csv(protocolo):
                self.atualizar_interface_geral()
                messagebox.showinfo("Sucesso", f"Chamado #{protocolo} excluído com sucesso!")

    # --------------------------------------------------------------------------
    # TELA 2: CRIAR NOVO CHAMADO
    # --------------------------------------------------------------------------
    def _construir_tela_criar(self):
        self.frame_criar = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_criar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_criar, text="Registrar Novo Chamado",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(22, 15))

        form = ctk.CTkFrame(self.frame_criar)
        form.grid(row=1, column=0, sticky="ew", padx=25, pady=5)
        form.grid_columnconfigure((0, 1), weight=1)

        # Protocolo automático (somente leitura)
        ctk.CTkLabel(form, text="Protocolo (Automático):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 4))
        self.lbl_novo_protocolo = ctk.CTkLabel(form, text="#000000", font=ctk.CTkFont(size=16, weight="bold"), text_color="#5DADE2")
        self.lbl_novo_protocolo.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 12))

        # Categoria
        ctk.CTkLabel(form, text="Categoria:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=20, pady=(18, 4))
        self.combo_criar_categoria = ctk.CTkOptionMenu(form, values=list(Lista_Categorias.keys()))
        self.combo_criar_categoria.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 12))

        # Pessoa
        ctk.CTkLabel(form, text="Nome do Solicitante:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, sticky="w", padx=20, pady=(8, 4))
        self.entry_criar_pessoa = ctk.CTkEntry(form, placeholder_text="Ex: Maria Oliveira")
        self.entry_criar_pessoa.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 12))

        # CPF
        ctk.CTkLabel(form, text="CPF (11 dígitos):", font=ctk.CTkFont(weight="bold")).grid(row=2, column=1, sticky="w", padx=20, pady=(8, 4))
        self.entry_criar_cpf = ctk.CTkEntry(form, placeholder_text="Ex: 123.456.789-00")
        self.entry_criar_cpf.grid(row=3, column=1, sticky="ew", padx=20, pady=(0, 12))

        # Local / Bairro
        ctk.CTkLabel(form, text="Local / Bairro:", font=ctk.CTkFont(weight="bold")).grid(row=4, column=0, sticky="w", padx=20, pady=(8, 4))
        self.entry_criar_local = ctk.CTkEntry(form, placeholder_text="Ex: Vila Carrão")
        self.entry_criar_local.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 12))

        # Data
        ctk.CTkLabel(form, text="Data (DD/MM/AAAA):", font=ctk.CTkFont(weight="bold")).grid(row=4, column=1, sticky="w", padx=20, pady=(8, 4))
        self.entry_criar_data = ctk.CTkEntry(form, placeholder_text="DD/MM/AAAA")
        self.entry_criar_data.grid(row=5, column=1, sticky="ew", padx=20, pady=(0, 12))

        # Status Inicial
        ctk.CTkLabel(form, text="Status Inicial:", font=ctk.CTkFont(weight="bold")).grid(row=6, column=0, sticky="w", padx=20, pady=(8, 4))
        self.combo_criar_status = ctk.CTkOptionMenu(form, values=list(STATUS_VALIDOS))
        self.combo_criar_status.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 12))

        # Descrição
        ctk.CTkLabel(form, text="Descrição da Ocorrência:", font=ctk.CTkFont(weight="bold")).grid(row=6, column=1, sticky="w", padx=20, pady=(8, 4))
        self.entry_criar_desc = ctk.CTkEntry(form, placeholder_text="Descreva o problema detalhadamente...")
        self.entry_criar_desc.grid(row=7, column=1, sticky="ew", padx=20, pady=(0, 12))

        # Feedback de validação e botão de envio
        self.lbl_feedback_criar = ctk.CTkLabel(form, text="", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_feedback_criar.grid(row=8, column=0, columnspan=2, pady=(10, 5))

        ctk.CTkButton(
            form, text="Salvar Chamado", height=42, font=ctk.CTkFont(size=14, weight="bold"),
            command=self._acao_criar_chamado
        ).grid(row=9, column=0, columnspan=2, sticky="ew", padx=20, pady=(8, 22))

    def _preparar_formulario_criacao(self):
        self.lbl_novo_protocolo.configure(text=f"#{gerar_proximo_protocolo()}")
        if not self.entry_criar_data.get():
            self.entry_criar_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

    def _acao_criar_chamado(self):
        dados_brutos = {
            "Categoria": self.combo_criar_categoria.get(),
            "Pessoa": self.entry_criar_pessoa.get(),
            "CPF": self.entry_criar_cpf.get(),
            "Descrição": self.entry_criar_desc.get(),
            "Local": self.entry_criar_local.get(),
            "Data": self.entry_criar_data.get(),
            "Status": self.combo_criar_status.get(),
        }

        dados_validados = {}
        for coluna, valor in dados_brutos.items():
            valido, resultado = validar_entrada(coluna, valor)
            if not valido:
                self.lbl_feedback_criar.configure(text=f"Erro: {resultado}", text_color="#FF6B6B")
                return
            dados_validados[coluna] = resultado

        protocolo = gerar_proximo_protocolo()
        novo = criar_chamado(
            dados_validados["Categoria"],
            protocolo,
            dados_validados["Pessoa"],
            dados_validados["CPF"],
            dados_validados["Descrição"],
            dados_validados["Local"],
            dados_validados["Data"],
            dados_validados["Status"]
        )

        if novo:
            # Limpa campos após salvar
            for entry in (self.entry_criar_pessoa, self.entry_criar_cpf, self.entry_criar_local, self.entry_criar_desc):
                entry.delete(0, "end")

            self.lbl_feedback_criar.configure(
                text=f"Chamado #{protocolo} registrado com sucesso!", text_color="#06D6A0"
            )
            self.atualizar_interface_geral()
            self._preparar_formulario_criacao()

    # --------------------------------------------------------------------------
    # TELA 3: ATUALIZAR CHAMADO EXISTENTE
    # --------------------------------------------------------------------------
    def _construir_tela_atualizar(self):
        self.frame_atualizar = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_atualizar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_atualizar, text="Atualizar Chamado",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(22, 15))

        card_edit = ctk.CTkFrame(self.frame_atualizar)
        card_edit.grid(row=1, column=0, sticky="ew", padx=25, pady=5)
        card_edit.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card_edit, text="Selecione o Chamado (Protocolo):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 4))
        self.combo_edit_protocolo = ctk.CTkOptionMenu(
            card_edit, values=["Nenhum chamado"], command=self._ao_trocar_protocolo_edit
        )
        self.combo_edit_protocolo.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

        # Caixa de pré-visualização dos dados atuais do protocolo selecionado
        self.lbl_preview_edit = ctk.CTkLabel(
            card_edit, text="", justify="left", anchor="w",
            fg_color=("gray85", "gray16"), corner_radius=8, padx=15, pady=12
        )
        self.lbl_preview_edit.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))

        ctk.CTkLabel(card_edit, text="Campo que deseja alterar:", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, sticky="w", padx=20, pady=(6, 4))
        self.combo_edit_coluna = ctk.CTkOptionMenu(
            card_edit, values=COLUNAS_EDITAVEIS, command=self._ao_trocar_coluna_edit
        )
        self.combo_edit_coluna.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 12))

        ctk.CTkLabel(card_edit, text="Novo Valor:", font=ctk.CTkFont(weight="bold")).grid(row=5, column=0, sticky="w", padx=20, pady=(6, 4))

        # Container dinâmico: exibe Entry ou OptionMenu dependendo da coluna escolhida
        self.container_novo_valor = ctk.CTkFrame(card_edit, fg_color="transparent")
        self.container_novo_valor.grid(row=6, column=0, sticky="ew", padx=20, pady=(0, 12))
        self.container_novo_valor.grid_columnconfigure(0, weight=1)

        self.entry_edit_valor = ctk.CTkEntry(self.container_novo_valor, placeholder_text="Digite o novo valor...")
        self.combo_edit_valor = ctk.CTkOptionMenu(self.container_novo_valor, values=list(Lista_Categorias.keys()))

        self.lbl_feedback_edit = ctk.CTkLabel(card_edit, text="", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_feedback_edit.grid(row=7, column=0, pady=(6, 4))

        ctk.CTkButton(
            card_edit, text="Confirmar Atualização", height=42, font=ctk.CTkFont(size=14, weight="bold"),
            command=self._acao_atualizar_chamado
        ).grid(row=8, column=0, sticky="ew", padx=20, pady=(8, 22))

        self._ao_trocar_coluna_edit(self.combo_edit_coluna.get())

    def _carregar_opcoes_atualizacao(self):
        linhas = carregar_chamados()
        if not linhas:
            self.combo_edit_protocolo.configure(values=["Nenhum chamado cadastrado"])
            self.combo_edit_protocolo.set("Nenhum chamado cadastrado")
            self.lbl_preview_edit.configure(text="Cadastre um chamado primeiro.")
            return

        opcoes = [f"{r['Protocolo']} - {r['Pessoa']} ({r['Categoria']})" for r in linhas]
        self.combo_edit_protocolo.configure(values=opcoes)
        self.combo_edit_protocolo.set(opcoes[0])
        self._ao_trocar_protocolo_edit(opcoes[0])

    def _selecionar_protocolo_atualizacao(self, protocolo):
        linhas = carregar_chamados()
        for r in linhas:
            if str(r["Protocolo"]).strip() == str(protocolo).strip():
                texto_opcao = f"{r['Protocolo']} - {r['Pessoa']} ({r['Categoria']})"
                self.combo_edit_protocolo.set(texto_opcao)
                self._ao_trocar_protocolo_edit(texto_opcao)
                break

    def _ao_trocar_protocolo_edit(self, escolha):
        protocolo = escolha.split(" - ")[0].strip()
        for r in carregar_chamados():
            if str(r["Protocolo"]).strip() == protocolo:
                resumo = (
                    f"Categoria: {r['Categoria']}   |   Status: {r['Status']}   |   Data: {r['Data']}\n"
                    f"Solicitante: {r['Pessoa']}   |   CPF: {r['CPF']}   |   Local: {r['Local']}\n"
                    f"Descrição: {r['Descrição']}"
                )
                self.lbl_preview_edit.configure(text=resumo)
                return

    def _ao_trocar_coluna_edit(self, coluna):
        self.entry_edit_valor.grid_forget()
        self.combo_edit_valor.grid_forget()

        if coluna == "Categoria":
            self.combo_edit_valor.configure(values=list(Lista_Categorias.keys()))
            self.combo_edit_valor.set(list(Lista_Categorias.keys())[0])
            self.combo_edit_valor.grid(row=0, column=0, sticky="ew")
        elif coluna == "Status":
            self.combo_edit_valor.configure(values=list(STATUS_VALIDOS))
            self.combo_edit_valor.set(STATUS_VALIDOS[0])
            self.combo_edit_valor.grid(row=0, column=0, sticky="ew")
        else:
            self.entry_edit_valor.delete(0, "end")
            self.entry_edit_valor.grid(row=0, column=0, sticky="ew")

    def _acao_atualizar_chamado(self):
        selecao = self.combo_edit_protocolo.get()
        if " - " not in selecao:
            return

        protocolo = selecao.split(" - ")[0].strip()
        coluna = self.combo_edit_coluna.get()

        if coluna in ("Categoria", "Status"):
            novo_valor = self.combo_edit_valor.get()
        else:
            novo_valor = self.entry_edit_valor.get()

        sucesso, mensagem = atualizar_registro_csv(protocolo, coluna, novo_valor)
        if sucesso:
            self.lbl_feedback_edit.configure(text=mensagem, text_color="#06D6A0")
            self.entry_edit_valor.delete(0, "end")
            self.atualizar_interface_geral()
            self._selecionar_protocolo_atualizacao(protocolo)
        else:
            self.lbl_feedback_edit.configure(text=f"Erro: {mensagem}", text_color="#FF6B6B")

    # --------------------------------------------------------------------------
    # CONTROLE DE NAVEGAÇÃO E SINCRONIZAÇÃO GLOBAL
    # --------------------------------------------------------------------------
    def mostrar_tela(self, nome_tela):
        for frame in (self.frame_consulta, self.frame_criar, self.frame_atualizar):
            frame.grid_forget()

        if nome_tela == "consulta":
            self.frame_consulta.grid(row=0, column=1, sticky="nsew")
            self.renderizar_lista_chamados()
        elif nome_tela == "criar":
            self._preparar_formulario_criacao()
            self.lbl_feedback_criar.configure(text="")
            self.frame_criar.grid(row=0, column=1, sticky="nsew")
        elif nome_tela == "atualizar":
            self._carregar_opcoes_atualizacao()
            self.lbl_feedback_edit.configure(text="")
            self.frame_atualizar.grid(row=0, column=1, sticky="nsew")

    def atualizar_interface_geral(self):
        linhas = carregar_chamados()
        total = len(linhas)
        abertos = sum(1 for r in linhas if r["Status"] == "Aberto")
        andamento = sum(1 for r in linhas if r["Status"] == "Em andamento")
        concluidos = sum(1 for r in linhas if r["Status"] == "Concluído")

        self.lbl_kpi_total.configure(text=f"Total: {total}")
        self.lbl_kpi_abertos.configure(text=f"Abertos: {abertos}")
        self.lbl_kpi_andamento.configure(text=f"Em andamento: {andamento}")
        self.lbl_kpi_concluidos.configure(text=f"Concluídos: {concluidos}")

        self.renderizar_lista_chamados()


if __name__ == "__main__":
    primeira_vez()
    app = SistemaChamadosApp()
    app.mainloop()