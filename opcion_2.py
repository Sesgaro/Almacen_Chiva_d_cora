def llegada_articulos(matrix):
    while True:
        try:
            modelo = input('Ingresa la clave de modelo del articulo entregado: \n')
            modelo=abs(modelo)
            break
        except ValueError:
            print('Error de ingreso. Solo se aceptan numeros enteros.')
          
    if modelo in matrix[1]:
        while True:
            try:
                unidad=int(input('Cantidad de unidades entregadas: \n'))
                unidades=abs(unidad)
                break
            except ValueError:
                print('Error de ingreso. Solo se aceptan numeros enteros.')

        matrix[2][i] = str(int(matrix[2][i])+unidades) 
        print('Lista actualizada: ')
        for fila in matrix:
            print(fila)
