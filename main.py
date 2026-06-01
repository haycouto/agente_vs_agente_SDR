import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import schemas
from workflow_simulator import WorkflowSimulator
from config import supabase

app = FastAPI(
    title="MindFlow Sales Simulation API",
    description="API para simulação interativa em tempo real de ligações de vendas (SDR vs Cliente) via WebSockets.",
    version="1.0.0"
)

# Adiciona suporte a CORS (importante para conexões de painéis web externos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "MindFlow Sales Simulation API",
        "websockets_endpoint": "/ws/simulacao-vendas"
    }

@app.get("/execucoes-recentes")
def get_execucoes_recentes(limit: int = 10):
    """Retorna a lista de simulações recentes gravadas no Supabase."""
    try:
        res = supabase.table("workflow_executions")\
            .select("id, status, input_data, output_data, error_details, started_at, completed_at")\
            .eq("workflow_name", "workflow_simulacao_vendas")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return res.data
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Falha ao consultar banco: {str(e)}"})

@app.websocket("/ws/simulacao-vendas")
async def websocket_simulacao_vendas(websocket: WebSocket):
    await websocket.accept()
    print("Nova conexão WebSocket estabelecida.")
    
    simulator: WorkflowSimulator = None
    
    try:
        # 1. Aguarda a mensagem inicial de parametrização
        data = await websocket.receive_text()
        payload_json = json.loads(data)
        
        # Valida os dados de entrada usando o Schema Pydantic
        start_payload = schemas.SimulacaoStartPayload(**payload_json)
        
        # 2. Inicializa o simulador
        simulator = WorkflowSimulator(start_payload)
        execution_id = await simulator.initialize()
        
        # Envia confirmação de início
        await websocket.send_json({
            "type": "start",
            "message": "Simulação de vendas inicializada.",
            "execution_id": execution_id
        })
        
        # 3. Executa o loop de simulação e envia os turnos em tempo real
        async for evento in simulator.run_simulation():
            await websocket.send_json(evento)
            
            # Se for uma mensagem de encerramento ou erro, encerra o loop local
            if evento.get("type") in ["fim", "erro"]:
                break
                
    except WebSocketDisconnect:
        print("Cliente WebSocket se desconectou abruptamente.")
        if simulator and simulator.execution_id:
            await simulator.finalize(
                status="FAILED",
                error_details="Conexão do cliente via WebSocket foi fechada abruptamente."
            )
            
    except Exception as e:
        error_msg = f"Erro crítico na simulação: {str(e)}"
        print(error_msg)
        try:
            await websocket.send_json({
                "type": "erro",
                "message": error_msg
            })
        except Exception:
            pass # Cliente já pode ter se desconectado
            
        if simulator and simulator.execution_id:
            await simulator.finalize(
                status="FAILED",
                error_details=error_msg
            )
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
        print("Conexão WebSocket finalizada.")
