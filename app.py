import os, urllib.request, json
from datetime import datetime

def obter_resposta(texto: str) -> str:

    def obter_localizacao_via_ip() -> dict:
        try:
            url: str = "http://ip-api.com/json/"
            with urllib.request.urlopen(url) as response:
                if response:
                    data = json.loads(response.read().decode())
                    return data['city'], data['country']
                else:
                    return f'Desculpa, não consegui obter a localização!'
        except Exception as e:
            return f'Desculpa, não consegui obter a localização! {e}'
        
    def descompactar(valor: tuple, tamanho: int, template: str) -> str:
        if isinstance(valor, tuple) and len(valor) == tamanho:
            return template.format(*valor)
        return valor

    respostas = {
         ('olá', 'boa tarde', 'bom dia'): 'Olá tudo bem!',
         'como estás': 'Estou bem, obrigado!',
         ('bye', 'adeus', 'tchau'): 'Gostei de falar contigo! Até breve...',
         ('minha localização', 'onde estou'): descompactar(obter_localizacao_via_ip(), 2, "Estás na cidade de {} em {}"),
     }

    comando: str = texto.lower()

    for chave, resposta in respostas.items():
         if isinstance(chave, tuple):
             if comando in chave:
                 return resposta
         elif chave in comando:
            return resposta
         
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