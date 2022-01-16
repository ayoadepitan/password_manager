import getpass
from os import close
import re
import csv
import random
import string
from checkmypass import password_check


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


def get_password():
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
    return password


def get_website():
    # Checks if input is valid website
    while True:
        website = input('Website: ')
        if check_website(website):
            break
        print('Not a valid website. Please try again')
    return website


def get_email():
    # Checks if input is valid email
    while True:
        email = input('Email: ')
        if check_email(email):
            break
        print('Not a valid email. Please try again')
    return email


def get_info():
    website = get_website()
    email = get_email()
    password = get_password()
    write_to_csv(website, email, password)


def write_to_csv(website, email, password):
    # Writes do database.csv
    with open('database.csv', mode='a', newline='') as database:
        csv_writer = csv.writer(database)
        csv_writer.writerow([website, email, password])


def read_csv():
    with open('database.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)


def website_exist():
    with open('database.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        website = input(
            'Enter the full website url you would like to Edit/Delete: ')
        for row in reader:
            if row['Website'] == website:
                return row
        print('Website does not exist. Try again...')
        return None


def delete_website():
    delete_row = None
    while delete_row == None:
        delete_row = website_exist()

    new_rows = []
    with open('database.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if delete_row['Website'] != row['Website']:
                new_rows.append(row)

    with open('database.csv', 'w', newline='') as csvfile:
        fieldnames = ['Website', 'Email', 'Password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in new_rows:
            writer.writerow(row)


def edit_csv():
    new_row = None
    while new_row == None:
        new_row = website_exist()

    print('Select which one to change...')

    while True:
        try:
            choice2 = int(
                input('\n1 - Password\n2 - Email\n3 - Website\n'))
        except ValueError:
            print('\nPlease enter a valid number.')
            continue
        if choice2 == 1:
            new_password = get_password()
            for key, value in new_row.items():
                if key == 'Password':
                    new_row[key] = new_password
        if choice2 == 2:
            new_email = get_email()
            for key, value in new_row.items():
                if key == 'Email':
                    new_row[key] = new_email
        if choice2 == 3:
            new_website = get_website()
            for key, value in new_row.items():
                if key == 'Website':
                    website = new_row[key]
                    new_row[key] = new_website
        break

    with open('database.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        new_rows = []
        for row in reader:
            if new_website:
                if website == row['Website']:
                    new_rows.append(row)
            new_rows.append(
                new_row) if new_row['Website'] == row['Website'] else new_rows.append(row)

    with open('database.csv', 'w', newline='') as csvfile:
        fieldnames = ['Website', 'Email', 'Password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in new_rows:
            writer.writerow(row)


def main():
    print('What do you want to do?')
    while True:
        try:
            choice = int(
                input('\n0 - End Session\n1 - Create\n2 - List\n3 - Check\n4 - Edit\n5 - Delete\n'))
        except ValueError:
            print('\nPlease enter a valid number.')
            continue
        if choice == 0:
            print('\nSession Ended')
            break
        elif choice == 1:
            get_info()
        elif choice == 2:
            read_csv()
        elif choice == 3:
            password_check(input(
                'Check the number of times a password has been breach.\nEnter any number of passwords: \n').split())
        elif choice == 4:
            edit_csv()
        elif choice == 5:
            delete_website()
        else:
            print('\nNot a valid choice. Try again...')


if __name__ == '__main__':
    main()
