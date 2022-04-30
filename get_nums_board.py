from bs4 import BeautifulSoup
import requests


def get_nums_board():
    url = "https://nine.websudoku.com/"
    data = BeautifulSoup(requests.get(url).text, "html.parser")

    table = list(list(list(data.body.table.tr.children)[5].table.children)[3].td.form.children)[4].div.table.find_all("tr")

    board_list = []
    for tr in table:  # For each tr from table
        all_td = tr.find_all("td")
        for td_num in range(len(tr)):  # For each td from tr
            input_tag = all_td[td_num].input
            if input_tag.attrs.get("readonly") is not None:
                board_list.append(int(input_tag.attrs["value"]))
            else:
                board_list.append(0)

    # List[list] in which each list has the index for a number in 1D_array
    list_block = []
    for i in range(81):
        lst = []

        if i in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
            for j in range(3):
                lst.append((j * 9) + i)
                lst.append((j * 9) + (i + 1))
                lst.append((j * 9) + (i + 2))

            list_block.append(lst)

    final_list = [[] for _ in range(9)]
    for i in range(9):
        for j in list_block[i]:
            final_list[i].append(board_list[j])

    return final_list


print("Web scraping data; Finished!\n")
