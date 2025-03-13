lista_volar = []
lista_comer = []

alumnos_aidone = {
    "Rodrigo": [5, 4],
    'Lucia': [2, -3],
    'Alejandro': [3, 5],
    'Valeria': [-5, 4],
    'Javier': [0, -1],
    'Camila': [3, 2],
    'Diego': [-1, 1],
    'Gabriela': [5, -2],
    'Mateo': [-5, 3],
    'Sofía': [-5, 1]
}
lista_volar = []
lista_comer = []
# Recorrer el diccionario y desestructurar los valores en volar y comer
for nombre, (volar, comer) in alumnos_aidone.items():
    lista_volar.append(volar)
    lista_comer.append(comer)

# Ahora puedes imprimir la lista_comer sin error
print(lista_comer)