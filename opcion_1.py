def registro(): 
    nombre = input('Ingresa el nombre del vendedor: \n').upper() 
    if nombre in vendedores[0]:
        print('Vendedor registrado')    

        modelo = input('Ingresa la clave de modelo del articulo vendido: \n').upper()
    
        for i in range(len(matrix[1])): 
            if matrix[1][i] == modelo: 
                print('Registro completado')
                while True:
                    try:
                        unidad=int(input('Cantidad de unidades vendidas: \n'))
                        unidades=abs(unidad)
                        break
                    except ValueError:
                        print('Error de ingreso. Solo se aceptan numeros enteros.')
            
                if unidades <= int(matrix[2][i]):
                    matrix[2][i] = str(int(matrix[2][i])-unidades) 
                    print('lista actualizada: ')
                    for fila in matrix:
                        print(fila)
                
                    indice_ven = vendedores[0].index(nombre)
                    vendedores[i+1][indice_ven]=str(int(vendedores[i+1][indice_ven] + unidades))
                    
                else:
                    print('No hay suficientes articulos en el inventario')
                break
        else:
                print('El modelo no se encuentra en el inventario')
                return 
    else: 
        print('El vendedor no se encuentra registrado.')
