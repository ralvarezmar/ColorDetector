# Color detector

## Objetivo

El objetivo de la práctica consiste en profundizar sobre algún tema abordado en la asignatura y presentar un proyecto con los resultados y conclusiones obtenidas.

En este caso, hemos decidido profundizar en el tema de morfología matemática en imágenes binarias, lo que nos va a ser de gran utilidad en el tema escogido, detección de una pelota en movimiento en base a su color.

El desarrollo del proyecto se ha llevado a cabo con el lenguaje de programación Python.


## Desarrollo 

Inicialmente, en el main del código añadimos opciones a la hora de lanzar el programa para que el usuario pueda elegir qué pelota quiere que se detecte. Tan solo es necesario que se le pase como argumentos, el color (RGB) y el video que queremos procesar (directorio). Se ha añadido la posibilidad de dar los valores RGB del color que queremos detectar.

Una vez introducidos los campos, el programa captura el video que se le ha pasado como argumento. De esta forma, se puede filtrar el color que queramos, en función de si es rojo, verde, azul o cualquier otro color definido por los valores que el usuario haya introducido.

Una vez hecho esto, se aplica un filtro gaussiano para eliminar cualquier tipo de ruido que pueda perjudicar al post-procesado del video. Después se convierte la imagen al espacio HSV, filtrando posteriormente con los valores que se hayan indicado al iniciar el programa.

Se aplica un filtro morfológico de apertura, para así redondear las esquinas donde no quepa el elemento estructurante, eliminar las protuberancias donde no quepa el elemento estructurante y separa los objetos de puntos estrechos. Esto si lo pensamos nos viene perfecto para este caso, porque es justo lo que estamos buscando.

Cuando ya hemos aplicado el filtro morfológico de apertura, binarizamos la imagen. Le pasamos este resultado a una pequeña función que lo que hace es detectar áreas bajo unos valores preestablecidos (las dimensiones de la pelota) y así poder representar un cuadrado de color verde, indicando donde se encuentra la pelota que se está detectando.
 
 
 
