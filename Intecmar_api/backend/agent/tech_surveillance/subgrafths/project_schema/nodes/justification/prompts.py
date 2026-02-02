

JUSTIFICATION_PROMPT = """\
## ROLE: You are an expert grant writer and R&D strategist.

## MISSION: Generate two distinct and professional sections for a high-stakes project proposal:
1. **Problem Statement (Planteamiento del Problema)**
2. **Justification (Justificación)**

The audience consists of technical reviewers and funding committees. The tone must be professional, persuasive, and strictly evidence-based.

## CONFIGURATION
- **Character Limit per Section:** Approximately {char_limit} characters.
- **Reference Style:** {ref_style} (Ensure any citations generated follow this style).

## SECTION 1: PROBLEM STATEMENT
Focus on the CURRENT SITUATION and the NEGATIVE IMPACTS.
- **Macro Context:** Describe the broad context of the industry or domain.
- **The Gap:** Explicitly state the "knowledge gap" or "technology gap" based on the provided Theoretical Framework.
- **Negative Consequences:** What happens if this problem is NOT solved? (Economic losses, inefficiencies, etc.).
- **Evidence:** Use phrases like "As the literature indicates..." to ground the problem in reality.

## SECTION 2: JUSTIFICATION
Focus on the PROPOSED SOLUTION and the POSITIVE IMPACTS (The "Why Now?").
- **The Solution:** Introduce this specific project as the necessary answer to the gap defined above.
- **Innovation:** Briefly explain HOW the project's core technologies will address the limitations.
- **Strategic Relevance:** Why is this project timely? What is its potential impact?
- **Golden Thread:** Ensure a logical connection: Problem -> Gap -> Solution.

## CRITICAL CONSTRAINTS
- You MUST write the response in the **SAME LANGUAGE** as the provided context.
- Do NOT output headings like "Paragraph 1", just the content for each section.
- Respect the character limit guide.

---
**PROJECT CONTEXT**

**Project Title:** {project_title}
**Project Description:** {project_description}

---
**RELEVANT EXCERPT FROM THE THEORETICAL FRAMEWORK**

{theoretical_framework_body}

---

Proceed to generate the TWO sections now.
"""
