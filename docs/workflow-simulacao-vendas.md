# Workflow de Simulação de Vendas (SDR vs. Cliente)

## Descrição Geral
Este workflow do n8n automatiza uma **simulação interativa de ligação de vendas** entre dois agentes inteligentes baseados em IA (LangChain):
1. **Agente Cliente (Lead)**: Representa um lead com perfil específico (ex: "cético") que reage às investidas do vendedor.
2. **Agente SDR (Kaique)**: Simula um profissional de vendas pré-venda (Sales Development Representative) conduzindo a ligação por meio da metodologia **SPIN Selling**.

O fluxo opera em um loop contínuo de conversação de até **12 turnos** (limite configurável), permitindo o treino, simulação ou análise de abordagens de vendas. No encerramento, o sistema gera uma mensagem final indicando o fim da simulação.

---

## Flowchart

```mermaid
flowchart TD
    %% Nós Principais
    Start([Iniciar Simulação]) --> Init[Inicializar Variáveis]
    Init --> AgentClient[Agente Cliente (Lead)]
    
    %% Loop de Conversação
    AgentClient --> AgentSDR[Agente SDR (Kaique)]
    AgentSDR --> UpdateState[Atualizar Estado do Loop]
    UpdateState --> CheckLimits[Verificar Limite de Turnos]
    CheckLimits --> Router{Roteador Continuar}
    
    %% Decisão do IF
    Router -- "Sim (continuar = true)" --> AgentClient
    Router -- "Não (continuar = false)" --> EndSim[Fim da Simulação]

    %% Modelos e Memória (AI Sub-conexões)
    MemClient[(Historico Agente treino)] -.-> AgentClient
    ModelClient(OpenAI Model - Cliente) -.-> AgentClient

    MemSDR[(Histórico agente SDR)] -.-> AgentSDR
    ModelSDR(OpenAI Model - SDR) -.-> AgentSDR
```

---

## Detalhes dos Nós

### 1. Iniciar Simulação
- **Tipo**: `n8n-nodes-base.manualTrigger` (Versão 1)
- **Descrição**: Ponto de partida manual para iniciar a execução da simulação do diálogo.
- **Entradas**: Nenhuma (execução sob demanda).
- **Saídas**: `Inicializar Variáveis`.

### 2. Inicializar Variáveis
- **Tipo**: `n8n-nodes-base.set` (Versão 3.4)
- **Descrição**: Configura os dados iniciais do lead fictício, o limite de turnos e o primeiro gancho de fala da simulação.
- **Variáveis Configuradas**:
  - `turno_atual` (number): `0` (contador de turnos do diálogo).
  - `max_turnos` (number): `12` (limite máximo de iterações do loop).
  - `customer_name` (string): `"Carlos Mendes"`
  - `email` (string): `"carlos.mendes@distribuidora.com.br"`
  - `numero_do_lead` (string): `"+5548999990000"`
  - `perfil_cliente` (string): `"cetico"` (controla o tom das respostas da IA do cliente).
  - `ultima_fala_sdr` (string): `"Iniciar simulação. O SDR vai ligar agora. Atenda como o perfil selecionado."`
- **Entradas**: `Iniciar Simulação`
- **Saídas**: `Agente Cliente (Lead)`

### 3. Agente Cliente (Lead)
- **Tipo**: `@n8n/n8n-nodes-langchain.agent` (Versão 1.7)
- **Descrição**: Agente baseado em modelo de linguagem que encena o papel do cliente que atende a ligação. Suas reações são calibradas de acordo com o perfil comportamental fornecido.
- **Prompt**:
  ```text
  A última fala do SDR foi:

  {{ $json.ultima_fala_sdr }}

  Responda como o cliente do perfil "{{ $json.perfil_cliente }}" responderia a essa fala em uma ligação real. Máximo 2-3 frases.
  ```
- **Conexões de Suporte**:
  - **Modelo**: `OpenAI Model - Cliente`
  - **Memória**: `Historico Agente treino`
- **Entradas**: `Inicializar Variáveis` e `Roteador Continuar` (Retorno do loop)
- **Saídas**: `Agente SDR (Kaique)`

### 4. Agente SDR (Kaique)
- **Tipo**: `@n8n/n8n-nodes-langchain.agent` (Versão 1.7)
- **Descrição**: Agente baseado em modelo de linguagem que encena o papel do SDR Kaique. Ele analisa a resposta dada pelo cliente e formula um argumento comercial guiado pelas diretrizes de **SPIN Selling** (perguntas de Situação, Problema, Implicação e Necessidade de solução).
- **Prompt**:
  ```text
  a data atual é {{ $now }}

  <InformacoesVariaveis>
  nome do lead: {{ $('Inicializar Variáveis').item.json.customer_name }}
  email do lead: {{ $('Inicializar Variáveis').item.json.email }}
  número do lead: {{ $('Inicializar Variáveis').item.json.numero_do_lead }}
  </InformacoesVariaveis>

  A última resposta do cliente foi:

  {{ $json.output }}

  Responda como o SDR Kaique responderia a essa fala, seguindo o script e as técnicas de SPIN selling.
  ```
- **Conexões de Suporte**:
  - **Modelo**: `OpenAI Model - SDR`
  - **Memória**: `Histórico agente SDR`
- **Entradas**: `Agente Cliente (Lead)`
- **Saídas**: `Atualizar Estado do Loop`

### 5. Atualizar Estado do Loop
- **Tipo**: `n8n-nodes-base.set` (Versão 3.4)
- **Descrição**: Incrementa o contador de rodadas da conversa (`turno_atual`) e atualiza a última fala do SDR com o output gerado por Kaique para alimentar a próxima iteração.
- **Mapeamento de Variáveis**:
  - `turno_atual` (number): `{{ $('Inicializar Variáveis').item.json.turno_atual + 1 }}`
  - `max_turnos` (number): `{{ $('Inicializar Variáveis').item.json.max_turnos }}`
  - `customer_name`, `email`, `numero_do_lead`, `perfil_cliente`: preserva os dados originais do lead.
  - `ultima_fala_sdr` (string): `{{ $json.output }}` (resposta gerada pelo Agente SDR).
- **Entradas**: `Agente SDR (Kaique)`
- **Saídas**: `Verificar Limite de Turnos`

### 6. Verificar Limite de Turnos
- **Tipo**: `n8n-nodes-base.code` (Versão 2)
- **Descrição**: Bloco de código JavaScript executado no servidor do n8n para comparar o turno atual com o limite configurado e decidir se a simulação continua ativa.
- **Script**:
  ```javascript
  const turno = $input.item.json.turno_atual;
  const max = $input.item.json.max_turnos;

  if (turno < max) {
    return [{ json: { ...$input.item.json, continuar: true } }];
  } else {
    return [{ json: { ...$input.item.json, continuar: false } }];
  }
  ```
- **Entradas**: `Atualizar Estado do Loop`
- **Saídas**: `Roteador Continuar`

### 7. Roteador Continuar
- **Tipo**: `n8n-nodes-base.if` (Versão 2.2)
- **Descrição**: Bifurca o fluxo de acordo com a propriedade boolena `continuar` calculada no nó anterior.
- **Condições**:
  - `continuar` é igual a `true` (Boolean).
- **Entradas**: `Verificar Limite de Turnos`
- **Saídas**:
  - **Saída 0 (True)**: `Agente Cliente (Lead)` (Fecha o loop para nova rodada de diálogo).
  - **Saída 1 (False)**: `Fim da Simulação` (Encaminha para encerramento).

### 8. Fim da Simulação
- **Tipo**: `n8n-nodes-base.set` (Versão 3.4)
- **Descrição**: Define a mensagem de conclusão da simulação uma vez atingido o limite estipulado de turnos de diálogo.
- **Variáveis**:
  - `resultado`: `"Simulação encerrada. Limite de turnos atingido. Digite /feedback para gerar o relatório."`
- **Entradas**: `Roteador Continuar` (Saída False).
- **Saídas**: Nenhuma.

---

## Componentes de Inteligência Artificial (LangChain)

### Histórico agente SDR / Historico Agente treino
- **Tipo**: `@n8n/n8n-nodes-langchain.memoryBufferWindow` (Versão 1.3)
- **Descrição**: Provê memória de curto prazo tipo janela deslizante para os respectivos agentes. Armazena as últimas **10 interações** da conversa sob a chave `simulacao_mindflow` para garantir a consistência das respostas e evitar perda de contexto.

### OpenAI Model - Cliente / OpenAI Model - SDR
- **Tipo**: `@n8n/n8n-nodes-langchain.lmChatOpenAi` (Versão 1)
- **Descrição**: Interface de conexão com a API da OpenAI. Configurado para usar o modelo `gpt-4.1` com credenciais específicas para ambos os lados do diálogo.
