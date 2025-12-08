
import sys
import os
import json 
import asyncio
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de rutas
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir) 
sys.path.append(parent_dir)

# Importar el agente
from src.agents.tech_surveillance.graph import agent 
from langchain_core.messages import HumanMessage

def json_serializer(obj):
    """Función para ayudar a json a guardar objetos complejos"""
    # Para objetos Pydantic v2 (usado en versiones recientes de LangChain)
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    # Para objetos Pydantic v1 o LangChain legacy
    if hasattr(obj, 'dict'):
        return obj.dict()
    # Para cualquier otro objeto desconocido, conviértelo a string
    return str(obj)

async def test_agent():
    """
    Test completo del flujo del agente:
    1. Ingerir información de convocatoria
    2. Generar ideas de proyecto
    3. Seleccionar una idea (simulado)
    4. Generar esquema inicial y documento
    5. Realizar investigación completa y generar documentos finales
    """
    global_state = {} # estadoi global para los flujos 

    print("="*80)
    print("🔬 TEST COMPLETO DEL AGENTE DE VIGILANCIA TECNOLÓGICA")
    print("="*80)
    print("🔑 Verificando API KEY...", "✅ OK" if os.environ.get("GEMINI_API_KEY") else "❌ Falta KEY")
    print()
    
    # ========================================================================
    # PASO 1: INGESTA DE INFORMACIÓN DE CONVOCATORIA
    # ========================================================================
    
    texto_convocatoria = """
    Asunto: Intención de postulación - Convocatoria 966 Colombia Inteligente

    Hola,

    He decidido que vamos a aplicar a la "CONVOCATORIA COLOMBIA INTELIGENTE: CIENCIA Y TECNOLOGÍAS CUÁNTICAS E INTELIGENCIA ARTIFICIAL PARA LOS TERRITORIOS | Convocatoria 966". Esta es una excelente oportunidad para financiar nuestro proyecto de Investigación Aplicada, Desarrollo Tecnológico e Innovación (CTeI).

    La convocatoria está dirigida específicamente a grupos de investigación, academia y startups como la nuestra que estén desarrollando soluciones disruptivas. El objetivo principal es impulsar proyectos en tecnologías cuánticas e Inteligencia Artificial que generen un impacto medible y ayuden a cerrar brechas tecnológicas en los territorios del país.

    Entre los beneficios que obtendríamos al participar están:

    El fomento de la transferencia tecnológica.
    El desarrollo de talento especializado.
    El fortalecimiento de nuestra vinculación con la industria y el sector público.

    Aunque las fechas de inicio y cierre, así como el monto exacto de financiamiento, aún aparecen como "No especificados", debemos estar atentos y tener lista la propuesta.

    Puedes consultar más detalles directamente en el enlace oficial:
    https://minciencias.gov.co/convocatorias/convocatoria-colombia-inteligente-ciencia-y-tecnologias-cuanticas-e-inteligencia
    """
    print("-" * 80)
    print("📥 PASO 1: INGESTA DE CONVOCATORIA")
    print("-" * 80)
    
    initial_state = {
        "messages": [HumanMessage(content=texto_convocatoria)],
        "route_decision": "ingest" 
    }

    print("🚀 Procesando información de la convocatoria...")
    state_after_ingest = await agent.ainvoke(initial_state)

    print("\n✅ Ingesta completada")
    if state_after_ingest.get("call_info"):
        call_info = state_after_ingest["call_info"]
        print(f"   � Título: {call_info.title}")
        print(f"   🎯 Objetivo: {call_info.objective[:100] if call_info.objective else 'N/A'}...")
        print(f"   💰 Financiamiento: {call_info.funding or 'No especificado'}")
        if call_info.keywords:
            print(f"   🏷️  Keywords: {', '.join(call_info.keywords[:5])}")
    
    # Verificar si se generaron documentos de presentación
    if state_after_ingest.get("docs_paths"):
        docs = state_after_ingest["docs_paths"]
        if docs.presentation_oath_md:
            print(f"   📄 Presentación MD: {docs.presentation_oath_md}")
        if docs.presentation_oath_pdf:
            print(f"   📄 Presentación PDF: {docs.presentation_oath_pdf}")
        if docs.presentation_oath_pptx:
            print(f"   📄 Presentación PPTX: {docs.presentation_oath_pptx}")
    
    print()

    # actualizamos el esatdo global de la ejecucion 

    global_state = state_after_ingest

    with open('state_test/state_p1.json', 'w', encoding='utf-8') as archivo:
        json.dump(global_state, archivo, indent=4, ensure_ascii=False, default=json_serializer)
    
    # ========================================================================
    # PASO 2: GENERACIÓN DE IDEAS DE PROYECTO
    # ========================================================================
    print("-" * 80)
    print("� PASO 2: GENERACIÓN DE IDEAS DE PROYECTO")
    print("-" * 80)

    global_state["route_decision"] = "proposal_ideas"

    state_after_proposal_ai = await agent.ainvoke(global_state)

    if state_after_proposal_ai["proposal_ideas"]:
        print("-----------------------------------")
        for idea in state_after_proposal_ai["proposal_ideas"].ideas:
            print(f"  titulo : \n {idea.idea_title}")
            print(f"  descripcion : \n {idea.idea_description}")
            print(f"  objetivos : \n ")
            for obj in idea.idea_objectives:
                print(f"    - {obj}")
    else:
        print(" ideas no encontradas ")

    global_state = state_after_proposal_ai
    
    with open('state_test/state_p2.json', 'w', encoding='utf-8') as archivo:
        json.dump(global_state, archivo, indent=4, ensure_ascii=False, default=json_serializer)
    
   

    # ========================================================================
    # PASO 3: selecion de idea y genracion de es quema incial  
    # ========================================================================
    print("-" * 80)
    print("� PASO 3: selecion y genraciond e esquema incial  ")
    print("-" * 80)

    global_state["route_decision"] = "project_idea"
    global_state["selected_idea"] = state_after_proposal_ai.get("proposal_ideas").ideas[1]

    state_after_project_idea = await agent.ainvoke(global_state)

    if state_after_project_idea.get("report_components"):
        print("--------- info del proyecto -------------")
        general_info = state_after_project_idea.get("report_components").general_info

        print(f" titulo :\n {general_info.project_title}")
        print(f" descripcion :\n {general_info.project_description}")
        print(f" keywords :\n {general_info.keywords}")
        
    else:
        print(" esquema incial no encontrado ")

    if state_after_project_idea.get("initial_schema"):
        print("--------- esquema incial del proyecto -------------")
        print(state_after_project_idea.get("initial_schema"))
    else:
        print(" esquema incial no encontrado ")

    if state_after_project_idea.get("docs_paths"):
        docs = state_after_project_idea.get("docs_paths")
        print(" documentos generados ")
        print(f" - pdf : {docs.proyect_proposal_initial_schema_pdf}")
        print(f" - md : {docs.proyect_proposal_initial_schema_md}")
    else:
        print("documentos no genrados")

    global_state = state_after_project_idea

    with open('state_test/state_p3.json', 'w', encoding='utf-8') as archivo:
        json.dump(global_state, archivo, indent=4, ensure_ascii=False, default=json_serializer)
    

    # ========================================================================
    # PASO 4: generacion de investiagcioin y documento final 
    # ========================================================================
    print("-" * 80)
    print("� PASO 4: genracion de documemnto e investigacion final   ")
    print("-" * 80)

    global_state["route_decision"] = "generate_proyect"

    state_after_generate_proyect = await agent.ainvoke(global_state)

    if state_after_generate_proyect.get("docs_paths"):
        docs = state_after_generate_proyect.get("docs_paths")
        print(" documentos generados ")
        print(f" - pdf : {docs.proyect_proposal_pdf}")
        print(f" - md : {docs.proyect_proposal_md}")
        print(f" - img : {docs.poster_image_path}")
    else:
        print("documentos no genrados")


    global_state = state_after_generate_proyect

    with open('state_test/state_p4.json', 'w', encoding='utf-8') as archivo:
        json.dump(global_state, archivo, indent=4, ensure_ascii=False, default=json_serializer)

if __name__ == "__main__":
    asyncio.run(test_agent())