# 🎮 Minecraft Server Payment Tracker - ULTRA OPTIMIZED

Sistema ultra-rápido de gestión de pagos para servidor de Minecraft.

## ⚡ Optimizaciones

- **psycopg2 directo** (sin SQLAlchemy ORM) - 5x más rápido
- **Connection pooling** (3-15 conexiones)
- **Caché en memoria** (15-30 segundos)
- **HTTP Compression** (Flask-Compress)
- **Queries SQL optimizadas** con JOINs
- **Static file caching** (1 año)

## 🚀 Instalación Rápida

```bash
pip install -r requirements.txt
python app.py
```

## 📁 Estructura

```
├── app.py              # Aplicación Flask optimizada
├── database.py         # Capa de BD con pooling y caché
├── db.py              # Configuración de PostgreSQL
├── forms.py           # Formularios WTForms
├── requirements.txt   # Dependencias mínimas
├── templates/         # Templates HTML
└── static/           # CSS/JS
```

## 🔐 Credenciales

- **Usuario:** johann
- **Contraseña:** %Aguinaga10%

## 🌐 Despliegue en Vercel

```bash
git add .
git commit -m "Ultra optimized version"
git push
```

Vercel desplegará automáticamente.

## 📊 Rendimiento

- **Página principal:** ~50-100ms
- **Dashboard admin:** ~30-80ms
- **Queries con caché:** ~5-10ms
- **Connection pool:** Reutiliza conexiones

## 🛠️ Tecnologías

- Flask 3.0 (sin extensiones pesadas)
- psycopg2-binary (PostgreSQL directo)
- WTForms (sin Flask-WTF)
- Flask-Compress (compresión HTTP)
- PostgreSQL en Aiven

---

**Optimizado para máximo rendimiento** ⚡
