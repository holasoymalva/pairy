# app.py
import streamlit as st
import anthropic
from datetime import datetime
import json
import os
from typing import Dict, List, Optional
import yaml

class PairyApp:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        self.load_topics()
        self.load_difficulty_levels()
        self.load_coding_problems()
        
    def load_topics(self):
        """Carga los temas de entrevista desde el archivo YAML"""
        with open('topics.yaml', 'r') as f:
            self.topics = yaml.safe_load(f)
    
    def load_coding_problems(self):
        """Carga los problemas de programación"""
        with open('coding_problems.yaml', 'r') as f:
            self.coding_problems = yaml.safe_load(f)
    
    def load_difficulty_levels(self):
        """Define los niveles de dificultad disponibles"""
        self.difficulty_levels = {
            "Junior": "L3-L4",
            "Mid-Level": "L4-L5",
            "Senior": "L5-L6",
            "Staff": "L6+"
        }
    
    def get_random_problem(self, topic: str, difficulty: str) -> Optional[Dict]:
        """Obtiene un problema aleatorio basado en el tema y dificultad"""
        import random
        
        if topic in self.coding_problems:
            category = self.coding_problems[topic]
            if isinstance(category, dict) and difficulty.lower() in category:
                problems = category[difficulty.lower()]
                return random.choice(problems) if problems else None
        return None
    
    def generate_interview_prompt(self, topic: str, difficulty: str) -> str:
        """Genera el prompt para Claude basado en el tema y dificultad seleccionados"""
        problem = self.get_random_problem(topic, difficulty)
        
        base_prompt = f"""Eres un entrevistador técnico experimentado de una empresa FAANG 
        realizando una entrevista técnica sobre {topic} a nivel {difficulty}.
        
        Directrices para la entrevista:
        1. Mantén un tono profesional pero amigable
        2. Haz preguntas progresivamente más difíciles
        3. Proporciona retroalimentación constructiva
        4. Evalúa los siguientes aspectos:
           - Comprensión del problema
           - Calidad del código y diseño
           - Complejidad temporal y espacial
           - Manejo de casos edge
           - Claridad en la comunicación
        5. Pide al candidato que:
           - Explique su enfoque antes de codificar
           - Escriba código real (no pseudocódigo)
           - Analice la complejidad de su solución
           - Considere optimizaciones
        6. Proporciona hints si el candidato se estanca
        7. Al final, da una evaluación detallada
        
        Guía de evaluación:
        - Excelente: Solución óptima, código limpio, análisis completo
        - Bueno: Solución correcta, algunas optimizaciones posibles
        - Regular: Solución funcional pero con áreas de mejora
        - Necesita mejorar: Solución incompleta o con errores significativos
        """
        
        if problem:
            base_prompt += f"""
            
            Comienza con este problema:
            Nombre: {problem['name']}
            Descripción: {problem['description']}
            Ejemplo de entrada: {problem['example_input']}
            Ejemplo de salida: {problem['example_output']}
            """
        
        base_prompt += """
        
        Comienza la entrevista presentándote y explicando el primer problema técnico."""
        
        return base_prompt

    def evaluate_code(self, code: str, topic: str) -> str:
        """Evalúa el código proporcionado por el candidato"""
        evaluation_prompt = f"""Analiza el siguiente código de manera detallada considerando:

        1. Corrección:
           - ¿Resuelve el problema completamente?
           - ¿Maneja casos edge?

        2. Eficiencia:
           - Complejidad temporal
           - Complejidad espacial
           - Posibles optimizaciones

        3. Calidad del código:
           - Legibilidad
           - Estructura y organización
           - Convenciones de estilo
           - Manejo de errores

        Código a evaluar:
        ```
        {code}
        ```

        Proporciona una evaluación estructurada con ejemplos específicos y sugerencias de mejora.
        """

        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": evaluation_prompt
            }]
        )
        
        return response.content[0].text

    def start_interview(self, topic: str, difficulty: str):
        """Inicia una nueva sesión de entrevista"""
        prompt = self.generate_interview_prompt(topic, difficulty)
        
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text

    def continue_interview(self, conversation_history: List[Dict], user_input: str):
        """Continúa la conversación de la entrevista"""
        messages = [{"role": msg["role"], "content": msg["content"]} 
                   for msg in conversation_history]
        messages.append({"role": "user", "content": user_input})
        
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.7,
            messages=messages
        )
        
        return response.content[0].text

def initialize_session_state():
    """Inicializa todas las variables del estado de la sesión"""
    if 'app' not in st.session_state:
        st.session_state.app = PairyApp()
    
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    
    if 'current_input' not in st.session_state:
        st.session_state.current_input = ""
    
    if 'message_counter' not in st.session_state:
        st.session_state.message_counter = 0
    
    if 'code_editor_key' not in st.session_state:
        st.session_state.code_editor_key = 0

def main():
    st.set_page_config(page_title="Pairy - Technical Interview Practice", layout="wide")
    
    # Inicializar el estado de la sesión al principio
    initialize_session_state()
    
    st.title("🤝 Pairy - Práctica de Entrevistas Técnicas")
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("Configuración de la Entrevista")
        
        selected_topic = st.selectbox(
            "Selecciona un tema",
            options=list(st.session_state.app.topics.keys())
        )
        
        selected_difficulty = st.selectbox(
            "Selecciona el nivel",
            options=list(st.session_state.app.difficulty_levels.keys())
        )
        
        if st.button("Iniciar Nueva Entrevista"):
            st.session_state.conversation = []
            st.session_state.message_counter = 0
            st.session_state.code_editor_key += 1
            response = st.session_state.app.start_interview(selected_topic, selected_difficulty)
            st.session_state.conversation.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()
    
    # Área principal - Dividida en dos columnas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat container
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.conversation:
                if message["role"] == "assistant":
                    st.markdown(f"🤖 **Entrevistador:**\n{message['content']}")
                else:
                    st.markdown(f"👤 **Tú:**\n{message['content']}")
        
        # Input del usuario
        user_input = st.text_area(
            "Tu explicación/respuesta:",
            key=f"input_{st.session_state.message_counter}",
            value=st.session_state.current_input,
            height=100
        )
    
    with col2:
        # Editor de código
        st.subheader("Editor de Código")
        code_input = st.text_area(
            "Escribe tu código aquí:",
            height=300,
            key=f"code_editor_{st.session_state.code_editor_key}"
        )
        
        # Botones de acción
        col_explain, col_submit = st.columns(2)
        
        with col_explain:
            if st.button("Explicar Enfoque", key=f"explain_{st.session_state.message_counter}"):
                if user_input.strip():
                    st.session_state.conversation.append({
                        "role": "user",
                        "content": f"Mi enfoque para resolver este problema es:\n{user_input}"
                    })
                    response = st.session_state.app.continue_interview(
                        st.session_state.conversation,
                        user_input
                    )
                    st.session_state.conversation.append({
                        "role": "assistant",
                        "content": response
                    })
                    st.session_state.message_counter += 1
                    st.session_state.current_input = ""
                    st.rerun()
        
        with col_submit:
            if st.button("Enviar Código", key=f"submit_{st.session_state.message_counter}"):
                if code_input.strip():
                    evaluation = st.session_state.app.evaluate_code(code_input, selected_topic)
                    st.session_state.conversation.append({
                        "role": "user",
                        "content": f"Mi implementación:\n```\n{code_input}\n```"
                    })
                    st.session_state.conversation.append({
                        "role": "assistant",
                        "content": f"Evaluación del código:\n{evaluation}"
                    })
                    st.session_state.message_counter += 1
                    st.session_state.code_editor_key += 1
                    st.rerun()

if __name__ == "__main__":
    main()