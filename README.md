# API de Pacientes (FastAPI + SQLite)

API REST  para **registrar** y **consultar** pacientes (nombre, edad, síntomas).  

---

## 🏗 Arquitectura

flowchart LR  
  A[Cliente HTTP (curl/Postman/navegador)] -->|JSON/HTTP| B[FastAPI (main.py)]  
  B --> C[Pydantic (Validación I/O)]  
  B --> D[SQLAlchemy ORM]  
  D --> E[(SQLite patients.db)]  
  B --> F[OpenAPI Docs (/docs, /redoc)]  

**Descripción de la arquitectura:**  
- **FastAPI**: framework principal para exponer la API REST.  
- **Pydantic**: validación de datos de entrada y salida.  
- **SQLAlchemy**: ORM para interactuar con la base de datos.  
- **SQLite**: base de datos simple en archivo (`patients.db`).  
- **OpenAPI**: documentación automática disponible en `/docs` y `/redoc`.  

---

## 📋 Requisitos

- Python **3.10+**  
- (Opcional) `virtualenv` o `uv` para aislar dependencias.  
- Paquetes definidos en `requirements.txt`:  
  - `fastapi`  
  - `uvicorn`  
  - `SQLAlchemy`  
  - `pydantic`  

---

## ⚙️ Cómo ejecutar el proyecto

### 1) Descargar/clonar el repositorio
```bash
git clone https://github.com/559Emmanuel/ROMI-Asistente-M-dico-Virtual
cd ROMI-Asistente-M-dico-Virtual
```

### 2) Crear entorno virtual (opcional pero recomendado)
```bash
python -m venv .venv
```

- **Activar el entorno virtual**  
  - En **Linux/Mac**:  
    ```bash
    source .venv/bin/activate
    ```  
  - En **Windows (PowerShell)**:  
    ```powershell
    .venv\Scripts\Activate.ps1
    ```  

- **Desactivar el entorno virtual**  
  En cualquier sistema operativo, dentro del entorno ejecuta:  
  ```bash
  deactivate
  ```

### 3) Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4) Ejecutar en desarrollo
```bash
uvicorn main:app --reload
```

### 5) Probar la API
- Swagger UI: **http://127.0.0.1:8000/docs**  
- Redoc: **http://127.0.0.1:8000/redoc**  

> Al iniciar, se creará automáticamente el archivo **`patients.db`** en la raíz del proyecto con la tabla necesaria.  

---

## 🗂 Endpoints principales

- `POST /patients` → Registrar un paciente  
- `GET /patients` → Consultar todos los pacientes (con filtro opcional por nombre)  
- `GET /patients/{id}` → Consultar un paciente por su id  

---

## 📌 Ejemplos de uso

### Registrar un paciente
```bash
curl -X POST http://127.0.0.1:8000/patients   -H "Content-Type: application/json"   -d '{"name":"Juan Pérez","age":28,"symptoms":["fiebre","tos"]}'
```

### Registrar un paciente (síntomas como texto)
```bash
curl -X POST http://127.0.0.1:8000/patients   -H "Content-Type: application/json"   -d '{"name":"Ana","age":35,"symptoms":"dolor de cabeza, náusea"}'
```

### Consultar todos los pacientes
```bash
curl http://127.0.0.1:8000/patients
```

### Consultar pacientes por nombre
```bash
curl "http://127.0.0.1:8000/patients?name=ana"
```

### Consultar un paciente por ID
```bash
curl http://127.0.0.1:8000/patients/1
```

---

## 📌 Roadmap (mejoras a futuro)

- CRUD completo (PUT, PATCH, DELETE).  
- Paginación en `GET /patients`.  
- Autenticación con JWT.  
- Normalizar síntomas en tabla aparte (relación 1–N).  
- Tests automáticos (`pytest`, `httpx`).  
- Dockerfile para despliegue.  

---

## 📜 Licencia

Uso libre con fines del reto.
