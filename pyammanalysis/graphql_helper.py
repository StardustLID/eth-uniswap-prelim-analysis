import requests

# function to use requests.post to make an API call to the subgraph url
def run_query(url: str, query):
    # endpoint where you are making the request
    request = requests.post(url, \
        '', \
        json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. Return code is {}.      {}'.format(request.status_code, query))