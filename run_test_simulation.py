import asyncio
import sys
import io
from workflow_simulator import WorkflowSimulator
import schemas
from config import BR_ZONE

# Corrige codificação do terminal Windows para suportar emojis do log
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def main():
    print("==================================================")
    print("🤖 INICIANDO SIMULAÇÃO DE VENDAS LOCAL (TESTE) 🤖")
    print("==================================================")
    
    # Prepara o payload de teste
    payload = schemas.SimulacaoStartPayload(
        customer_name="Carlos Mendes",
        email="carlos.mendes@distribuidora.com.br",
        numero_do_lead="+5548996027108",
        perfil_cliente="sobrecarregado_comercial",
        max_turnos=3,  # 3 turnos para o teste ser rápido e econômico
        prompt_id_cliente=67,
        prompt_id_sdr=16
    )
    
    # Inicializa o simulador
    simulator = WorkflowSimulator(payload)
    
    print("\n[INFO] Conectando ao Supabase e registrando auditoria...")
    try:
        execution_id = await simulator.initialize()
        print(f"[SUCCESS] Registro mestre criado. Execution ID: {execution_id}\n")
    except Exception as e:
        print(f"[FAIL] Falha na inicialização: {str(e)}")
        return
        
    print("==================================================")
    print("           INÍCIO DO DIÁLOGO DE VENDAS           ")
    print("==================================================\n")
    
    try:
        async for evento in simulator.run_simulation():
            ev_type = evento.get("type")
            
            if ev_type == "turno":
                speaker = evento.get("speaker", "").upper()
                message = evento.get("message")
                turno = evento.get("turno")
                
                if speaker == "CLIENTE":
                    res = evento.get("resistance_level")
                    print(f"👤 [Turno {turno}] CLIENTE ({payload.customer_name}):")
                    print(f"   \"{message}\"")
                    print(f"   (Resistência: {res}/100)\n")
                else:
                    print(f"👔 [Turno {turno}] SDR (Kaique):")
                    print(f"   \"{message}\"\n")
                    print("-" * 50 + "\n")
                    
            elif ev_type == "fim":
                print("==================================================")
                print("            FIM DA SIMULAÇÃO DE VENDAS            ")
                print("==================================================\n")
                print(f"Pontuação Final do SDR: {evento.get('score')}/100")
                print(f"\nFeedback Report:\n{evento.get('feedback_report')}")
                
            elif ev_type == "erro":
                print(f"\n❌ ERRO NA SIMULAÇÃO: {evento.get('message')}\n")
                
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado no loop: {str(e)}")
        
if __name__ == "__main__":
    asyncio.run(main())
