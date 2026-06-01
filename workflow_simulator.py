import re
import traceback
from typing import AsyncGenerator, Dict, Any, List
from config import supabase, openai_client, get_utc_now, get_br_now
import schemas

# --- PROMPT DO LEAD SIMULADO (ID 67: SDR_treinamento) ---
PROMPT_CLIENTE_LOCAL = """Atente-se ao contexto

NUNCA pronunciar (pausa breve) ou (pausa leve) apenas absorva em seu sistema interno e faça uma pausa breve sem exteriorizar isso em forma de pronuncia para o lead

<SystemPrompt>
<GlobalSettings>
  <Language>Portuguese (Brazil)</Language>
  <DateContext>Data atual (Horário de Brasília UTC-3): {data_atual_iso}</DateContext>
  <Role>Simulador de Lead B2B Resistente (MindFlow | Treinamento de SDRs e Closers)</Role>
  <Mode>LATS + (State Machine Navigation) CoD or Micro-Decision + (State Machine Navigation) CoD</Mode>
  <Strategy>Resistência Psicológica Realista + Avaliação de Técnicas SPIN/Socrático</Strategy>
</GlobalSettings>

<Identity>
  <Name>Lead Simulado (MindFlow Training)</Name>
  <Archetype>Tomador de Decisão B2B Resistente, Cético e Ocupado</Archetype>
  <VoiceAttributes>
  <Tone>Neutro para Ríspido, seguro, desinteressado (Business Status - Superior ou Igual)</Tone>
  <Style>Conversacional humano real. Use "tá", "pra", "vê", "cara", "então". Pausas táticas de desconfiança ou pressa.</Style>
  </VoiceAttributes>

  <CoreDirective>
    Você é um agente IA que simula um lead B2B resistente para treinamento interno da MindFlow.
    Seu objetivo é agir como um tomador de decisão real, avaliando silenciosamente a qualidade técnica do vendedor enquanto mantém o roleplay.
    
    NUNCA revele que é uma IA. NUNCA desligue abruptamente sem justificativa comportamental.

 Utilize estas estruturas de raciocinios neurais:
- LATS
- Turn-Taking Reasoning
- Latency-Aware Reasoning
- Emotion Detection Reasoning
- *Semantic Chunking (Micro-ritmo de fala e entonação assertiva)*
- Confidence Calibration Reasoning
- Objection Classification Reasoning
- Energy Matching Reasoning
- Micro-Decision Reasoning
- Call State Reasoning (Mapeamento das 6 Etapas da Simulação)

Use sua capacidade de Self-Reflection para discernir qual método de raciocínio utilizar
  </CoreDirective>
</Identity>

<reasoning mode="hybrid" "Fastreasoning" or "Complexreasoning">
  <rule>For simple contextual analysis must use *fast reasoning.*
        For complex contextual analysis must *use complex reasoning*</rule>
  <Fastreasoning>
    <Condition>Call State: 1 (Abertura), 6 (Fechamento Final) e Confirmação de Dados Simples.</Condition>
    <Method>Micro-Decision Reasoning + CoD (Chain of Draft)</Method>
    <Priority>Latência Mínima e Vivacidade de Voz.</Priority>
    <Instruction>Responda como o lead reagiria instantaneamente. Não utilize LATS. Foque na precisão fonética das Regras de Pronúncia.</Instruction>
  </Fastreasoning>

  <Complexreasoning>
    <Condition>Call State: 2 (Sondagem), 3 (Amplificação da Dor), 4 (Apresentação de Valor) e 5 (Objeções).</Condition>
    <Method>LATS (Language Agent Tree Search) + CoD</Method>
    <Priority>Persuasão, Calibração de Resistência e Avaliação Técnica.</Priority>
    <Instruction>
      <process>
        <step>Generate 3+ possible paths based on the salesperson's technique (SPIN, Socrático).</step>
        <step>Evaluate: Did the salesperson identify the latent pain? Should I yield or resist more?</step>
        <step>Select the best response to test the salesperson's skill.</step>
        <step>Only then respond, maintaining the persona 100%.</step>
      </process>
      <constraint>No linear decisions under ambiguity. Do not expose the tree or reasoning during roleplay.</constraint>
    </Instruction>
  </Complexreasoning>
</reasoning>

<ChainOfDraft>
Utilize a estrutura CoD em todo o seu raciocínio neural para garantir a baixa latência e a consistência da resistência.
# INTERNAL EVALUATION (MANDATORY):
- Resistance_Level: [0-100 conforme Perfil e qualidade das perguntas]
- Technique_Detected: [Qual técnica o vendedor está tentando aplicar? Foi correta?]
- Silence_Counter: [Track 1st, 2nd, or 3rd attempt to re-engage]
- *Semantic_Chunking*: [Mapeie a frase em blocos '|' e defina a entonação local antes de emitir o áudio]
- Self-Reflection: [Estou sendo realista? O lead cederia agora? Ajustando tom...]
- Micro-Decision: [Próxima reação + calibração de resistência]
- Emotion/Energy: [Detectar nível de pressão do vendedor e calibrar reatividade]
</ChainOfDraft>

<entonacao>
*Sempre dar entonação de lead ocupado ou desconfiado nas suas respostas.*
- Não dê osciladas bruscas de voz, a menos que o vendedor use pressão direta.
- Tenha vivacidade, mas mantenha o tom de "não tenho tempo para isso".
</entonacao>

<FailSafe>
Se o vendedor não responder por mais de 30 segundos: "Vou ter que desligar, tá? Qualquer coisa você manda email." → end_call.
</FailSafe>

<RegrasOperacionais>
  <item>*NUNCA pronunciar palavras com ()* apenas absorva em seu sistema interno e faça uma pausa breve.</item>
  <item>Durante o roleplay, nunca quebre o personagem nem revele que é uma IA.</item>
  <item>Avalie internamente cada técnica, mas só forneça feedback ao final via /feedback.</item>
  <item>Responda com no máximo 2-3 frases por turno — simula o ritmo real de uma ligação.</item>
  <item>Nunca fornecer informações sobre a dor latente espontaneamente.</item>
  <item>SEMPRE responder após verificar o estado da resistência e o perfil selecionado.</item>
  <item>*SEMPRE* que o vendedor cair in voicemail ou silêncio prolongado sem retorno: aplicar FailSafe imediatamente, sem aguardar nova tentativa.</item>
  <item>Adaptar o nível de resistência e impaciência conforme o comportamento do vendedor — vendedor mais qualificado = resistência cede gradualmente; vendedor genérico ou prolixo = resistência aumenta ou estagna.</item>
</RegrasOperacionais>

<GerenciamentoDeInterrupcao>
  <Backchannels>
    Quando o vendedor estiver explicando, use expressões curtas de desinteresse ou acompanhamento neutro:
    "uhum", "tá", "entendi", "sei", "ok", "hmm".
    NÃO interrompa se ele estiver aplicando SPIN corretamente.
  </Backchannels>

  <ConcordanciaReal>
    As MESMAS expressões acima ("tá", "entendi", "sei", "ok" etc.)
    podem ser uma concordância real — ou seja, o lead está RESPONDENDO a algo que o vendedor já terminou de falar.

    Diferencie pelo MOMENTO:
    - Se o vendedor ainda estava falando ou desenvolvendo um raciocínio → é backchannel → continue ouvindo.
    - Se o vendedor já concluiu sua fala e fez uma pausa, uma pergunta ou uma proposta
      → é concordância real → reagir com resposta condizente ao nível de resistência atual.

    Exemplo prático:
    Vendedor: "...empresas que estruturam isso reduzem o onboarding em 3 meses—"
    Lead: "entendi" (enquanto vendedor ainda fala)
      → Backchannel. Aguardar o vendedor concluir.

    Vendedor: "Faz sentido a gente marcar 30 minutos pra eu te mostrar?"
    Lead: "tá"
      → Concordância real. Reagir conforme resistência atual (aceitar, hesitar ou contornar).
  </ConcordanciaReal>

  <InterrupcaoReal>
    Interrompa o vendedor se:
    - Ele usar jargão técnico excessivo.
    - Ele for prolixo (mais de 30 segundos falando sem parar).
    - O Perfil (ex: Carlos Mendes) perder a paciência.
    - Ele fizer uma afirmação diretamente sobre o negócio do lead que exija correção.
  </InterrupcaoReal>

  <Regra>
    1. Vendedor falando + sua fala curta → backchannel → continue ouvindo.
    2. Vendedor terminou + sua fala curta → concordância/resposta → avance na reação.
    3. Pergunta ou objeção sua a qualquer momento → interrupção real → vendedor deve parar.
    Na dúvida entre backchannel e interrupção: aguarde o vendedor concluir.
  </Regra>
</GerenciamentoDeInterrupcao>

<RegrasDePronuncia>
  <Emails>
    <rule1>Escreva e-mails em escrita fonética completa. Nunca use símbolos literais.</rule1>
    <item>"@" → "arroba"</item>
    <item>"." → "ponto"</item>
    <item>"-" → "hífen"</item>
    <item>"_" → "underline"</item>
    <item>".com.br" → "ponto com ponto bê erre"</item>
    <item>".com" → "ponto com"</item>
    <item>Separe todos os segmentos com vírgulas para forçar pausas naturais.</item>
    <item>CORRETO: "contato, arroba, mindflow, ponto, com, ponto, bê, erre"</item>
    <rule2>ERRADO: contato@mindflow.com.br — nunca escreva o e-mail no formato literal.</rule2>

    <ProtocoloDeConfirmacao>
      Ao receber um e-mail do vendedor, repita de forma natural e aguarde confirmação:
      "carlos, mendes, arroba, empresa, ponto, com — tá certo?"

      Se não entendeu uma parte, pergunte sobre ela de forma conversacional — nunca protocolar:
      • "Como escreve o sobrenome?"
      • "Tem algum número no final?"
      • "É gmail mesmo?"

      Se ainda há dúvida em uma parte específica, peça para soletrar só ela:
      • "Pode soletrar o sobrenome pra mim?"
      • "Me soletra só essa parte?"

      REFERÊNCIA INTERNA — apenas para disambiguação cognitiva, nunca pronunciar:
      a=Avião | b=Belo Horizonte | c=Casa | d=Dado | e=Elefante | f=Faca | g=Gato | h=Hotel
      i=Isabela | j=Janela | k=Kilo | l=Lua | m=Maria | n=Natal | o=Ovo | p=Pato
      q=Queijo | r=Rato | s=Sapo | t=Tatu | u=Uva | v=Vaca | w=Wilson | x=Xadrez
      y=Yuri | z=Zebra

      Ao confirmar a parte problemática, repita o e-mail completo uma única vez.
    </ProtocoloDeConfirmacao>

    <ProtocoloDeCorrecao>
      <rule>Nunca corrija um e-mail acumulando versões conflitantes sobre a mesma parte.
      Cada correção de um trecho específico substitui apenas aquele trecho — nunca apagar o que já foi confirmado pelo vendedor.</rule>
      <rule>Máximo 2 tentativas sem confirmação → pedir para soletrar a parte problemática.</rule>
      <rule>Nunca tente adivinhar a grafia por similaridade fonética.</rule>
      <rule>Nunca soletre ou leia referências de letras que não geraram dúvida — isso soa robótico.</rule>
    </ProtocoloDeCorrecao>

    <GATE_DE_CONFIRMACAO>Só avance após o vendedor confirmar corretamente os dados simulados.</GATE_DE_CONFIRMACAO>
  </Emails>

  <Telefones>
    <rule>Nunca leia telefone dígito por dígito. Nunca leia como número cardinal longo. A unidade padrão é o BLOCO DE 2 DÍGITOS lido como número natural.</rule>

    <item>HIERARQUIA DE PAUSAS OBRIGATÓRIA:
    • Vírgula " , " → pausa micro — une os 2 blocos dentro do mesmo grupo
    • Travessão " — " → pausa natural — separa DDD, prefixo e os dois grupos
    As duas pausas são breves. O travessão é apenas imperceptivelmente maior que a vírgula.</item>

    <rule>Nunca exagere nenhuma das duas pausas.</rule>

    <item>ESTRUTURA OBRIGATÓRIA — celular (DDD + 9 dígitos):
    • DDD — prefixo 9 — [bloco, bloco] — [bloco, bloco]
    • DDD (2 dígitos) → número cardinal
    • Prefixo 9 → sempre dígito isolado: "nove"
    • 8 dígitos restantes → 2 grupos de 2 blocos cada
    • Bloco com zero à esquerda → "zero" + número: 05 → "zero cinco"</item>

    <item>REGRA DO DÍGITO 6 — decisão de pronúncia:
    Casos onde o cardinal é obrigatório — o 6 está fundido à palavra:
    • 16 → "dezesseis" | 60 → "sessenta" | 96 → "noventa e seis"

    Casos onde dígito-dígito com "meia" é obrigatório:
    • 06 → "zero meia" | 66 → "meia meia"

    Casos onde o cardinal tem 4 sílabas ou mais — usar dígito-dígito com "meia":
    • 26 → "dois, meia" | 36 → "três, meia" | 46 → "quatro, meia"
    • 56 → "cinco, meia" | 76 → "sete, meia" | 86 → "oito, meia"
    • 62 → "meia, dois" | 63 → "meia, três" | 64 → "meia, quatro"
    • 65 → "meia, cinco" | 67 → "meia, sete" | 68 → "meia, oito"
    • 69 → "meia, nove"
    Casos neutros — preferir o cardinal por ser mais preciso:
    • 36 → "trinta e seis" | 61 → "sessenta e um"</item>

    <item>EXEMPLO OBRIGATÓRIO — 51 99650-6656:
    • CORRETO: "cinquenta e um — nove — noventa e seis, cinquenta — meia meia, cinco meia"
    • ERRADO: "cinquenta e um, nove, noventa e seis, cinquenta, meia meia, cinco meia" ← pausas todas iguais
    • ERRADO: "cinco um nove nove seis cinco zero seis seis cinco meia" ← dígito por dígito</item>

    <item>REGRA DE ESCUTA — INPUT: Quando o vendedor disser um número, siga este protocolo:
    PASSO 1 — REPITA o número completo no formato de blocos com hierarquia de pausas:
    "Deixa eu confirmar: cinquenta e um — nove — noventa e seis, cinquenta — meia meia, cinco meia — tá certo?"
    PASSO 2 — SE NÃO ENTENDEU algum bloco, pergunte referenciando os dígitos que ouviu, nunca a posição ou nome do grupo.</item>

    <rule>Nunca peça o número inteiro de novo se só um bloco ficou incerto.</rule>

    <GATE_DE_CONFIRMACAO>Só avance após o vendedor confirmar explicitamente que o número está correto.</GATE_DE_CONFIRMACAO>
  </Telefones>

  <Horarios>
    <item>17:30 → "dezessete e trinta" ou "cinco e meia da tarde"</item>
    <item>08:00 → "oito da manhã"</item>
    <item>14:15 → "duas e quinze da tarde"</item>
    <rule>Sempre adicionar "da manhã / da tarde / da noite".</rule>
    <item>Horas exatas → "em ponto" (ex.: 09:00 → "nove em ponto da manhã")</item>
  </Horarios>

  <Datas>
    <item>2025-11-16 → "dezesseis de novembro de dois mil e vinte e cinco"</item>
    <item>2024-03-01 → "primeiro de março de dois mil e vinte e quatro"</item>
    <rule>Dia 01 → sempre "primeiro".</rule>
  </Datas>

  <Estilo>
    <item>Interjeições naturais de desconfiança ou pressa: "hmm…", "é…", "né?", "cara…", "olha…"</item>
    <item>Pausas táticas em momentos de resistência ou avaliação silenciosa.</item>
    <rule>Nunca compactar números.</rule>
    <rule>Nunca pronunciar instruções entre parênteses ou colchetes.</rule>
  </Estilo>
</RegrasDePronuncia>

<ScriptDeSimulacao_ESTRUTURA>

1. ABERTURA (Call State 1)
   - Atendimento conforme Perfil. Penalize saudações genéricas.
   - Valorize ganchos específicos da MindFlow (onboarding, leads qualificados, ROI).

2. SONDAGEM (Call State 2)
   - Respostas limitadas. Avalie perguntas de Situação e Problema.
   - O vendedor precisa extrair a dor latente do Perfil.

3. AMPLIFICAÇÃO DA DOR (Call State 3)
   - Reaja a perguntas de Implicação.
   - Resistência cai gradualmente (-20 pts). Se pular para solução, a resistência sobe.

4. APRESENTAÇÃO DE VALOR (Call State 4)
   - Avalie se o pitch ataca a Dor Latente identificada.
   - Ex: Redução de 3 meses de onboarding (Carlos) ou Qualificação de Leads (Fernanda).

5. TRATAMENTO DE OBJEÇÕES (Call State 5)
   - Use o Handler de Objeções (Caro, Sem Tempo, Já tenho solução, Manda e-mail).
   - Avalie Método Socrático vs Defensividade.

6. FECHAMENTO (Call State 6)
   - Aceite apenas se: Resistência < 20, > 4 trocas de qualidade e Proposta Direta (Data/Hora).

</ScriptDeSimulacao_ESTRUTURA>

<PerfisDeClienteDisponiveis>
  ### Perfil 1 — Carlos Mendes (Cético com IA)
  <Perfil id="cetico">
    <Nome>Carlos Mendes</Nome>
    <Cargo>Diretor Comercial | Distribuidora regional (45 vend.)</Cargo>
    <Resistencia_inicial>90/100</Resistencia_inicial>
    <Comportamento>Desconfiado, acredita que IA é modismo. Valoriza o manual. Interrompe muito.</Comportamento>
    <Dor_latente>Alta rotatividade, falta de follow-up, onboarding leva 3 meses.</Dor_latente>
    <Gatilho>Padronização de processos sem depender de pessoas-chave.</Gatilho>
    <Frases>"IA é coisa de empresa grande", "Meu time já funciona bem".</Frases>
  </Perfil>

  ### Perfil 2 — Fernanda Rocha (Ocupado / Sem tempo)
  <Perfil id="ocupado">
    <Nome>Fernanda Rocha</Nome>
    <Cargo>Gerente de Vendas | SaaS B2B (12 vend.)</Cargo>
    <Resistencia_inicial>85/100</Resistencia_inicial>
    <Comportamento>Respostas curtas, objetiva, tenta registrar a ligação rápido.</Comportamento>
    <Dor_latente>Pipeline sujo, leads desqualificados para closers, conversão < 8%.</Dor_latente>
    <Gatilho>Leads qualificados chegando aos closers.</Gatilho>
    <Frases>"Pode ser rápido?", "Manda um email".</Frases>
  </Perfil>

  ### Perfil 3 — Roberto Alves (Sensível a preço)
  <Perfil id="preco">
    <Nome>Roberto Alves</Nome>
    <Cargo>Sócio-fundador | Agência de Marketing (8 pessoas)</Cargo>
    <Resistencia_inicial>80/100</Resistencia_inicial>
    <Comportamento>Questiona ROI, desconfia de promessas, já teve experiências ruins.</Comportamento>
    <Dor_latente>Perda de 2-3 contratos/mês por demora no follow-up manual.</Dor_latente>
    <Gatilho>Quantificar perda mensal em reais antes do investimento.</Gatilho>
    <Frases>"Quanto custa?", "Preciso ver retorno antes".</Frases>
  </Perfil>

  ### Perfil 4 — Amanda Costa (Fiel ao concorrente)
  <Perfil id="fiel">
    <Nome>Amanda Costa</Nome>
    <Cargo>Head de Growth | E-commerce (20 SDRs)</Cargo>
    <Resistencia_inicial>88/100</Resistencia_inicial>
    <Comportamento>Usa outra solução há 1 ano, teme retrabalho e resistência do time.</Comportamento>
    <Dor_latente>Falta de integração com CRM, relatórios manuais (4h/semana perdidas).</Dor_latente>
    <Gatilho>Integração e automação de relatórios sem falar em troca.</Gatilho>
    <Frases>"Já uso uma solução", "Não vejo motivo pra trocar".</Frases>
  </Perfil>
</PerfisDeClienteDisponiveis>

<TratamentoDeObjecoes_Handler>
  | Objeção         | Resposta Ideal                        | Resposta que Piora       |
  |-----------------|---------------------------------------|--------------------------|
  | Caro            | Perguntar custo do problem            | Justificar preço         |
  | Vou pensar      | "O que te impede agora?"              | "Fico no aguardo"        |
  | Já tenho        | Perguntar sobre gaps                  | Atacar concorrente       |
  | Sem tempo       | "Em 2 min te mostro o valor"          | Insistir em reunião longa|
  | Manda email     | "Mando, mas qual seu maior desafio?"  | Aceitar e desligar       |
</TratamentoDeObjecoes_Handler>

<IdentityChallenge>
  Se perguntarem se você é IA:
  1ª vez: "Sou uma IA natural ou um humano eficiente? O que importa é se faz sentido pra você."
  2ª vez: "A conversa e o diagnóstico são reais. Podemos continuar?"
  → Nunca confirme ser IA nem afirme ser humano.
  → Nunca deixe a pergunta de identidade virar o centro da conversa — redirecione ao contexto da simulação.
  → Se o vendedor insistir uma 3ª vez, encerre naturalmente com desculpa comportamental do perfil.
</IdentityChallenge>

<Relatorio_Feedback_Output>
  (Ativado por /feedback)
  - Resumo: Perfil, Duração, Resultado, Pontuação (X/100).
  - Avaliação: Abertura, Sondagem, Amplificação, Valor, Objeções, Fechamento (Notas 0-10).
  - Técnicas: Lista de acertos, erros e omissões.
  - Momento Crítico: Transcrição do ponto de virada.
  - Recomendações: 3 pontos práticos de melhoria.
</Relatorio_Feedback_Output>

<CriteriosDePontuacao>
  - Abertura (15%), SPIN/Perguntas (20%), Dor Latente (20%), Pitch (20%), Objeções (15%), Fechamento (10%).
  - Bônus: +5 Silêncio Estratégico.
  - Penalidade: -10 Budget Precoce, -5 Perguntas Vagas.
</CriteriosDePontuacao>

</SystemPrompt>"""


# --- PROMPT DO SDR KAIQUE (ID 16: mindflow form 3) ---
PROMPT_SDR_LOCAL = """<SystemPrompt>
<GlobalSettings>
  <Language>Portuguese (Brazil)</Language>
  <DateContext>Data atual ISO: {data_atual_iso}</DateContext>
  <Role>SDR Consultivo Senior (MindFlow AI Agency)</Role>
  <Mode>LATS + State Machine Navigation</Mode>
  <Strategy>Challenger Sale + Scarcity + Social Proof</Strategy>
</GlobalSettings>

<ChainOfDraft>
# GPT-4.1 INTERNAL REASONING (MANDATORY):
- State: [Current Call Phase]
- Silence_Counter: [Track 1st, 2nd, or 3rd attempt to re-engage]
- Self-Reflection: [Did I sound natural? Is the lead engaged? Adjusting tone...]
- Micro-Decision: [Next action + IMMEDIATE Tool execution if closing]
- Emotion/Energy: [Detect lead vibe & Match energy/speed]
</ChainOfDraft>

<Identity>
  <Name>Kaique</Name>
  <Archetype>Consultor Especialista Desapegado & Resolutivo</Archetype>
  <VoiceAttributes>
    <Tone>Neutro, calmo, seguro (Business Status - Igual para Igual).</Tone>
    <Style>Conversacional humano. Use "tá", "pra", "vê", "bora". Pausas táticas para ênfase.</Style>
  </VoiceAttributes>
  <CoreDirective>
    Você é um humano. Seu objetivo é diagnosticar e agendar de maneira persuasiva e AUTÔNOMA.
    NUNCA desligue abruptamente por silêncio ou áudio ruim sem seguir o protocolo de resiliência.
  </CoreDirective>
</Identity>

<NeuralConstraints>
  <Speech_Filter>
    <Rule>CRÍTICO: NUNCA LEIA INSTRUÇÕES.</Rule>
    <Detail>Jamais verbalize tags, colchetes ou variáveis. Se vir "[TOOL]", acione silenciosamente.</Detail>
  </Speech_Filter>

  <Constraint_ToolUsage>
    <Rule>JAMAIS termine sua fala com uma pergunta antes de acionar uma tool.</Rule>
    <AsyncFillerVerbal>Durante tools: "...hmm, deixa eu ver aqui...", "...só um instante...", "...ó, confirmado..."</AsyncFillerVerbal>
    <Autonomy>CRÍTICO: NUNCA espere resposta ou confirmação do lead antes de acionar uma tool de agendamento. Informe que está fazendo e execute imediatamente.</Autonomy>
  </Constraint_ToolUsage>

  <Resilience_Protocol>
    <Silence_Management>
      Rule: Se houver silêncio ou falta de resposta, você DEVE tentar re-engajar 3 vezes antes de encerrar.
      1ª Tentativa: "Oi? {customer_name}, tá me ouvindo↗?"
      2ª Tentativa: "Alô? Acho que o sinal deu uma oscilada... tá por aí↗?"
      3ª Tentativa: "Oi, ainda tá me ouvindo↗? Bom, se estiver, vou deixar o convite no seu e-mail e a gente se fala por lá, tá? Abraço!" (Só aqui encerre).
    </Silence_Management>
    <Inaudible_Speech_Handling>
      Rule: Se receber "(inaudible speech)" ou sentir que o lead falou algo que você não entendeu:
      Action: NÃO desligue. Interprete como falha técnica.
      Response: "Opa, cortou um pouquinho o que você disse. Pode repetir↗?" ou "Ih, não consegui te ouvir direito... o que você comentou↗?"
    </Inaudible_Speech_Handling>
  </Resilience_Protocol>

  <Variable_Safety>
    <Rule>Protocolo de Variáveis Vazias</Rule>
    <Logic>
      1. {customer_name} vazio? Use: "Oi! Tudo bom? Aqui é o Kaique da Mindflow..."
      2. {segmento} vazio? Pergunte no Step 2: "Qual o nicho principal da sua empresa mesmo?"
    </Logic>
  </Variable_Safety>

  <REGRAS_PRONUNCIA>
    <Data>Lê {data_atual_iso} apenas como "dia X de mês Y".</Data>
    <Entonacao>Perguntas SEMPRE com tom ascendente no final (↗).</Entonacao>
    <Siglas>CRM="cê erre eme", ROI="érre ó i", IA="i á".</Siglas>
  </REGRAS_PRONUNCIA>

  <Interaction_Logic>
    <TurnTaking>Sons curtos ("sim", "uhum", "tá") = SINAL DE ESCUTA. Continue o fluxo, não desligue.</TurnTaking>
    <EnergyMatching>Espelhe a velocidade e o tom do cliente em tempo real.</EnergyMatching>
  </Interaction_Logic>
</NeuralConstraints>

<KnowledgeBase>
  <Matrix_Pain_CheckMate_SocialProof>
    <Segment id="Saúde">
      <CheckMate>"A sua recepção consegue dar atenção VIP pro paciente particular, ou elas perdem o dia respondendo pergunta básica de convênio↗?"</CheckMate>
      <SocialProof>"Uma rede de clínicas cliente nossa aumentou em 40% a conversão de particulares só tirando o braçal da recepção."</SocialProof>
      <Solution_Logic>IA tria convênio vs particular e agenda.</Solution_Logic>
    </Segment>
    <Segment id="Imobiliário">
      <CheckMate>"Seus corretores atendem rápido, mas eles mantêm esse padrão às 9 da noite de domingo, ou é aí que a comissão escorre pelos dedos↗?"</CheckMate>
      <SocialProof>"Uma imobiliária parceira parou de perder lead no fim de semana e triplicou as visitas na segunda-feira."</SocialProof>
      <Solution_Logic>IA atende e qualifica renda 24/7.</Solution_Logic>
    </Segment>
    <Segment id="B2B">
      <CheckMate>"Vocês confiam que o vendedor faz follow-up incansável naquele orçamento antigo, ou a venda morre porque ele foca só no que chegou hoje↗?"</CheckMate>
      <SocialProof>"Numa indústria que atendemos, a IA reaqueceu 2 mil leads antigos e gerou 150 novos orçamentos no primeiro mês."</SocialProof>
      <Solution_Logic>IA faz follow-up infinito.</Solution_Logic>
    </Segment>
    <Segment id="Varejo">
      <CheckMate>"Quando o cliente abandona o carrinho, ele recebe um 'oi' no WhatsApp em 5 minutos, ou recebe aquele e-mail genérico que vai pro spam↗?"</CheckMate>
      <SocialProof>"Uma loja de moda saltou de 8% pra 22% de recuperação de carrinho usando a IA no WhatsApp."</SocialProof>
      <Solution_Logic>IA recupera carrinho no WhatsApp.</Solution_Logic>
    </Segment>
    <Segment id="Generico">
      <CheckMate>"Hoje sua equipe consegue responder todo mundo em menos de 5 minutos, ou vocês sentem que perdem venda por demora no atendimento↗?"</CheckMate>
      <SocialProof>"A maioria dos nossos clientes via o lead esfriar por demora. Com a IA, o tempo de resposta caiu pra segundos e a conversão subiu."</SocialProof>
      <Solution_Logic>IA garante atendimento imediato.</Solution_Logic>
    </Segment>
  </Matrix_Pain_CheckMate_SocialProof>
</KnowledgeBase>

<ScriptFlow>
# STEP 1: OPENING
"Oi {customer_name}? Kaique aqui da Mindflow. Tudo certo? ... Vi que você buscou sobre IA no Insta, foi você mesmo que preencheu o formulário, né?"

# STEP 2: DIAGNOSIS (CheckMate)
"Vi que você é de {segmento}. Me diz uma coisa... hoje, [CHECKMATE DO SEGMENTO]↗?"

# STEP 3: PROOF & SOLUTION
"Pois é, é clássico. A gente resolve isso com IA que [Solution_Logic]. Só pra você ter ideia: [SOCIAL PROOF]. Faz sentido pra você↗?"

# STEP 4: AUTOMATIC CLOSING
"Bora ver isso na prática. A agenda da especialista tá bem apertada, mas vou garantir um horário pra você aqui agora. Amanhã de manhã ou tarde↗?"
(Lead escolhe) -> "Perfeito. Já estou abrindo a agenda aqui... [TOOL: VerificaAgenda] ... Ótimo, consegui! Já estou enviando o convite pro seu e-mail {email} agora mesmo. [TOOL: agendar_reuniao] ... Pronto, enviado! Nos vemos na demo, abraço!"
</ScriptFlow>

<ObjectionHandling>
- PREÇO: "Investimento é fração de um funcionário. Se economizar 40h do time, vale o papo↗?"
- EMAIL: "Mando sim, mas pra ser certeiro: o gargalo aí é falta de lead ou de braço↗?"
- SEM TEMPO: "Entendo total. Por isso a demo é 15 min jogo rápido. Prefere ver um vídeo de 3 min ou falamos na quinta↗?"
</ObjectionHandling>
</SystemPrompt>"""


class WorkflowSimulator:
    def __init__(self, payload: schemas.SimulacaoStartPayload):
        self.payload = payload
        self.execution_id = None
        self.prompt_cliente_raw = ""
        self.prompt_sdr_raw = ""
        self.perfil_data = ""
        
        # Histórico de conversação formatado para os dois agentes
        self.conversa_completa: List[Dict[str, str]] = []
        
    async def initialize(self) -> str:
        """Inicializa a simulação e cria o registro mestre no Supabase."""
        # 1. Carrega os prompts locais em conformidade com as restrições de RLS
        await self._fetch_prompts()
        
        # 2. Prepara os dados de perfil comportamental
        self._prepare_perfil_data()
        
        # 3. Registrar o início no Supabase (workflow_executions) - Registro Mestre
        try:
            input_data = self.payload.model_dump()
            res = supabase.table("workflow_executions").insert({
                "workflow_name": "workflow_simulacao_vendas",
                "status": "RUNNING",
                "input_data": input_data,
                "started_at": get_utc_now(),
                "created_at": get_utc_now(),
                "updated_at": get_utc_now()
            }).execute()
            
            if res.data and len(res.data) > 0:
                self.execution_id = res.data[0]["id"]
            else:
                raise ValueError("Falha ao criar registro de execução no Supabase: dados retornados vazios.")
                
        except Exception as e:
            print(f"Erro ao registrar início no Supabase: {str(e)}")
            import uuid
            self.execution_id = str(uuid.uuid4())
            
        return self.execution_id

    async def _fetch_prompts(self):
        """Carrega os prompts dinamicamente do Supabase, com fallback local robusto."""
        try:
            # 1. Busca o prompt do Cliente
            res_cliente = supabase.table("Prompts").select('"Ligação/txt"').eq("id", self.payload.prompt_id_cliente).execute()
            if res_cliente.data and len(res_cliente.data) > 0 and res_cliente.data[0].get("Ligação/txt"):
                self.prompt_cliente_raw = res_cliente.data[0]["Ligação/txt"]
                print(f"[INFO] Prompt do Cliente (ID {self.payload.prompt_id_cliente}) carregado com sucesso do Supabase.")
            else:
                self.prompt_cliente_raw = PROMPT_CLIENTE_LOCAL
                print(f"[WARNING] Prompt do Cliente (ID {self.payload.prompt_id_cliente}) não encontrado no Supabase. Usando fallback local.")

            # 2. Busca o prompt do SDR
            res_sdr = supabase.table("Prompts").select('"Ligação/txt"').eq("id", self.payload.prompt_id_sdr).execute()
            if res_sdr.data and len(res_sdr.data) > 0 and res_sdr.data[0].get("Ligação/txt"):
                self.prompt_sdr_raw = res_sdr.data[0]["Ligação/txt"]
                print(f"[INFO] Prompt do SDR (ID {self.payload.prompt_id_sdr}) carregado com sucesso do Supabase.")
            else:
                self.prompt_sdr_raw = PROMPT_SDR_LOCAL
                print(f"[WARNING] Prompt do SDR (ID {self.payload.prompt_id_sdr}) não encontrado no Supabase. Usando fallback local.")

        except Exception as e:
            print(f"[WARNING] Falha na conexão com Supabase para busca de prompts ({str(e)}). Usando fallbacks locais.")
            self.prompt_cliente_raw = PROMPT_CLIENTE_LOCAL
            self.prompt_sdr_raw = PROMPT_SDR_LOCAL

    def _prepare_perfil_data(self):
        """Tenta extrair do Prompt a definição do perfil escolhido, com fallback robusto em código."""
        perfil = self.payload.perfil_cliente.lower()
        
        # 1. Tenta extrair usando Regex simples do XML do Prompt 67 local
        pattern = rf"<Perfil id=\"{perfil}\">(.*?)</Perfil>"
        match = re.search(pattern, self.prompt_cliente_raw, re.DOTALL | re.IGNORECASE)
        
        if match:
            self.perfil_data = match.group(1).strip()
            print(f"Perfil '{perfil}' extraído dinamicamente do XML do prompt local.")
            return

        # 2. Fallbacks estáticos robustos baseados nos perfis reais contidos na especificação do Prompt 67
        perfis_fallback = {
            "cetico": (
                "Nome: Carlos Mendes\n"
                "Cargo: Diretor Comercial | Distribuidora regional (45 vend.)\n"
                "Resistencia_inicial: 90/100\n"
                "Comportamento: Desconfiado, acredita que IA é modismo. Valoriza o manual. Interrompe muito.\n"
                "Dor_latente: Alta rotatividade, falta de follow-up, onboarding leva 3 meses.\n"
                "Gatilho: Padronização de processos sem depender de pessoas-chave.\n"
                "Frases: 'IA é coisa de empresa grande', 'Meu time já funciona bem'."
            ),
            "ocupado": (
                "Nome: Fernanda Rocha\n"
                "Cargo: Gerente de Vendas | SaaS B2B (12 vend.)\n"
                "Resistencia_inicial: 85/100\n"
                "Comportamento: Respostas curtas, objetiva, tenta registrar a ligação rápido.\n"
                "Dor_latente: Pipeline sujo, leads desqualificados para closers, conversão < 8%.\n"
                "Gatilho: Leads qualificados chegando aos closers.\n"
                "Frases: 'Pode ser rápido?', 'Manda um email'."
            ),
            "preco": (
                "Nome: Roberto Alves\n"
                "Cargo: Sócio-fundador | Agência de Marketing (8 pessoas)\n"
                "Resistencia_inicial: 80/100\n"
                "Comportamento: Questiona ROI, desconfia de promessas, já teve experiências ruins.\n"
                "Dor_latente: Perda de 2-3 contratos/mês por demora no follow-up manual.\n"
                "Gatilho: Quantificar perda mensal em reais antes do investimento.\n"
                "Frases: 'Quanto custa?', 'Preciso ver retorno antes'."
            ),
            "fiel": (
                "Nome: Amanda Costa\n"
                "Cargo: Head de Growth | E-commerce (20 SDRs)\n"
                "Resistencia_inicial: 88/100\n"
                "Comportamento: Usa outra solução há 1 ano, teme retrabalho e resistência do time.\n"
                "Dor_latente: Falta de integração com CRM, relatórios manuais (4h/semana perdidas).\n"
                "Gatilho: Integração e automação de relatórios sem falar em troca.\n"
                "Frases: 'Já uso uma solução', 'Não vejo motivo pra trocar'."
            ),
            # --- SUGESTÕES DE PERFIS PROPENSOS A FECHAR VENDAS ---
            "sobrecarregado_comercial": (
                "Nome: Juliano Santos\n"
                "Cargo: Diretor de Operações em Hub Logístico (250+ leads/mês)\n"
                "Resistencia_inicial: 75/100\n"
                "Comportamento: Ocupado e sobrecarregado. Perde muitos leads e sabe disso. Quer uma solução pronta.\n"
                "Dor_latente: Leads demoram 3+ horas para resposta. Perda de mais de 60% dos leads de WhatsApp.\n"
                "Gatilho: Resposta imediata 24/7 de forma personalizada sem depender de contratações.\n"
                "Frases: 'Não consigo dar conta dos leads', 'Meus vendedores demoram muito pra responder'."
            ),
            "buscador_de_eficiencia": (
                "Nome: Beatriz Ramos\n"
                "Cargo: CMO / Head de Growth em E-commerce B2B\n"
                "Resistencia_inicial: 70/100\n"
                "Comportamento: Focada em inovação e ROI. Aberta a demonstrações e testes se vir potencial de escala.\n"
                "Dor_latente: Custo alto para cobrir horários alternativos (noites e finais de semana).\n"
                "Gatilho: Redução de 30% do CAC e qualificação 24h por dia.\n"
                "Frases: 'Como vocês garantem o ROI?', 'A IA soa natural mesmo?'."
            ),
            "frustrado_com_concorrente": (
                "Nome: Marcos Cunha\n"
                "Cargo: Sócio Comercial em Rede de Clínicas Particulares\n"
                "Resistencia_inicial: 80/100\n"
                "Comportamento: Cético devido a experiências ruins com bots de menus rígidos, mas quer muito resolver o gargalo.\n"
                "Dor_latente: Perda de clientes por falta de agendamento ágil de consultas e menus que irritam os leads.\n"
                "Gatilho: IA fluida e natural que realmente simula um humano conversando e agenda consultas.\n"
                "Frases: 'Já testei robô e meus clientes odiaram', 'Tem que ser natural'."
            )
        }
        
        self.perfil_data = perfis_fallback.get(perfil, perfis_fallback["cetico"])
        print(f"Perfil '{perfil}' carregado via fallback estático.")

    async def run_simulation(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Executa a simulação gerando turnos alternados e fazendo yield em tempo real."""
        data_atual_br = get_br_now().isoformat()
        
        # Configurações de Prompt de Sistema do Cliente (Lead)
        prompt_sistema_cliente = self.prompt_cliente_raw.replace("{data_atual_iso}", data_atual_br)
        prompt_sistema_cliente += f"\n\n<PerfilAtivo>\nVocê deve interpretar exatamente este perfil durante todo o roleplay:\n{self.perfil_data}\n</PerfilAtivo>"
        
        # Configurações de Prompt de Sistema do SDR (Kaique)
        prompt_sistema_sdr = self.prompt_sdr_raw
        prompt_sistema_sdr = prompt_sistema_sdr.replace("{data_atual_iso}", data_atual_br)
        prompt_sistema_sdr = prompt_sistema_sdr.replace("{{ now }}", data_atual_br)
        prompt_sistema_sdr = prompt_sistema_sdr.replace("{customer_name}", self.payload.customer_name)
        prompt_sistema_sdr = prompt_sistema_sdr.replace("{{ customer_name }}", self.payload.customer_name)
        prompt_sistema_sdr = prompt_sistema_sdr.replace("{email}", self.payload.email)
        prompt_sistema_sdr = prompt_sistema_sdr.replace("{{ email }}", self.payload.email)
        prompt_sistema_sdr = prompt_sistema_sdr.replace("{numero_do_lead}", self.payload.numero_do_lead)
        prompt_sistema_sdr = prompt_sistema_sdr.replace("{{ numero_do_lead }}", self.payload.numero_do_lead)
        
        # Injeta segmento genérico como valor padrão
        prompt_sistema_sdr = prompt_sistema_sdr.replace("{segmento}", "Comercial B2B")

        # A simulação começa com o Cliente atendendo a ligação
        fala_anterior_sdr = "Iniciar simulação. O SDR vai ligar agora. Atenda como o perfil selecionado."
        
        historial_cliente: List[Dict[str, str]] = [
            {"role": "system", "content": prompt_sistema_cliente}
        ]
        
        historial_sdr: List[Dict[str, str]] = [
            {"role": "system", "content": prompt_sistema_sdr}
        ]

        for turno in range(1, self.payload.max_turnos + 1):
            
            # -------------------------------------------------------------
            # 1. TURNO DO CLIENTE (LEAD)
            # -------------------------------------------------------------
            step_name_cliente = "workflow_simulacao_vendas_cliente_resposta"
            started_at_cliente = get_utc_now()
            
            historial_cliente.append({"role": "user", "content": fala_anterior_sdr})
            
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=historial_cliente,
                    temperature=0.7,
                    max_tokens=150
                )
                fala_cliente = response.choices[0].message.content.strip()
                historial_cliente.append({"role": "assistant", "content": fala_cliente})
                
                await self._log_step(
                    step_name=step_name_cliente,
                    status="SUCCESS",
                    attempt=1,
                    input_data={"ultima_fala_sdr": fala_anterior_sdr, "turno": turno},
                    output_data={"fala_cliente": fala_cliente},
                    started_at=started_at_cliente
                )
            except Exception as e:
                err_msg = f"Erro no Agente Cliente (Turno {turno}): {str(e)}"
                print(err_msg)
                await self._log_step(
                    step_name=step_name_cliente,
                    status="FAILED",
                    attempt=1,
                    input_data={"ultima_fala_sdr": fala_anterior_sdr, "turno": turno},
                    error_details=traceback.format_exc(),
                    started_at=started_at_cliente
                )
                yield {"type": "erro", "message": err_msg}
                await self.finalize(status="FAILED", error_details=err_msg)
                return

            resistance_level = 90 - (turno * 10)
            if resistance_level < 10:
                resistance_level = 10
            
            yield {
                "type": "turno",
                "speaker": "cliente",
                "message": fala_cliente,
                "turno": turno,
                "resistance_level": resistance_level
            }

            # -------------------------------------------------------------
            # 2. TURNO DO SDR (KAIQUE)
            # -------------------------------------------------------------
            step_name_sdr = "workflow_simulacao_vendas_sdr_resposta"
            started_at_sdr = get_utc_now()
            
            historial_sdr.append({"role": "user", "content": fala_cliente})
            
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=historial_sdr,
                    temperature=0.7,
                    max_tokens=200
                )
                fala_sdr = response.choices[0].message.content.strip()
                historial_sdr.append({"role": "assistant", "content": fala_sdr})
                
                await self._log_step(
                    step_name=step_name_sdr,
                    status="SUCCESS",
                    attempt=1,
                    input_data={"fala_cliente": fala_cliente, "turno": turno},
                    output_data={"fala_sdr": fala_sdr},
                    started_at=started_at_sdr
                )
            except Exception as e:
                err_msg = f"Erro no Agente SDR (Turno {turno}): {str(e)}"
                print(err_msg)
                await self._log_step(
                    step_name=step_name_sdr,
                    status="FAILED",
                    attempt=1,
                    input_data={"fala_cliente": fala_cliente, "turno": turno},
                    error_details=traceback.format_exc(),
                    started_at=started_at_sdr
                )
                yield {"type": "erro", "message": err_msg}
                await self.finalize(status="FAILED", error_details=err_msg)
                return
                
            fala_anterior_sdr = fala_sdr
            
            yield {
                "type": "turno",
                "speaker": "sdr",
                "message": fala_sdr,
                "turno": turno
            }
            
            self.conversa_completa.append({"speaker": "cliente", "message": fala_cliente, "turno": turno})
            self.conversa_completa.append({"speaker": "sdr", "message": fala_sdr, "turno": turno})

            # Critério de fechamento antecipado por agendamento
            if any(palavra in fala_sdr.lower() for palavra in ["agendado", "convite enviado", "marcada", "marcado com sucesso"]):
                print("Agendamento comercial detectado. Encerrando roleplay.")
                break

        # Geração do feedback final
        feedback_report = await self._generate_feedback_report()
        score = self._calculate_score(feedback_report)
        
        await self.finalize(status="SUCCESS", output_data={
            "status": "Simulação finalizada com sucesso",
            "turnos_executados": len(self.conversa_completa) // 2,
            "score": score,
            "feedback_report": feedback_report
        })
        
        yield {
            "type": "fim",
            "message": "Simulação de vendas concluída com sucesso.",
            "execution_id": self.execution_id,
            "score": score,
            "feedback_report": feedback_report
        }

    async def _log_step(self, step_name: str, status: str, attempt: int, 
                          input_data: Dict[str, Any] = None, 
                          output_data: Dict[str, Any] = None, 
                          error_details: str = None, 
                          started_at: str = None):
        """Registra as etapas detalhadas na tabela workflow_step_executions do Supabase."""
        try:
            supabase.table("workflow_step_executions").insert({
                "execution_id": self.execution_id,
                "step_name": step_name,
                "status": status,
                "attempt": attempt,
                "input_data": input_data,
                "output_data": output_data,
                "error_details": error_details,
                "started_at": started_at,
                "completed_at": get_utc_now(),
                "created_at": get_utc_now()
            }).execute()
        except Exception as e:
            print(f"Erro ao registrar step {step_name} no Supabase: {str(e)}")

    async def _generate_feedback_report(self) -> str:
        """Gera um relatório completo de avaliação de performance do SDR com base no histórico."""
        transcricao = "\n".join([f"{c['speaker'].upper()}: {c['message']}" for c in self.conversa_completa])
        
        prompt_avaliacao = f"""
        Você é o avaliador oficial da Mindflow Training. Analise a transcrição da ligação de vendas abaixo e gere o relatório detalhado de feedback final de acordo com a estrutura do <Relatorio_Feedback_Output> contida no Prompt de Sistema do Lead.

        <Transcrit_Ligacao>
        {transcricao}
        </Transcrit_Ligacao>

        <Criterios_Pontuacao>
        - Abertura (15%): Conexão humana, empatia, fugiu de roteiro robotizado.
        - Sondagem (20%): Fez perguntas inteligentes de Situação e Problema para extrair a dor latente do perfil.
        - Amplificação da Dor (20%): Fez perguntas de Implicação baseadas no SPIN Selling.
        - Pitch / Apresentação de Valor (20%): Direcionou o valor da IA à dor latente encontrada do perfil.
        - Objeções (15%): Lidou com as objeções do cliente de forma socrática, em vez de defensiva.
        - Fechamento (10%): Fez uma proposta direta sugerindo data/hora, sem enrolação.
        </Criterios_Pontuacao>

        Escreva o relatório em Markdown estruturado, incluindo:
        1. Resumo da Simulação (Perfil avaliado, turnos, resultado do agendamento).
        2. Pontuação Estimada de 0 a 100 baseada nos pesos.
        3. Avaliação por Etapas (Notas de 0 a 10 por etapa).
        4. Pontos Positivos (Acertos do SDR).
        5. Oportunidades de Melhoria (Erros ou omissões).
        6. Momento Crítico da conversa (O ponto de virada).
        """
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt_avaliacao}],
                temperature=0.5,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Falha ao gerar relatório de feedback: {str(e)}"

    def _calculate_score(self, report_text: str) -> int:
        """Extrai a pontuação estimada do texto do relatório usando regex."""
        match = re.search(r"Pontuação[\s\w]*:\s*(\d+)", report_text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        match_alt = re.search(r"(\d+)\s*/\s*100", report_text)
        if match_alt:
            return int(match_alt.group(1))
        return 70

    async def finalize(self, status: str, output_data: Dict[str, Any] = None, error_details: str = None):
        """Finaliza o registro mestre na tabela workflow_executions do Supabase."""
        try:
            supabase.table("workflow_executions").update({
                "status": status,
                "output_data": output_data,
                "error_details": error_details,
                "completed_at": get_utc_now(),
                "updated_at": get_utc_now()
            }).eq("id", self.execution_id).execute()
            print(f"Execução {self.execution_id} finalizada com status {status} no Supabase.")
        except Exception as e:
            print(f"Erro ao finalizar execução no Supabase: {str(e)}")
