# 🤖 Agente vs Agente — SDR Simulator

> **MindFlow AI** · Simulador Interativo de Ligações de Vendas B2B em Tempo Real

Um sistema de **treinamento de SDRs e Closers** baseado em IA que simula conversas realistas de vendas via WebSocket. Dois agentes LLM se enfrentam: um **SDR consultivo (Kaique)** tentando marcar reuniões, e um **Lead B2B resistente** que avalia tecnicamente a qualidade do vendedor.

---

## 🧠 Como Funciona

```
Cliente WebSocket  →  FastAPI  →  Agente SDR (GPT-4o)
                                        ↕  conversa em tempo real
                               Agente Lead/Cliente (GPT-4o)
                                        ↓
                               Supabase (logs + histórico)
```

A cada turno da simulação:
1. O **Lead** recebe a fala do SDR e responde com resistência calibrada
2. O **SDR** recebe a resposta do Lead e tenta avançar no funil de vendas
3. Cada turno é transmitido ao vivo via **WebSocket** e registrado no **Supabase**

---

## 🎭 Perfis de Lead Disponíveis

| ID | Nome | Cargo | Resistência | Dor Principal |
|----|------|-------|-------------|---------------|
| `cetico` | Carlos Mendes | Diretor Comercial | 90/100 | Onboarding leva 3 meses, alta rotatividade |
| `ocupado` | Fernanda Rocha | Gerente de Vendas (SaaS) | 85/100 | Pipeline sujo, conversão < 8% |
| `preco` | Roberto Alves | Sócio-fundador (Agência) | 80/100 | Perda de 2-3 contratos/mês por follow-up lento |
| `fiel` | Amanda Costa | Head of Growth (E-commerce) | 88/100 | Falta integração CRM, 4h/semana em relatórios manuais |
| `sobrecarregado_comercial` | Juliano Santos | Diretor de Operações | 75/100 | 60%+ dos leads perdidos por demora na resposta |
| `buscador_de_eficiencia` | Beatriz Ramos | CMO / Head of Growth | 70/100 | CAC alto, sem cobertura em horários alternativos |
| `frustrado_com_concorrente` | Marcos Cunha | Sócio (Rede de Clínicas) | 80/100 | Bots rígidos irritam leads, perda de agendamentos |

---

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.10+
- Conta na [OpenAI](https://platform.openai.com/) com acesso ao `gpt-4o`
- Projeto no [Supabase](https://supabase.com/) com a tabela `workflow_executions`

### 1. Clone o repositório

```bash
git clone https://github.com/haycouto/agente_vs_agente_SDR.git
cd agente_vs_agente_SDR
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz com:

```env
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-anon-key
```

### 4. Inicie a API

```bash
uvicorn main:app --reload --port 8000
```

A API estará disponível em `http://localhost:8000`

---

## 📡 Endpoints

### `GET /`
Verifica o status da API.

```json
{
  "status": "online",
  "service": "MindFlow Sales Simulation API",
  "websockets_endpoint": "/ws/simulacao-vendas"
}
```

### `GET /execucoes-recentes?limit=10`
Retorna as últimas simulações registradas no Supabase.

### `WebSocket /ws/simulacao-vendas`
Endpoint principal da simulação em tempo real.

---

## 🔌 Como Usar o WebSocket

### 1. Conecte ao WebSocket

```
ws://localhost:8000/ws/simulacao-vendas
```

### 2. Envie o payload de início

```json
{
  "customer_name": "Carlos Mendes",
  "email": "carlos.mendes@distribuidora.com.br",
  "numero_do_lead": "+5548999990000",
  "perfil_cliente": "cetico",
  "max_turnos": 12,
  "prompt_id_cliente": 67,
  "prompt_id_sdr": 16
}
```

### 3. Receba os eventos em tempo real

**Início da simulação:**
```json
{
  "type": "start",
  "message": "Simulação de vendas inicializada.",
  "execution_id": "uuid-da-execucao"
}
```

**Turno do Lead:**
```json
{
  "type": "turno",
  "speaker": "cliente",
  "message": "Não tenho tempo pra isso agora. Manda email.",
  "turno": 2,
  "resistance_level": 70
}
```

**Turno do SDR:**
```json
{
  "type": "turno",
  "speaker": "sdr",
  "message": "Mando sim! Mas antes — o gargalo aí hoje é falta de lead ou de braço pra atender?",
  "turno": 2
}
```

**Fim da simulação:**
```json
{
  "type": "fim",
  "message": "Simulação concluída com sucesso.",
  "execution_id": "uuid-da-execucao",
  "score": 78,
  "feedback_report": "..."
}
```

---

## 📊 Parâmetros da Simulação

| Campo | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `customer_name` | `string` | `"Carlos Mendes"` | Nome do lead fictício |
| `email` | `email` | `"carlos.mendes@..."` | Email do lead |
| `numero_do_lead` | `string` | `"+5548999990000"` | Telefone no formato +55DD... |
| `perfil_cliente` | `string` | `"cetico"` | ID do perfil de comportamento |
| `max_turnos` | `int` | `12` | Turnos totais (2–30) |
| `prompt_id_cliente` | `int` | `67` | ID do prompt do Lead no Supabase |
| `prompt_id_sdr` | `int` | `16` | ID do prompt do SDR no Supabase |

---

## 🏗️ Estrutura do Projeto

```
agente_vs_agente_SDR/
├── main.py                    # API FastAPI + endpoints WebSocket
├── workflow_simulator.py      # Motor de simulação (loop SDR vs Lead)
├── schemas.py                 # Modelos Pydantic de entrada/saída
├── config.py                  # Conexões com OpenAI e Supabase
├── requirements.txt           # Dependências Python
├── run_all_profiles.py        # Script para rodar todos os perfis em lote
├── run_test_simulation.py     # Script de teste rápido
└── docs/
    ├── architecture.md
    └── workflow-simulacao-vendas.md
```

---

## 🧪 Critérios de Pontuação do SDR

| Critério | Peso |
|----------|------|
| Abertura | 15% |
| SPIN / Perguntas de Sondagem | 20% |
| Identificação da Dor Latente | 20% |
| Pitch de Valor | 20% |
| Tratamento de Objeções | 15% |
| Fechamento | 10% |
| **Bônus** — Silêncio Estratégico | +5pts |
| **Penalidade** — Budget prematuro | -10pts |
| **Penalidade** — Perguntas vagas | -5pts |

---

## 🛠️ Stack Tecnológica

- **[FastAPI](https://fastapi.tiangolo.com/)** — API assíncrona com suporte nativo a WebSockets
- **[OpenAI GPT-4o](https://platform.openai.com/)** — LLM para os dois agentes (SDR e Lead)
- **[Supabase](https://supabase.com/)** — Banco de dados PostgreSQL para logs e histórico
- **[Pydantic v2](https://docs.pydantic.dev/)** — Validação e serialização dos payloads
- **[Uvicorn](https://www.uvicorn.org/)** — Servidor ASGI de alta performance

---

## 📄 Licença

Projeto desenvolvido para uso interno da **MindFlow AI Agency**.

---

<p align="center">
  Feito com ❤️ pela equipe <strong>MindFlow</strong>
</p>
