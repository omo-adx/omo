import hashlib
import hmac
import base64
import json
import time
import threading
import websocket
from websocket import create_connection

from urllib.parse import quote
import logging
import pyaudio
import requests
import ssl
import jsonpath
from sample import ne_utils, aipass_client

class Client():
    def __init__(self, app_id, api_key):
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = "ws://rtasr.xfyun.cn/v1/ws"
        self.ts = str(int(time.time()))
        tt = (self.app_id + self.ts).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding='utf-8')

        apiKey = self.api_key.encode('utf-8')
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        self.end_tag = "{\"end\": true}"
        self.buffer = []
        self.complete_sentences = []
        self.triggered = False
        self.trigger_sentences = []
        self.current_role = 0

        self.ws = create_connection(self.base_url + "?appid=" + self.app_id + "&ts=" + self.ts + "&signa=" + quote(signa) + "&roleType=2")
        self.connected = True
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()
        self.last_recv_time = time.time()
        self.check_timeout()

    def send(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        
        try:
            while self.connected:
                data = stream.read(1280)
                self.ws.send(data)
                time.sleep(0.04)
        except websocket.WebSocketConnectionClosedException:
            print("WebSocket connection closed unexpectedly.")
        except KeyboardInterrupt:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            if self.connected:
                self.ws.send(bytes(self.end_tag.encode('utf-8')))
                print("send end tag success")

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                self.last_recv_time = time.time()
                if len(result) == 0:
                    print("receive result end")
                    break
                result_dict = json.loads(result)
                action = result_dict.get("action", "")
                if action == "started":
                    print("Handshake success, result:", result_dict["desc"])
                elif action == "result":
                    data = json.loads(result_dict["data"])
                    if "cn" in data and "st" in data["cn"] and "rt" in data["cn"]["st"]:
                        sentence = ""
                        role = 0
                        for rt in data["cn"]["st"]["rt"]:
                            for ws in rt["ws"]:
                                for cw in ws["cw"]:
                                    sentence += cw["w"]
                                    role = int(cw.get("rl", 0))
                                    # 打印触发角色
                                    if role != 0:
                                        print("Role:", role)
                        if ("欧墨" in sentence) or ("Omar" in sentence) or ("omar" in sentence) or ("欧盟" in sentence):
                            self.triggered = True
                            self.current_role = role
                            print("Trigger detected!")
                        if data["cn"]["st"]["type"] == "0":  # Complete sentence
                            if self.triggered and role == self.current_role:
                                self.trigger_sentences.append(sentence)
                            self.complete_sentences.append(sentence)
                            print(sentence)
                elif action == "error":
                    print("RTASR error:", result_dict["desc"])
                    self.close()
                    return
        except websocket.WebSocketConnectionClosedException:
            print("receive result end")

    def check_timeout(self):
        if time.time() - self.last_recv_time > 1.5:
            if self.triggered:
                self.close()
                print("connection closed due to timeout")
                print("Transcribed text after trigger: ", ' '.join(self.trigger_sentences))
                self.send_to_chatgpt(' '.join(self.trigger_sentences))
            else:
                print("Still listening...")
                self.last_recv_time = time.time()
                threading.Timer(1, self.check_timeout).start()
        else:
            threading.Timer(1, self.check_timeout).start()

    def send_to_chatgpt(self, text):
        headers = {
            "Authorization": "Bearer sk-BU8Fh1RQcGBapCPK6bDaC60567Da4d88B46f889cBd167dA9",
            "Content-Type": "application/json"
        }
        data = {
            "model": "tianli",
            "messages": [

                {
                    "role": "user",
                    "content": text
                }
            ]
        }
        response = requests.post("https://openai.tianli0.top/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            print("Full GPT response:", result)
            if 'choices' in result:
                print("GPT response:", result['choices'][0]['message']['content'])
                self.text_to_speech(result['choices'][0]['message']['content'])
            else:
                print("No 'choices' in response")
        else:
            print("Failed to get response from ChatGPT, status code:", response.status_code)
            print("Response content:", response.content)

    def text_to_speech(self, text):
        with open("./resource/input/1.txt", "w", encoding="utf-8") as f:
            f.write(text)
        request_data = {
            "header": {
                "app_id": APPId,
                "status": 0
            },
            "parameter": {
                "oral": {
                    "oral_level": "mid",
                    "spark_assist": 1,
                    "scenarized": 0
                },
                "tts": {
                    "vcn": "x4_lingxiaoxuan_oral",
                    "volume": 50,
                    "speed": 50,
                    "pitch": 50,
                    "bgs": 0,
                    "rhy": 0,
                    "audio": {
                        "encoding": "lame",
                        "sample_rate": 16000,
                        "channels": 1,
                        "bit_depth": 16,
                        "frame_size": 0
                    },
                    "pybuf": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "plain"
                    }
                }
            },
            "payload": {
                "text": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain",
                    "status": 0,
                    "seq": 0,
                    "text": "./resource/input/1.txt"
                }
            }
        }

        auth_request_url = ne_utils.build_auth_request_url(request_url, "GET", APIKey, APISecret)
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(auth_request_url, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        ws.on_open = lambda ws: self.on_open(ws, request_data)
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def on_open(self, ws, request_data):
        def run():
            exist_audio = jsonpath.jsonpath(request_data, "$.payload.*.audio")
            exist_video = jsonpath.jsonpath(request_data, "$.payload.*.video")
            multi_mode = True if exist_audio and exist_video else False

            frame_rate = None
            if jsonpath.jsonpath(request_data, "$.payload.*.frame_rate"):
                frame_rate = jsonpath.jsonpath(request_data, "$.payload.*.frame_rate")[0]
            time_interval = 40
            if frame_rate:
                time_interval = round((1 / frame_rate) * 1000)

            media_path2data = aipass_client.prepare_req_data(request_data)
            aipass_client.send_ws_stream(ws, request_data, media_path2data, multi_mode, time_interval)

        threading.Thread(target=run).start()

    def on_message(self, ws, message):
        data = aipass_client.deal_message(ws, message)
        status = jsonpath.jsonpath(data, "$.header.status")
        if status and status[0] == 2:
            ws.close()
            self.triggered = False
            self.trigger_sentences.clear()
            self.current_role = 0
            print("Finished processing AI response, continuing to listen...")
            self.connected = True
            self.trecv = threading.Thread(target=self.recv)
            self.trecv.start()
            self.send()

    def on_error(self, ws, error):
        print("### error:", error)

    def on_close(self, ws, *args):
        print("### 执行结束，连接自动关闭 ###")

    def close(self):
        if self.connected:
            self.connected = False
            self.ws.close()
            print("connection closed")


APPId = "xxx"
APIKey = "xxx"
APISecret = "xxxx"
request_url = "ws://tianli0.top/v1/private/medd90fec"

if __name__ == '__main__':
    logging.basicConfig()

    app_id = "xxx"
    api_key = "xxx"

    client = Client(app_id, api_key)
    client.send()
