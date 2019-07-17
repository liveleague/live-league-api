import requests

def send_email(url, headers, response):
    url = "https://api.sendinblue.com/v3/smtp/email"
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'api-key': """xkeysib-89806c8caff61d84f23c55
                      6438982606fd7908565ceb07b62cc0
                      25383605837e-zXEW93Ub0k1mfA5s"""
    }
    response = requests.request("POST", url, headers=headers)
    print(response.text)
