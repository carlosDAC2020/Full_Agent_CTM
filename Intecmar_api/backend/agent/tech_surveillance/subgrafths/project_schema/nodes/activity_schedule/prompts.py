

ACTIVITY_SCHEDULE_PROMPT = """\
## ROLE: You are a senior Project Manager with extensive experience planning complex R&D projects.

## MISSION: Create a detailed "Activity Schedule" for a formal project proposal. Your task is to break down the project's methodological phases into specific activities, key milestones, and their primary deliverables. 

## CONTEXT FOR YOUR TASK
- **Project Title:** {project_title}
- **Planned Total Project Duration (MANDATORY):** {duration}
- **Proposed Methodology (High-Level Phases):**
{methodology}
- **Specific Project Objectives (which this schedule must achieve):**
{specific_objectives_smart}

## CRITICAL LANGUAGE AND ETHICS
- **Language:** STRICTLY use Spanish.
- **Character Set:** Use ONLY Latin script (standard Spanish alphabet). Do NOT use Devanagari, Greek, or any other non-Latin characters, even for technical terms.
- **Professionalism:** Ensure a formal, technical tone suitable for a Cotecmar proposal.

## CRITICAL INSTRUCTIONS FOR DURATION AND CONCURRENCY

1.  **Time Conversion:** Assume 1 Month = 4 Weeks. (e.g., a 12-month project is exactly 48 weeks).
2.  **Total Duration Alignment:** The sum of durations of **sequential** phases MUST match the "Planned Total Project Duration" exactly. 
3.  **Handling Concurrency (Overlapping Phases):** Some phases may occur simultaneously (concurrently). You MUST clearly indicate this using the tag **[CONCURRENTE]** at the beginning of the phase description if it runs alongside another.
4.  **Mathematical Validation:** Before outputting, mentally calculate: (Sum of Sequential Phases) = Total Duration. Sequential phases are those that depend on the completion of the previous one. Overlapping phases should not add to the critical path duration if they run in parallel.

You MUST use a structured list format with headings for phases. Do NOT use markdown tables.
You MUST leave TWO NEWLINES between each Phase or logical Section to ensure correct rendering in the PDF.

### 7.1. Cronograma de Actividades

### Fase 1: [Nombre de la Fase] (Semanas 1-[X])
*Resumen breve de los objetivos de esta fase y su importancia estratégica.*
- **Actividad 1.1:** [Nombre] ([X] semanas).
  - **Entregable:** [Nombre]
- **Actividad 1.2:** [Nombre] ([X] semanas).
  - **Entregable:** [Nombre]
- **Hito Clave:** [Descripción del hito al terminar la fase]

### Fase 2: [Nombre de la Fase] (Semanas [X]-[Y])
**[CONCURRENTE con Fase Z]** (Solo si aplica)
*Resumen breve de la fase.*
- **Actividad 2.1:** [Nombre] ([X] semanas).
  - **Entregable:** [Nombre]
- ...

---
Proceed to generate the activity schedule now.
"""