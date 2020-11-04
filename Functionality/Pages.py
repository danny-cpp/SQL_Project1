from prettytable import PrettyTable


class Pages:
    def __init__(self, record_list, page_number, col_name=[]):
        self.__page_number = page_number
        self.__record_list = record_list
        self.__col_name = col_name

    # This function is for internal call only, it print pages of the record
    def printPages(self):
        table = PrettyTable()
        table.field_names = self.__col_name

        for row in self.__record_list[self.__page_number]:
            row = list(row)

            # if len(row[2]) > 30:
            #     row[2] = row[2][:27] + "..."
            #
            # if len(row[3]) > 45:
            #     row[3] = row[3][:42] + "..."

            table.add_row(row)

        # aligning text:
        table.align["pid"] = 'l'
        table.align["title"] = 'l'
        table.align["content"] = 'l'
        table.align["poster"] = 'l'

        print(table)
        print(f"                                        Page {self.__page_number + 1}/{len(self.__record_list)}")
        print("\nTo navigate through the result pages, enter 'prev' or 'next'.")

    # This function display the next page
    def nextPage(self):
        if self.__page_number + 1 >= len(self.__record_list):
            print("\nEND OF TABLE\n")
            self.printPages()
            return
        else:
            self.__page_number += 1
            self.printPages()

    def prevPage(self):
        if self.__page_number - 1 < 0:
            print("\nEND OF TABLE\n")
            self.printPages()
            return
        else:
            self.__page_number -= 1
            self.printPages()


if __name__ == '__main__':
    record = [[('p100', 'relational'), ('p100', 'database')],
              [('p200', 'relational'), ('p200', 'sql')], [('p500', 'Database')]]

    bookkeeper = Pages(record, 0)
    bookkeeper.printPages()
    bookkeeper.nextPage()
    bookkeeper.nextPage()
    bookkeeper.nextPage()
    bookkeeper.prevPage()
    bookkeeper.prevPage()