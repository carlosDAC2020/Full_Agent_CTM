template = """\
{%- if project_title -%}
You are a helpful conversational assistant currently working on a project titled "{{ project_title }}". 
Use this context to answer the user's questions and provide relevant assistance.
{%- else -%}
You are a helpful conversational assistant ready to help with various tasks and questions.
{%- endif %}

Your goal is to provide clear, accurate, and contextual responses based on the conversation history and the current request.

{% if message_history and message_history|length > 0 -%}
Previous conversation:
{% for msg in message_history -%}
{{ msg.type|upper }}: {{ msg.content }}
{% endfor %}
{%- endif %}

Current user message: {{ current_message }}

Please provide a helpful and contextual response."""