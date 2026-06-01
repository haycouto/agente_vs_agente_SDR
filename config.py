import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
# Damos preferência para a service_role key se ela estiver presente, para ignorar RLS
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL e SUPABASE_KEY (ou SUPABASE_SERVICE_ROLE_KEY) devem estar configurados no arquivo .env")

# Inicializa o cliente Supabase uma única vez (Module-level Singleton)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configurações do OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY deve estar configurada no arquivo .env")

# Inicializa o cliente OpenAI uma única vez (Module-level Singleton)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# --- Gestão de Tempo e Datas (Convenções EDW) ---

BR_ZONE = ZoneInfo("America/Sao_Paulo")

def get_utc_now() -> str:
    """Retorna o timestamp atual em UTC no formato ISO 8601 com 'Z' (offset zero)."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def get_br_now() -> datetime:
    """Retorna o datetime atual no fuso horário de Brasília (America/Sao_Paulo)."""
    return datetime.now(BR_ZONE)

def parse_iso_to_br(iso_date_str: str) -> datetime:
    """Converte uma string ISO 8601 de qualquer fuso horário para o fuso de Brasília (America/Sao_Paulo)."""
    if iso_date_str.endswith("Z"):
        iso_date_str = iso_date_str.replace("Z", "+00:00")
    dt = datetime.fromisoformat(iso_date_str)
    return dt.astimezone(BR_ZONE)
