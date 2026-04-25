import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
from datos_educativos import INFO_INSTITUCIONAL
from datos_colegio import generar_contexto_completo
from psicopedagogia import INFO_PSICOPEDAGOGIA

load_dotenv()

# Configuración de página
st.set_page_config(
    page_title="Lumi - Asistente Escolar",
    page_icon="🎓",
    layout="wide"
)

# Estilos básicos
st.markdown("""
<style>
.main { background-color: #f0f4f8; }
.stChatMessage { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Título
st.title("🎓 Lumi - Asistente Virtual Escolar")
st.caption("Cundinamarca y Boyacá · Transformación Digital Educativa")

# Sidebar con estadísticas básicas
with st.sidebar:
    st.header("📊 Panel de Uso")
    if "contador" not in st.session_state:
        st.session_state.contador = {}
    
    st.metric("Consultas hoy", len(st.session_state.get("messages", [])))
    
    st.divider()
    st.subheader("🔖 Temas frecuentes")
    temas = ["📅 Calendario", "📋 Matrículas", "📄 Certificados", 
             "🚌 Rutas", "📚 Recursos"]
    for t in temas:
        if st.button(t, use_container_width=True):
            st.session_state.pregunta_rapida = t

    st.divider()
    st.error("🆘 ¿Estás en peligro?")
    st.markdown("""
**Llama ahora:**
- 🚨 Emergencias: **123**
- 💙 Salud mental: **106**
- 👶 ICBF: **018000 918080**
- ⚖️ Fiscalía: **122**
""")

    st.caption("🔒 Tus datos están protegidos según la Ley 1581 de 2012")
    

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": """👋 Bienvenido/a a **Lumi**, asistente virtual oficial de tu institución educativa.

---

🔒 **Aviso de Privacidad y Protección de Datos**

Antes de continuar, te informamos que:

- 📋 Los datos que compartas en esta conversación son **confidenciales** y están protegidos por la **Ley 1581 de 2012** (Protección de Datos Personales de Colombia).
- 🔐 La información es usada **únicamente** para orientarte y gestionar tus solicitudes escolares.
- 🚫 Tus datos **no serán compartidos** con terceros sin tu consentimiento.
- 👤 Tienes derecho a **conocer, actualizar y rectificar** tus datos en cualquier momento dirigiéndote a la secretaría del colegio.
- 📵 Te recomendamos **no compartir contraseñas ni información sensible** en este chat.

Al continuar usando Lumi, aceptas estas condiciones. ✅

---

¿En qué te puedo ayudar hoy? Puedo orientarte sobre:
- 📅 Horarios y calendario académico
- 📊 Notas y asistencias
- 📄 Trámites y certificados
- 🚨 Situaciones de riesgo o convivencia
- 📚 Recursos de aprendizaje"""
    })

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input del usuario
prompt = st.chat_input("Escribe tu pregunta aquí...")

# Manejar botones rápidos del sidebar
if "pregunta_rapida" in st.session_state:
    prompt = st.session_state.pregunta_rapida
    del st.session_state.pregunta_rapida

if prompt:
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar a Claude
    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            
            system_prompt = f"""Eres Lumi, asistente virtual oficial de instituciones
educativas de Cundinamarca y Boyaca, Colombia.

════════════════════════════════════
PERSONALIDAD
════════════════════════════════════
- Amable, paciente y claro
- Lenguaje sencillo para padres, estudiantes y docentes
- Siempre en español, emojis con moderacion

════════════════════════════════════
1. INFORMACION GENERAL
════════════════════════════════════
{INFO_INSTITUCIONAL}

════════════════════════════════════
2. DATOS DEL COLEGIO
════════════════════════════════════
{generar_contexto_completo()}

INSTRUCCIONES DE BUSQUEDA:
- Horarios → busca en HORARIOS DE CLASES
- Tareas → busca en TAREAS Y EVALUACIONES PENDIENTES
- Estudiantes → busca en ESTUDIANTES REGISTRADOS
- Profesores → busca en DIRECTORIO DE PROFESORES
- Asistencias → busca en REGISTRO DE ASISTENCIAS
- Si no encuentras algo: dilo claramente, NUNCA inventes datos
- Respuestas maximas 150 palabras con listas cuando aplique

════════════════════════════════════
3. TRAMITES - LINKS DIRECTOS
════════════════════════════════════
Si piden CERTIFICADO o CONSTANCIA:
"Para solicitar su constancia complete este formulario 📄
https://docs.google.com/forms/d/e/1FAIpQLSdcGlKKjuplMuxWdJw1GX5LnkSZAOQdL7caRS_i739gzv8_tQ/viewform
Listo en secretaria en 2 dias habiles. Tenga el codigo del estudiante a mano."

Si piden JUSTIFICAR INASISTENCIA o entregar excusa:
"Para reportar la inasistencia complete este formulario 📋
https://docs.google.com/forms/d/e/1FAIpQLSdE1hdc_9ZwRZac9ks89EoPYakUg1379w-qT8KmDf0dj2ElUA/viewform
Tiene 3 dias habiles para justificar. Lleve el documento fisico a secretaria."

REGLAS DE TRAMITES:
- Siempre incluye el link completo
- Siempre menciona el tiempo de respuesta
- Siempre pregunta si necesita algo mas

════════════════════════════════════
4. PROTECCION Y RUTAS DE ATENCION
════════════════════════════════════
{INFO_PSICOPEDAGOGIA}

CUANDO DETECTES: bullying, acoso, golpes, abuso, maltrato,
tocamientos, amenazas, ciberacoso, me pegan, me hacen daño,
me molestan, tengo miedo, me amenazan, violencia:

PASO 1 - Empatia siempre primero:
"Gracias por contarme. Lo que describes es muy serio y
merece atencion inmediata. No estas solo/a."

PASO 2 - Si hay peligro inmediato da estos numeros primero:
- Emergencias: 123
- Salud mental: 106
- ICBF: 018000 918080

PASO 3 - Siempre da el formulario confidencial:
"Puedes hacer un reporte confidencial y seguro aqui:
https://docs.google.com/forms/d/e/1FAIpQLSd0BMHEamk40__cGwpTzXpytSRu4CHOhwb25E_AchtuP4GOIA/viewform
Tu reporte es completamente confidencial.
El colegio esta obligado por la Ley 1620 de 2013 a protegerte."

PASO 4 - Ruta segun el caso:
- Bullying entre estudiantes → Ruta interna Comite de Convivencia
- Abuso por adulto o abuso sexual → Ruta Violeta + ICBF inmediato
- Ciberacoso → Ruta interna + pide guardar capturas de pantalla

REGLAS CRITICAS:
- NUNCA minimices la situacion
- NUNCA pidas detalles innecesarios del abuso
- SIEMPRE menciona Ley 1620 de 2013 como respaldo legal
- Para abuso sexual SIEMPRE activa Ruta Violeta

════════════════════════════════════
5. PRIVACIDAD
════════════════════════════════════
Todos los datos estan protegidos por la Ley 1581 de 2012.
No solicites datos sensibles innecesarios en el chat.
"""

            response = client.messages.create(
                model="claude-haiku-4-5-20251001",  # Modelo más económico
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            
            respuesta = response.content[0].text
            st.markdown(respuesta)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": respuesta
            })