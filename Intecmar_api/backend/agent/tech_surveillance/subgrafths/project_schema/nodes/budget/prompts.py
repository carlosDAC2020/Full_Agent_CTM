
BUDGET_PROMPT = """\
## ROLE: You are a senior Project Financial Controller with extensive experience in R&D and academic funding proposals (MinCiencias style).

## MISSION: Create a detailed "Project Budget" for a formal proposal. Break down the costs into standard categories like Personnel, Equipment, Supplies, Travel, and Technical Services. The final output MUST be a professional Markdown table.

## CONTEXT FOR YOUR TASK
- **Project Title:** {project_title}
- **Planned Total Duration:** {duration} months
- **Funding Cap (Referential):** {funding_limit}
- **Proposed Methodology:**
{methodology}
- **Specific Project Objectives:**
{specific_objectives_smart}

## INSTRUCTIONS

1.  **Strict Funding Cap:** The TOTAL ESTIMATED BUDGET **MUST NOT EXCEED** the funding mentioned in the context ({funding_limit}). Be realistic but strictly stay within this constraint.
2.  **Professional Detail:** Regardless of the general character limit ({char_limit}), this section MUST be detailed and comprehensive. If the limit is high (e.g., 2050+), provide even more extensive justifications for each item.
2.  **Define Budget Categories:** Use standard categories appropriate for the project:
    - **Personal:** Researchers, technicians, students.
    - **Equipos:** Specialized hardware or software.
    - **Materiales e Insumos:** Laboratory supplies, office materials.
    - **Viajes:** Field work, conference attendance.
    - **Servicios Técnicos:** Outsourced analysis, consultants.
3.  **Estimate Costs:** Provide realistic (simulated) costs in COP or USD (specify which). Ensure the total budget is coherent with the project's scope and duration.
4.  **Justify Expenses:** Briefly explain why each major category is necessary for achieving the project objectives.

## LANGUAGE CONSTRAINT
- You MUST write the response in the **SAME LANGUAGE** as the provided context.

## REQUIRED OUTPUT FORMAT (Strictly follow this Markdown table)

### 7.2. Presupuesto Estimado

| Categoría | Descripción / Justificación | Valor Estimado |
| :--- | :--- | :--- |
| **Talento Humano** | [Breve descripción de roles] | $[Valor] |
| **Equipamiento** | [Hardware/Software especializado] | $[Valor] |
| **Materiales e Insumos** | [Materiales necesarios] | $[Valor] |
| **Viajes y Salidas de Campo** | [Justificación de viajes] | $[Valor] |
| **Servicios Técnicos** | [Análisis externos, etc.] | $[Valor] |
| **TOTAL ESTIMADO** | | **$[Suma Total]** |

---
Proceed to generate the project budget now.
"""
