# ⚡ Intervalo Já — Cantina CESAR (versão go-horse)

Hackathon Relâmpago #1 · FDS 2026.2 · Prof. Lucas Farias · Cap. 5 (Engenharia de Software Moderna)

## O que é

Um app pra fazer os 15 minutos de intervalo renderem. O aluno pede **antes do sinal tocar** e só desce na hora certa:

- **Status da cantina:** aberta/fechada (07:30–21:30), contagem regressiva pro próximo intervalo e termômetro da fila.
- **Filtro por tempo:** "Tenho 5 / 10 / 15 min" mostra só o que dá tempo de sair.
- **Slots de retirada:** o intervalo vira 5 janelas de 3 min, com no máximo 5 pedidos cada. Slot lotado ou que não dá tempo de preparar fica bloqueado.
- **Pagamento:** Pix, Cartão Estudante, Cartão de Crédito ou Vale-Lanche.
- **Radar do pedido:** código pra mostrar no balcão e aviso "Desça da sala agora!" quando falta ≤ 3 min pro slot.

É uma PoC: sem banco, sem pagamento real. Os dados ficam em memória.

## Stack

**Python + Streamlit.** Escolhemos porque dá pra ter uma interface web rodando em minutos, todo mundo da equipe já mexe com Python e fica fácil mostrar no vídeo.

## Equipe

| Integrante | Papel |
|---|---|
| João Gabriel| Interface e CSS (telas, cartão do pedido, radar) |
| Matheus Lucena | Regras de slot e capacidade |
| Theo Monteiro | Checkout e formas de pagamento |
| Larissa Almeida | Cardápio, estoque e filtro por tempo |
| Mateus Lacerda | Status da cantina e fila |
| Julio Cesar | README e análise dos princípios |
| Caio Brayner | Vídeo e testes da demo |
| Jhorge Araújo | Apoio na revisão do código e na gravação do vídeo |

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

Na barra lateral tem **"Simular horário"** (padrão 20:12) pra demo funcionar a qualquer hora do dia.

## Onde estão os princípios (e onde ainda não estão)

Esta é a versão **go-horse**: tudo num arquivo só, de propósito. Ela serve de "antes" pra Entrega 2. O que já mapeamos:

| Princípio (cap. 5) | Situação na v1 | Onde no código |
|---|---|---|
| **Aberto/Fechado** | ❌ Violado. Cada pagamento novo exige mais um `elif` dentro do checkout. | `app.py` linhas ~397–413 |
| **Responsabilidade Única / Coesão** | ❌ O mesmo bloco calcula total, valida slot, cobra, baixa estoque, ocupa slot e notifica. | `app.py` linhas ~311–429 |
| **Inversão de Dependência** | ❌ A "notificação" é um `print` direto no meio da regra de negócio. | `app.py` linha ~425 |
| **Ocultamento de Informação** | ❌ Cardápio, slots e fila são variáveis globais / `session_state` mexidas de qualquer lugar. | `app.py` linhas ~131–155 |
| **Acoplamento** | ❌ Regra de negócio, UI e até o CSS do design no mesmo arquivo; não dá pra testar sem a interface. | arquivo todo |
| **Integridade conceitual** | ✅ Uma ideia central (render o intervalo) guia todas as telas: tempo aparece em tudo (fila, filtro, slot, aviso). | fluxo do app |

**Métrica (complexidade ciclomática):** o bloco de checkout (linhas ~391–429) tem 13 pontos de decisão → **complexidade 14**. Vamos medir de novo na Entrega 2.

## Plano pra Entrega 2 (PoC refatorada)

- `MetodoPagamento` (interface) + uma classe por pagamento → **OCP**; no vídeo, adicionar um pagamento novo sem tocar no `CheckoutService`.
- `CheckoutService` recebe um `Notificador` abstrato por injeção → **DIP**.
- Separar `Cardapio`, `AgendadorSlots`, `FilaVirtual`, `ValidadorFuncionamento` → **SRP / coesão**.
- `agendador.reservar_slot(pedido, slot)` em vez de mexer na lista de slots direto → **ocultamento / Demeter**.
- Testes unitários da regra de negócio, sem Streamlit.
