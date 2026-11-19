import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

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

COLUMNAS = ["Fecha y hora"] + ASPECTOS + ["Opinión"]


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
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES
# ============================================================

def crear_archivo():
    """Crea el archivo CSV si no existe."""
    
    if not ARCHIVO.exists():
        pd.DataFrame(
            columns=COLUMNAS
        ).to_csv(
            ARCHIVO,
            index=False,
            encoding="utf-8-sig"
        )


def cargar_datos():
    """Lee las encuestas guardadas."""
    
    crear_archivo()

    try:
        return pd.read_csv(
            ARCHIVO,
            encoding="utf-8-sig"
        )

    except (pd.errors.EmptyDataError, FileNotFoundError):
        return pd.DataFrame(columns=COLUMNAS)


def guardar_encuesta(calificaciones, opinion):
    """Guarda una nueva encuesta."""
    
    datos = {
        "Fecha y hora": datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        ),
        **calificaciones,
        "Opinión": opinion.strip()
    }

    df = cargar_datos()

    df = pd.concat(
        [
            df,
            pd.DataFrame([datos])
        ],
        ignore_index=True
    )

    df.to_csv(
        ARCHIVO,
        index=False,
        encoding="utf-8-sig"
    )


def estrellas(valor):
    """Convierte un número en estrellas."""

    if valor is None:
        return "Selecciona una calificación"

    valor = int(round(valor))

    return "⭐" * valor + "☆" * (5 - valor)


def generar_opinion_general(promedios):
    """Genera una opinión general automáticamente."""

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
        f"representa el principal punto de oportunidad "
        f"para mejorar."
    )


# ============================================================
# INICIALIZACIÓN
# ============================================================

crear_archivo()


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
    [
        "📝 Encuesta",
        "📊 Resultados"
    ]
)


# ============================================================
# ENCUESTA
# ============================================================

with tab_encuesta:

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

                # IMPORTANTE:
                # Ninguna opción aparece seleccionada
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

            max_chars=500
        )

        enviar = st.form_submit_button(
            "⭐ Enviar evaluación",
            use_container_width=True
        )


    # ========================================================
    # VALIDAR ENCUESTA
    # ========================================================

    if enviar:

        faltantes = [
            aspecto

            for aspecto, calificacion
            in calificaciones.items()

            if calificacion is None
        ]


        # Si falta alguna calificación
        if faltantes:

            st.error(
                "Por favor, califica todos los aspectos "
                "antes de enviar la encuesta."
            )

            st.write(
                "Falta calificar: "
                + ", ".join(faltantes)
            )


        # Si todo está contestado
        else:

            guardar_encuesta(
                calificaciones,
                opinion
            )

            st.success(
                "¡Gracias por evaluar nuestro billar! "
                "Tu respuesta fue registrada correctamente."
            )

            # Limpiar las calificaciones
            for aspecto in ASPECTOS:

                st.session_state.pop(
                    f"cal_{aspecto}",
                    None
                )

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

        # Convertir las calificaciones a números

        for aspecto in ASPECTOS:

            df[aspecto] = pd.to_numeric(
                df[aspecto],
                errors="coerce"
            )


        # ====================================================
        # PROMEDIOS
        # ====================================================

        promedios = df[ASPECTOS].mean()

        promedio_general = promedios.mean()

        cantidad = len(df)


        # ====================================================
        # INDICADORES
        # ====================================================

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


        # ====================================================
        # TABLA
        # ====================================================

        st.divider()

        st.subheader(
            "⭐ Promedio por aspecto"
        )


        tabla = pd.DataFrame({

            "Aspecto": ASPECTOS,

            "Promedio": [
                round(
                    promedios[aspecto],
                    2
                )

                for aspecto in ASPECTOS
            ],

            "Calificación": [
                estrellas(
                    promedios[aspecto]
                )

                for aspecto in ASPECTOS
            ]
        })


        st.dataframe(
            tabla,

            hide_index=True,

            use_container_width=True
        )


        # ====================================================
        # GRÁFICA
        # ====================================================

        st.subheader(
            "📊 Gráfica de calificaciones"
        )


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


        # ====================================================
        # OPINIÓN GENERAL
        # ====================================================

        st.subheader(
            "🧠 Opinión general"
        )


        st.info(
            generar_opinion_general(
                promedios
            )
        )


        # ====================================================
        # OPINIONES DE CLIENTES
        # ====================================================

        st.subheader(
            "💬 Opiniones de los clientes"
        )


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
                    f"**Cliente {numero}:** "
                    f"{comentario}"
                )


        # ====================================================
        # DESCARGAR RESULTADOS
        # ====================================================

        st.divider()

        st.subheader(
            "📥 Exportar resultados"
        )


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


        # ====================================================
        # ADMINISTRACIÓN
        # ====================================================

        with st.expander(
            "⚙️ Administración"
        ):

            st.warning(
                "Esta sección es para el responsable "
                "del proyecto. Borrar los datos es "
                "una acción permanente."
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