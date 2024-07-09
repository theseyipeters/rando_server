from urllib.parse import quote_plus

username = 'theseyipeters'
password = 'Oluwaseyi@02'

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

print(f'Encoded username: {encoded_username}')
print(f'Encoded password: {encoded_password}')
