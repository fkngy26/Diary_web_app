def main():
    import requests

    response = requests.put(
        'http://localhost:5000/a' \
        'pi/diaries/2026-01-15',
        json={
            "memo": "今日は調子が良かった",
            "action_logs": [{"action_id": 1, "status": "done"}]
        }
    )
    print(response.json())

if __name__ == "__main__":
    main()
