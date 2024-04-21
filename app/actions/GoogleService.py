from googleapiclient.discovery import build


class GoogleService:
    def __init__(self, api_key, cx):
        try:
            self.cx = cx
            self.service = build("customsearch", "v1", developerKey=api_key)
        except Exception as e:
            raise Exception(f"Cannot create google service: {e}")

    def askGoogle(self, phrase):
        try:
            request = self.service.cse().list(
                q=phrase,
                cx=self.cx,
            )
            response = request.execute()
            return response
        except Exception as e:
            raise Exception(f"Cannot get google response: {e}")
