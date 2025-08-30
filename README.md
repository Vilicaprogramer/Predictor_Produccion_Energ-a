# ⚡ Predicción de Producción Eléctrica en España

Este proyecto tiene como objetivo **predecir la producción eléctrica en España por tipo de fuente** (renovables, fósiles, nuclear, solar y gas) utilizando datos oficiales del portal [ENTSO-E Transparency](https://transparency.entsoe.eu/).  

La aplicación **descarga automáticamente los datos actualizados**, compara las predicciones anteriores con los datos reales y **lanza una nueva predicción para los próximos 15 días**. Todo ello se visualiza en una **interfaz interactiva desarrollada en Streamlit**.

---

## 📂 **Estructura del Proyecto**

```
.
├── README.md               # Documentación principal
└── src/
    ├── app/
    │   ├── .streamlit/     # Configuración de Streamlit
    │   ├── utils/
    │   │   └── utils.py    # Funciones auxiliares (procesamiento y predicción)
    │   └── predictor.py    # App principal de Streamlit
    ├── data/
    │   └── produccion_electrica_ES.csv   # Base de datos local
    └── notebooks/
        └── transparecyplatform.ipynb     # Notebook de experimentación y selección del modelo
```

---

## 🔍 **Descripción del Flujo**

1. **Notebook de experimentación**  
   En `transparecyplatform.ipynb` se prueban varios modelos de predicción para series temporales multisalida.  
   Finalmente, se selecciona un **XGBoost con MultiOutputRegressor** y un `Pipeline` con escalado y ajuste de hiperparámetros usando `RandomizedSearchCV` y `TimeSeriesSplit`.

   **Mejores hiperparámetros encontrados:**
   ```python
   {
       'scaler': MinMaxScaler(),
       'multi_model__estimator__subsample': 0.8,
       'multi_model__estimator__reg_lambda': 0,
       'multi_model__estimator__n_estimators': 200,
       'multi_model__estimator__max_depth': 5,
       'multi_model__estimator__learning_rate': 0.05,
       'multi_model__estimator__gamma': 1,
       'multi_model__estimator__colsample_bytree': 0.8
   }
   ```
   **Resultados del modelo:**
   - **Score de Train:** 0.9880  
   - **Score de Test:** 0.8502  
   - **MAE:** 666.81  
   - **RMSE:** 1064.55  

---

2. **Aplicación Streamlit (`predictor.py`)**  
   - **Carga la base de datos local** (`produccion_electrica_ES.csv`).
   - **Descarga datos faltantes** desde la API oficial hasta la fecha actual.
   - **Compara predicciones pasadas vs datos reales** de los últimos 15 días.
   - **Genera nueva predicción para 15 días** usando el modelo entrenado.
   - **Visualiza todo** con gráficos interactivos (Plotly + Streamlit).

   Las pestañas disponibles en la app:
   - `Total_Renovable`
   - `Total_Fossil`
   - `Nuclear`
   - `Solar`
   - `Fossil Gas`

---

## ⚙️ **Tecnologías Utilizadas**
- **Python 3.10+**
- **Pandas**, **NumPy**
- **Scikit-learn**
- **XGBoost**
- **Plotly**, **Matplotlib**, **Seaborn**
- **Streamlit**
- **ENTSO-E API (transparency.entsoe.eu)**

---

## 🚀 **Cómo Ejecutar el Proyecto**

### 1️⃣ **Clonar el repositorio**
```bash
git clone https://github.com/usuario/proyecto-prediccion.git
cd proyecto-prediccion/src/app
```

### 2️⃣ **Crear entorno virtual e instalar dependencias**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows

pip install -r requirements.txt
```

### 3️⃣ **Configurar la API Key**
Debes crear una cuenta en [ENTSO-E Transparency](https://transparency.entsoe.eu/) y obtener tu **API Key**.  
Guárdala en un archivo `token.txt` en la raíz del proyecto, tal como lo espera la app:
```
/src/token.txt
```

### 4️⃣ **Ejecutar la aplicación Streamlit**
```bash
streamlit run predictor.py
```

---

## 📊 **Visualización y Funcionalidades**
✅ Descarga automática de datos actualizados.  
✅ Comparación de predicciones pasadas vs valores reales.  
✅ Predicción multisalida para los próximos 15 días.  
✅ Gráficos interactivos por categoría energética.  

---

## 📌 **Notas Importantes**
- El modelo está entrenado y optimizado para datos diarios de **producción eléctrica en España**.
- Si quieres adaptarlo a otro país, solo debes cambiar el `country_code` en el código (por ejemplo `'FR'` para Francia).
- El CSV se actualiza automáticamente después de cada ejecución.

---

## 🏆 **Resultados Esperados**
- **Análisis histórico de la producción eléctrica**.
- **Predicciones a 15 días por tipo de energía** con visualización clara y dinámica.
- **Pipeline reproducible para mejorar o cambiar el modelo en el futuro**.

---

### ✨ Autor: *[Vicente Limones Cantero]*  
📧 Contacto: [vilicaprogramer@gmail.com]  
🔗 [[LinkedIn](www.linkedin.com/in/vicente-limones-cantero-3a167328a) / [GitHub](https://github.com/Vilicaprogramer) / [Portafolio](https://vilicaprogramer.github.io/Portfolio_HTML/)]  
