import pprint

import requests

import nb.post
import nb.image


class MediumUser:
    def __init__(self, api_key: str):
        self._key = api_key
        user_info = self._get_user_info()
        self.__dict__.update(user_info)

    def assert_response(self, response, expected_code: int=200):
        if response.status_code != expected_code:
            formatted_message = \
                "Response Failed! Code: {} Expected: {}\n" \
                "Response-Headers:\n{}\n Repsonse-Body:\n{}\n".format(
                    response.status_code, expected_code,
                    pprint.pformat(dict(response.headers.items())),
                    response.raw.read()
                )
            print(formatted_message)
            raise AssertionError(formatted_message)

        return response.json()["data"]

    def _do_authed_get(self, resource: str) -> dict:
        response = requests.get(
            resource,
            headers={"Authorization": "Bearer " + self._key}
        )
        return self.assert_response(response)

    def _do_authed_put(self, resource: str, json):
        pprint.pprint((resource, json))
        response = requests.post(
            resource,
            headers={"Authorization": "Bearer " + self._key},
            json=json
        )
        return self.assert_response(response, expected_code=201)

    def _get_user_info(self):
        return self._do_authed_get("https://api.medium.com/v1/me")

    def get_my_posts(self):
        return self._do_authed_get(
            "https://api.medium.com/v1/users/" + self.id + "/publications")

    def new_post(self, post: nb.post.Post):
        post.validate_post()
        return self._do_authed_put(
            "https://api.medium.com/v1/users/" + self.id + "/posts",
            post.to_json()
        )

    def update_post(self, post: nb.post.Post):
        pass

    def upload_image(self, image: nb.image.MediumImage):
        self._do_authed_put(

        )
