def mas_vendido(matrix,vendedores):
    total_v=[]
    for i in range(len(matrix[1])):
        suma = 0
        for f in range(len(vendedores[0])):
            suma += int(vendedores[i+1][f])
        total_v.append(suma)

    ind_max=total_v.index(max(total_v))

    clave = matrix[1][ind_max]
    descr = matrix[0][ind_max]
    desc = print(f"Modelo con mas unidades vendidas: '{descr}'.\nClave del articulo: {clave}. \nLa cantidad de articulos vendidos: {max(total_v)}.")
    return clave, desc
