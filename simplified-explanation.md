# Simplified explanation

*Los algoritmos de la familia Deutsch-Jozsa explicados en lenguaje
sencillo. Si puedes explicar esto en una conversación, puedes
explicarlo en una entrevista.*

---

## 🔮 El juego del oráculo

Imagina una caja negra mágica: le metes una pregunta y te responde,
pero no puedes ver cómo funciona por dentro. A eso los físicos le
dicen **oráculo**. Los tres algoritmos de esta familia son tres
formas de hacerle preguntas *muy inteligentes* a la caja, de modo
que con poquísimas preguntas descubres su secreto.

El truco que comparten: en vez de preguntar una cosa a la vez, la
computadora cuántica pregunta **todas las posibilidades al mismo
tiempo** (superposición), y luego usa interferencia para que la
respuesta correcta "brille" y las demás se cancelen.

---

## 🕵️ Bernstein-Vazirani: adivinar el código secreto de una vez

La caja esconde un código binario, digamos `101`. Cada vez que le
preguntas algo, la caja responde con un solo bit calculado a partir
del código.

- **Detective clásico:** necesita 3 preguntas, una por cada bit del
  código. Con un código de 50 bits, 50 preguntas.
- **Detective cuántico:** hace **UNA** pregunta, pero la hace "en
  superposición", preguntando todos los códigos posibles a la vez.
  Gracias a un truco llamado *phase kickback* (la respuesta se
  escribe como un patrón de fases en vez de como bits), al final la
  medición revela el código completo: `101`, de una sentada.

En el proyecto probamos tres códigos distintos (`101`, `011`,
`110`) y los tres se recuperan perfectos con una sola consulta.

> 💡 *"¿Y eso para qué sirve?"*
> Es la demostración más limpia de que lo cuántico extrae más
> información por consulta que lo clásico. El mismo truco de fases
> aparece en algoritmos mucho más serios.

---

## 🥁 Simon: encontrar el ritmo escondido

Ahora la caja esconde un **período**: un patrón que se repite. Por
ejemplo, con período `101`, la caja responde igual para `000` que
para `101`, igual para `001` que para `100`, etc. Todo viene en
parejas separadas por el período.

- **Detective clásico:** tiene que probar entradas al azar hasta
  encontrar dos que den la misma respuesta (como buscar dos personas
  con el mismo cumpleaños). Para n bits necesita del orden de
  2^(n/2) preguntas. Con n=50, eso son 33 millones.
- **Detective cuántico:** cada pregunta le da una **ecuación**
  (una pista del tipo "el período multiplicado por este vector da
  cero"). Con unas n preguntas ya tiene suficientes ecuaciones para
  resolver el sistema y despejar el período. Para n=50, unas 50
  preguntas contra 33 millones.

Este es el salto **exponencial**, y es el antepasado directo del
algoritmo de Shor: el que en teoría podría romper el RSA. Simon es
el prototipo; Shor es la aplicación que asustó al mundo de la
seguridad.

---

## 📊 La tabla de la ventaja

| Algoritmo | Preguntas cuánticas | Preguntas clásicas |
|---|---|---|
| Deutsch-Jozsa | 1 | hasta 2^(n-1) + 1 |
| Bernstein-Vazirani | 1 | n |
| Simon | O(n) | O(2^(n/2)) |

*(Resultados clásicos de la teoría, no medidos aquí: las
implementaciones que demuestran la columna cuántica están en los
scripts 01 y 02.)*

---

## ▶️ Cómo correrlo

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash run_all.sh
```

Verás los códigos secretos recuperados de una sola consulta, el
período escondido despejado por eliminación lineal, y la tabla de la
ventaja cuántica. 🎉
