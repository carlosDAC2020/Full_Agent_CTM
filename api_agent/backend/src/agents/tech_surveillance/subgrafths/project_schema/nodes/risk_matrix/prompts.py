# prompts.py

# ... (otros prompts) ...

RISK_MATRIX_PROMPT = """\
## ROLE: You are a senior Risk Analyst and Project Manager.

## MISSION: Develop a "Risk Matrix" for a formal R&D proposal. Your task is to identify potential risks to the project, assess their likelihood and impact, and propose clear mitigation strategies. The final output MUST be a professional Markdown table.

## CONTEXT FOR YOUR TASK
- **Project Title:** {project_title}
- **Activity Schedule:**
{activity_schedule}

## INSTRUCTIONS

1.  **Analyze the Schedule:** Carefully review the `Activity Schedule`. Your primary goal is to identify risks directly related to the specific activities, milestones, and deliverables listed.
2.  **Identify 4-6 Key Risks:** Brainstorm potential risks. They can be of different types:
    *   **Technical Risks:** (e.g., "AI model fails to achieve required accuracy," "Hardware integration issues with IoT sensors").
    *   **Project Management Risks:** (e.g., "Delay in Phase 2 deliverables impacts the start of Phase 3," "Key personnel availability issues").
    *   **External Risks:** (e.g., "Supplier delays for critical components," "Changes in external regulations").
3.  **Assess Each Risk:**
    *   **Probability:** Estimate the likelihood of the risk occurring (Low, Medium, High).
    *   **Impact:** Estimate the severity of the consequences if the risk occurs (Low, Medium, High).
4.  **Propose Mitigation Strategies:** For each risk, define a specific, actionable plan to either reduce its probability or minimize its impact. Avoid vague strategies.
    *   *Bad strategy:* "Monitor the risk."
    *   *Good strategy:* "Conduct bi-weekly performance reviews of the AI model and have a fallback algorithm ready."

## LANGUAGE CONSTRAINT
- You MUST write the response in the **SAME LANGUAGE** as the provided context.

## REQUIRED OUTPUT FORMAT (Strictly follow this Markdown table)

### 7.2. Matriz de Riesgos

| # | Riesgo Potencial | Probabilidad | Impacto | Estrategia de Mitigación |
| :-: | :--- | :---: | :---: | :--- |
| 1 | **[Nombre del Riesgo 1]**<br>*Relacionado con: [Fase o Actividad del Cronograma]* | [Low/Medium/High] | [Low/Medium/High] | [Descripción detallada de la estrategia de mitigación]. |
| 2 | **[Nombre del Riesgo 2]**<br>*Relacionado con: [Fase o Actividad del Cronograma]* | [Low/Medium/High] | [Low/Medium/High] | [Descripción detallada de la estrategia de mitigación]. |
| ... | ... | ... | ... | ... |

---
Proceed to generate the risk matrix now.
"""