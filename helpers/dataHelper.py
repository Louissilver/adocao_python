def retornar_data(valor):
    data = valor.split('/')
    dia, ano = int(data[0]), int(data[2])
    if(data[1][0] != 0):
        mes = int(data[1])
    else:
        mes = int(data[1].replace("0", ""))
    return dia, mes, ano
