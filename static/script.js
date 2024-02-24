document.addEventListener('DOMContentLoaded', function () {
    updateWeatherData('/get_weather_data/臺北市');

    var citySelect = document.getElementById('city-select');
    citySelect.addEventListener('change', function () {
        var selectedCity = citySelect.value;
        var cityName = citySelect.options[citySelect.selectedIndex].getAttribute('value');
        updateWeatherData('/get_weather_data/' + encodeURIComponent(cityName));
    });
});

function updateWeatherData(data) {
    fetch(data)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            document.getElementById('time-display').innerText = data.time;
            document.getElementById('temperature-display').innerText = data.temperature + '°C';
            document.getElementById('additional-info').innerText = data.additional_info;
            document.getElementById('real_feel').innerText = '體感溫度: ' + data.real_feel;
            document.getElementById('humidity').innerText = '溼度: ' + data.humidity;
            document.getElementById('visibility').innerText = '能見度: ' + data.visibility;
            document.getElementById('uv-index').innerText = '紫外線指數: ' + data.uv_index;
        });
}
