import requests
import sys

class ClassRoom:
    """勉強会情報

    勉強会の統計に関わる各種情報を格納するクラスです。
    最終的に集計などに用いる見込みです。
    """

    def __init__(self, title, limit, accepted, waiting):
        def or_zero(v):
            if isinstance(v, int):
                return v
            return 0
        self.title = title
        self.limit = or_zero(limit)
        self.joins = or_zero(accepted) + or_zero(waiting)
        self.score = self.joins / self.limit if self.limit != 0 else 1

    def __str__(self):
        return f'ClassRoom({self.title}, {self.limit}, {self.joins}, {self.score})'


class ClassRoomLoader:
    """ClassRoom を読み込むためのインターフェースです。
    """

    def load_class_rooms(self, month: str) -> list:
        """ClassRoom のインスタンスリストを返すインターフェース.

        Arguments:
            month {str} -- 取得対象月

        Returns:
            list -- クラスリスト
        """

        pass


class AbstractCompassAtnd(ClassRoomLoader):
    def __init__(self, api_url: str, max_event_num: int):
        self.api_url = api_url
        self.max_event_num = max_event_num


    def create_request_parameter(self, target_month: str, top: int):
        return {"ym": target_month, "count": self.max_event_num, "format": "json", "start": top}


    def request_to_compass(self, target_month: str, top: int) -> requests.Response:
        params = self.create_request_parameter(target_month, top)
        query = '&'.join([f'{key}={params[key]}' for key in params.keys()])
        print(f'Request: {query}')
        return requests.get(self.api_url + '?' + query)


    def convert(self, event) -> ClassRoom:
        try:
            return ClassRoom(event['title'], event['limit'], event['accepted'], event['waiting'])
        except:
            print(f'Error: {sys.exc_info()[0]}')
            print(f'Value: {event}')
            raise Exception('Cannot convert')


    def load_request(self, target_month: str, top: int):
        class_rooms = []
        r_get = self.request_to_compass(target_month, top)
        print(r_get.status_code)

        respond_json = r_get.json()

        for ev in respond_json['events']:
            class_rooms.append(self.convert(ev))

        return (respond_json['results_returned'], class_rooms)


    def load_class_rooms(self, month: str) -> list:
        getted = self.max_event_num
        current_top = 1
        class_rooms = []
        request = 0

        while getted == self.max_event_num:  # 最大数以下が返ってきている == まだ次がある
            request += 1

            getted, tmp_rooms = self.load_request(month, current_top)
            current_top += self.max_event_num
            class_rooms.extend(tmp_rooms)

            print(
                f'Request: {request}, Return: {getted}, currentTop: {current_top}')

        return class_rooms


class AtndLoader(AbstractCompassAtnd):
    """ATND から指定月の情報を取得するクラス.

    Arguments:
        ClassRoomLoader {ClassRoomLoader} -- ClassRoom をロードするクラス
    """
    COMPASS_API = 'http://api.atnd.org/events/'
    WANT_EVENT_NUM = 100

    def __init__(self):
        super().__init__(AtndLoader.COMPASS_API, AtndLoader.WANT_EVENT_NUM)

    def convert(self, event) -> ClassRoom:
        return super().convert(event['event'])


    def create_request_parameter(self, target_month: str, top: int):
        return {"ym": target_month, "count": self.max_event_num, "format": "json", "start": top}



class CompassLoader(ClassRoomLoader):
    """Compass から指定月の情報を取得するクラス.

    Arguments:
        ClassRoomLoader {ClassRoomLoader} -- ClassRoom をロードするクラス
    """
    COMPASS_API = 'https://connpass.com/api/v1/event/'
    WANT_EVENT_NUM = 100

    def __init__(self):
        super().__init__(CompassLoader.COMPASS_API, CompassLoader.WANT_EVENT_NUM)


    def create_request_parameter(self, target_month: str, top: int):
        return {"ym": target_month, "count": self.max_event_num, "order": 1, "start": top}


if __name__ == "__main__":
    class_rooms = AtndLoader().load_class_rooms("201904")
    print("\n".join([str(s) for s in class_rooms]))

