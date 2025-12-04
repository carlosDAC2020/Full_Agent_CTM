import chainlit as cl
import json
import asyncio
import os
from graph_workflow import dummy_graph 

# Cargar datos
try:
    with open("data/convocatorias.json", "r", encoding="utf-8") as f:
        CONVOCATORIAS_DATA = json.load(f)
except FileNotFoundError:
    CONVOCATORIAS_DATA = []
    print("Error: No se encontró data/convocatorias.json")

# Configurar CSS personalizado al iniciar
@cl.on_chat_start
async def start():
    # Aunque el CSS lo oculta, mantenemos esto por seguridad
    await cl.ChatSettings(
        input_enabled=False
    ).send()

    selector = cl.CustomElement(
        name="ConvocatoriaSelector", 
        props={"convocatorias": CONVOCATORIAS_DATA, "selected_id": ""}
    )
    await cl.Message(
        content="👋 **Bienvenido al Asistente de Gestión de Proyectos**.\nSelecciona una convocatoria para comenzar:",
        elements=[selector]
    ).send()

@cl.on_message
async def main(message: cl.Message):
    content = message.content

    # --- PASO 2: CONVOCATORIA SELECCIONADA ---
    if content.startswith("SELECCION_CONVOCATORIA:"):
        c_id = content.split(":")[1].strip()
        conv = next((c for c in CONVOCATORIAS_DATA if c["id"] == c_id), None)
        
        if conv:
            cl.user_session.set("current_convocatoria", conv)

            # --- CORRECCIÓN PDF ---
            pdf_name = "Presentacion_Base" # Nombre sin espacios raros ayuda
            pdf_path = "files_examples/presentacion.pdf"
            
            if os.path.exists(pdf_path):
                pdf_element = cl.Pdf(
                    name=pdf_name, 
                    display="side", 
                    path=pdf_path
                )
                elements_list = [pdf_element]
                # IMPORTANTE: El nombre "Presentacion_Base" DEBE estar en el texto
                msg_text = f"✅ Has seleccionado: **{conv['titulo']}**.\n\n📄 He cargado el documento: **{pdf_name}** (Revisa el panel lateral 👉)."
            else:
                elements_list = []
                msg_text = f"✅ Has seleccionado: **{conv['titulo']}**.\n\n⚠️ **Alerta:** No encontré el archivo '{pdf_path}'."

            await cl.Message(
                content=msg_text,
                elements=elements_list
            ).send()

            actions = [
                cl.Action(name="apply_yes", value="yes", payload={"value": "yes"}, label="🚀 Sí, quiero aplicar"),
                cl.Action(name="apply_no", value="no", payload={"value": "no"}, label="❌ No, ver otra")
            ]
            await cl.Message(content="¿Procedemos a generar ideas?", actions=actions).send()
        else:
             await cl.ErrorMessage(content="No se encontró la convocatoria seleccionada.").send()

    # --- PASO 3: RESPUESTA DE SI APLICAR ---
    elif content.startswith("IDEA_SELECCIONADA:"):
        json_str = content.replace("IDEA_SELECCIONADA: ", "")
        selected_idea = json.loads(json_str)
        cl.user_session.set("selected_idea", selected_idea)

        await cl.Message(content="Excelente elección. Ahora, por favor **refina los detalles** del proyecto antes de generar el documento final:").send()
        
        editor = cl.CustomElement(
            name="ProjectEditor",
            props={"project": selected_idea}
        )
        await cl.Message(content="", elements=[editor]).send()

    # --- PASO 4: PROYECTO FINALIZADO ---
    elif content.startswith("PROYECTO_FINALIZADO:"):
        json_str = content.replace("PROYECTO_FINALIZADO: ", "")
        final_project = json.loads(json_str)

        msg = cl.Message(content="⏳ Procesando proyecto y generando documento final...")
        await msg.send()

        inputs = {"selected_project": final_project}
        
        async for output in dummy_graph.astream(inputs):
            for key, value in output.items():
                await msg.stream_token(f"\n- Fase completada: {key}...")
        
        await msg.update()

        # PDF Final
        final_pdf_name = "Documento_Final"
        final_pdf_path = "files_examples/documento_final.pdf"
        
        if os.path.exists(final_pdf_path):
            final_pdf = cl.Pdf(
                name=final_pdf_name,
                display="side",
                path=final_pdf_path
            )
            final_elements = [final_pdf]
            final_text = f"🎉 **¡Felicidades!** El documento para **{final_project['title']}** ha sido generado.\n\nPuedes ver el **{final_pdf_name}** en el panel lateral."
        else:
            final_elements = []
            final_text = f"🎉 **¡Felicidades!** Proyecto completado (PDF no encontrado)."

        await cl.Message(
            content=final_text,
            elements=final_elements
        ).send()

@cl.action_callback("apply_yes")
async def on_apply(action):
    await action.remove() 
    
    conv = cl.user_session.get("current_convocatoria")
    msg = cl.Message(content="🤖 **IA Thinking:** Analizando convocatoria y generando 5 ideas SMART...")
    await msg.send()

    if conv:
        inputs = {"convocatoria_titulo": conv["titulo"]}
        result = await dummy_graph.ainvoke(inputs) 
        ideas = result["project_ideas"] 

        msg.content = "He generado las siguientes propuestas. Por favor selecciona una:"
        await msg.update() 

        selector_ideas = cl.CustomElement(
            name="IdeaSelector",
            props={"ideas": ideas}
        )
        await cl.Message(content="", elements=[selector_ideas]).send()
    else:
        msg.content = "Hubo un error recuperando la convocatoria de la sesión."
        await msg.update()

@cl.action_callback("apply_no")
async def on_cancel(action):
    await action.remove()
    await cl.Message(content="Entendido. Puedes seleccionar otra convocatoria arriba.").send()