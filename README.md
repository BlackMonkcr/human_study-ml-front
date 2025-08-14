# Estudio de Clasificación Musical - Frontend

Este es un frontend desarrollado con Streamlit para realizar un estudio de clasificación de canciones en español con contenido explícito.

## Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crea un archivo `.env` con las siguientes variables:

```bash
MONGODB_URI=tu_connection_string_mongodb
MONGODB_DB=ml-workshop
SONGS_COLLECTION=songs_lang
RESPONSES_COLLECTION=user_responses
APP_TITLE=Estudio de Clasificación Musical
APP_DESCRIPTION=Clasificación de contenido explícito en canciones en español
```

**⚠️ IMPORTANTE**: Nunca subas el archivo `.env` a control de versiones. Asegúrate de que esté en tu `.gitignore`.

### 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

## Funcionalidades

### Para los usuarios:
- **Información del participante**: Recolección de género y edad
- **Reproducción de canciones**: YouTube embeds y Spotify previews
- **Clasificación**: Marcado de contenido explícito y sexual
- **Navegación**: Avance, retroceso y omitir canciones
- **Progreso**: Seguimiento del progreso del usuario
- **Persistencia**: Mantiene el progreso en la sesión

### Para el estudio:
- **Filtrado automático**: Solo canciones con `spotify_found: true` e `is_human_study: true`
- **Base de datos**: Almacenamiento seguro en MongoDB
- **Identificación única**: Cada usuario tiene un ID único
- **Metadatos**: Información completa de cada respuesta

## Estructura de datos

### Colección de entrada (`songs_lang`)
Las canciones filtradas con los criterios:
- `spotify_found: true`
- `is_human_study: true`

### Colección de respuestas (`user_responses`)
Cada respuesta incluye:
- `user_id`: ID único del usuario
- `user_gender`: Género del participante
- `user_age`: Edad del participante
- `song_id`: ID de la canción clasificada
- `spotify_id`: ID de Spotify de la canción
- `artist`: Artista de la canción
- `title`: Título de la canción
- `explicit_content`: Clasificación de contenido explícito
- `sexual_content`: Clasificación de contenido sexual
- `comments`: Comentarios adicionales (opcional)
- `timestamp`: Fecha y hora de la respuesta
- `song_index`: Índice de la canción en la lista

## Características técnicas

- **Framework**: Streamlit para una interfaz web intuitiva
- **Base de datos**: MongoDB para almacenamiento escalable
- **Gestión de estado**: Session state para persistencia local
- **Seguridad**: Variables de entorno para credenciales
- **Navegación**: Sistema de navegación flexible
- **Progreso**: Indicadores visuales de progreso
- **Validación**: Validación de datos de entrada

## Uso recomendado

1. **Preparación**: Asegúrate de tener las 30 canciones marcadas correctamente en la base de datos
2. **Distribución**: Comparte la URL de la aplicación con los participantes
3. **Monitoreo**: Supervisa las respuestas en la colección `user_responses`
4. **Análisis**: Exporta los datos para análisis posterior

## Notas importantes

- La aplicación maneja automáticamente la persistencia del progreso del usuario
- Los usuarios pueden navegar libremente entre canciones
- Se evita la duplicación de respuestas mediante el sistema de seguimiento
- La interfaz es responsiva y funciona en dispositivos móviles
