# 🎱 Encuesta de satisfacción para un billar

Proyecto académico desarrollado con **Python + Streamlit + Pandas**.

## Funciones

- Encuesta de 5 aspectos.
- Calificación de 1 a 5 estrellas.
- Comentario libre.
- Registro de múltiples clientes.
- Promedio de cada aspecto.
- Promedio general.
- Identificación del mejor y peor aspecto.
- Opinión general automática.
- Gráfica de barras.
- Visualización de opiniones.
- Exportación de resultados a CSV.

## Archivos

- `app.py` → programa principal.
- `requirements.txt` → librerías necesarias.
- `encuestas.csv` → se crea automáticamente cuando se ejecuta la aplicación.

## Ejecutar en una computadora

Instala Python y después ejecuta:

```bash
pip install -r requirements.txt
streamlit run app.py
```

La aplicación se abrirá en el navegador.

## Publicarla en internet

Streamlit Community Cloud permite desplegar aplicaciones desde GitHub. Se necesita una cuenta de GitHub y un repositorio con el código.

1. Crea un repositorio en GitHub.
2. Sube `app.py` y `requirements.txt`.
3. Entra a Streamlit Community Cloud.
4. Conecta GitHub.
5. Selecciona el repositorio.
6. Selecciona `app.py` como archivo principal.
7. Presiona Deploy.

La aplicación recibirá una dirección `https://...streamlit.app`.

## Nota sobre los datos

Esta versión usa un archivo CSV, lo cual es muy práctico para demostrar el proyecto en una computadora.

Para una encuesta pública con muchas personas, conviene cambiar el almacenamiento por una base de datos o un servicio externo, porque el almacenamiento local de una aplicación desplegada no debe tratarse como una base de datos permanente.

## Conceptos de Python que puedes explicar

- Variables.
- Listas.
- Diccionarios.
- Funciones.
- Condicionales `if / elif / else`.
- Ciclos `for`.
- Lectura y escritura de archivos.
- Manejo de fechas.
- Librería Pandas.
- Promedios.
- Procesamiento de datos.
- Gráficas.
- Interfaz web con Streamlit.
