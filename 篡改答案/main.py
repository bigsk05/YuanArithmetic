import re
import time
import sys
import threading
import argparse

import adbutils

from mitmproxy import http
from mitmproxy.tools.main import mitmdump

auto_jump = True

# 拦截 HTTP 响应，检查 URL 并逐个字段替换
def response(flow: http.HTTPFlow):
    # 匹配目标 URL
    url_pattern = re.compile(r"https?://xyks\.yuanfudao\.com/leo-game-pk/(iphone|android)/math/pk/match.+")
    
    # 如果 URL 匹配
    if url_pattern.match(flow.request.url):
        # 如果响应类型是 JSON
        if "application/json" in flow.response.headers.get("Content-Type", ""):
            # 读取原始响应体
            response_text = flow.response.text

            # 使用正则表达式逐个替换字段
            response_text = re.sub(r'"answer":"[0-9><=]+"', '"answer":"1"', response_text)
            response_text = re.sub(r'"answers":\["[0-9><=]+"\]', '"answers":["1"]', response_text)
            response_text = re.sub(r'"status":0', '"status":0', response_text)  # 如果其他字段也需要类似替换，可以添加

            # 更新修改后的响应体
            flow.response.text = response_text

        threading.Thread(target=answer_write, args=(len(re.findall(r'answers', flow.response.text)),)).start()

    # 检测提交
    if auto_jump and re.compile(r"https?://xyks\.yuanfudao\.com/leo-game-pk/(iphone|android)/math/pk/submit.+").match(flow.request.url):
        threading.Thread(target=jump_to_next).start()

def jump_to_next():
    # 结束，自动进下一局
    device = adbutils.adb.device()
    time.sleep(3)
    command = "input tap 540 1520"
    device.shell(command)  # “开心收下”按钮的坐标
    time.sleep(0.3)
    command = "input tap 780 1820"
    device.shell(command)  # “继续”按钮的坐标
    time.sleep(0.3)
    command = "input tap 510 1700"
    device.shell(command)  # “继续PK”按钮的坐标

def swipe_screen():
    xy = [[1310, 540], [1410, 560]]
    command = f"input swipe {xy[0][1]} {xy[0][0]} {xy[1][1]} {xy[1][0]} 0"
    
    device = adbutils.adb.device()
    device.shell(command)
    print(command)

def answer_write(answer):
    time.sleep(13)
    for _ in range(answer):
        swipe_screen()
        time.sleep(0.01)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument("-P", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    args = parser.parse_args()

    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]
    mitmdump()