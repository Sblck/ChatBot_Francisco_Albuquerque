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
    
    
    def resposta_calculadora() -> str:
        '''
        Calcular várias operações entre dois numeros por input do utilizador
        Suporta soma, subtração, multiplicação, divisão e exponenciação
        Fork: https://github.com/Sblck/Calculadora
        Repo Original: https://github.com/cbarata-formador/Calculadora

        '''
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

        try:
            operador = menu_operacoes()
            if operador is None:
                return 'Opção inválida!'
            num1 = float(input('Digite o primeiro número: '))
            num2 = float(input('Digite o segundo número: '))
            resultado = calculadora(num1, num2, operador)
            return f' {num1} {operador} {num2} = {resultado}'

        except ValueError:
            print('Dados inválidos! -> Tente novamente!')
        except ZeroDivisionError:
            print('Impossível dividir por zero! -> Tente novamente!')

    respostas = {
         ('olá', 'boa tarde', 'bom dia'): 'Olá tudo bem!',
         'como estás': 'Estou bem, obrigado!',
         ('bye', 'adeus', 'tchau'): 'Gostei de falar contigo! Até breve...',
         ('minha localização', 'onde estou'): resposta_localizacao,
         ('tempo', 'metereologia'): resposta_metereologia,
         ('calcular', 'calculadora') : resposta_calculadora

     }
    
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