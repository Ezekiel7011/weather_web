from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


global weather_data
weather_data = {
    "臺北市": "",
    "雲林縣": "",
    "新北市": "",
    "嘉義市": "",
    "基隆市": "",
    "臺南市": "",
    "桃園市": "",
    "高雄市": "",
    "新竹市": "",
    "屏東縣": "",
    "苗栗縣": "",
    "宜蘭縣": "",
    "臺中市": "",
    "花蓮縣": "",
    "彰化縣": "",
    "臺東縣": "",
    "南投縣": "",
}

city_code = {
    "臺北市": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E8%87%BA%E5%8C%97%E5%B8%82/%E8%87%BA%E5%8C%97%E5%B8%82-2306179",
    "雲林縣": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E9%9B%B2%E6%9E%97/%E9%9B%B2%E6%9E%97-2347346",
    "新北市": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E6%96%B0%E5%8C%97%E5%B8%82/%E6%96%B0%E5%8C%97%E5%B8%82-20070569",
    "嘉義市": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E5%98%89%E7%BE%A9%E5%B8%82/%E5%98%89%E7%BE%A9%E5%B8%82-2296315",
    "基隆市": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E5%9F%BA%E9%9A%86%E5%B8%82/%E5%9F%BA%E9%9A%86%E5%B8%82-2306188",
    "臺南市": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E8%87%BA%E5%8D%97%E5%B8%82/%E8%87%BA%E5%8D%97%E5%B8%82-2306182",
    "桃園市": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E6%A1%83%E5%9C%92%E5%B8%82/%E6%A1%83%E5%9C%92%E5%B8%82-2298866",
    "高雄市": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E9%AB%98%E9%9B%84%E5%B8%82/%E9%AB%98%E9%9B%84%E5%B8%82-2306180",
    "新竹市": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E6%96%B0%E7%AB%B9%E5%B8%82/%E6%96%B0%E7%AB%B9%E5%B8%82-2306185",
    "屏東縣": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E5%B1%8F%E6%9D%B1%E5%B8%82/%E5%B1%8F%E6%9D%B1%E5%B8%82-2306189",
    "苗栗縣": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E8%8B%97%E6%A0%97%E5%B8%82/%E8%8B%97%E6%A0%97%E5%B8%82-2301128",
    "宜蘭縣": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E5%AE%9C%E8%98%AD%E5%B8%82/%E5%AE%9C%E8%98%AD%E5%B8%82-2306198",
    "臺中市": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E8%87%BA%E4%B8%AD%E5%B8%82/%E8%87%BA%E4%B8%AD%E5%B8%82-2306181",
    "花蓮縣": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E8%8A%B1%E8%93%AE%E5%B8%82/%E8%8A%B1%E8%93%AE%E5%B8%82-2306187",
    "彰化縣": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E5%BD%B0%E5%8C%96%E5%B8%82/%E5%BD%B0%E5%8C%96%E5%B8%82-2306183",
    "臺東縣": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E8%87%BA%E6%9D%B1%E5%B8%82/%E8%87%BA%E6%9D%B1%E5%B8%82-2306190",
    "南投縣": "https://tw.news.yahoo.com/weather/%E8%87%BA%E7%81%A3/%E5%8D%97%E6%8A%95%E5%B8%82/%E5%8D%97%E6%8A%95%E5%B8%82-2306204",
}


def catch_data():
    for city, url in city_code.items():
        response = requests.get(url)
        additional_info = ""
        # 檢查是否成功下載網頁
        if response.status_code == 200:
            # 使用Beautiful Soup解析HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # 提取溫度
            temperature = soup.find(
                "span", class_="Va(t) D(n) celsius celsius_D(b)"
            ).text
            # 提取時間
            time = soup.find(
                "time", class_="Lts(1px) Fz(0.875rem) Fs(i) Lh(2.5) Fw(300)"
            ).text
            # 提取額外敘述
            target_div = soup.find("div", class_="Py(10px) Px(4px) Fz(0.8125rem)")
            paragraphs = target_div.find_all("p", class_="My(10px)")
            for paragraph in paragraphs:
                additional_info += paragraph.text + "\n"

            # 提取體感溫度
            real_feel = (
                soup.find_all(
                    "div",
                    class_="D(f) Py(8px) Bdb Bdbs(d) Bdbw(1px) Bdbc($weatherBorderColor) Jc(sb)",
                )[0]
                .find_all("dd")[1]
                .text
            )

            # 提取溼度
            humidity = (
                soup.find_all(
                    "div",
                    class_="D(f) Py(8px) Bdb Bdbs(d) Bdbw(1px) Bdbc($weatherBorderColor) Jc(sb)",
                )[1]
                .find_all("dd")[0]
                .text
            )

            # 提取能見度
            visibility = (
                soup.find_all(
                    "div",
                    class_="D(f) Py(8px) Bdb Bdbs(d) Bdbw(1px) Bdbc($weatherBorderColor) Jc(sb)",
                )[2]
                .find_all("dd")[0]
                .text
            )

            # 提取紫外線指數
            uv_index = (
                soup.find(
                    "div", class_="D(f) Py(8px) Bdb Bdbs(d) Bdbw(1px) Bdbc(t) Jc(sb)"
                )
                .find("dd")
                .text
            )

            # 更新天氣資料
            weather_data[city] = {
                "temperature": temperature,
                "time": time,
                "additional_info": additional_info,
                "real_feel": real_feel,
                "humidity": humidity,
                "visibility": visibility,
                "uv_index": uv_index,
            }
        else:
            # 如果無法下載網頁，將天氣資料設定為 None
            weather_data[city] = "None"


@app.route("/get_weather_data/<city_name>")
def get_weather_data(city_name):
    return jsonify(weather_data[city_name])


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(catch_data, "interval", seconds=10)
    scheduler.start()
    catch_data()
    app.run(debug=True)
