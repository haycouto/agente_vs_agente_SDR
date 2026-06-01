from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class SimulacaoStartPayload(BaseModel):
    customer_name: str = Field(default="Carlos Mendes", description="Nome completo do lead/cliente fictício")
    email: EmailStr = Field(default="carlos.mendes@distribuidora.com.br", description="Email de contato do lead/cliente")
    numero_do_lead: str = Field(default="+5548999990000", description="Número de telefone do lead no formato +55DDXXXXXXXXX")
    perfil_cliente: str = Field(default="cetico", description="ID do perfil de comportamento (cetico, ocupado, preco, fiel)")
    max_turnos: int = Field(default=12, ge=2, le=30, description="Quantidade máxima de iterações do diálogo")
    prompt_id_cliente: int = Field(default=67, description="ID do prompt do Lead Simulado na tabela Prompts (padrão 67: SDR_treinamento)")
    prompt_id_sdr: int = Field(default=16, description="ID do prompt do SDR Kaique na tabela Prompts (padrão 16: mindflow form 3)")

class TurnoMessage(BaseModel):
    type: str = Field(default="turno", description="Tipo da mensagem (turno, info, fim, erro)")
    speaker: str = Field(..., description="Quem está falando (cliente ou sdr)")
    message: str = Field(..., description="Conteúdo da fala")
    turno: int = Field(..., description="Turno atual da simulação")
    resistance_level: Optional[int] = Field(None, description="Nível de resistência estimado do cliente (apenas para turnos do cliente)")

class InfoMessage(BaseModel):
    type: str = Field(default="info", description="Tipo da mensagem")
    message: str = Field(..., description="Mensagem de informação")
    execution_id: Optional[str] = Field(None, description="UUID da execução no Supabase")

class FimMessage(BaseModel):
    type: str = Field(default="fim", description="Tipo da mensagem")
    message: str = Field(default="Simulação concluída com sucesso.", description="Mensagem de encerramento")
    execution_id: str = Field(..., description="UUID da execução no Supabase")
    score: Optional[int] = Field(None, description="Pontuação final obtida na simulação (0-100)")
    feedback_report: Optional[str] = Field(None, description="Relatório de feedback gerado pela IA ao final")

class ErroMessage(BaseModel):
    type: str = Field(default="erro", description="Tipo da mensagem")
    message: str = Field(..., description="Detalhes do erro ocorrido")
