def main():
    import requests

    response = requests.post(
        'http://localhost:5000/api/actions',
        json={
            "title": "ランニング",
        }
    )
    print(response.json())

if __name__ == "__main__":
    main()
