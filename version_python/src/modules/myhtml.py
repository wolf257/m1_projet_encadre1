#!/usr/bin/env python3
# -*- coding : utf8 -*-


def generate_html_head(file, charset='utf8', title="sans_titre"):
    head = """
    <!DOCTYPE html>
    <html lang="fr" dir="ltr">
        <head>
            <meta charset={}>
            <title> {} </title>
            <link rel="stylesheet" href="style.css">
        </head>

        <body>

    """.format(charset, title)

    with open(file, mode='w', encoding="utf8") as fileout:
        fileout.write(head)


def generate_html_tail(file):
    tail = """

        </body>
    </html>
    """

    with open(file, mode='a', encoding="utf8") as fileout:
        fileout.write(tail)


def generate_html_table_open(file):
    with open(file, mode='a', encoding="utf8") as fileout:
        opening = """<table border='2'>"""
        fileout.write(opening)


def generate_html_table_main_row(file, listContent):
    with open(file, mode='a', encoding="utf8") as fileout:
        therow = '<tr> '
        for i in range(len(listContent)):
            therow += '\n\t<td>'+'<strong>'+str(listContent[i])+'</strong>'+'</td> '
        therow += ' </tr>'
        fileout.write(therow)
        fileout.write('\n')


def generate_html_table_other_row(file, listContent):
    with open(file, mode='a', encoding="utf8") as fileout:
        therow = '<tr> '
        for i in range(len(listContent)):
            therow += '\n\t<td>'+str(listContent[i])+'</td> '
        therow += ' </tr>'
        fileout.write(therow)
        fileout.write('\n')


def generate_html_table_close(file):
    with open(file, mode='a', encoding="utf8") as fileout:
        closing = """</table>"""
        fileout.write(closing)


def append_line_to_html(file, sentence):
    with open(file, mode='a', encoding="utf8") as fileout:
        fileout.write(sentence)

def main():
    test_html = 'test.html'

    table_data = [
        ['Smith',       'John',         30],
        ['Carpenter',   'Jack',         47],
        ['Johnson',     'Paul',         62],
    ]

    generate_html_head(test_html)
    generate_html_table_open(test_html)
    for row in table_data :
        generate_html_table_other_row(test_html, row)
    generate_html_table_close(test_html)
    generate_html_tail(test_html)

if __name__ == '__main__':
    main()
