def mas_vendedor(vendedores):
    fila = len(vendedores)
    col = len(vendedores[0])
    total=[]
    
    for c in range(col):
        suma = 0
        for f in range(1,fila):
            suma += int(vendedores[f][c])
        total.append(suma)
    num_max = max(total)
    indice_max=total.index(num_max)
    v_max=print(f'El vendedor que más vendió articulos fue {vendedores[0][indice_max]} con {num_max} articulos vendidos\n')
    return v_max
