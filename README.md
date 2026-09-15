# Snake Game AI

IA autónoma que aprende a jugar al Snake, con un frontend en JavaScript y un modelo entrenado en Python servido en tiempo real.

## Qué hace

- Genera e ingiere datos de partidas para entrenar una red neuronal con TensorFlow (`dataset.py`, `train.py`).
- Sirve el modelo entrenado a través de una API en `modeloAPI.py` (FastAPI), que responde en tiempo real a cada estado del tablero.
- El juego (`snake.js`, `index.html`) corre en el navegador y consulta a la API para que la serpiente juegue de forma autónoma.

## Tecnología

Python (TensorFlow, FastAPI), JavaScript, WebSockets.

## Cómo ejecutarlo

```bash
pip install fastapi uvicorn tensorflow numpy pandas
python train.py                   # entrena el modelo (opcional si ya existe uno en /Modelos)
uvicorn modeloAPI:app --reload    # levanta la API
```

Con la API corriendo, abre `index.html` en el navegador para ver a la IA jugar en tiempo real.
