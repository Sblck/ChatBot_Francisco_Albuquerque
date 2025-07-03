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
            print("DEBUG resposta:", resposta)
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
        apikey = "Zq675bviMboZ3K6bRlke9TpXQl53U5fB"
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{simbolo}?apikey={apikey}"
        try:
            resposta = url_request(url)
            if not resposta or not resposta.strip().startswith('['):
                return "Erro ao obter cotação: Limite de requisições atingido ou resposta inválida da API."
            data = json.loads(resposta)
            if data and isinstance(data, list) and 'price' in data[0]:
                return f"A cotação atual de {simbolo} é ${data[0]['price']}"
            else:
                return f"Não foi possível obter a cotação para '{simbolo}'."
        except Exception as e:
            return f"Erro ao obter cotação: {e}"


    def resposta_conversao_moeda() -> str:
        
        '''
        Conversoa de moeda usando (exchangerate.host)
        '''
        moedas_disponiveis = {
            '1': 'EUR',
            '2': 'USD',
            '3': 'BRL',
            '4': 'GBP',
            '5': 'JPY'
        }

        def mostrar_menu():
            print('Escolha a moeda:')
            for chave, valor in moedas_disponiveis.items():
                print(f'{chave} - {valor}')
            return moedas_disponiveis

        def modo_conversao():
            print('Moeda de origem:')
            moedas = mostrar_menu()
            op_origem = input('Digite o número da moeda de origem: ')
            moeda_origem = moedas.get(op_origem)
            if not moeda_origem:
                return None
            print('Moeda de destino:')
            moedas = mostrar_menu()
            op_destino = input('Digite o número da moeda de destino: ')
            moeda_converter = moedas.get(op_destino)
            if not moeda_converter:
                return None
            return (moeda_origem, moeda_converter)

        def conversao(moedas, valor):
            moeda_origem, moeda_converter = moedas
            apikey = "41b52179a4fbb952ea8ef628aa90edf9"
            url = f"https://api.exchangerate.host/convert?from={moeda_origem}&to={moeda_converter}&amount={valor}&access_key={apikey}"
            resposta = url_request(url)
            data = json.loads(resposta)
            if data.get('success') and 'result' in data:
                convertido = data['result']
                taxa = data['info']['quote']
                return (convertido, taxa)
            else:
                raise ValueError('Não foi possível obter a taxa de câmbio.')

        def formatar(moedas, valores, resultado):
            moeda_origem, moeda_converter = moedas
            valor = valores[0]
            convertido, taxa = resultado
            return f"{valor} {moeda_origem} equivalem a {convertido:.2f} {moeda_converter} (taxa: {taxa:.4f})"

        return fluxo_interativo(modo_conversao, ["Valor a converter: "], conversao, formatar)
    
    
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
    

    def resposta_recomendacao_filmes() -> str:
        '''
        Recomenda filmes usando a API do TMDB.
        fonte: https://developer.themoviedb.org/reference/intro/getting-started
        '''
        apikey = "5534120401107e1e58645bb7090ef0bf"

        opcoes = {
            '1': ('Populares', f"https://api.themoviedb.org/3/movie/popular?api_key={apikey}&language=pt-PT&page=1"),
            '2': ('Melhor avaliados', f"https://api.themoviedb.org/3/movie/top_rated?api_key={apikey}&language=pt-PT&page=1")
        }

        def menu_filmes():
            print("Escolha o tipo de recomendação:")
            for k, (nome, _) in opcoes.items():
                print(f"{k} - {nome}")
            escolha = input("Digite o número da opção: ")
            return escolha if escolha in opcoes else None

        def obter_filmes(tipo, *_):
            if tipo not in opcoes:
                raise ValueError("Opção inválida")
            url = opcoes[tipo][1]
            resposta = url_request(url)
            data = json.loads(resposta)
            filmes = data.get('results', [])
            return filmes[:10]

        def formatar(modo, valores, filmes):
            if not filmes:
                return "Não foi possível obter recomendações no momento."
            lista = [f"{i+1}. {filme['title']} ({filme.get('release_date', 's/ data')[:4]})" for i, filme in enumerate(filmes)]
            return "Sugestões de 10 filmes:\n" + "\n".join(lista)

        return fluxo_interativo(menu_filmes, [], obter_filmes, formatar)
    

    def resposta_cores() -> str:
        '''
        Cor complementar/oposta de uma cor dada pelo utilizador.
        Aceita entrada em RGB (255,0,0) ou nome (vermelho).
        Usa a conversão para o espaço HSL (hue,saturation,luminosity)
        '''

        # TODO - Rever range de cada "cor", clamp 
        nomes_cores = {
            'vermelho': (255, 0, 0),
            'verde': (0, 255, 0),
            'azul': (0, 0, 255),
            'amarelo': (255, 255, 0),
            'ciano': (0, 255, 255),
            'magenta': (255, 0, 255),
            'preto': (0, 0, 0),
            'branco': (255, 255, 255),
            'laranja': (255, 165, 0),
            'roxo': (128, 0, 128)
        }
        nomes_cores_inv = {v: k for k, v in nomes_cores.items()}

        entrada = input("Digite uma cor (nome ou RGB, ex: 255,0,0): ").strip().lower()
        if ',' in entrada:
            try:
                r, g, b = [int(x) for x in entrada.split(',')]
            except Exception:
                return "Formato inválido! Use: 255,0,0 para RGB"
        elif entrada in nomes_cores:
            r, g, b = nomes_cores[entrada]
        else:
            return "Cor não reconhecida. Tente nomes básicos ou RGB."
        
        def rgb_para_hsl(r, g, b):
            r, g, b = [x / 255.0 for x in (r, g, b)]
            mx = max(r, g, b)
            mn = min(r, g, b)
            l = (mx + mn) / 2
            if mx == mn:
                h = s = 0
            else:
                d = mx - mn
                s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
                if mx == r:
                    h = (g - b) / d + (6 if g < b else 0)
                elif mx == g:
                    h = (b - r) / d + 2
                else:
                    h = (r - g) / d + 4
                h /= 6
            return round(h * 360), round(s * 100), round(l * 100)
        
        
        resultado = nomes_cores_inv.get((r,g,b))
        return f"A cor é : {resultado} :"



    respostas = {
         ('olá', 'boa tarde', 'bom dia'): 'Olá tudo bem!',
         'como estás': 'Estou bem, obrigado!',
         ('bye', 'adeus', 'tchau'): 'Gostei de falar contigo! Até breve...',
         ('minha localização', 'onde estou'): resposta_localizacao,
         ('tempo', 'metereologia'): resposta_metereologia,
         ('calcular', 'calculadora', 'somar', 'subtrair', 'multiplicar', 'dividir') : resposta_calculadora,
         ('cores','complementa') : resposta_cores,
         ('converte', 'temperatura') : resposta_conversao_temperatura,
         ('peso') : resposta_conversao_peso,
         ('cotação', 'ação', 'ações', 'stock', 'preço ação'): reposta_obter_cotacao_acao,
         ('converte', 'moeda', 'câmbio', 'cambio'): resposta_conversao_moeda,
         ('jogo', 'adivinhar') : adivinhador,
         ('recomendação filmes','filmes', 'top filmes') : resposta_recomendacao_filmes,

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