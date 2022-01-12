import getpass
import re
import csv
import random
import string


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


def password_generator(size):
    # Generates random string according to the size inputted
    return ''.join(random.choices(string.ascii_letters + string.digits + '!@?#$&', k=size))


def get_info():
    # Checks if input is valid website
    while True:
        website = input('Website: ')
        if check_website(website):
            break
        print('Not a valid website. Please try again')

    # Checks if input is valid email
    while True:
        email = input('Email: ')
        if check_email(email):
            break
        print('Not a valid email. Please try again')

    # Asks if you want to generate a password
    # If yes then it runs password_generator() and returns random string
    # If no then it asks for you to enter your own password that's hidden.
    while True:
        type = input('Do you want to generate a random password? (y/n): ')
        if type in {'y', 'Y', 'yes', 'Yes'}:
            while True:
                try:
                    length = int(
                        input('Password length: '))
                    break
                except ValueError:
                    print('Oops! That wasn\'t a valid number. Try again...')
            password = password_generator(length)
            break
        elif type in {'n', 'N', 'no', 'No'}:
            password = getpass.getpass()
            break
        else:
            print('Not a valid answer. Try again...')

    write_to_csv(website, email, password)


def write_to_csv(website, email, password):
    # Writes do database.csv
    with open('database.csv', mode='a', newline='') as database:
        csv_writer = csv.writer(database)
        csv_writer.writerow([website, email, password])


get_info()
