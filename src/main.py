import numpy as np
import math
dataset = 'dataset/'

def parse_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # read first line: number_videos, number_endpoints, number_requests, number_caches, capacity
    number_videos, number_endpoints, number_requests, number_caches, capacity = map(int, lines[0].split())

    # read video sizes
    video_sizes = list(map(int, lines[1].split()))

    # read endpoint information
    index = 2
    endpoints = []
    for _ in range(number_endpoints):
        latency, K = map(int, lines[index].split())
        index += 1
        cache_connections = []
        for _ in range(K):
            c, Lc = map(int, lines[index].split())
            cache_connections.append((c, Lc))
            index += 1
        endpoints.append({'latency': latency, 'cache_connections': cache_connections})

    # read request descriptions
    requests = []
    for _ in range(number_requests):
        v, e, n = map(int, lines[index].split())
        requests.append({'video_id': v, 'endpoint_id': e, 'num_requests': n})
        index += 1

    return {
        'number_videos': number_videos,
        'number_endpoints': number_endpoints,
        'number_requests': number_requests,
        'number_caches': number_caches,
        'capacity': capacity,
        'video_sizes': video_sizes,
        'endpoints': endpoints,
        'requests': requests
    }

# Usage
filename = "me_at_the_zoo.in"  
parsed_data = parse_input(filename)

# Pretty-print the parsed data
import pprint
pprint.pprint(parsed_data)