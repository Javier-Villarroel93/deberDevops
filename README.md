# Ejemplo de CI/CD hasta la construcción del *package*

**Asignatura:** 5-VE-B-SD4-515-2025-II  
**Unidad:** UNIDAD III  
**Tarea 7.0:** Ciclo CI/CD hasta la construcción del package

Este repositorio muestra, con un ejemplo práctico, cómo funciona un flujo de **CI/CD** (Integración Continua / Entrega Continua) hasta la etapa de **construcción del package** de una aplicación en Python.

La idea es que con solo hacer `git push` a GitHub, se ejecute automáticamente:

1. Instalación de dependencias.
2. Ejecución de pruebas automatizadas.
3. Construcción de un **paquete** (`.whl` y `.tar.gz`) listo para ser distribuido.
4. Publicación de ese paquete como artefacto del pipeline.

---

## 1. ¿Qué es CI/CD?

- **CI (Integración Continua):**  
  Cada vez que se sube código al repositorio remoto (push), se ejecutan procesos automáticos para:
  - Verificar que el proyecto compile o se instale.
  - Correr pruebas automatizadas.
  - Detectar errores temprano.

- **CD (Entrega / Despliegue Continuo):**  
  Después de que la CI termina correctamente, se puede:
  - Construir el artefacto (package).
  - Publicarlo en algún repositorio de paquetes o
  - Desplegarlo en un servidor.  

  En esta tarea **nos quedamos hasta la construcción del package**, es decir, el pipeline termina cuando genera el artefacto.

En este repositorio el ciclo es:

```text
Desarrollar → Commit → Push a GitHub → Workflow (CI) → Pruebas → Construcción de package → Artefacto listo
```

---

## 2. Estructura del proyecto

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline de CI/CD (GitHub Actions)
├── src/
│   └── calc/
│       ├── __init__.py
│       └── main.py         # Lógica simple: operaciones de suma y resta
├── tests/
│   └── test_calc.py        # Pruebas unitarias básicas
├── pyproject.toml          # Configuración para construir el package
├── requirements.txt        # Dependencias (si se necesitan)
└── README.md               # Este documento
```

---

## 3. Ejemplo práctico: mini biblioteca de cálculo

La aplicación es muy sencilla: un pequeño módulo de cálculo con operaciones básicas.

Archivo `src/calc/main.py`:

```python
def sumar(a: float, b: float) -> float:
    """Suma dos números y devuelve el resultado."""
    return a + b


def restar(a: float, b: float) -> float:
    """Resta b de a y devuelve el resultado."""
    return a - b


if __name__ == "__main__":
    # Ejemplo de uso básico
    print("5 + 3 =", sumar(5, 3))
    print("5 - 3 =", restar(5, 3))
```

---

## 4. Pruebas automatizadas (Tests)

Para cumplir con la parte de **Pruebas** de la rúbrica, se incluye un conjunto mínimo de pruebas unitarias con `pytest`.

Archivo `tests/test_calc.py`:

```python
from calc.main import sumar, restar


def test_sumar_numeros_positivos():
    assert sumar(2, 3) == 5


def test_sumar_con_negativos():
    assert sumar(-1, 1) == 0


def test_restar_numeros():
    assert restar(5, 3) == 2


def test_restar_resultado_negativo():
    assert restar(3, 5) == -2
```

Para ejecutarlas de forma local:

```bash
pip install -r requirements.txt
pytest
```

---

## 5. Configuración del package (pyproject.toml)

El archivo `pyproject.toml` define cómo se construye el package del proyecto usando `setuptools`.

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "calc-ci-cd-ejemplo"
version = "0.1.0"
description = "Ejemplo simple de CI/CD y empaquetado con Python"
authors = [
    { name = "Tu Nombre" }
]
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[tool.setuptools]
package-dir = {"" = "src"}
packages = ["calc"]
```

Con esta configuración, el comando:

```bash
python -m build
```

genera en la carpeta `dist/` dos archivos, por ejemplo:

- `calc_ci_cd_ejemplo-0.1.0-py3-none-any.whl`
- `calc_ci_cd_ejemplo-0.1.0.tar.gz`

Eso es el **package** del proyecto.

---

## 6. Workflow de CI/CD en GitHub Actions

El pipeline se define en `.github/workflows/ci.yml`.  
Cada vez que se hace `push` a la rama `main`, el flujo:

1. Crea un entorno con Python.
2. Instala dependencias.
3. Ejecuta las pruebas.
4. Construye el package.
5. Publica los archivos generados en `dist/` como artefactos del workflow.

```yaml
name: CI - Tests y Package

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-test-package:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout del código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install build

      - name: Ejecutar pruebas
        run: |
          pytest

      - name: Construir package
        run: |
          python -m build

      - name: Publicar artefactos de build
        uses: actions/upload-artifact@v4
        with:
          name: dist-packages
          path: dist/
```

Con esto se cumple:

- **Configuración del CI/CD:** archivo de workflow funcional.
- **Pruebas:** se ejecutan automáticamente.
- **Construcción del package:** se ejecuta `python -m build` y se generan artefactos.

---

## 7. Cómo reproducir el flujo CI/CD

1. Crear un repositorio en GitHub.
2. Subir todos los archivos de este proyecto (`README.md`, `pyproject.toml`, `src/`, `tests/`, `.github/`).
3. Hacer `commit` y `push` a la rama `main`.
4. Ir a la pestaña **Actions** en GitHub.
5. Verificar que se ejecuta el workflow **"CI - Tests y Package"**.
6. Revisar:
   - Logs de pruebas.
   - Artefactos generados en la sección de **Artifacts** (los packages construidos).

Con esto se cubren los puntos de la rúbrica:

1. **README.md:** explicación clara del ciclo CI/CD con ejemplo práctico.  
2. **Configuración CI/CD:** workflow de GitHub Actions.  
3. **Pruebas:** archivo `tests/test_calc.py` ejecutado en el pipeline.  
4. **Construcción del package:** `python -m build` genera artefactos en `dist/`.  
5. **Repositorio y entrega:** al subir este proyecto a un repo público y compartir el enlace, se completa la tarea.
