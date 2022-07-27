import requests
from json import JSONEncoder

from kivy.network.urlrequest import UrlRequest


class HttpManager(object):
    appointments = 'api/appointments/get-appointments/'
    products = 'api/products/get-available-products/'
    remove_product = 'api/products/delete-product/'
    adjust_product = 'api/products/edit-product/'
    orders = 'api/products/get-orders/'
    messages = 'api/products/get-messages/'
    reply = 'api/products/create-reply/'
    customers = 'api/accounts/get-customers/'
    registration = 'api/accounts/register/'
    login = 'api/accounts/login/'
    headers = {'Content-type': 'application/json'}

    def __init__(self):
        self.domain = 'http://127.0.0.1:8000/'

    def user_login(self, username: str, password: str, on_complete, on_error):

        def http_200_ok(request, result):
            token = result.get('token')
            if on_complete:
                on_complete(token)

        def http_400_bad_request(request, response):
            message = ''
            for key in response.keys():
                text = f'Error!\n {response[key][0]}\n'
                message += text
            if on_error:
                on_error(message)

        def http_500_server_error(request, response):
            if on_error:
                on_error('Check your connection!')

        body = {"username": f"{username}", "password": f"{password}"}
        params = JSONEncoder().encode(body)
        UrlRequest(url=self.domain + self.login,
                   req_body=params,
                   req_headers=self.headers,
                   on_success=http_200_ok,
                   on_error=http_500_server_error,
                   on_failure=http_400_bad_request)

    def register_user(self, email: str, username: str, password: str, password2: str, on_complete, on_error):

        def http_200_ok(request, response):
            if on_complete:
                on_complete(response)

        def http_500_server_error(request, response):
            if on_error:
                if response.get('email'):
                    on_error(response.get('email'))
                else:
                    on_error('Check your connection!')

        body = {"email": email, "username": f"{username}", "password": f"{password}", "password2": password2}
        params = JSONEncoder().encode(body)
        UrlRequest(url=self.domain + self.registration,
                   req_body=params,
                   req_headers=self.headers,
                   on_success=http_200_ok,
                   on_error=http_500_server_error,
                   on_failure=http_500_server_error)

    def get_data(self, model: str, token: str):
        """ Function that gets data depending on model (appointments, products, orders, customers or messages) """
        request = UrlRequest(self.domain + eval(f'self.{model}'), req_headers={'Authorization': f'Token {token}'})
        request.wait()
        return request.result

    def send_reply(self, on_complete, on_error, body, token: str):

        def success(request, response):
            if on_complete:
                on_complete('Successfully sent!')

        def failure(request, response):
            if on_error:
                on_error('Failed!')

        UrlRequest(url=self.domain + self.reply,
                   req_body=body,
                   req_headers={'Content-type': 'application/json', 'Authorization': f'Token {token}'},
                   on_success=success,
                   on_failure=failure)

    def edit_product(self, body, token: str):
        requests.post(self.domain + self.adjust_product, data=body, headers={'Authorization': f'Token {token}'})

    def delete_product(self, product_id, token: str):
        body = {'id': product_id}
        requests.post(self.domain + self.remove_product, data=body, headers={'Authorization': f'Token {token}'})


http_manager = HttpManager()
