from tabulate import tabulate
from abc import abstractmethod, ABC


class ConsoleOutput(ABC):

    @abstractmethod
    def show_in_console(self, data: list, headers='firstrow', format='fancy_grid'):
        pass


class TableOutput(ConsoleOutput):

    def show_in_console(self, data: list, headers='firstrow', format='fancy_grid'):
        print(tabulate(data, headers=headers, tablefmt=format, showindex='always'))


show_in_console = TableOutput.show_in_console
