def main():
    import requests

    response = requests.get(
        'http://localhost:5000/api/actions/getall'
    )
    print(response.json())

if __name__ == "__main__":
    main()
