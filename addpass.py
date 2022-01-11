import getpass
import re


def check_website(website):
    # Regex for validating website
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, website) is not None


def check_email(email):
    # Regex for validating an email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    return re.fullmatch(regex, email)


def get_info():
    while True:
        website = input('Website: ')
        if check_website(website):
            break
        print('Not a valid website. Please try again')

    while True:
        email = input('Email: ')
        if check_email(email):
            break
        print('Not a valid email. Please try again')
    password = getpass.getpass()


get_info()
