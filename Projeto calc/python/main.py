import re  # Para as expressões regulares
from pyscript import document

from traceback import print_exc as error







def prevenir_scripts_maliciosos(original):
    operadores = ['+', '-', '/', '*', ' ']

    # Todos os caracteres, para cada caractere na string original, devem ser um inteiro ou estar na lista de operadores 
    return all([char for char in original if char.isdigit() or char in operadores])



# Dicionário de bases
dicionario_bases = {
    '10': '₁₀',
    '2': '₂',
    '8': '₈',
    '16': '₁₆'
}
dicionario_bases2 = {
    '₁₀': '10',
    '₂': '2',
    '₈': '8',
    '₁₆': '16'  
}


letras = ['A', 'B', 'C', 'D', 'E', 'F']





def igualar_casas_binarias(numero, agrupamento):
    numero_dividido = ''
    for pos, char in enumerate(numero):
        if pos % agrupamento == 0:
            numero_dividido += ' '
            
        numero_dividido += char

    return numero_dividido




def originalmente_decimal(numero, nova_base, incremento=''):
    global letras

    if not incremento and nova_base > numero > 9: # Hexadecimal divisor > dividendo     EX: 15 / 16
        letras_invertidas = letras[::-1] # Inverter letras

        return letras_invertidas[15 - numero]
        

    resto = numero % nova_base
    numero = numero // nova_base

    if resto > 9:
        resto = letras[resto - 9 - 1]
    
    incremento += str(resto)
    
    if numero > 0:
        return originalmente_decimal(numero, nova_base, incremento)
    
    # Se o cálculo estiver completo, retorne o contrário de todo o incremento
    return incremento[::-1]



def para_decimal(numero, base_original, incremento=''):
    global letras

    numero = str(numero)
    valor_posicional = len(numero) - 1

    if numero[0] in letras:
        multiplicador = letras.index(numero[0]) + 10

    else:
        multiplicador = numero[0]
    
    incremento += f'{base_original} ** {valor_posicional} * {multiplicador} +'
    
    numero = numero[1:]
    
    if len(numero) > 0:
        return para_decimal(numero, base_original, incremento)
        
    # Se o cálculo estiver completo, retorne o contrário de todo o incremento
    return eval(incremento[:-1])


def binario_para_oh(numero, nova_base):
    global letras
    
    numero = str(numero)
    
    if nova_base == 8:
        agrupamento = 3
        
    else:
        agrupamento = 4
        
    while len(numero) % agrupamento != 0:
        numero = '0' + numero
        
    numero_dividido = ''
    for pos, char in enumerate(numero):
        if pos % agrupamento == 0:
            numero_dividido += ' '
            
        numero_dividido += char
            
    lista_binaria = numero_dividido.strip().split(' ')
    
    resultado = ''
    for binario in lista_binaria:
        novo_numero = para_decimal(binario, 2)
        
        if novo_numero > 9:
            novo_numero = letras[novo_numero - 9 - 1]
            
        resultado += str(novo_numero)


    return resultado





def oh_para_binario(numero, nova_base):
    global letras
    
    numero = str(numero)
    novo_numero = ''
    
    for char in numero:
        if char in letras:
            novo_numero += str(letras.index(char) + 10)
            
        else:
            novo_numero += char
            
        novo_numero += ' '
        
    novo_numero = novo_numero[:-1] # Tirar o ultimo caractere, que é um espaço
        
    em_binario = ''
    for char in novo_numero.split(' '):
        em_binario += ' ' + originalmente_decimal(int(char), 2)
           
    if nova_base == 8:
        agrupamento = 3
        
    else:
        agrupamento = 4
       

    em_binario = em_binario.split(' ')[1:]     # Transformar em lista e sumir com o primeiro elemento: " "
    
    
    def igualar(numero, agrupamento):
        while len(numero) % agrupamento != 0:
            numero = '0' + numero
            
        return numero
    
    em_binario = [igualar(grupo_binario, agrupamento) for grupo_binario in em_binario]
    
    #lista em_binario para int(string)
    return ''.join(em_binario)




def converter(numero, base_original, nova_base):
    global dicionario_bases2

    nbase_original = int(dicionario_bases2[base_original])
    nnova_base = int(dicionario_bases2[nova_base])

    if numero.isdigit():
        numero = int(numero)



    if nbase_original == 10: # Para bases originais decimais
        novo_numero = originalmente_decimal(numero, nnova_base)

    elif nbase_original == 2: # Para bases originais binárias
        if nnova_base == 10:
            novo_numero = para_decimal(numero, nbase_original)
        else:
            novo_numero = binario_para_oh(numero, nnova_base)

    elif nnova_base == 2: # Para converter para binário
        novo_numero = oh_para_binario(numero, nbase_original)

    elif nnova_base == 10:
        novo_numero = para_decimal(numero, nbase_original)

    else: # base_original = 8 ou 16
        cbinaria = str(oh_para_binario(numero, nbase_original))
        novo_numero = binario_para_oh(cbinaria, nnova_base)

    try: novo_numero = novo_numero.lstrip('0') # Remover 0 a esquerda
    except: pass

    return f'({novo_numero}){nova_base}'











def corrigir_base(numero, base, automatico=False): # Caso exista algum número impossível de acontecer, por exemplo o caractere "2" em binário
    global dicionario_bases2
    
    lista_bases = [2, 8, 10, 16]

    if automatico: # Significa que nenhuma base foi especificada
        intbase = int(dicionario_bases2[base]) # Pegar a base padrão

    else:
        intbase = int(base)


    if intbase != 16: # Se não for hexadecimal
        if any([char for char in str(numero) if char.isalpha()]): # any = qualquer ocorrencia / [caractere para caractere dentro de str(numero_sem_parenteses) se algum caractere for uma letra]
            intbase = 16 # Corrigir base para hexadecimal

        else:
            while any([char for char in str(numero) if int(char) > int(intbase) - 1]): # Enquanto tiver algum caractere no número original que seja maior que o da base                  EX: caractere 8 em octal (Não existe)
                novo_indice = lista_bases.index(intbase) + 1
                intbase = lista_bases[novo_indice] # base se tornará a próxima base na lista de bases até ser válido

    return str(intbase)














base_padrao = dicionario_bases['2']
base_resultado = dicionario_bases['2']

#\d+               [\dA-F]+
formatos_validos = re.compile(r"""
\([\dA-F]+\)(?:₁₀|₂|₈|₁₆)   |          # (num)baseconvertida[nada]
[\dA-F]+b(?:10|2|8|16|1)   |           # numb + basedigitada
[\dA-F]+b\d*   |                       # numb + b seguido de número ou nada (2b2)
(?: ^|\s|\+|\-|\*|\/)[\dA-F]+\b   |    # num isolado com operador antes (garantido)
\b[\dA-F]+\b   |                       # num isolado                                       
(?:\+|\-|\*|\/)   |                    # Operadores lógico
\([\dA-F]+[,.]\d+\)(?:₁₀|₂)   |        # Decimais e binários fracionários
\s                                     # Espaços
""", re.VERBOSE)

bases_invalidas = re.compile(r"""
\(([01]*[2-9A-F]+[01]*)\)(₂)|     # Base binária: qualquer número 2-9 ou letras (A-F) no meio de 0s e 1s
\(([0-7]*[8-9A-F]+[0-7]*)\)(₈)|   # Base octal: qualquer número 8-9 ou letras (A-F) no meio de 0-7
\(([0-9]*[A-F]+[0-9]*)\)(₁₀)                 # Base decimal: apenas letras (A-F são inválidas)
""", re.VERBOSE)


parentese_sem_base = re.compile(r"""
\(([\dA-F]+)\)(?:₁|₀|₆)?(?!\S)
""", re.VERBOSE)

calculo_verdadeiro = re.compile(r"""
\(([\dA-F]+)\)(₁₀|₂|₈|₁₆)|        # Normal
\(([\dA-F]+[,.]\d+)\)(₁₀|₂)|      # Fracionários
(\+|\-|\*|\/)                     # Operadores
""", re.VERBOSE)


def handle_input_change(event):
    global input, dicionario_bases, dicionario_bases2, letras
    global key_pressed, formatos_validos, parentese_sem_base, calculo_verdadeiro
    global base_resultado

    valor_input = input.value  # Pega o valor do input

    # Verificar se o caractere digitado é válido
    if valor_input and not valor_input[-1].isdigit() and not valor_input[-1] in ['A', 'B', 'C', 'D', 'E', 'F', 'b', '+', '-', '*', '/', ' ', ')', '(', ',', '.']:
        document.querySelector('#main_input').value = valor_input[:-1]
        return



    input_simplificado = re.sub(parentese_sem_base, r'\1', valor_input)
    
    valor_input_original = valor_input.strip()

    if valor_input != input_simplificado:
        valor_input = input_simplificado



    #if not key_pressed == 'b':
    garantir_formato = re.findall(formatos_validos, valor_input)

    valor_input = ' '.join(garantir_formato)

    operadores = ['+', '-', '/', '*']

    valor_sem_op_repetido = ''
    numero = True
    for char in valor_input: # Retirar sinais repetidos
        if char not in operadores: # Se char for um operador:
            if char != ' ':
                numero = True
            
            valor_sem_op_repetido += char
            
        else:
            if numero:
                valor_sem_op_repetido += char
                if char != ' ':
                    numero = False
            
    valor_input = valor_sem_op_repetido
    
    valor_input = re.sub(r'\s+', ' ', valor_input) # Retirar espaços desnecessários


    if 'b ' in valor_input or 'b1 ' in valor_input or 'bb' in valor_input: # Remover formatos inválidos de pré-inserção
        if key_pressed == ' ' and ('b1 ' in valor_input or 'b ' in valor_input):
            valor_input = valor_input.replace('b ', '').replace('b1 ', '')

        else:
            valor_input = valor_input.replace('bb', '')


    else:
        if key_pressed == ' ' and re.findall(r"(?<!\()[\dA-F]+\s(?!\))", valor_input): # Para base automática (não especificada)
            numero_sem_parenteses = list(re.finditer(r"(?<!\()[\dA-F]+\s(?!\))", valor_input))  # Formato !(     numero    !)    espaço    

            for match in numero_sem_parenteses: #  Retornar o número detectado e sua posição
                numero_sem_parenteses = match.group(0).strip()  # Número
                nstart, nend = match.span()  # Início e fim da localização do número                

            nova_base = corrigir_base(numero_sem_parenteses, base_padrao, 'Automático')
            base_formatada = dicionario_bases[nova_base]

            valor_input = valor_input[:nstart] + f'({numero_sem_parenteses}){base_formatada} ' + valor_input[nend:]
    

        else: # Para base manualmente especificada:                EX: 10b2
            regex = r"([\dA-F]+)b(\d+)" # Formato       Numero   b   Numerodabase

            ocorrencia = re.findall(regex, valor_input) #    retorna [(numero, base)]


            if ocorrencia: # Se tiver algo no formato correspondente dentro do input
                numero, base = ocorrencia[0]

                if base != '1': # Se a base atual for 1, espere o usuário digitar mais um número          EX:      9b1 pode ser 9b10 ou 9b16
                    ocorrencia_original = f'{numero}b{base}'
                    
                    base = corrigir_base(numero, base)

                    if base in list(dicionario_bases.keys()): # Se essa base realmente existir, formate    (numero)base
                        valor_input = valor_input.replace(ocorrencia_original, f'({numero}){dicionario_bases[base]} ')

                    else: # Se não existir, tire essa base, deixando só o número
                        valor_input = valor_input.replace(ocorrencia_original, numero)




    def substituir_bases_invalidas(match):
        global dicionario_bases, bases_invalidas
        
        numero = match.group(1)  # (numero) 
        base_original = match.group(0).replace(f'({numero})', '')

        if not numero: # Se numero é None, a base inválida capturada é 10
            numero = base_original.split(')')[0][1:]
            base_original = '₁₀'

        
        elif numero.isdigit():
            numero = int(numero)

        nova_base = corrigir_base(numero, base_original, 'Automático')
        
        nova_base_formatada = dicionario_bases[nova_base]
        
        return f'({numero}){nova_base_formatada}'

    valor_input = re.sub(bases_invalidas,substituir_bases_invalidas,valor_input)

    try:
        valores = re.findall(calculo_verdadeiro, valor_input)
        #print(valores)


        calculo = ''
        if valores:
            for valor in valores:          # Cada valor é uma tupla de valores (x, y, z)

                if not valor[0]: # Significa que não é um numero comum, mas sim um operador ou fracionario      EX:  (' ', ' ', '+')  ou (' ', ' ', '11,1')
                    print(valor[2:4])
                    valor = valor[2:4] # Pular valores vazios


                #print(valor)

                try: 
                    numero, base = valor[0], valor[1]
                    """
                    if ',' in numero or '.' in numero:
                        if ',' in numero:
                            numero = numero.split(',')

                        else:
                            numero = numero.split('.')

                        numero_inteiro, parte_fracionaria = int(numero[0]), 0.1 * float(numero[1])

                        # Novo numero
                        #numero = originalmente_decimal(numero_inteiro, 2) + '.' + originalmente_decimal(parte_fracionaria, 2, '*') 

                    """
                    novo_valor = converter(numero, base, '₁₀').split(')')[0][1:]
                except: # É um operador (valor único)   ['+']
                    novo_valor = valor[0]

                calculo += novo_valor + ' '

            #print(calculo)

            for i in range(2): # Trocar espaços entre números que não possuem operadores por *
                calculo = re.sub(r'([\dA-F]+)\s+([\dA-F]+)', r'\1*\2', calculo)


            calculo = calculo.replace(' ', '') # Remover todos os espaços
            if prevenir_scripts_maliciosos(calculo):
                try: 
                    resultado_em_decimal = str(eval(calculo))

                except: 
                    resultado_em_decimal = calculo[:-2].strip()
                    resultado_em_decimal = str(eval(calculo))
                
                resultado_convertido = converter(resultado_em_decimal, '₁₀', base_resultado)

                limite_de_caracteres = 50
                if len(resultado_convertido) > limite_de_caracteres:
                    resultado_convertido = resultado_convertido[:limite_de_caracteres].replace(')','') + f'...){base_resultado}'

                document.querySelector('#result').innerText = '= ' + resultado_convertido

        else:
            document.querySelector('#result').innerText = '-'

    except: print(error())


    posicao_cursor = input.selectionStart

    document.querySelector('#main_input').value = valor_input

    valor_input = valor_input.strip()


    try:
        if len(valor_input_original) > len(valor_input): # Se o tamanho do input original for maior que o tamanho atual, significa que caracteres foram deletados, então o cursor deve ser movido pra esquerda em relação à posição atual
            posicao_cursor -= len(valor_input_original) - len(valor_input)
            while valor_input[posicao_cursor] != ' ': # Se mover até o próximo espaço
                posicao_cursor -= 1

            
        elif len(valor_input_original) < len(valor_input): # Caso contrário, mover pra direita
            posicao_cursor += len(valor_input) - len(valor_input_original)
            while valor_input[posicao_cursor] != ' ': # Se mover até o próximo espaço
                posicao_cursor += 1
    
    except: pass

    input.setSelectionRange(posicao_cursor, posicao_cursor)




def detect_key(event):#
    global key_pressed

    key_pressed = event.key


def select(event):
    id = event.target.id
    opcao = int(event.target.value)

    lista_bases = [0, '2', '8', '10', '16']

    if id == 'selector_confor':
        global input, base_padrao
        valor_input = input.value
 

        nova_base = dicionario_bases[lista_bases[opcao]]


        converter_outras_bases = "₁₀|₂|₈|₁₆".replace(nova_base, "X")


        def substituido(match):
            valor = match.group(1)  # (numero)
            base_original = match.group(2)  # base
            return converter(valor, base_original, nova_base)  # String formatada


        valor_input = re.sub(rf'\(([\dA-F]+)\)({converter_outras_bases})', substituido, valor_input)

        document.querySelector('#main_input').value = valor_input
        base_padrao = nova_base

    elif id == 'selector_reba': 
        global display_resultado, base_resultado

        valor_resultado = display_resultado.textContent

        if '...' in valor_resultado: # Valor muito grande, parte da conversão será perdida
            valor_resultado = valor_resultado.replace('...', '')

        valores = re.findall(calculo_verdadeiro, valor_resultado)[0]

        if valores[0]: # Significa que há resultado
            numero, base_original = valores[0], valores[1]
            base_resultado = dicionario_bases[lista_bases[opcao]]

            novo_resultado = converter(numero, base_original, base_resultado) 
            
            document.querySelector('#result').innerText = '= ' + novo_resultado


def base_button_click(event):
    global input, dicionario_bases, dicionario_bases2

    valor_input = input.value
    input.focus()

    posicao_cursor = input.selectionStart
    nova_base = event.target.textContent
    nova_base_formatada = dicionario_bases[nova_base]

    novo_valor_input = ''
    alteracao_feita = False
    for match in re.finditer(r'(\([\dA-F]+\)(?:₁₀|₂|₈|₁₆))|[\dA-F]+', valor_input): # Pegar todos os números com base ou sem base do input
        inicio, fim = match.span()
        valor = match.group()
        if not alteracao_feita and inicio <= posicao_cursor <= fim + 1: # Verificar onde foi feita a alteração de base
            numero = match.group()                # Retorna (numero)base        ou       numero

            if ')' in numero: # Tinha base anteriormente
                numero = numero.split(')')[0][1:]             # EX:   (12)₁₀  ->   ['(12'] -> '12'
            
            valor = f'({numero}){nova_base_formatada}'

            alteracao_feita = True


        novo_valor_input += valor


    document.querySelector('#main_input').value = novo_valor_input
    handle_input_change(event) # Detectar se o formato está correto




selector_confor = document.querySelector('#selector_confor')
base_buttons = document.querySelectorAll('.base-button')

selector_reba = document.querySelector('#selector_reba')


input = document.querySelector('#main_input')
display_resultado = document.querySelector('#result')
key_pressed = None

input.onkeydown = detect_key
input.oninput = handle_input_change

selector_confor.onchange = select
selector_reba.onchange = select

for button in base_buttons:
    button.onclick = base_button_click




