# Arquitetura Técnica — API de Simulação de Vendas por WebSocket

Este documento descreve a infraestrutura, a arquitetura e a modelagem do sistema para a **API de Simulação de Vendas interativa em tempo real**. A solução migra a lógica do workflow do n8n para uma aplicação assíncrona robusta em Python (FastAPI).

---

## 🏗️ Visão Geral dos Componentes

O projeto adota uma arquitetura desacoplada e assíncrona dividida nas seguintes camadas lógicas:

```
┌────────────────────────────────────────────────────────┐
│                    Cliente WebSocket                   │
│          (Interface Web, Agente de Teste ou CLI)       │
└───────────────────────────┬────────────────────────────┘
                            │ (JSON via WS)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   FastAPI Application                  │
│       [main.py] Endpoint WebSocket & Rotas REST       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│              Motor de Simulação da Ligação             │
│        [workflow_simulator.py] WorkflowSimulator      │
└───────────────┬─────────────────────────┬──────────────┘
                │                         │
                │ (Query de Prompts)      │ (Chat Completions)
                ▼                         ▼
┌────────────────────────┐       ┌───────────────────────┐
│      Supabase DB       │       │      OpenAI API       │
│  [workflow_executions] │       │  Agente Cliente (Lead)│
│  [workflow_steps]      │       │  Agente SDR (Kaique)  │
└────────────────────────┘       └───────────────────────┘
```

---

## 🗄️ Modelagem de Dados e Rastreabilidade EDW

Toda simulação é auditável de ponta a ponta nas tabelas de auditoria do **Supabase** seguindo a modelagem Mestre-Detalhe (EDW):

### 1. `workflow_executions` (Mestre)
Representa a simulação geral.
- Criada com status `RUNNING` assim que a conexão WebSocket é validada.
- Finalizada com status `SUCCESS` ao atingir o limite de turnos ou ocorrer o fechamento comercial (agendamento).
- Finalizada com status `FAILED` se a conexão for abortada pelo cliente ou se ocorrer erro interno na OpenAI.

### 2. `workflow_step_executions` (Detalhe)
Grava individualmente cada interação (fala) gerada.
- **Cliente**: Registrado sob o `step_name` `"workflow_simulacao_vendas_cliente_resposta"`.
- **SDR (Kaique)**: Registrado sob o `step_name` `"workflow_simulacao_vendas_sdr_resposta"`.

---

## 🤖 Engenharia de Prompts e Perfis Comportamentais

### 1. Prompt do Agente Cliente (ID 67: `SDR_treinamento`)
Utiliza o prompt corporativo detalhado do Supabase para instanciar um lead ultra realista e resistente.
O simulador lê as regras do Prompt 67 e injeta dinamicamente no prompt de sistema as características do perfil comportamental selecionado:
- **`cetico`**: Carlos Mendes (Desconfiado, valoriza processos manuais).
- **`ocupado`**: Fernanda Rocha (Gerente atarefada, respostas curtas).
- **`preco`**: Roberto Alves (Sensível a custos, exige cálculo de ROI).
- **`fiel`**: Amanda Costa (Fiel ao concorrente, teme migração comercial).
- **`sobrecarregado_comercial`** *(Propensidade Alta)*: Juliano Santos (Perde leads e quer automação imediata).
- **`buscador_de_eficiencia`** *(Propensidade Alta)*: Beatriz Ramos (Focada em ROI de canais alternativos).
- **`frustrado_com_concorrente`** *(Propensidade Alta)*: Marcos Cunha (Frustrado com bots chatos, exige fluidez natural).

### 2. Prompt do SDR (ID 16: `mindflow form 3`)
Utiliza o prompt do SDR Kaique do Supabase, realizando o parsing e a injeção adequada de variáveis cadastrais em tempo real (`{customer_name}`, `{email}`, `{numero_do_lead}`, `{now}`).

---

## 🛡️ Protocolos de Resiliência e Conectividade

1. **Gestão de Timezones**:
   - Persistência no banco realizada estritamente em **UTC** (ISO 8601 com sufixo `Z`).
   - Lógica de contexto de data gerida internamente sob o fuso **`America/Sao_Paulo`** (Brasília).

2. **Fechamento de Conexão Gracionado**:
   - Em caso de desconexão abrupta do cliente (ex: fechamento da aba do navegador), a API intercepta o evento `WebSocketDisconnect`, cancela as chamadas pendentes e atualiza o status mestre no Supabase para `FAILED` com as devidas explicações no log, evitando processos fantasmas pendentes.

3. **Singleton pattern**:
   - Conexões pesadas com o Supabase e o OpenAI são inicializadas uma única vez por módulo em `config.py` para evitar gargalo de recursos.
