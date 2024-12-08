# app.py
import streamlit as st
import anthropic
from datetime import datetime
import json
import os
from typing import Dict, List
import yaml

class PairyApp:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        self.load_topics()
        self.load_difficulty_levels()
        
    def load_topics(self):
        """Carga los temas de entrevista desde el archivo YAML"""
        with open('topics.yaml', 'r') as f:
            self.topics = yaml.safe_load(f)
    
    def load_difficulty_levels(self):
        """Define los niveles de dificultad disponibles"""
        self.difficulty_levels = {
            "Junior": "L3-L4",
            "Mid-Level": "L4-L5",
            "Senior": "L5-L6",
            "Staff": "L6+"
        }
    
    def generate_interview_prompt(self, topic: str, difficulty: str) -> str:
        """Genera el prompt para Claude basado en el tema y dificultad seleccionados"""
        return f"""Eres un entrevistador técnico experimentado de una empresa FAANG. 
        Realizarás una entrevista técnica sobre {topic} a nivel {difficulty}.
        
        Sigue estas reglas:
        1. Mantén un tono profesional pero amigable
        2. Haz preguntas progresivamente más difíciles
        3. Proporciona retroalimentación constructiva
        4. Simula una entrevista real con preguntas de seguimiento
        5. Al final, proporciona una evaluación detallada
        
        Comienza la entrevista presentándote y haciendo la primera pregunta técnica."""

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
            response = st.session_state.app.start_interview(selected_topic, selected_difficulty)
            st.session_state.conversation.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()
    
    # Área principal
    chat_container = st.container()
    
    # Mostrar la conversación
    with chat_container:
        for message in st.session_state.conversation:
            if message["role"] == "assistant":
                st.markdown(f"🤖 **Entrevistador:**\n{message['content']}")
            else:
                st.markdown(f"👤 **Tú:**\n{message['content']}")
    
    # Input del usuario con key única
    user_input = st.text_area(
        "Tu respuesta:",
        key=f"input_{st.session_state.message_counter}",
        value=st.session_state.current_input
    )
    
    # Botón de enviar
    if st.button("Enviar", key=f"send_{st.session_state.message_counter}"):
        if user_input.strip():  # Verificar que el input no esté vacío
            # Agregar respuesta del usuario
            st.session_state.conversation.append({
                "role": "user",
                "content": user_input
            })
            
            # Obtener respuesta del asistente
            response = st.session_state.app.continue_interview(
                st.session_state.conversation,
                user_input
            )
            
            # Agregar respuesta del asistente
            st.session_state.conversation.append({
                "role": "assistant",
                "content": response
            })
            
            # Incrementar el contador y limpiar el input actual
            st.session_state.message_counter += 1
            st.session_state.current_input = ""
            st.rerun()

if __name__ == "__main__":
    main()