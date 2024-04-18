from requests import get


def get_quote_of_the_day():
    resp_dict = get('https://favqs.com/api/qotd').json()
    quote_data = resp_dict['quote']
    answer_dict = {
        "author": quote_data['author'],
        "quote": quote_data['body']
    }
    return answer_dict


if __name__ == "__main__":
    print(get_quote_of_the_day())
