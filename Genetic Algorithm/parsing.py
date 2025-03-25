def parse_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    V, E, R, C, X = map(int, lines[0].split())

    video_sizes = list(map(int, lines[1].split()))

    endpoints = []
    line_idx = 2

    for _ in range(E):
        data_center_latency, num_cache_connections = map(int, lines[line_idx].split())
        line_idx += 1
        caches = {}
        for _ in range(num_cache_connections):
            cache_id, latency = map(int, lines[line_idx].split())
            caches[cache_id] = latency
            line_idx += 1
        endpoints.append((data_center_latency, caches))

    requests = []
    for _ in range(R):
        video_id, endpoint_id, num_requests = map(int, lines[line_idx].split())
        requests.append((video_id, endpoint_id, num_requests))
        line_idx += 1

    return V, E, R, C, X, video_sizes, endpoints, requests
