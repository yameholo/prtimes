import json
from typing import List, Dict
from requests_oauthlib import OAuth1Session

from poptimes.twitter_key import CK, CS, AT, ATS

URL = 'https://api.twitter.com/1.1/search/tweets.json'

API = OAuth1Session(CK, CS, AT, ATS)


def create_params(q: str) -> Dict[str, str]:
    return {
        'count': 30,      # 取得するtweet数
        'q': q  # 検索キーワード
    }


def get_tweet_user(title: str) -> List[Dict[str, str]]:
    """
    {title}のことについて呟いた人のユーザー情報

    :param title: (str) 記事のタイトル
    :return: [
        {
            "name": "name"
            "user_url": "profile url by twitter"
            "icon_url": "profile image url by twitter"
        }
    ]
    """
    res = API.get(URL, params=create_params(title))
    if res.status_code == 200:
        return [
            {
                "name": tweet["user"]["name"],
                "user_url": "https://twitter.com/"+tweet["user"]["screen_name"],
                "icon_url": tweet["user"]["profile_image_url_https"]
            }
            for tweet in json.loads(res.text)['statuses']]
    raise RuntimeError("リクエストが上手く行きませんでした。")


if __name__ == '__main__':
    print(json.dumps(get_tweet_user("テスト"), indent=2))
