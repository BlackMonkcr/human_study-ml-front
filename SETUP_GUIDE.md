# Guía de Configuración Paso a Paso

## 🚀 Configuración Rápida

### 1. Clonar y preparar el proyecto

```bash
# Si estás en macOS/Linux
./setup.sh

# Si estás en Windows
setup.bat
```

### 2. Configurar variables de entorno

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Edita el archivo `.env` con tus credenciales reales:
```bash
MONGODB_URI=tu_connection_string_aqui
MONGODB_DB=ml-workshop
SONGS_COLLECTION=songs_lang
RESPONSES_COLLECTION=user_responses
```

### 3. Ejecutar la aplicación

```bash
# Activar entorno virtual
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate.bat  # Windows

# Ejecutar la aplicación principal
streamlit run app.py

# O ejecutar la demo (sin MongoDB)
streamlit run demo.py
```

## 📊 Estructura de Datos

### Colección de Canciones (`songs_lang`)

Filtro aplicado:
```javascript
{
  "spotify_found": true,
  "is_human_study": true
}
```

Campos importantes utilizados:
- `_id`: ID único de MongoDB
- `artist`: Nombre del artista
- `title_songs_new`: Título de la canción
- `genre`: Género musical
- `spotify_id`: ID de Spotify para embeds
- `embed`: Código HTML de YouTube
- `popularity`: Popularidad en Spotify (0-100)
- `release_date`: Fecha de lanzamiento
- `duration_ms`: Duración en milisegundos

### Colección de Respuestas (`user_responses`)

Estructura de documento guardado:
```javascript
{
  // Información del usuario
  "user_id": "uuid4-generado-automaticamente",
  "user_gender": "Masculino|Femenino|Otro|Prefiero no decir",
  "user_age": 25,

  // Información de la canción
  "song_id": "ObjectId de MongoDB",
  "spotify_id": "ID de Spotify",
  "artist": "Nombre del artista",
  "title": "Título de la canción",
  "genre": "Género musical",
  "release_date": "2020-01-01",
  "popularity": 85,

  // Clasificaciones del usuario
  "explicit_content": "No|Sí|No estoy seguro/a",
  "sexual_content": "No|Sí|No estoy seguro/a",
  "confidence_level": "Muy inseguro|Inseguro|Neutral|Seguro|Muy seguro",
  "comments": "Comentarios opcionales del usuario",

  // Metadatos
  "timestamp": "2025-08-14T13:41:06.123456",
  "song_index": 0,
  "session_duration_seconds": 127.45,
  "classification_source": "human_study_frontend"
}
```

## 🎯 Funcionalidades Implementadas

### Para los Participantes:
- ✅ **Registro demográfico**: Género y edad
- ✅ **Reproducción multimedia**: YouTube (principal) + Spotify (respaldo)
- ✅ **Clasificación dual**: Contenido explícito + contenido sexual
- ✅ **Escala de confianza**: 5 niveles de certeza
- ✅ **Comentarios opcionales**: Campo de texto libre
- ✅ **Navegación flexible**: Avanzar, retroceder, saltar canciones
- ✅ **Progreso visual**: Barras de progreso y métricas
- ✅ **Persistencia de sesión**: Mantiene el progreso durante la sesión
- ✅ **Interfaz responsiva**: Funciona en móviles y tablets

### Para los Investigadores:
- ✅ **Filtrado automático**: Solo canciones marcadas para el estudio
- ✅ **Almacenamiento seguro**: MongoDB con variables de entorno
- ✅ **IDs únicos**: Cada participante tiene un identificador único
- ✅ **Metadatos completos**: Tiempo de sesión, timestamps, etc.
- ✅ **Prevención de duplicados**: Sistema de tracking de canciones completadas
- ✅ **Logs de actividad**: Registro de toda la actividad del usuario

## 🔧 Configuración Avanzada

### Variables de Entorno Adicionales

```bash
# Configuración de sesión
SESSION_TIMEOUT_MINUTES=30
MAX_SONGS_PER_SESSION=30

# Configuración de la aplicación
APP_TITLE=Estudio de Clasificación Musical
APP_DESCRIPTION=Clasificación de contenido explícito en canciones en español
```

### Personalización de la Interfaz

Edita `/utils/ui_components.py` para:
- Cambiar colores del tema
- Modificar estilos CSS
- Personalizar componentes visuales

### Configuración de Streamlit

Edita `.streamlit/config.toml` para:
- Cambiar puerto de la aplicación
- Modificar tema visual
- Ajustar configuraciones del servidor

## 📈 Análisis de Datos

### Consultas MongoDB Útiles

```javascript
// Contar respuestas por género
db.user_responses.aggregate([
  { $group: { _id: "$user_gender", count: { $sum: 1 } } }
]);

// Promedio de edad por clasificación
db.user_responses.aggregate([
  { $group: {
    _id: "$explicit_content",
    avg_age: { $avg: "$user_age" },
    count: { $sum: 1 }
  }}
]);

// Canciones más clasificadas como explícitas
db.user_responses.aggregate([
  { $match: { explicit_content: "Sí" } },
  { $group: { _id: "$title", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
]);

// Tiempo promedio por clasificación
db.user_responses.aggregate([
  { $group: {
    _id: null,
    avg_duration: { $avg: "$session_duration_seconds" }
  }}
]);
```

### Exportar Datos

```bash
# Exportar todas las respuestas
mongoexport --uri="tu_connection_string" --db=ml-workshop --collection=user_responses --out=responses.json

# Exportar como CSV
mongoexport --uri="tu_connection_string" --db=ml-workshop --collection=user_responses --type=csv --fields=user_gender,user_age,explicit_content,sexual_content,artist,title --out=responses.csv
```

## 🛠️ Solución de Problemas

### Error de Conexión a MongoDB
1. Verifica que el `MONGODB_URI` en `.env` sea correcto
2. Asegúrate de que tu IP esté en la whitelist de MongoDB Atlas
3. Verifica que las credenciales no hayan expirado

### Problemas con YouTube Embeds
- Los embeds de YouTube pueden fallar por restricciones de región
- Usa el enlace de Spotify como alternativa
- Considera usar URLs directas como última opción

### Sesión Perdida
- La sesión se mantiene mientras la página esté abierta
- Al cerrar el navegador se pierde el progreso
- Para sesiones persistentes, implementa almacenamiento local

### Rendimiento Lento
```bash
# Instalar watchdog para mejor rendimiento
pip install watchdog

# Usar caché para queries frecuentes
# (ya implementado en el código)
```

## 📋 Lista de Verificación Pre-Estudio

- [ ] MongoDB configurado y accesible
- [ ] 30 canciones marcadas con `is_human_study: true`
- [ ] Aplicación probada en diferentes dispositivos
- [ ] Variables de entorno configuradas correctamente
- [ ] Backup de la base de datos realizado
- [ ] URL de la aplicación compartida con participantes
- [ ] Monitoreo de respuestas configurado

## 🚨 Consideraciones de Seguridad

- ⚠️ **Nunca** subir el archivo `.env` a control de versiones
- 🔒 Usar variables de entorno para todas las credenciales
- 🛡️ Configurar whitelist de IPs en MongoDB Atlas
- 📊 Limitar acceso a las colecciones de datos
- 🔐 Rotar credenciales regularmente

## 📞 Soporte

Para problemas técnicos:
1. Revisa esta documentación
2. Verifica los logs en la terminal
3. Prueba la aplicación demo primero
4. Consulta la documentación de Streamlit y MongoDB
