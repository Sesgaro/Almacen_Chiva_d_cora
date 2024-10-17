import flet as ft
import os
import csv
from typing import Dict

os.environ["FLET_SECRET_KEY"] = os.urandom(12).hex()

def main(page: ft.Page):
    page.bgcolor="#1f262f"
    # page.vertical_alignment="center"
    # page.horizontal_alignment="center"

    #Lee archivo reciente subido y guardado en el mismo codigo
    def reciente(event: ft.ContainerTapEvent):
        recent=open("temp.txt", "r")
        aux=recent.read()
        archivo_seleccionado.value=aux
        recent.close()
        return (leer_resultados())

    #Carga de archivos
    def file_picker_result(event: ft.FilePickerResultEvent):
        barras_progreso.clear()
        archivos.current.controls.clear()

        if event.files is not None:
            for f in event.files:
                pbr_archivo = ft.ProgressRing(value=0, bgcolor='#eeeeee', width=20, height=20)
                barras_progreso[f.name] = pbr_archivo
                archivo_seleccionado.value=f.name
                
                recent=open("temp.txt", "w")
                recent.write(f.name)
                recent.close

                items=[pbr_archivo, ft.Text(f.name)]
                archivos.current.controls.append(ft.Row(items,alignment=ft.MainAxisAlignment.CENTER))
        
        page.update()
        return (upload_files(None))
    
    #Ordena matriz de los vendedores
    def elmejor(fila):
        suma=sum(c for c in fila[1:] if isinstance(c, (int, float)))
        return suma

    def on_upload_progress(event: ft.FilePickerUploadEvent):
        barras_progreso[event.file_name].value = event.progress
        barras_progreso[event.file_name].update()

        if barras_progreso[event.file_name].value==1:
            return(leer_resultados())
    
    file_picker = ft.FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

    def upload_files(event):
        lista_archivos = []

        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                lista_archivos.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600)
                    )
                )
            
            file_picker.upload(lista_archivos)

    #Boton de volver
    def volver_fun(e):
        datos_ven(messi,vend_buscado.value)
        datos_pro()
        the_best_product.visible=False
        llegada.disabled=False
        venta.disabled=False
        agregar_pro.visible=False
        registra_ven.visible=False
        volver.disabled=True
        vend_buscado.value=""
        claves.value=""
        claves_ven.value=""
        empleado.value=""
        cantidad_ven.value=0
        cantidad_pro.value=0
        page.update()

    
    #Al momento de cargarse el archivo, se lee y se separan datos en 2 matrizes
    def leer_resultados():        

        global matrix_pro,x,y,matrix_ven,messi,num

        num=0

        messi=False
        
        page.snack_bar = ft.SnackBar(ft.Text("Espera un momento, estamos analizando el archivo"))
        page.snack_bar.open = True
        page.update()
            
        try:
                
                archivo=open(f"uploads/{archivo_seleccionado.value}",'r')
                datos=csv.reader(archivo)
                
                fil=[]

                matrix=[]
                matrix_pro=[]
                matrix_ven=[]

                for fila in datos:
                    matrix.append(fila)
                x=len(matrix)
                y=len(matrix[0])
                archivo.close()
                auxven=False
                opc=True
                for i in range(x):
                    for j in range(y):
                        try:
                            matrix[i][j]=int(matrix[i][j])
                        except ValueError:
                            pass
                        if matrix[i][j]=='':
                            matrix[i][j]=0
                for i in range(x):
                    for j in range(y):
                        pass
                        if j<=2:
                            fil.append(matrix[i][j])
                    
                    if matrix[i][0]=='Vendedores':
                        auxven=True
                        opc=False
                    if auxven:
                        matrix_ven.append(matrix[i])
                    if opc:
                        matrix_pro.append(fil)
                        fil=[]
                
                print(*matrix, sep='\n')
                print()
                print()
                
                print(*matrix_pro, sep='\n')
                print()
                print(*matrix_ven, sep='\n')
                
                llegada.disabled=False
                venta.disabled=False

                tabla_pro.update()
                page.snack_bar = ft.SnackBar(ft.Text("Listo!"))
                page.snack_bar.open = True
                datos_pro()
                datos_ven(messi,vend_buscado.value)
                
                
                    
        except Exception as ex:
                t.value = str(ex)
                print(str(ex))
                page.snack_bar = ft.SnackBar(ft.Text("Error, hablale al tecnico"))
                page.snack_bar.open = True
                page.update()        
    
    #Se imprime la tabla de productos
    def datos_pro():
        checker.disabled=False
        try:
            grafica.visible=False
            # tabla_vend.visible = False
            # pro_btn.disabled=True
            grafica.update()

            carga.visible=True
            carga.update()

            t.visible=False
            t.update()
            
            tabla_pro.rows.clear()
            filas=len(matrix_pro)
            for fila in range(filas):
                if fila==0:
                    continue

                tabla_pro.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(matrix_pro[fila][i])))for i in range(3)
                    ]
                )
            )
            
            carga.visible=False
            carga.update()
            tabla_pro.update()
            t.value="Hola!, bienvenido ;)"
            t.visible=True
            t.update()
            select_btn.visible=False
            # vend_btn.disabled=False
            tabla_pro.visible = True

            grafica.visible=True
            grafica.update()
            
            columna_archivos.visible=False
            recent_btn.visible=False
            page.update()
            
        except Exception as ex:
            t.value = str(ex)
            print(str(ex))

    #Se imprime tabla de vendedores
    def datos_ven(messi,buscado):
        try:
            grafica.visible = False
            # tabla_pro.visible = False
            # vend_btn.disabled = True

            carga.visible = True
            carga.update()

            tabla_vend.rows.clear()
            tabla_vend.columns.clear()

            filas=matrix_ven[1:]
            columnas=matrix_ven[0]
            if messi:
                filas_ord = sorted(filas, key=elmejor, reverse=True)

                matrix_ord=[columnas]+filas_ord
                tabla_vend.columns.extend(
                    [ft.DataColumn(ft.Text(celda)) for celda in matrix_ord[0]]
                )

                for fila in matrix_ord[1:]:
                    j=len(fila)

                    if buscado != '' and buscado in fila[0]:
                        tabla_vend.rows.append(
                            ft.DataRow(
                                cells=[ft.DataCell(ft.Text(str(fila[i]))) for i in range(j)]
                            )
                        )
                    else:
                        if buscado=='':
                            # tabla_vend.rows.append(
                            #     ft.DataRow(
                            #         cells = [ft.DataCell(ft.Text(medalla + str(fila[i]))) if i == 0 else ft.DataCell(ft.Text(str(fila[i]))) for i in range(y)]
                            #     )
                            # )

                            tabla_vend.rows.append(
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("🥇"+str(fila[i]))) if i == 0 and matrix_ord[1][0]==fila[i] else ft.DataCell(ft.Text(str(fila[i])))for i in range(j)
                                    ]
                                )
                            )

            else:
                tabla_vend.columns.extend(
                    [ft.DataColumn(ft.Text(celda)) for celda in matrix_ven[0]]
                )
                for fila in matrix_ven[1:]:
                    if buscado != '' and buscado in fila[0]:
                        print(buscado)
                        tabla_vend.rows.append(
                            ft.DataRow(
                                cells=[ft.DataCell(ft.Text(str(celda))) for celda in fila]
                            )
                        )
                    else:
                        if buscado == '':
                            tabla_vend.rows.append(
                                ft.DataRow(
                                    cells=[ft.DataCell(ft.Text(str(celda))) for celda in fila]
                                )
                            )
            carga.visible = False
            carga.update()
            tabla_vend.update()

            t.update()
            select_btn.visible = False
            # pro_btn.disabled = False
            tabla_vend.visible = True
            grafica.visible = True
            grafica.update()

            columna_archivos.visible = False
            recent_btn.visible = False

        except Exception as ex:
            t.value = str(ex)
            print(str(ex))

    #Botton de check
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        if e.control.checked:
            messi=True
            datos_ven(messi,vend_buscado.value)
        else:
            messi=False
            datos_ven(messi,vend_buscado.value)

        page.update()
    
    #Identifica solo valores enteros para los productos
    def enteros(e):
        try:
            num=int(e.control.value)
            print("valor: ",num)
            error2_pro.value=""
            error2_pro.update()
        except:
            num=0
            error2_pro.value="INTRODUCE VALORES ENTEROS"
            error2_pro.update()
    def enteros_ven(e):
        try:
            num=int(e.control.value)
            print("valor: ",num)
            error2_ven.value=""
            error2_ven.update()
        except:
            num=0
            error2_ven.value="INTRODUCE VALORES ENTEROS"
            error2_ven.update()
    #Busca vendedor
    def buscar_vendedor(e):
        vend_buscado.value = e.control.value.upper()
        datos_ven(messi,vend_buscado.value)

    #LLegada de articulos
    def llegada_articulos(e:ft.ContainerTapEvent):
        volver.disabled=False
        grafica.visible=False
        t.visible=False
        checker.disabled=True
        agregar_pro.visible=True
        aux=0
        productos=len(matrix_pro)
        num=int(cantidad_pro.value)
        page.update()   
        
        try:
            clave = claves.value.upper()
            llegada.disabled=True
            venta.disabled=True


            for i in range(productos):
                if clave == matrix_pro[i][1] and clave != '':
                    aux=i
                    error1_pro.value=""
                    error1_pro.update()
                    break
                elif clave != '' and clave != matrix_pro[i][1]:
                    error1_pro.value="ERROR, CLAVE NO ENCONTRADA"
                else:
                    pass
            if aux != 0 and aux>0 and num != 0:
                res=matrix_pro[aux][2]+num
                matrix_pro[aux][2]=res
                page.snack_bar = ft.SnackBar(ft.Text("Cambio realizado, puedes volver para ver los cambios :)"))
                page.snack_bar.open = True
                matrix_new=matrix_pro+matrix_ven
                print(*matrix_new, sep='\n')
                num=0
                archivo=open(f"uploads/{archivo_seleccionado.value}",'w',newline='')
                datos=csv.writer(archivo)
                datos.writerows(matrix_new)
                archivo.close()

                page.update()
                
            else:
                print(num)
                page.snack_bar = ft.SnackBar(ft.Text("No se realizo ningun cambio"))
                page.snack_bar.open = True
                page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(str(ex)))
            page.snack_bar.open = True
            page.update()
            clave = ''
    def producto_mas_vendido(e):
        ventas = []
        aux_ps=0
        c_de_vend=len(matrix_ven[1:])
        for i in range(c_de_vend):
            ventas.append(0)
        for fila in matrix_ven[1:]:
            for i in range(1, len(fila)):
                ventas[i - 1] += int(fila[i])
        
        aux_ventas=len(ventas)
        for i in range(aux_ventas):
            if ventas[i]>ventas[aux_ps]:
                aux_ps=i
            else:
                pass
        print(ventas)
        the_best_product.visible=True
        the_best_product.value=f"El producto mas vendido es {matrix_ven[0][aux_ps+1]}"
        the_best_product.update()

    #Vender
    def registra_venta(e:ft.ContainerTapEvent):
        volver.disabled=False
        grafica.visible=False
        t.visible=False
        checker.disabled=True
        registra_ven.visible=True
        aux=0
        num=int(cantidad_ven.value)
        page.update()   
        
        try:
            clave = claves_ven.value.upper()
            llegada.disabled=True
            venta.disabled=True

            listas_vende=len(matrix_ven)

            empleado_aux = empleado.value.upper()
            for i in range(listas_vende):
                    if empleado_aux == matrix_ven[i][0]:
                        aux_emp=i
                        error_ven.value="Empleado valido"
                        error_ven.color="#00ff00"
                        error_ven.update()
                        break

                    elif empleado_aux != '' and empleado_aux != matrix_ven[i][0]:
                        error_ven.value="ERROR, EMPLEADO NO ENCONTRADO"
                        error_ven.color="#ff0000"
                        error_ven.update()

                    else:
                        pass
            for i in range(listas_vende):
                if clave == matrix_pro[i][1] and clave != '':
                    aux=i
                    error1_ven.value=""
                    error1_ven.update()
                    break
                elif clave != '' and clave != matrix_pro[i][1]:
                    error1_ven.value="ERROR, CLAVE NO ENCONTRADA"
                else:
                    pass
            if aux != 0 and aux>0 and num != 0 and aux_emp != 0:
                        
                # if aux_emp != 0:
                res=matrix_pro[aux][2]-num
                if res >=0:
                    matrix_pro[aux][2]=res
                    matrix_ven[aux_emp][aux]+=num
                    page.snack_bar = ft.SnackBar(ft.Text("Cambio realizado, puedes volver para ver los cambios :)"))
                    page.snack_bar.open = True
                    matrix_new=matrix_pro+matrix_ven
                    print(*matrix_new, sep='\n')
                    num=0
                    archivo=open(f"uploads/{archivo_seleccionado.value}",'w',newline='')
                    datos=csv.writer(archivo)
                    datos.writerows(matrix_new)
                    archivo.close()

                    page.update()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("No se puede hacer esto, cantidad no disponible"))
                    page.snack_bar.open = True
                
            else:
                print(num)
                page.snack_bar = ft.SnackBar(ft.Text("No se realizo ningun cambio"))
                page.snack_bar.open = True
                page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(str(ex)))
            print(str(ex))
            page.snack_bar.open = True
            page.update()
            clave = ''
        

    #Menu Expandible
    volver=ft.PopupMenuItem(icon=ft.icons.ARROW_BACK,text="Volver", on_click=volver_fun,disabled=True)
    llegada=ft.PopupMenuItem(icon=ft.icons.POWER_INPUT, text="Llegada de productos",on_click=llegada_articulos,disabled=True)
    checker=ft.PopupMenuItem(text="Mejor Empleado", checked=False, on_click=check_item_clicked,disabled=True)
    venta=ft.PopupMenuItem(icon=ft.icons.SHOP, text="Registrar venta",on_click=registra_venta,disabled=True)

    pb = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Funciones"),
            volver,
            llegada,
            venta,
            ft.PopupMenuItem(),
            checker,
        ]
    )
    page.add(pb)
            
    page.scroll='auto'

    page.overlay.append(file_picker)

    barras_progreso: Dict[str, ft.ProgressRing] = {}

    archivos = ft.Ref[ft.Column]()

    #Llegada de articulos

    texto_pro=ft.Text("Llegada de productos",size=30)

    claves=ft.TextField(label="Introduce la clave del producto", width=200)

    cantidad_pro=ft.TextField(label="Introduce la cantidad",value=0, on_change=enteros ,width=200)

    error1_pro=ft.Text("",color="#ff0000",italic=True)
    error2_pro=ft.Text("",color="#ff0000",italic=True)

    subir_pro = ft.ElevatedButton('Actualizar datos', icon=ft.icons.SAVE, on_click=llegada_articulos)

    lista_productos=[texto_pro,claves,error1_pro,cantidad_pro,error2_pro, subir_pro]

    agregar_pro=ft.Container(
        visible=False,

        alignment=ft.alignment.center,

        content=ft.Column(lista_productos,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    #Registro de venta

    texto_venta=ft.Text("Registrar venta",size=30)

    # cantidad_venta=ft.TextField(label="Introduce la cantidad",value=0, on_change=enteros ,width=200)
    empleado=ft.TextField(label="Introduce el empleado", width=200)
    
    error_ven=ft.Text("",color="#ff0000",italic=True)
    claves_ven=ft.TextField(label="Introduce la clave del producto", width=200)

    cantidad_ven=ft.TextField(label="Introduce la cantidad",value=0, on_change=enteros_ven ,width=200)

    error1_ven=ft.Text("",color="#ff0000",italic=True)
    error2_ven=ft.Text("",color="#ff0000",italic=True)

    subir_ven = ft.ElevatedButton('Actualizar datos', icon=ft.icons.SAVE, on_click=registra_venta)

    lista_venta=[texto_venta,empleado,error_ven,claves_ven,error1_ven,cantidad_ven,error2_ven,subir_ven]

    registra_ven=ft.Container(
        visible=False,

        alignment=ft.alignment.center,

        content=ft.Column(lista_venta,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    
    #Tabla de productos
    mas_vendido = ft.ElevatedButton('Consultar producto mas vendido', icon=ft.icons.KING_BED, on_click=producto_mas_vendido)

    tabla_pro=ft.DataTable(
        border=ft.border.all(2, "#3f3f3f"),
        border_radius=10,
        divider_thickness=0,
        bgcolor="#2a2e33",
        vertical_lines=ft.border.BorderSide(2, "#4f4f4f"),
        horizontal_lines=ft.border.BorderSide(1, "#4f4f4f"),
        column_spacing=10,
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Clave")),
            ft.DataColumn(ft.Text("Cantidad")),
        ],
        rows=[]
    )

    #Tabla de Vendedores

    buscador = ft.TextField(label="Buscar empleado", on_change=buscar_vendedor ,width=200)

    tabla_vend=ft.DataTable(
        border=ft.border.all(2, "#3f3f3f"),
        border_radius=10,
        divider_thickness=0,
        bgcolor="#2a2e33",
        vertical_lines=ft.border.BorderSide(2, "#4f4f4f"),
        horizontal_lines=ft.border.BorderSide(1, "#4f4f4f"),
        column_spacing=10,
        columns=[
            ft.DataColumn(ft.Text("Vendedores")),
        ],
        rows=[]
    )

    archivo_info = ft.FilePicker(on_result=leer_resultados)

    archivo_seleccionado = ft.Text()
    
    t=ft.Text(size=30)
    vend_buscado=ft.Text('')

    #Bienvenida

    carga=ft.ProgressRing(visible=False)
    
    select_btn = ft.ElevatedButton('Selecciona un archivo', icon=ft.icons.FOLDER_OPEN, on_click=lambda _: file_picker.pick_files(allow_multiple=False,allowed_extensions=["csv"]))
    
    recent_btn = ft.ElevatedButton('Abrir el mas reciente', icon=ft.icons.FOLDER_OPEN, on_click=reciente)
    try:
        recent=open("temp.txt", "r")
        aux=recent.read()
        if aux == '':
            recent_btn.disabled=True
            recent.close()
        else:
            select_btn.disabled=True
    except:
        recent=open("temp.txt", "w")
        recent.close()
        recent_btn.disabled=True


    columna_archivos = ft.Column(ref=archivos,horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    concarga=ft.Container(alignment=ft.alignment.center,height=300,content=carga)

    #Interfaz
    the_best_product=ft.Text(size=30)

    items_grafica=[tabla_pro,mas_vendido,the_best_product,buscador,tabla_vend]

    grafica=ft.Container(
        visible=False,
        alignment=ft.alignment.center,

        content=ft.Column(items_grafica,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    
    col = ft.Column(spacing=10,horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[select_btn, recent_btn, columna_archivos, t, grafica, agregar_pro,registra_ven, concarga])

    contenedor = ft.Container(col, alignment=ft.alignment.top_center, margin=0,)
    
    #Se inicializa la ventana
    page.add(
        contenedor
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER, upload_dir='uploads')
