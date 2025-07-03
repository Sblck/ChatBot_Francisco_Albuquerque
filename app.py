import os, urllib.request, json
from datetime import datetime

def obter_resposta(texto: str) -> str:


    def url_request(url: str) -> str:
        try:
            with urllib.request.urlopen(url) as response:
                return response.read().decode()
        except Exception as e:
            return f'Desculpa, não consegui obter a informação! {e}'

    def obter_localizacao_via_ip() -> dict:
        try:
            url: str = "http://ip-api.com/json/"
            resposta = url_request(url)
            data = json.loads(resposta)
            return data['city'], data['country']
        except Exception as e:
            return f'Desculpa, não consegui obter a localização! {e}'
        
    def obter_metereologia() -> dict:
        '''
        Obter a metereologia da localização do utilizador
        Fonte: https://wttr.in
        Exemplo: http://wttr.in/Lisboa?format=3
        Referencia: https://github.com/chubin/wttr.in
        Formato:
        '''
        try:
            url = f"http://wttr.in/{obter_localizacao_via_ip()[0]}?format=3"
            data = url_request(url)
            return data
        except Exception as e:
            return f'Desculpa, não consegui obter a metereologia! {e}'
        
    def descompactar(valor: tuple, template: str) -> str:
        if isinstance(valor, tuple):
            return template.format(*valor)
        

    def resposta_localizacao() -> str:
        return f'{descompactar(obter_localizacao_via_ip(), "Estás na cidade de {} em {}")}'
    

    def resposta_metereologia() -> str:
        return f'{obter_metereologia()}'
    
    def fluxo_interativo(menu_func, input_msgs, calc_func, format_func):
        try:
            modo = menu_func()
            if modo is None:
                raise ValueError
            valores = []
            for msg in input_msgs:
                valores.append(float(input(msg)))
            resultado = calc_func(modo, *valores)
            return format_func(modo, valores, resultado)
        except ValueError:
            return 'Dados inválidos!'
        except ZeroDivisionError:
            return 'Impossível dividir por zero!'

    def calculadora(num1: float, num2: float, operador: str) -> float:
        """
        Usar nan como valor inicial é uma boa prática. 
        Se o operador fornecido não corresponder a nenhuma das opções válidas (+, -, etc.), a função retornará nan, 
        sinalizando que o cálculo não pôde ser realizado.
        """
        result = float("nan")
        if operador == '+':
            result = num1 + num2
        elif operador == '-':
            result = num1 - num2
        elif operador == '*':
            result = num1 * num2
        elif operador == '/':
            if num2 == 0:
                raise ZeroDivisionError
            result = num1 / num2
        elif operador == '^':
            result = num1 ** num2
        return result

    def resposta_calculadora() -> str:
        '''
        Calcular várias operações entre dois numeros por input do utilizador
        Suporta soma, subtração, multiplicação, divisão e exponenciação
        Fork: https://github.com/Sblck/Calculadora
        Repo Original: https://github.com/cbarata-formador/Calculadora
        '''

        def menu_operacoes() -> str:
            print('Escolha a operação:')
            print('1 - Soma (+)')
            print('2 - Subtração (-)')
            print('3 - Multiplicação (*)')
            print('4 - Divisão (/)')
            print('5 - Exponenciação (^)')
            opcao = input('Digite o número da operação desejada: ')
            if opcao == '1':
                return '+'
            elif opcao == '2':
                return '-'
            elif opcao == '3':
                return '*'
            elif opcao == '4':
                return '/'
            elif opcao == '5':
                return '^'
            else:
                return None

        def calc(operador, num1, num2):
            return calculadora(num1, num2, operador)

        def formatar(operador, valores, resultado):
            num1, num2 = valores
            return f'{num1} {operador} {num2} = {resultado}'

        return fluxo_interativo(menu_operacoes, ['Digite o primeiro número: ', 'Digite o segundo número: '], calc, formatar)

    def resposta_conversao_temperatura() -> str:
        '''
        Conversão de temperaturas (Celsius e Fahrenheit).
        '''
        C_PARA_F = 1
        F_PARA_C = 2

        def modo_conversao() -> int:
            print('Escolha o tipo de conversão:')
            print(f'{C_PARA_F} - Celsius para Fahrenheit')
            print(f'{F_PARA_C} - Fahrenheit para Celsius')
            opcao = input(f'Digite {C_PARA_F} ou {F_PARA_C}: ')
            if opcao == str(C_PARA_F):
                return C_PARA_F
            elif opcao == str(F_PARA_C):
                return F_PARA_C
            else:
                return None
 
 
        def conversao(modo: int, valor: float) -> float:
            # C para F -> (valor * 9 / 5) + 32
            if modo == C_PARA_F:
                return calculadora(calculadora(calculadora(valor, 9, '*'), 5, '/'), 32, '+')
            # F para C -> (valor - 32) * 5 / 9
            elif modo == F_PARA_C:
                return calculadora(calculadora(calculadora(valor, 32, '-'), 5, '*'), 9, '/')

        def formatar(modo, valores, resultado):
            temp = valores[0]
            if modo == C_PARA_F:
                return f'{temp}°C equivalem a {resultado:.2f}°F'
            else:
                return f'{temp}°F equivalem a {resultado:.2f}°C'
     

        return fluxo_interativo(modo_conversao, ["Valor da temperatura para conversão: "], conversao, formatar)

    def resposta_conversao_peso() -> str:
        '''
        Conversão de peso entre quilogramas (kg) e libras (lb).
        '''
        KG_PARA_LB = 1
        LB_PARA_KG = 2

        def modo_conversao() -> int:
            print('Escolha o tipo de conversão:')
            print(f'{KG_PARA_LB} - Quilogramas para Libras')
            print(f'{LB_PARA_KG} - Libras para Quilogramas')
            opcao = input(f'Digite {KG_PARA_LB} ou {LB_PARA_KG}: ')
            if opcao == str(KG_PARA_LB):
                return KG_PARA_LB
            elif opcao == str(LB_PARA_KG):
                return LB_PARA_KG
            else:
                return None

        def conversao(modo: int, valor: float) -> float:
            # 1 kg = 2.20462 lb
            if modo == KG_PARA_LB:
                return calculadora(valor, 2.20462, '*')
            # 1 lb = 0.453592 kg
            elif modo == LB_PARA_KG:
                return calculadora(valor, 0.453592, '*')
            

        def formatar(modo, valores, resultado):
            temp = valores[0]
            if modo == KG_PARA_LB:
                return f'{temp} kg equivalem a {resultado:.2f} lb'
            else:
                return f'{temp} lb equivalem a {resultado:.2f} kg'

        return fluxo_interativo(modo_conversao, ["Valor do peso para conversão: "],conversao, formatar)


    def reposta_obter_cotacao_acao() -> str:
        simbolo = input("Digite o símbolo da ação (ex: AAPL, MSFT, TSLA): ").upper()
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={simbolo}"
        try:
            resposta = url_request(url)
            data = json.loads(resposta)
            resultado = data['quoteResponse']['result']
            if not resultado:
                return f"Não encontrei cotação para o símbolo '{simbolo}'."
            preco = resultado[0].get('regularMarketPrice')
            nome = resultado[0].get('shortName', simbolo)
            if preco is not None:
                return f"A cotação atual de {nome} ({simbolo}) é ${preco}"
            else:
                return f"Não foi possível obter o preço para '{simbolo}'."
        except Exception as e:
            return f"Erro ao obter cotação: {e}"

    def adivinhador() -> str:
        contador = 0
        min = 1
        max = 100
        print('==== Adivinhador ====')
        print(f'Pense num número entre {min} e {max}')

        while contador < 7 and min < max:
            valor = (min + max) // 2
            resposta = input(f'O seu número é maior que {valor}? (s/n): ').strip().lower()
            if resposta in ('sim', 's'):
                min = valor + 1
            else:
                max = valor
            contador += 1

        return f'O seu número é {min}'
    
    respostas = {
         ('olá', 'boa tarde', 'bom dia'): 'Olá tudo bem!',
         'como estás': 'Estou bem, obrigado!',
         ('bye', 'adeus', 'tchau'): 'Gostei de falar contigo! Até breve...',
         ('minha localização', 'onde estou'): resposta_localizacao,
         ('tempo', 'metereologia'): resposta_metereologia,
         ('calcular', 'calculadora', 'somar', 'subtrair', 'multiplicar', 'dividir') : resposta_calculadora,
         ('converte', 'temperatura') : resposta_conversao_temperatura,
         ('peso') : resposta_conversao_peso,
         ('cotação', 'ação', 'ações', 'stock', 'preço ação'): reposta_obter_cotacao_acao,
         ('jogo', 'adivinhar') : adivinhador,

     }
    
    # TODO - Acrescentar pelo menos 10 novas interações que o chatbot possa responder e testá-las
    
    def processar_resposta(resposta):
        return resposta() if callable(resposta) else resposta

    comando: str = texto.lower()

    for chave, resposta in respostas.items():
        if isinstance(chave, tuple) and any(k in comando for k in chave):
            return processar_resposta(resposta)
        elif isinstance(chave, str) and chave in comando:
            return processar_resposta(resposta)
         
    if 'horas' in comando:
        return f'São: {datetime.now():%H:%M} horas'
    if 'data' in comando:
        return f'Hoje é dia: {datetime.now():%d-%m-%Y}'

    return f'Desculpa, não entendi a questão! {texto}'


def chat() -> None:
    print('Bem-vindo ao ChatBot!')
    print('Escreva "bye" para sair do chat')
    name: str = input('Bot: Como te chamas? ')
    print(f'Bot: Olá, {name}! \n Como te posso ajudar?')

    while True:
        user_input: str = input('Tu: ')
        resposta: str = obter_resposta(user_input)
        print(f'Bot: {resposta}')

        if resposta == 'Gostei de falar contigo! Até breve...':
            break

    print('Chat acabou')
    print()


def main() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    chat()


if __name__ == '__main__':
    main()