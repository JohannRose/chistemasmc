# Despliegue en Vercel - Minecraft Payment Tracker

## 📋 Requisitos Previos

1. Cuenta en [Vercel](https://vercel.com)
2. Base de datos PostgreSQL en Aiven (o cualquier proveedor)
3. Repositorio Git (GitHub, GitLab, o Bitbucket)

## 🚀 Pasos para Desplegar

### 1. Preparar el Repositorio

```bash
# Inicializar git si no lo has hecho
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Preparar para despliegue en Vercel"

# Conectar con tu repositorio remoto
git remote add origin <tu-repositorio-url>
git push -u origin main
```

### 2. Importar Proyecto en Vercel

1. Ve a [Vercel Dashboard](https://vercel.com/dashboard)
2. Click en **"Add New Project"**
3. Importa tu repositorio de Git
4. Vercel detectará automáticamente que es un proyecto Python

### 3. Configurar Variables de Entorno

En la configuración del proyecto en Vercel, agrega las siguientes variables de entorno:

#### Variables Requeridas:

```bash
# Flask Configuration
SECRET_KEY=tu-clave-secreta-super-segura-aqui

# PostgreSQL Database (Aiven)
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/database?sslmode=require

# Flask Environment
FLASK_ENV=production
```

#### Ejemplo con Aiven PostgreSQL:

```bash
SECRET_KEY=minecraft-payment-tracker-2025-secret-key
DATABASE_URL=postgresql://avnadmin:AVNS_Ip7pf989aOcdP6_SaZx@minecraftjohann-usat-fc50.e.aivencloud.com:17580/defaultdb?sslmode=require
FLASK_ENV=production
```

### 4. Desplegar

1. Click en **"Deploy"**
2. Vercel construirá y desplegará tu aplicación automáticamente
3. Recibirás una URL de producción (ej: `tu-proyecto.vercel.app`)

## 🔧 Configuración Post-Despliegue

### Inicializar Base de Datos

Después del primer despliegue, necesitas inicializar la base de datos:

**Opción 1: Usar script local**
```bash
# Asegúrate de tener la DATABASE_URL en tu .env local
python init_mysql_simple.py
```

**Opción 2: Ejecutar SQL directamente en Aiven**
1. Conecta a tu base de datos PostgreSQL en Aiven
2. Ejecuta el contenido de `database_init.sql` (adaptado para PostgreSQL)

### Crear Usuario Admin

Si usaste el script de inicialización, ya tendrás un usuario admin:
- **Usuario:** admin
- **Contraseña:** admin123

⚠️ **IMPORTANTE:** Cambia la contraseña inmediatamente después del primer login.

## 📁 Estructura de Archivos para Vercel

```
PagoIzipay/
├── api/
│   └── index.py          # Punto de entrada WSGI para Vercel
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── templates/            # Templates HTML
├── app.py               # Aplicación Flask principal
├── models.py            # Modelos de base de datos
├── forms.py             # Formularios WTForms
├── config.py            # Configuración
├── requirements.txt     # Dependencias Python
├── vercel.json          # Configuración de Vercel
└── .vercelignore        # Archivos a ignorar en el despliegue
```

## 🔐 Seguridad en Producción

### 1. Cambiar SECRET_KEY

Genera una clave secreta segura:

```python
import secrets
print(secrets.token_hex(32))
```

Usa el resultado como tu `SECRET_KEY` en las variables de entorno de Vercel.

### 2. Cambiar Contraseña de Admin

1. Inicia sesión en `/admin/login`
2. Cambia la contraseña inmediatamente

### 3. Configurar Dominio Personalizado (Opcional)

En Vercel Dashboard:
1. Ve a tu proyecto
2. Settings → Domains
3. Agrega tu dominio personalizado

## 🐛 Solución de Problemas

### Error: "Application failed to start"

**Causa:** Variables de entorno no configuradas correctamente

**Solución:**
1. Verifica que `DATABASE_URL` esté correctamente configurada
2. Asegúrate de que `SECRET_KEY` esté definida
3. Revisa los logs en Vercel Dashboard

### Error: "Database connection failed"

**Causa:** Problemas con la conexión a PostgreSQL

**Solución:**
1. Verifica que la URL de PostgreSQL sea correcta
2. Asegúrate de que incluya `?sslmode=require`
3. Verifica que la base de datos esté accesible desde internet

### Error: "Static files not loading"

**Causa:** Configuración incorrecta de rutas estáticas

**Solución:**
1. Verifica que `vercel.json` tenga la configuración correcta de rutas
2. Asegúrate de que los archivos estén en la carpeta `static/`

## 📊 Monitoreo

Vercel proporciona:
- **Analytics:** Estadísticas de uso
- **Logs:** Logs de la aplicación en tiempo real
- **Performance:** Métricas de rendimiento

Accede a estos desde el Dashboard de Vercel.

## 🔄 Actualizaciones

Para actualizar tu aplicación:

```bash
# Hacer cambios en tu código
git add .
git commit -m "Descripción de cambios"
git push

# Vercel desplegará automáticamente
```

## 📝 Notas Importantes

1. **Base de Datos:** Vercel es serverless, por lo que SQLite NO funcionará. Debes usar PostgreSQL u otra base de datos externa.

2. **Archivos Temporales:** No puedes escribir archivos en el sistema de archivos de Vercel. Todo debe guardarse en la base de datos.

3. **Cold Starts:** La primera petición después de inactividad puede ser lenta (cold start).

4. **Límites:** Vercel tiene límites en el plan gratuito:
   - 100 GB de ancho de banda
   - 100 horas de ejecución
   - Funciones serverless con timeout de 10 segundos

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs en Vercel Dashboard
2. Consulta la [documentación de Vercel](https://vercel.com/docs)
3. Verifica la configuración de PostgreSQL en Aiven

## ✅ Checklist de Despliegue

- [ ] Repositorio Git creado y pusheado
- [ ] Proyecto importado en Vercel
- [ ] Variables de entorno configuradas
- [ ] Base de datos PostgreSQL creada en Aiven
- [ ] Tablas de base de datos inicializadas
- [ ] Usuario admin creado
- [ ] Primer despliegue exitoso
- [ ] Aplicación accesible en URL de Vercel
- [ ] Contraseña de admin cambiada
- [ ] SECRET_KEY actualizada con valor seguro
- [ ] Dominio personalizado configurado (opcional)

---

**¡Listo!** Tu aplicación debería estar funcionando en Vercel. 🎉
