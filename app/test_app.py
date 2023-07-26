import requests
import time


def send_request(url):
    start_time = time.time()
    response = requests.post(url, files={'file': open("../report/crosby.jpg", 'rb')})
    end_time = time.time()
    return response, end_time - start_time


def test_health_check():
    # Test if the API is up and running
    response = requests.get("http://localhost:8000/docs")
    assert response.status_code == 200


def test_object_detection():
    url = 'http://localhost:8000/predict/image'  # Replace with your FastAPI service URL
    num_requests = 5

    total_time = 0
    for _ in range(num_requests):
        start_time = time.time()
        response = requests.post(url, files={'file': open("../report/crosby.jpg", 'rb')})
        end_time = time.time()
        assert response.status_code == 200
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        print(f'Response time: {elapsed_time:.5f} seconds')

        # Add your test assertions here (if required)

    average_time = total_time / num_requests
    print(f'Average response time: {average_time:.5f} seconds')
