# Exame-backend-dtlabs-2025

Teste técnico com o objetivo de avaliar as seguintes competências:

* Desenvolvimento de APIs.
* Desenvolvimento de testes.
* Lógica de programação.
* Engenharia de Software.

## Case

Você irá desenvolver o backend de uma aplicação de IoT. Seu produto consiste em um
servidor que está localizado on-premise no seu cliente. Este servidor coleta dados de
diversos sensores. Os servidores enviam para um único banco de dados. Cada servidor
comporta até 4 (quatro) sensores diferentes:

- Sensor de Temperatura.
    * Valores são medidos em graus celsius.
- Sensor de Umidade.
    * Valores são medidos em %, de 0 a 100.
- Sensor de Tensão Elétrica.
    * Valores são medidos em Volts.
- Sensor de Corrente Elétrica.
    * Valores são medidos em Ampère.

É possível que um servidor tenha um sensor de temperatura e um sensor de umidade.
Portanto, eles enviam os dois valores na mesma requisição. Cada servidor vai possuir
apenas 1 (um) sensor de cada. Logo, não existem servidores que possuem 3 (três)
sensores de temperatura e 1 (um) sensor de corrente elétrica.

Os servidores podem enviar dados com uma frequência de, no mínimo, 1 Hz, e, no máximo, 10 Hz.

A seguir, serão descritos os endpoints necessários para serem implementados e descritivo do que eles devem fazer.


## Como rodar

### Requisitos

* [Docker compose](https://docs.docker.com/compose/)

1. Clone esse repositório e entre no diretório clonado:

   ```bash
   git clone https://github.com/joaovs2004/exame-backend-dtlabs-2025
   cd exame-backend-dtlabs-2025
   ```
2. Crie uma SECRET_KEY com openssl e escreva no .env:

   ```bash
   openssl rand -hex 32 > .env
3. Rode o projeto com:

    ```bash
    docker compose up
4. Acesse localhost:8000/docs para testar a Api

Os testes serão rodados automaticamente