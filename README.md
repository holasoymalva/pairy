# Pairy 🤝 - Tu Compañero de Práctica para Entrevistas Técnicas

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit Version](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success)

## 🎯 Descripción

Pairy es una aplicación interactiva diseñada para ayudarte a prepararte para entrevistas técnicas en empresas FAANG y similares. Utilizando la API de Anthropic (Claude), simula un entrevistador técnico que te ayuda a practicar problemas de programación, diseño de sistemas y otros temas técnicos relevantes.

## ✨ Características Principales

- 🤖 **Entrevistador IA Avanzado**: Powered by Anthropic's Claude
- 💻 **Editor de Código Integrado**: Escribe y prueba tu código en tiempo real
- 📊 **Múltiples Niveles de Dificultad**:
  - Junior (L3-L4)
  - Mid-Level (L4-L5)
  - Senior (L5-L6)
  - Staff (L6+)
- 📚 **Temas Diversos**:
  - Estructuras de Datos
  - Algoritmos
  - Diseño de Sistemas
  - Programación Orientada a Objetos
  - ... y más
- 🔄 **Feedback en Tiempo Real**
- 📝 **Evaluación de Código Detallada**

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Una clave API de Anthropic

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/pairy.git
cd pairy
```

2. **Crear y activar un entorno virtual**
```bash
# En Unix/macOS:
python -m venv env
source env/bin/activate

# En Windows:
python -m venv env
env\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tu editor preferido y agregar tu API key
nano .env
```

5. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

## 💡 Uso

1. **Iniciar la Aplicación**
   - Selecciona un tema técnico
   - Elige tu nivel de experiencia
   - Haz clic en "Iniciar Nueva Entrevista"

2. **Durante la Entrevista**
   - Escucha/lee las preguntas del entrevistador
   - Usa el editor de código para implementar soluciones
   - Explica tu enfoque antes de codificar
   - Recibe feedback detallado

3. **Evaluación de Código**
   - Análisis de complejidad temporal y espacial
   - Sugerencias de optimización
   - Feedback sobre estilo y buenas prácticas

## 🏗️ Estructura del Proyecto

```
pairy/
├── app.py                 # Aplicación principal
├── coding_problems.yaml   # Base de datos de problemas
├── topics.yaml           # Configuración de temas
├── requirements.txt      # Dependencias
├── .env.example         # Plantilla de variables de entorno
├── .gitignore          # Configuración de git
└── README.md           # Este archivo
```

## 📝 Configuración

### Variables de Entorno

```env
ANTHROPIC_API_KEY=your_api_key_here
APP_ENV=development
DEBUG=True
```

### Configuración de Streamlit

```toml
[server]
port = 8501
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- [Anthropic](https://www.anthropic.com/) - Por proporcionar la API de Claude
- [Streamlit](https://streamlit.io/) - Por el framework de la interfaz
- La comunidad de código abierto

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:
1. Revisa los [issues existentes](https://github.com/tu-usuario/pairy/issues)
2. Abre un nuevo issue con detalles del problema/sugerencia

## 🛣️ Roadmap

- [ ] Soporte para más lenguajes de programación
- [ ] Sistema de seguimiento de progreso
- [ ] Base de datos expandida de problemas
- [ ] Módulo de práctica de System Design
- [ ] Integración con IDEs populares

---

Desarrollado con ❤️ para la comunidad de desarrolladores