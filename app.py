import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import uuid

# ============================================================
# ENCUESTA DE SATISFACCIÓN - BILLAR
# ============================================================

st.set_page_config(
    page_title="Encuesta del Billar",
    page_icon="🎱",
    layout="centered"
)

ARCHIVO = Path("encuestas.csv")

ASPECTOS = [
    "Atención",
    "Limpieza",
    "Mesas y equipo",
    "Ambiente",
    "Precios"
]

# Se agrega un ID para identificar cada envío
COLUMNAS = ["ID", "Fecha y hora"] + ASPECTOS + ["Opinión"]


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>
    .titulo {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitulo {
        text-align: center;
        color: #777;
        margin-bottom: 25px;
    }

    .confirmacion {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        background-color: rgba(0, 180, 80, 0.12);
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES
# ============================================================

def crear_archivo():
    """Crea el CSV si no existe."""
    if not ARCHIVO.exists():
        pd.DataFrame(columns=COLUMNAS).to_csv(
            ARCHIVO,
            index=False,
            encoding="utf-8-sig"
        )


def cargar_datos():
    """Lee las encuestas guardadas."""
    crear_archivo()

    try:
        df = pd.read_csv(
            ARCHIVO,
            encoding="utf-8-sig"
        )

        # Compatibilidad con un CSV anterior que no tenía ID
        if "ID" not in df.columns:
            df.insert(0, "ID", [
                str(uuid.uuid4()) for _ in range(len(df))
            ])
            df.to_csv(
                ARCHIVO,
                index=False,
                encoding="utf-8-sig"
            )

        return df

    except (pd.errors.EmptyDataError, FileNotFoundError):
        return pd.DataFrame(columns=COLUMNAS)


def guardar_encuesta(calificaciones, opinion, envio_id):
    """Guarda una encuesta solamente una vez."""
    df = cargar_datos()

    # Protección contra un envío duplicado
    if not df.empty and "ID" in df.columns:
        if envio_id in df["ID"].astype(str).values:
            return False

    datos = {
        "ID": envio_id,
        "Fecha y hora": datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        ),
        **calificaciones,
        "Opinión": opinion.strip()
    }

    nueva = pd.DataFrame([datos])

    df = pd.concat(
        [df, nueva],
        ignore_index=True
    )

    df.to_csv(
        ARCHIVO,
        index=False,
        encoding="utf-8-sig"
    )

    return True


def estrellas(valor):
    """Convierte un número en estrellas."""
    if valor is None:
        return "Selecciona una calificación"

    valor = int(round(valor))

    return "⭐" * valor + "☆" * (5 - valor)


def generar_opinion_general(promedios):
    """Genera una opinión general automática."""
    promedio_general = promedios.mean()

    mejor = promedios.idxmax()
    peor = promedios.idxmin()

    if promedio_general >= 4.5:
        nivel = "excelente"
    elif promedio_general >= 4:
        nivel = "muy positiva"
    elif promedio_general >= 3:
        nivel = "regular"
    else:
        nivel = "baja"

    return (
        f"La opinión general de los clientes es {nivel}, "
        f"con un promedio de {promedio_general:.2f} estrellas. "
        f"El aspecto mejor evaluado es {mejor}, con "
        f"{promedios[mejor]:.2f} estrellas. "
        f"El aspecto con menor calificación es {peor}, con "
        f"{promedios[peor]:.2f} estrellas, por lo que "
        f"representa el principal punto de oportunidad para mejorar."
    )


def limpiar_encuesta():
    """Prepara la aplicación para una nueva encuesta."""
    for aspecto in ASPECTOS:
        st.session_state.pop(f"cal_{aspecto}", None)

    st.session_state.pop("opinion", None)
    st.session_state.submitted = False
    st.session_state.envio_id = str(uuid.uuid4())


# ============================================================
# INICIALIZACIÓN
# ============================================================

crear_archivo()

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "envio_id" not in st.session_state:
    st.session_state.envio_id = str(uuid.uuid4())


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<p class="titulo">🎱 Mi Billar</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitulo">'
    'Encuesta de satisfacción de clientes'
    '</p>',
    unsafe_allow_html=True
)


# ============================================================
# PESTAÑAS
# ============================================================

tab_encuesta, tab_resultados = st.tabs(
    ["📝 Encuesta", "📊 Resultados"]
)


# ============================================================
# ENCUESTA
# ============================================================

with tab_encuesta:

    # --------------------------------------------------------
    # SI YA FUE ENVIADA
    # --------------------------------------------------------

    if st.session_state.submitted:

        st.markdown(
            """
            <div class="confirmacion">
                <h2>✅ ¡Encuesta enviada!</h2>
                <p>
                    Tu evaluación ya fue registrada correctamente.
                </p>
                <p>
                    <strong>
                    No necesitas volver a presionar ningún botón.
                    </strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "Si otra persona quiere contestar la encuesta "
            "desde este mismo dispositivo, presiona "
            "«Nueva encuesta»."
        )

        if st.button(
            "📝 Nueva encuesta",
            use_container_width=True
        ):
            limpiar_encuesta()
            st.rerun()

    # --------------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------------

    else:

        st.subheader("Califica tu experiencia")

        st.write(
            "Selecciona de 1 a 5 estrellas en cada aspecto."
        )

        with st.form("formulario_encuesta"):

            calificaciones = {}

            for aspecto in ASPECTOS:

                calificaciones[aspecto] = st.radio(
                    f"**{aspecto}**",
                    options=[1, 2, 3, 4, 5],
                    index=None,
                    horizontal=True,
                    format_func=estrellas,
                    key=f"cal_{aspecto}"
                )

            st.markdown("### 💬 Tu opinión")

            opinion = st.text_area(
                "¿Qué te pareció el billar?",
                placeholder=(
                    "Escribe aquí algún comentario, "
                    "sugerencia o experiencia..."
                ),
                max_chars=500,
                key="opinion"
            )

            enviar = st.form_submit_button(
                "⭐ ENVIAR EVALUACIÓN",
                use_container_width=True
            )

        # ----------------------------------------------------
        # VALIDACIÓN
        # ----------------------------------------------------

        if enviar:

            faltantes = [
                aspecto
                for aspecto, calificacion
                in calificaciones.items()
                if calificacion is None
            ]

            if faltantes:

                st.error(
                    "Por favor, califica todos los aspectos "
                    "antes de enviar la encuesta."
                )

                st.write(
                    "Falta calificar: "
                    + ", ".join(faltantes)
                )

            else:

                # El mismo ID se utiliza durante esta encuesta.
                # Si se intenta repetir el envío, la función
                # detectará que ese ID ya existe.
                guardada = guardar_encuesta(
                    calificaciones,
                    opinion,
                    st.session_state.envio_id
                )

                if guardada:

                    st.session_state.submitted = True

                    st.rerun()

                else:

                    st.session_state.submitted = True

                    st.rerun()


# ============================================================
# RESULTADOS
# ============================================================

with tab_resultados:

    df = cargar_datos()

    if df.empty:

        st.info(
            "Todavía no hay evaluaciones. "
            "Cuando los clientes respondan la encuesta, "
            "aquí aparecerán los resultados."
        )

    else:

        for aspecto in ASPECTOS:

            df[aspecto] = pd.to_numeric(
                df[aspecto],
                errors="coerce"
            )

        promedios = df[ASPECTOS].mean()
        promedio_general = promedios.mean()
        cantidad = len(df)

        # ----------------------------------------------------
        # INDICADORES
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Encuestas",
                cantidad
            )

        with col2:
            st.metric(
                "Promedio general",
                f"{promedio_general:.2f} ⭐"
            )

        with col3:
            st.metric(
                "Mejor aspecto",
                promedios.idxmax()
            )

        # ----------------------------------------------------
        # TABLA
        # ----------------------------------------------------

        st.divider()

        st.subheader("⭐ Promedio por aspecto")

        tabla = pd.DataFrame({
            "Aspecto": ASPECTOS,
            "Promedio": [
                round(promedios[aspecto], 2)
                for aspecto in ASPECTOS
            ],
            "Calificación": [
                estrellas(promedios[aspecto])
                for aspecto in ASPECTOS
            ]
        })

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )

        # ----------------------------------------------------
        # GRÁFICA
        # ----------------------------------------------------

        st.subheader("📊 Gráfica de calificaciones")

        grafica = pd.DataFrame({
            "Promedio": promedios
        })

        st.bar_chart(
            grafica,
            y="Promedio",
            horizontal=True,
            x_label="Estrellas",
            y_label="Aspecto"
        )

        # ----------------------------------------------------
        # OPINIÓN GENERAL
        # ----------------------------------------------------

        st.subheader("🧠 Opinión general")

        st.info(
            generar_opinion_general(promedios)
        )

        # ----------------------------------------------------
        # OPINIONES
        # ----------------------------------------------------

        st.subheader("💬 Opiniones de los clientes")

        opiniones = (
            df["Opinión"]
            .fillna("")
            .astype(str)
        )

        opiniones = opiniones[
            opiniones.str.strip() != ""
        ]

        if opiniones.empty:

            st.write(
                "Todavía no hay opiniones escritas."
            )

        else:

            for numero, comentario in enumerate(
                opiniones,
                1
            ):

                st.markdown(
                    f"**Cliente {numero}:** {comentario}"
                )

        # ----------------------------------------------------
        # DESCARGAR
        # ----------------------------------------------------

        st.divider()

        st.subheader("📥 Exportar resultados")

        csv = df.to_csv(
            index=False,
            encoding="utf-8-sig"
        )

        st.download_button(
            label="Descargar encuestas en CSV",
            data=csv,
            file_name="encuestas_billar.csv",
            mime="text/csv",
            use_container_width=True
        )

        # ----------------------------------------------------
        # ADMINISTRACIÓN
        # ----------------------------------------------------

        with st.expander("⚙️ Administración"):

            st.warning(
                "Esta sección es para el responsable del proyecto. "
                "Borrar los datos es una acción permanente."
            )

            if st.button(
                "🗑️ Borrar todas las encuestas"
            ):

                pd.DataFrame(
                    columns=COLUMNAS
                ).to_csv(
                    ARCHIVO,
                    index=False,
                    encoding="utf-8-sig"
                )

                st.success(
                    "Todas las encuestas fueron eliminadas."
                )

                st.rerun()
