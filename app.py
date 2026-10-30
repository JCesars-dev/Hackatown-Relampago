# Intervalo Ja - versao GO-HORSE (Entrega 1)
# Tudo num arquivo so, de proposito (logica + UI + CSS misturados).
# A refatoracao com os principios do cap. 5 vem na Entrega 2.
# Rodar: streamlit run app.py

import streamlit as st
import random
import segno
from datetime import datetime, timedelta

st.set_page_config(page_title="Intervalo Já", page_icon="⚡", layout="centered", initial_sidebar_state="collapsed")


def html(s):
    # tira a indentacao pra o markdown nao achar que e bloco de codigo
    st.markdown("\n".join(l.strip() for l in s.splitlines()), unsafe_allow_html=True)


# ---------------- design system (cores da especificacao) ----------------
LARANJA = "#D9531E"
VERDE = "#10B981"
AMARELO = "#F59E0B"
VERMELHO = "#EF4444"
FUNDO = "#F8F9FA"
TEXTO = "#1E293B"
CINZA = "#64748B"
BORDA = "#E2E8F0"

html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"], .stApp, button, input {{ font-family: 'Inter', -apple-system, Roboto, sans-serif !important; }}
.stApp {{ background: {FUNDO}; color: {TEXTO}; }}
header[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {{ display: none !important; }}
.block-container {{ max-width: 460px !important; padding: 1.2rem 1rem 6rem !important; }}
h1, h2, h3, h4 {{ color: {TEXTO}; letter-spacing: -0.01em; }}
p {{ margin-bottom: 0; }}

/* cards */
.ij-card {{ background: #fff; border: 1px solid {BORDA}; border-radius: 16px; padding: 16px; box-shadow: 0 1px 2px rgba(15,23,42,.04); margin-bottom: 12px; }}
.ij-section {{ font-size: 12px; font-weight: 700; color: {CINZA}; text-transform: uppercase; letter-spacing: .06em; margin: 22px 0 8px; }}
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) {{ border-radius: 16px; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ background: #fff; border-color: {BORDA} !important; border-radius: 16px !important; }}

/* topo */
.ij-top {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }}
.ij-logo {{ display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 20px; }}
.ij-logo span.b {{ width: 36px; height: 36px; border-radius: 10px; background: {LARANJA}; color: #fff; display: grid; place-items: center; font-size: 18px; }}
.ij-user {{ display: flex; align-items: center; gap: 8px; background: #fff; border: 1px solid {BORDA}; border-radius: 999px; padding: 4px 10px 4px 4px; font-size: 12px; }}
.ij-avatar {{ width: 26px; height: 26px; border-radius: 50%; background: #FDE7DC; color: {LARANJA}; display: grid; place-items: center; font-weight: 700; }}

/* status */
.ij-badge {{ display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 999px; }}
.ij-badge.ok {{ background: #E7F8F1; color: #047857; }}
.ij-badge.off {{ background: #FDECEC; color: #B91C1C; }}
.ij-dot {{ width: 8px; height: 8px; border-radius: 50%; background: {VERDE}; animation: pulse 1.6s infinite; }}
@keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(16,185,129,.6); }} 70% {{ box-shadow: 0 0 0 7px rgba(16,185,129,0); }} 100% {{ box-shadow: 0 0 0 0 rgba(16,185,129,0); }} }}
.ij-count {{ display: flex; align-items: baseline; gap: 8px; margin: 14px 0 2px; }}
.ij-count b {{ font-size: 44px; font-weight: 800; line-height: 1; color: {LARANJA}; }}
.ij-count span {{ font-size: 16px; font-weight: 600; }}
.ij-sub {{ font-size: 13px; color: {CINZA}; }}
.ij-thermo {{ position: relative; height: 8px; border-radius: 999px; margin: 14px 0 8px;
  background: linear-gradient(90deg, {VERDE} 0 33%, {AMARELO} 33% 66%, {VERMELHO} 66% 100%); opacity: .9; }}
.ij-thermo i {{ position: absolute; top: -4px; width: 16px; height: 16px; border-radius: 50%; background: #fff; border: 3px solid {TEXTO}; transform: translateX(-50%); }}
.ij-row {{ display: flex; justify-content: space-between; font-size: 13px; }}

/* produtos */
.ij-prod {{ display: flex; gap: 12px; align-items: center; }}
.ij-thumb {{ width: 52px; height: 52px; border-radius: 12px; background: #FFF4EE; display: grid; place-items: center; font-size: 26px; flex-shrink: 0; }}
.ij-pname {{ font-weight: 600; font-size: 15px; line-height: 1.25; }}
.ij-price {{ font-weight: 700; font-size: 15px; margin-top: 2px; }}
.ij-chips {{ display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap; }}
.ij-chip {{ font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 999px; background: #F1F5F9; color: {CINZA}; }}
.ij-chip.g {{ background: #E7F8F1; color: #047857; }}
.ij-chip.y {{ background: #FEF3C7; color: #B45309; }}
.ij-chip.r {{ background: #FDECEC; color: #B91C1C; }}
.ij-off {{ opacity: .45; }}

/* botoes */
.stButton > button {{ border-radius: 12px; font-weight: 600; border: 1px solid {BORDA}; min-height: 40px; }}
.stButton > button:hover {{ border-color: {LARANJA}; color: {LARANJA}; }}
.stButton > button[kind="primary"] {{ background: {LARANJA}; border-color: {LARANJA}; color: #fff; min-height: 52px; font-size: 16px; }}
.stButton > button[kind="primary"]:hover {{ background: #BF4515; color: #fff; }}

/* segmented control / pills */
[data-testid="stButtonGroup"] button {{ border-radius: 12px !important; font-weight: 600; }}
[data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[kind*="Active"] {{ background: {LARANJA} !important; color: #fff !important; border-color: {LARANJA} !important; }}

/* radio como cards (slots e pagamento) */
.st-key-slots div[role="radiogroup"], .st-key-pag div[role="radiogroup"] {{ gap: 8px; width: 100%; }}
.st-key-slots div[role="radiogroup"] > div, .st-key-pag div[role="radiogroup"] > div {{ width: 100%; }}
.st-key-slots div[role="radiogroup"] label[data-testid="stRadioOption"], .st-key-pag div[role="radiogroup"] label[data-testid="stRadioOption"] {{
  background: #fff; border: 1.5px solid {BORDA}; border-radius: 12px; padding: 12px 14px; width: 100%; margin: 0; box-sizing: border-box; }}
.st-key-slots div[role="radiogroup"] p {{ font-variant-numeric: tabular-nums; white-space: pre; font-size: 14px; }}
.st-key-slots div[role="radiogroup"] label:is([data-selected], :has(input:checked)), .st-key-pag div[role="radiogroup"] label:is([data-selected], :has(input:checked)) {{
  border-color: {LARANJA}; background: #FFF7F3; box-shadow: 0 0 0 3px rgba(217,83,30,.12); }}

.st-key-slots [data-testid="stElementContainer"], .st-key-pag [data-testid="stElementContainer"], .st-key-slots [data-testid="stRadio"], .st-key-pag [data-testid="stRadio"], .st-key-slots [data-testid="stRadio"] > div, .st-key-pag [data-testid="stRadio"] > div {{ width: 100% !important; }}
.st-key-slots label[data-testid="stRadioOption"], .st-key-pag label[data-testid="stRadioOption"] {{ display: flex !important; }}
[data-testid="stCode"] pre, [data-testid="stCode"] code {{ white-space: pre-wrap !important; word-break: break-all; }}

/* barra do carrinho */
.ij-cartbar {{ position: fixed; left: 50%; transform: translateX(-50%); bottom: 14px; width: min(428px, calc(100% - 32px));
  background: {TEXTO}; color: #fff; border-radius: 14px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;
  font-size: 14px; font-weight: 600; z-index: 999; box-shadow: 0 8px 24px rgba(15,23,42,.25); }}
.ij-cartbar b {{ background: {LARANJA}; padding: 2px 8px; border-radius: 8px; margin-right: 8px; }}

/* stepper de quantidade: forca ficar na horizontal no celular */
[class*="st-key-step"] [data-testid="stHorizontalBlock"] {{ flex-wrap: nowrap !important; gap: 8px; }}
[class*="st-key-step"] [data-testid="stColumn"] {{ min-width: 0 !important; }}
[class*="st-key-step"] {{ background: #FFF7F3; border-radius: 12px; padding: 4px; }}
.ij-qtd {{ text-align: center; font-weight: 700; color: {LARANJA}; }}

/* radar */
.ij-step {{ display: flex; gap: 10px; align-items: flex-start; font-size: 14px; padding: 6px 0; }}
.ij-step .c {{ width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center; font-size: 12px; font-weight: 800; flex-shrink: 0; }}
.ij-step .c.done {{ background: {VERDE}; color: #fff; }}
.ij-step .c.now {{ background: {LARANJA}; color: #fff; }}
.ij-step .c.todo {{ background: #F1F5F9; color: {CINZA}; }}
.ij-alert {{ border-radius: 16px; padding: 16px; margin-bottom: 12px; }}
.ij-alert.go {{ background: {LARANJA}; color: #fff; }}
.ij-alert.wait {{ background: #EEF2FF; color: #3730A3; }}
.ij-alert h3 {{ color: inherit; margin: 0 0 4px; font-size: 22px; padding: 0; }}
.ij-qr {{ text-align: center; }}
.ij-qr svg {{ display: block; margin: 10px auto 0; }}
.ij-code {{ font-family: ui-monospace, monospace !important; font-weight: 700; font-size: 18px; letter-spacing: .08em; margin-top: 6px; }}
</style>
""")

# ---------------- "banco de dados" (variaveis globais mesmo) ----------------
CARDAPIO = [
    {"id": 1, "nome": "Coxinha de frango c/ catupiry", "emoji": "🍗", "preco": 8.50, "tempo": 2, "cat": 5, "estoque": 12},
    {"id": 2, "nome": "Pão de queijo (3 un)", "emoji": "🧀", "preco": 6.00, "tempo": 1, "cat": 5, "estoque": 20},
    {"id": 3, "nome": "Suco de laranja 300ml", "emoji": "🍊", "preco": 7.00, "tempo": 2, "cat": 5, "estoque": 3},
    {"id": 4, "nome": "Café expresso", "emoji": "☕", "preco": 4.50, "tempo": 4, "cat": 10, "estoque": 50},
    {"id": 5, "nome": "Misto quente", "emoji": "🥪", "preco": 10.00, "tempo": 7, "cat": 10, "estoque": 15},
    {"id": 6, "nome": "Tapioca de queijo coalho", "emoji": "🌮", "preco": 12.00, "tempo": 10, "cat": 15, "estoque": 10},
    {"id": 7, "nome": "Açaí 300ml", "emoji": "🍇", "preco": 15.00, "tempo": 9, "cat": 15, "estoque": 0},
]
INTERVALOS = ["09:15", "15:15", "20:30"]  # inicio dos intervalos de 15 min
ABRE, FECHA = "07:30", "21:30"
CAPACIDADE_SLOT = 5

if "carrinho" not in st.session_state:
    st.session_state.carrinho = {}
if "slots" not in st.session_state:
    st.session_state.slots = [5, 3, 1, 0, 0]  # ocupacao simulada dos 5 slots de 3 min
if "pedidos_na_fila" not in st.session_state:
    st.session_state.pedidos_na_fila = random.randint(4, 9)
if "pedido_final" not in st.session_state:
    st.session_state.pedido_final = None
if "saldo" not in st.session_state:
    st.session_state.saldo = 42.00

# ---------------- sidebar: simular horario (pra demo funcionar a qualquer hora) ----------------
st.sidebar.header("⚙️ Modo demo")
simular = st.sidebar.toggle("Simular horário", value=True)
if simular:
    hora_txt = st.sidebar.text_input("Hora atual (HH:MM)", "20:12")
    agora = datetime.strptime(datetime.now().strftime("%Y-%m-%d") + " " + hora_txt, "%Y-%m-%d %H:%M")
else:
    agora = datetime.now()
if st.sidebar.button("Resetar tudo"):
    st.session_state.clear()
    st.rerun()

# ---------------- topo ----------------
html(f"""
<div class="ij-top">
<div class="ij-logo"><span class="b">⚡</span>Intervalo Já</div>
<div class="ij-user"><div class="ij-avatar">L</div>Saldo <b>R$ {st.session_state.saldo:.2f}</b></div>
</div>
""")
unidade = st.segmented_control("Unidade", ["Brum", "Tiradentes"], default="Brum", label_visibility="collapsed") or "Brum"

# ---------------- status da cantina (tudo misturado: horario, intervalo, fila) ----------------
hoje = agora.strftime("%Y-%m-%d")
abre = datetime.strptime(hoje + " " + ABRE, "%Y-%m-%d %H:%M")
fecha = datetime.strptime(hoje + " " + FECHA, "%Y-%m-%d %H:%M")

if agora < abre or agora > fecha:
    html(f"""
    <div class="ij-card">
    <span class="ij-badge off">● Fechada</span>
    <div class="ij-count"><span>Cantina do {unidade} fechada agora</span></div>
    <div class="ij-sub">Funciona das {ABRE} às {FECHA}. Volta amanhã pra pedir antes do sinal 😉</div>
    </div>""")
    st.stop()

prox = None
for i in INTERVALOS:
    ini = datetime.strptime(hoje + " " + i, "%Y-%m-%d %H:%M")
    if ini + timedelta(minutes=15) > agora:
        prox = ini
        break

n = st.session_state.pedidos_na_fila
espera = n * 0.75  # chute: 45s por pedido
if espera < 3:
    fila_txt, fila_pos = "Tranquila", 15
elif espera <= 8:
    fila_txt, fila_pos = "Moderada", 50
else:
    fila_txt, fila_pos = "Lotada", 85

if prox is None:
    contagem = '<div class="ij-count"><span>Sem mais intervalos hoje</span></div>'
elif prox > agora:
    falta = int((prox - agora).total_seconds() // 60)
    contagem = f'<div class="ij-count"><b>{falta} min</b><span>até o sinal</span></div><div class="ij-sub">Próximo intervalo: {prox.strftime("%H:%M")} – {(prox + timedelta(minutes=15)).strftime("%H:%M")}</div>'
else:
    resta = int((prox + timedelta(minutes=15) - agora).total_seconds() // 60)
    contagem = f'<div class="ij-count"><b>{resta} min</b><span>de intervalo restantes</span></div><div class="ij-sub">Intervalo rolando agora 🔔</div>'

html(f"""
<div class="ij-card">
<div class="ij-row"><span class="ij-badge ok"><span class="ij-dot"></span>Aberta · {ABRE}–{FECHA}</span><span class="ij-sub">Cantina do {unidade}</span></div>
{contagem}
<div class="ij-thermo"><i style="left:{fila_pos}%"></i></div>
<div class="ij-row"><span>Fila <b>{fila_txt}</b></span><span class="ij-sub">~{espera:.0f} min · {n} pedidos na frente</span></div>
</div>
""")

# ---------------- pedido ja confirmado: tela de radar ----------------
if st.session_state.pedido_final:
    p = st.session_state.pedido_final
    slot_ini = datetime.strptime(hoje + " " + p["slot"][:5], "%Y-%m-%d %H:%M")
    min_ate_slot = (slot_ini - agora).total_seconds() / 60
    descer = min_ate_slot <= 3
    codigo = f"{unidade[:4].upper()}-{p['id']}-{p['slot'][:5].replace(':', '')}"
    qr_svg = segno.make(codigo).svg_inline(scale=7, dark=TEXTO, border=2)

    html(f'<div class="ij-section">Pedido #{p["id"]}</div>')
    if descer:
        html('<div class="ij-alert go"><h3>🏃 Desça da sala agora!</h3>Seu pedido fica pronto no balcão em instantes. Vai pela escada da direita pra fugir do congestionamento.</div>')
    else:
        html(f'<div class="ij-alert wait"><h3>Pode ficar na aula 😌</h3>A gente avisa quando for a hora de descer (3 min antes das {p["slot"][:5]}).</div>')

    passo3 = "now" if not descer else "done"
    html(f"""
    <div class="ij-card">
    <div class="ij-step"><div class="c done">✓</div><div><b>Pagamento aprovado</b><div class="ij-sub">{p['metodo']} · R$ {p['total']:.2f}</div></div></div>
    <div class="ij-step"><div class="c done">✓</div><div><b>Confirmado na cozinha</b><div class="ij-sub">{p['itens']}</div></div></div>
    <div class="ij-step"><div class="c {passo3}">3</div><div><b>Janela de retirada</b><div class="ij-sub">{p['slot']} · Balcão Expresso {unidade}</div></div></div>
    <div class="ij-step"><div class="c {'now' if descer else 'todo'}">4</div><div><b>Retirar no balcão</b></div></div>
    </div>
    <div class="ij-card ij-qr">
    <div class="ij-sub">Mostre no balcão expresso</div>
    {qr_svg}
    <div class="ij-code">{codigo}</div>
    </div>
    """)
    if st.button("Fazer novo pedido", use_container_width=True):
        st.session_state.pedido_final = None
        st.session_state.carrinho = {}
        st.rerun()
    st.stop()

# ---------------- cardapio com filtro por tempo ----------------
html('<div class="ij-section">Quanto tempo você tem?</div>')
filtro = st.segmented_control("Filtro", ["⚡ 5 min", "⏱️ 10 min", "🍽️ 15 min"], default="⚡ 5 min", label_visibility="collapsed") or "⚡ 5 min"
limite = int(filtro.split()[1])
legenda = {5: "Prontos na estufa e geladeira — pega e vai", 10: "Inclui preparo rápido: café e misto", 15: "Libera a chapa: tapioca, açaí e afins"}
html(f'<div class="ij-sub" style="margin:6px 0 10px">{legenda[limite]}</div>')

itens_ok = [i for i in CARDAPIO if i["cat"] <= limite]
itens_fora = [i for i in CARDAPIO if i["cat"] > limite]

for item in itens_ok + itens_fora:
    fora = item["cat"] > limite
    esgotado = item["estoque"] == 0
    qtd = st.session_state.carrinho.get(item["id"], 0)
    if esgotado:
        chip_est = '<span class="ij-chip r">Esgotado</span>'
    elif item["estoque"] <= 3:
        chip_est = f'<span class="ij-chip y">Últimas {item["estoque"]}</span>'
    else:
        chip_est = f'<span class="ij-chip g">{item["estoque"]} disponíveis</span>'
    chip_fora = f'<span class="ij-chip">Não dá em {limite} min</span>' if fora else ""
    with st.container(border=True):
        html(f"""
        <div class="ij-prod {'ij-off' if fora or esgotado else ''}">
        <div class="ij-thumb">{item['emoji']}</div>
        <div style="flex:1"><div class="ij-pname">{item['nome']}</div>
        <div class="ij-price">R$ {item['preco']:.2f}</div>
        <div class="ij-chips"><span class="ij-chip">⏱ {item['tempo']} min</span>{chip_est}{chip_fora}</div></div>
        </div>""")
        if not fora and not esgotado:
            if qtd == 0:
                if st.button("＋ Adicionar", key=f"add{item['id']}", use_container_width=True):
                    st.session_state.carrinho[item["id"]] = 1
                    st.rerun()
            else:
                with st.container(key=f"step{item['id']}"):
                    b1, b2, b3 = st.columns([1, 2, 1], vertical_alignment="center")
                    if b1.button("−", key=f"menos{item['id']}", use_container_width=True):
                        if qtd == 1:
                            del st.session_state.carrinho[item["id"]]
                        else:
                            st.session_state.carrinho[item["id"]] = qtd - 1
                        st.rerun()
                    b2.markdown(f"<div class='ij-qtd'>{qtd} no pedido</div>", unsafe_allow_html=True)
                    if b3.button("+", key=f"mais{item['id']}", use_container_width=True):
                        if qtd < item["estoque"]:
                            st.session_state.carrinho[item["id"]] = qtd + 1
                        else:
                            st.toast("Sem estoque suficiente")
                        st.rerun()

# ---------------- carrinho + slots + pagamento (tudo junto, go-horse raiz) ----------------
if not st.session_state.carrinho:
    html('<div class="ij-sub" style="text-align:center;margin-top:18px">Adicione itens pra escolher seu horário de retirada 👆</div>')
    st.stop()

total = 0
tempo_preparo = 0
qtd_total = 0
linhas = ""
nomes = []
for id_item, qtd in st.session_state.carrinho.items():
    for item in CARDAPIO:
        if item["id"] == id_item:
            linhas += f'<div class="ij-row" style="padding:4px 0"><span>{qtd}× {item["nome"]}</span><b>R$ {item["preco"] * qtd:.2f}</b></div>'
            nomes.append(f"{qtd}× {item['nome']}")
            total += item["preco"] * qtd
            qtd_total += qtd
            if item["tempo"] > tempo_preparo:
                tempo_preparo = item["tempo"]

html(f'<div class="ij-cartbar"><span><b>{qtd_total}</b>{"item" if qtd_total == 1 else "itens"} no pedido</span><span>R$ {total:.2f}</span></div>')

html('<div class="ij-section">Seu pedido</div>')
html(f"""
<div class="ij-card">{linhas}
<div style="border-top:1px dashed {BORDA};margin:8px 0"></div>
<div class="ij-row"><span class="ij-sub">Preparo estimado: {tempo_preparo} min</span><b>R$ {total:.2f}</b></div>
</div>""")

html('<div class="ij-section">Quando você quer retirar?</div>')
html(f'<div class="ij-sub" style="margin-bottom:8px">Cada janela de 3 min aceita até {CAPACIDADE_SLOT} pedidos — sem multidão no balcão.</div>')
if prox is None:
    st.error("Não há intervalo disponível hoje.")
    st.stop()
opcoes = []
bloqueados = []
for i in range(5):
    ini = prox + timedelta(minutes=3 * i)
    fim = ini + timedelta(minutes=3)
    ocupados = st.session_state.slots[i]
    livres = CAPACIDADE_SLOT - ocupados
    bolinhas = "●" * ocupados + "○" * livres
    label = f"{ini.strftime('%H:%M')} – {fim.strftime('%H:%M')}   {bolinhas}   "
    if ocupados >= CAPACIDADE_SLOT:
        label += "🔴 Lotado"
        bloqueados.append(i)
    elif agora + timedelta(minutes=tempo_preparo) > ini:
        label += "⏳ Não fica pronto a tempo"
        bloqueados.append(i)
    elif livres <= 2:
        label += f"🟡 {livres} vaga{'s' if livres > 1 else ''}"
    else:
        label += f"🟢 {livres} vagas"
    opcoes.append(label)
livres_idx = [i for i in range(5) if i not in bloqueados]
if not livres_idx:
    st.error("Todos os horários desse intervalo estão lotados 😕")
    st.stop()
css_bloq = "".join(f'.st-key-slots div[role="radiogroup"] > div:nth-child({i + 1}) label{{opacity:.45;pointer-events:none;background:#F1F5F9}}' for i in bloqueados)
html(f"<style>{css_bloq}</style>")
with st.container(key="slots"):
    escolha = st.radio("Slot", opcoes, index=livres_idx[0], label_visibility="collapsed")
idx = opcoes.index(escolha)

html('<div class="ij-section">Pagamento</div>')
with st.container(key="pag"):
    metodo = st.radio("Método", ["Pix", "Cartão Estudante CESAR", "Cartão de Crédito", "Vale-Lanche CESAR"],
                      format_func=lambda m: {"Pix": "💠  Pix — sem taxa",
                                             "Cartão Estudante CESAR": f"🎓  Cartão Estudante — saldo R$ {st.session_state.saldo:.2f}",
                                             "Cartão de Crédito": "💳  Crédito / Débito",
                                             "Vale-Lanche CESAR": "🎟️  Vale-Lanche CESAR"}[m],
                      label_visibility="collapsed")
cupom = ""
if metodo == "Vale-Lanche CESAR":
    cupom = st.text_input("Código do vale", "CESAR-VALE-123")
if metodo == "Pix":
    html('<div class="ij-sub" style="margin:8px 0 4px">Pix copia e cola</div>')
    st.code("00020126580014br.gov.bcb.pix0136cantina-brum@cesar.org", language=None)

st.write("")
if st.button(f"Confirmar e agendar · R$ {total:.2f}", type="primary", use_container_width=True):
    # valida slot
    if idx in bloqueados:
        st.error("Esse horário não está disponível, escolhe outro.")
        st.stop()
    # paga (if/elif gigante -> pra cada pagamento novo, mexe aqui)
    aprovado = False
    if metodo == "Pix":
        aprovado = True
    elif metodo == "Cartão Estudante CESAR":
        if st.session_state.saldo >= total:
            st.session_state.saldo -= total
            aprovado = True
        else:
            st.error("Saldo insuficiente na carteira estudantil.")
    elif metodo == "Cartão de Crédito":
        aprovado = random.random() > 0.1
        if not aprovado:
            st.error("Cartão recusado. Tenta outro método.")
    elif metodo == "Vale-Lanche CESAR":
        if cupom.startswith("CESAR-VALE"):
            aprovado = True
        else:
            st.error("Vale inválido.")
    if aprovado:
        # baixa estoque, ocupa slot, "notifica" (print no terminal)
        for id_item, qtd in st.session_state.carrinho.items():
            for item in CARDAPIO:
                if item["id"] == id_item:
                    item["estoque"] -= qtd
        st.session_state.slots[idx] += 1
        st.session_state.pedidos_na_fila += 1
        pid = random.randint(1000, 9999)
        slot_txt = escolha.split("   ")[0]
        print(f"[PUSH] Pedido #{pid} aprovado, descer as {slot_txt[:5]}")
        st.session_state.pedido_final = {
            "id": pid, "metodo": metodo, "total": total, "slot": slot_txt, "itens": ", ".join(nomes),
        }
        st.rerun()
