from strugglebusapi.users.requests import auth_user

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from users import get_single_user, update_user


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:
            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return(resource, key, value)

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return(resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = ""
        elif len(parsed) == 3:
            (resource, key, value) = parsed
            if key == "email" and resource == "user":
                response = auth_user(value)

        self.wfile.write(response.encode())

    # def do_POST(self):
    #     self._set_headers(201)
    #     content_len = int(self.headers.get('content-length', 0))
    #     post_body = self.rfile.read(content_len)

    #     post_body = json.loads(post_body)
    #     (resource, id) = self.parse_url(self.path)

    #     if resource == "users":
    #         new_user = None
    #         new_user = create_user(post_body)
    #         self.wfile.write(f"{new_user}".encode())
    #     elif resource == "articles":
    #         new_article = None
    #         new_article = create_article(post_body)
    #         self.wfile.write(f"{new_article}".encode())
    #     elif resource == "tags":
    #         new_tag = None
    #         new_tag = create_tag(post_body)
    #         self.wfile.write(f"{new_tag}".encode())
    #     elif resource == "categories":
    #         new_article = None
    #         new_article = create_category(post_body)
    #         self.wfile.write(f"{new_article}".encode())
    #     elif resource == "comments":
    #         new_comment = None
    #         new_comment = create_comment(post_body)
    #         self.wfile.write(f"{new_comment}".encode())

    # def do_DELETE(self):
    #     self._set_headers(204)
    #     (resource, id) = self.parse_url(self.path)
    #     if resource == 'users':
    #             delete_user(id)
    #     elif resource == 'articles':
    #             delete_article(id)
    #     elif resource == 'categories':
    #         delete_category(id)
    #     elif resource == 'tags':
    #         delete_tag(id)
    #     elif resource == 'comments':
    #         delete_comment(id)
    #     self.wfile.write("".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        success = False
        if resource == "users":
            success = update_user(id, post_body)
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        self.wfile.write("".encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.end_headers()


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
