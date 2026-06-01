import asyncio
import sys
import io
import schemas
from workflow_simulator import WorkflowSimulator

# Corrige codificação do terminal Windows para suportar emojis nos logs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def run_single_simulation(perfil_id: str, customer_name: str, email: str, numero_do_lead: str):
    print("=" * 60)
    print(f"🤖 INICIANDO SIMULAÇÃO: Perfil '{perfil_id}' ({customer_name}) 🤖")
    print("=" * 60)
    
    payload = schemas.SimulacaoStartPayload(
        customer_name=customer_name,
        email=email,
        numero_do_lead=numero_do_lead,
        perfil_cliente=perfil_id,
        max_turnos=3,  # 3 turnos para manter rapidez e economia de tokens
        prompt_id_cliente=67,
        prompt_id_sdr=16
    )
    
    simulator = WorkflowSimulator(payload)
    
    print(f"[INFO] Inicializando conexão e criando registro mestre no Supabase...")
    try:
        execution_id = await simulator.initialize()
        print(f"[SUCCESS] Registro mestre criado. Execution ID: {execution_id}\n")
    except Exception as e:
        print(f"[FAIL] Falha na inicialização do perfil '{perfil_id}': {str(e)}\n")
        return {"perfil": perfil_id, "status": "FALHA_INICIALIZACAO", "score": 0, "execution_id": None}
        
    print("-" * 40)
    print(f"           DIÁLOGO DE VENDAS - {customer_name.upper()}           ")
    print("-" * 40)
    
    score = 0
    feedback = ""
    status = "SUCCESS"
    
    try:
        async for evento in simulator.run_simulation():
            ev_type = evento.get("type")
            
            if ev_type == "turno":
                speaker = evento.get("speaker", "").upper()
                message = evento.get("message")
                turno = evento.get("turno")
                
                if speaker == "CLIENTE":
                    res = evento.get("resistance_level")
                    print(f"👤 [Turno {turno}] CLIENTE ({customer_name}):")
                    print(f"   \"{message}\"")
                    print(f"   (Resistência: {res}/100)\n")
                else:
                    print(f"👔 [Turno {turno}] SDR (Kaique):")
                    print(f"   \"{message}\"\n")
                    
            elif ev_type == "fim":
                score = evento.get('score', 0)
                feedback = evento.get('feedback_report', "")
                print(f"✅ FIM DA SIMULAÇÃO - SCORE: {score}/100")
                
            elif ev_type == "erro":
                print(f"❌ ERRO NO FLUXO: {evento.get('message')}")
                status = "FAILED"
                
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado no loop: {str(e)}")
        status = "FAILED"
        
    print("=" * 60)
    print(f"🤖 FIM DA SIMULAÇÃO: Perfil '{perfil_id}' 🤖")
    print("=" * 60 + "\n\n")
    
    # Pequena pausa para evitar taxa limite da API da OpenAI em chamadas sequenciais rápidas
    await asyncio.sleep(2)
    
    return {
        "perfil": perfil_id,
        "customer": customer_name,
        "status": status,
        "score": score,
        "execution_id": execution_id
    }

async def main():
    perfis_teste = [
        {"id": "cetico", "name": "Carlos Mendes", "email": "carlos.mendes@distribuidora.com.br", "number": "+5548999990001"},
        {"id": "ocupado", "name": "Fernanda Rocha", "email": "fernanda.rocha@saas.com.br", "number": "+5548999990002"},
        {"id": "preco", "name": "Roberto Alves", "email": "roberto.alves@agencia.com.br", "number": "+5548999990003"},
        {"id": "fiel", "name": "Amanda Costa", "email": "amanda.costa@ecommerce.com.br", "number": "+5548999990004"},
        {"id": "sobrecarregado_comercial", "name": "Juliano Santos", "email": "juliano.santos@hub.com.br", "number": "+5548999990005"},
        {"id": "buscador_de_eficiencia", "name": "Beatriz Ramos", "email": "beatriz.ramos@growth.com.br", "number": "+5548999990006"},
        {"id": "frustrado_com_concorrente", "name": "Marcos Cunha", "email": "marcos.cunha@clinica.com.br", "number": "+5548999990007"}
    ]
    
    print("==========================================================")
    print("🚀 INICIANDO SIMULAÇÕES EM LOTE PARA TODOS OS PERFIS 🚀")
    print("==========================================================\n")
    
    resultados = []
    
    for p in perfis_teste:
        res = await run_single_simulation(p["id"], p["name"], p["email"], p["number"])
        resultados.append(res)
        
    print("==========================================================")
    print("📊            TABELA RESUMO DAS SIMULAÇÕES               📊")
    print("==========================================================")
    print(f"{'Perfil':<26} | {'Cliente':<15} | {'Score':<5} | {'Status':<8} | {'Execution ID':<36}")
    print("-" * 100)
    for r in resultados:
        perfil_str = r["perfil"]
        cust_str = r["customer"]
        score_str = str(r["score"])
        status_str = r["status"]
        exec_str = str(r["execution_id"]) if r["execution_id"] else "N/A"
        print(f"{perfil_str:<26} | {cust_str:<15} | {score_str:<5} | {status_str:<8} | {exec_str:<36}")
    print("==========================================================\n")

if __name__ == "__main__":
    asyncio.run(main())
