import os
import sys


class Trabalho:
    def __init__(self, entrada: str):
        self.entrada = entrada
        if os.path.split(entrada)[0] != "":
            self.saida = f'{os.path.split(entrada)[0] + "/" + os.path.basename(entrada).split(".")[0]}.out'
        else:
            self.saida = f'{os.path.split(entrada)[0] + os.path.basename(entrada).split(".")[0]}.out'
        self.input = None
        self.output = None
        self.aux = None
        self.simbolos = []
        self.estados = []

    def abre_arquivo(self):
        self.input = open(self.entrada, "r")
        self.output = open(self.saida, "w")
        self.aux = open("aux.txt", "w")

        for line in self.input:
            if len(line.split()) == 5:
                cur_state, cur_symbol, new_symbol, direction, new_state = line.split()

                if cur_symbol not in self.simbolos:
                    self.simbolos.append(cur_symbol)
                if new_symbol not in self.simbolos:
                    self.simbolos.append(new_symbol)

                if cur_state not in self.estados:
                    self.estados.append(cur_state)
                if new_state not in self.estados and new_state[:4] != 'halt':
                    # Segundo o http://morphett.info/turing/turing.html, se começa com halt é a parada
                    self.estados.append(new_state)

    def modifica_estado_0(self):
        first = True
        self.input = open(self.entrada, "r")  # O python está fechando automaticamente após o uso de cada função
        self.aux = open("aux.txt", "w")  # O python está fechando automaticamente após o uso de cada função

        for line in self.input:
            if len(line.split()) == 5:
                cur_state, cur_symbol, new_symbol, direction, new_state = line.split()
                old_cur_state = f"old_{cur_state}"
                if new_state[:4] != 'halt':
                    old_new_state = f"old_{new_state}"
                else:
                    old_new_state = new_state
                if first:
                    self.aux.write(f"{old_cur_state} {cur_symbol} {new_symbol} {direction} {old_new_state}\n")
                    first = False
                else:
                    self.aux.writelines(f"{old_cur_state} {cur_symbol} {new_symbol} {direction} {old_new_state}\n")

        self.output = open(self.saida, "w")  # O python está fechando automaticamente após o uso de cada função
        self.output.write("0 0 & r was_0\n")
        self.output.writelines("0 1 & r was_1\n")
        self.output.writelines("was_0 0 0 r was_0\n")
        self.output.writelines("was_0 1 0 r was_1\n")
        self.output.writelines("was_0 _ 0 r was_u\n")
        self.output.writelines("was_1 0 1 r was_0\n")
        self.output.writelines("was_1 1 1 r was_1\n")
        self.output.writelines("was_1 _ 1 r was_u\n")
        self.output.writelines("was_u _ # l go_back\n")
        self.output.writelines("go_back & & r old_0\n")
        self.output.writelines("go_back * * l go_back\n")

    def acrescenta_verificao_inicio(self):
        new_lines = []
        for estado in self.estados:
            new_lines.append(f"old_{estado} & & r add_u_old_{estado}")

            for simbolo in self.simbolos:
                new_simbolo = simbolo
                if simbolo == '_':
                    new_simbolo = 'u'

                new_lines.append(f"add_u_old_{estado} {simbolo} _ r was_{new_simbolo}_old_{estado}")

            for simbolo in self.simbolos:
                new_simbolo = simbolo
                if simbolo == '_':
                    new_simbolo = 'u'

                for simbolo_interno in self.simbolos:
                    new_simbolo_interno = simbolo_interno
                    if simbolo_interno == '_':
                        new_simbolo_interno = 'u'
                    new_lines.append(
                        f"was_{new_simbolo}_old_{estado} {simbolo_interno} {simbolo} r was_{new_simbolo_interno}_old_{estado}")

                new_lines.append(
                    f"was_{new_simbolo}_old_{estado} # {simbolo} r was_#_old_{estado}")

            new_lines.append(f"was_#_old_{estado} _ # l go_back_old_{estado}")
            new_lines.append(f"go_back_old_{estado} & & r old_{estado}")
            new_lines.append(f"go_back_old_{estado} * * l go_back_old_{estado}")

        for linha in new_lines:
            self.aux.writelines(f"{linha}\n")

    def acrescenta_verificao_fim(self):
        self.aux = open("aux.txt", "a")  # O python está fechando automaticamente após o uso de cada função
        for estado in self.estados:
            new_line1 = f"old_{estado} # _ r was_old_{estado}"
            new_line2 = f"was_old_{estado} _ # l old_{estado}"
            self.aux.writelines(f"{new_line1}\n")
            self.aux.writelines(f"{new_line2}\n")

    def fecha_arquivos(self):
        self.aux = open("aux.txt", "r")  # O python está fechando automaticamente após o uso de cada função
        self.output = open(self.saida, "a")  # O python está fechando automaticamente após o uso de cada função
        for linha in self.aux:
            self.output.writelines(linha)

        if self.input is not None:
            self.input.close()

        if self.output is not None:
            self.output.close()

        if self.aux is not None:
            self.aux.close()
            os.remove("aux.txt")

    def transforma(self):
        self.abre_arquivo()
        self.modifica_estado_0()
        self.acrescenta_verificao_inicio()
        self.acrescenta_verificao_fim()
        self.fecha_arquivos()


def main():
    if len(sys.argv) < 2:
        print("Entre com o nome do arquivo de entrada!")
        exit()
    trabalho = Trabalho(sys.argv[1])
    trabalho.transforma()


if __name__ == '__main__':
    main()


# TODO: testar com movimento estacionário
