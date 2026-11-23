# app/datos.py
# Nuestra "base de datos": una lista de diccionarios a nivel de módulo.
# Vive en memoria: se reinicia cada vez que el servidor recarga.
MATERIAS: list[dict] = [
 {"codigo": "SAL101", "nombre": "Sala Clásica A", "butacas": 120, "piso": 1, "es_3d": false},
 {"codigo": "SAL102", "nombre": "Sala Clásica B", "butacas": 95, "piso": 1, "es_3d": false},
 {"codigo": "SAL201", "nombre": "Sala Panorámica", "butacas": 180, "piso": 2, "es_3d": true},
 {"codigo": "SAL202", "nombre": "Sala Premier", "butacas": 60, "piso": 2, "es_3d": true},
 {"codigo": "SAL301", "nombre": "Sala IMAX", "butacas": 320, "piso": 3, "es_3d": true},
 {"codigo": "SAL302", "nombre": "Sala Infantil", "butacas": 80, "piso": 3, "es_3d": false}
]