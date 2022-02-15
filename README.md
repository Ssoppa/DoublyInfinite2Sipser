# DoublyInfinite2Sipser

**O que é:**

O objetivo deste trabalho é trabalhar a simulação entre modelos de máquina de Turing. Para isto, será utilizada a sintaxe disponível no simulador online de máquinas de Turing em http://morphett.info/turing/turing.html

O trabalho consistirá na programação de um "tradutor" de modelos de máquina de Turing. A entrada será um arquivo texto com extensão .in com um programa para o simulador online, consistindo em um programa para a máquina de Turing utilizando fita duplamente infinita, podendo fazer uso de movimento estacionário. A saída deve ser um arquivo texto com extensão .out com um programa capaz de ser executado no simulador a partir do modelo de fita semi-infinita (modelo de Sipser), podendo fazer uso de movimento estacionário.

Todos os programas dados como entrada serão para reconhecimento de linguagens sobre o alfabeto {0,1}.

**Como rodar:**

Utilizando Python 3.6.9 rode o seguinte comando:
```sh
$ python main.py <arquivo de entrada>
```

Pegue o resultado no arquivo teste.out e coloque no simulador citado anteriormente, junto com uma respectiva entrada.

Utilizando o exemplo de verificação da quantidade de 0 e 1:
```sh
$ python main.py sameamount10.in
```

**Exemplos:**

Alguns exemplos inclusos são:

1 - sameamount10.in, verifica se a quantidade de 0 e 1 são iguais

2 - teste.in, verifica se a entrada é um palíndromo binário

3 - teste1.in, realiza a conversão de binário para decimal

4 - teste2.in, veririca se o numério binário é primo (teste pesado)