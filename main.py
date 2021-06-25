import requests
import os
from lxml import etree
import xpath
import re


if __name__ == "__main__":
    url_ = input("please enter the URL: ")

    headers_ = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Cookie": "uuid=0C1604F1-1AB4-EC1A-308B-1ADD70AF333E79922infoc; buvid3=427CCCA9-51F7-4F28-8725-37A6F1CC575C184996infoc; buvid_fp=427CCCA9-51F7-4F28-8725-37A6F1CC575C184996infoc; buvid_fp_plain=427CCCA9-51F7-4F28-8725-37A6F1CC575C184996infoc; SESSDATA=8ca6ba80%2C1633805297%2C35011%2A41; bili_jct=3702c2178cf76e4e9be3315d7c905946; DedeUserID=477745681; DedeUserID__ckMd5=d8640505054832dd; sid=6x6gxn4f; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(kJmJJkR|Y~0J'uYu)k~YklJ; CURRENT_QUALITY=80; LIVE_BUVID=AUTO3716221631764540; fingerprint3=819bb7966371ceba68f3e6b745dfbdf1; fingerprint=cb4b3c78f976b2cc80fdda19e8b54e7d; fingerprint_s=584c89c4cbc7887790b046b8f69ff07f; bp_t_offset_477745681=536253665076997530; bp_video_offset_477745681=539945193755935672; PVID=5",
        "Referer": "https://www.bilibili.com/"
    }

    response_ = requests.get(url_, headers=headers_)
    data_ = response_.text

    html_boj = etree.HTML(data_)
    title_name = html_boj.xpath('//title/text()')[0]

    title_name = re.findall(r"(.*?)_哔哩哔哩_bilibili", title_name)[0]

    # print(title_name)

    url_str = html_boj.xpath("//script[contains(text(),'window.__playinfo__')]/text()")[0]
    video_url = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)",', url_str)[0]

    # print(video_url)
    audio_url = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)",', url_str)[0]

    # print(audio_url)

    headers_ = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Cookie": "uuid=0C1604F1-1AB4-EC1A-308B-1ADD70AF333E79922infoc; buvid3=427CCCA9-51F7-4F28-8725-37A6F1CC575C184996infoc; buvid_fp=427CCCA9-51F7-4F28-8725-37A6F1CC575C184996infoc; buvid_fp_plain=427CCCA9-51F7-4F28-8725-37A6F1CC575C184996infoc; SESSDATA=8ca6ba80%2C1633805297%2C35011%2A41; bili_jct=3702c2178cf76e4e9be3315d7c905946; DedeUserID=477745681; DedeUserID__ckMd5=d8640505054832dd; sid=6x6gxn4f; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(kJmJJkR|Y~0J'uYu)k~YklJ; CURRENT_QUALITY=80; LIVE_BUVID=AUTO3716221631764540; fingerprint3=819bb7966371ceba68f3e6b745dfbdf1; fingerprint=cb4b3c78f976b2cc80fdda19e8b54e7d; fingerprint_s=584c89c4cbc7887790b046b8f69ff07f; bp_t_offset_477745681=536253665076997530; bp_video_offset_477745681=539945193755935672; PVID=5",
        "Referer": url_
    }

    response_video = requests.get(video_url, headers=headers_)
    response_audio = requests.get(audio_url, headers=headers_)

    data_video = response_video.content
    data_audio = response_audio.content

    title_new = title_name + '!'

    with open(f'{title_new}.mp4', 'wb') as f:
        f.write(data_video)

    with open(f'{title_new}.mp3', 'wb') as f:
        f.write(data_audio)

    os.system(f'ffmpeg -i "{title_new}.mp4" -i "{title_new}.mp3" -c copy "{title_name}.mp4"')

    os.remove(f'{title_new}.mp4')
    os.remove(f'{title_new}.mp3')
