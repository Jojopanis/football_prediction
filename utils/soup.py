import requests

def download_csv():
    # CSV dosyasının bulunduğu URL
    csv_url = "https://www.football-data.co.uk/mmz4281/2425/B1.csv"

    # İstek gönder
    response = requests.get(csv_url)

    # Dosya başarılı bir şekilde indirilmişse
    if response.status_code == 200:
        # Dosya adını belirle
        file_name = '/opt/airflow/data/data.csv'
        
        # Dosyayı yaz
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f'{file_name} başarıyla indirildi.')
    else:
        print('CSV dosyası indirilemedi.')

download_csv()