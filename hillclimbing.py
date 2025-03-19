import os
import sys
import random

def parse_input(file_path):
    """Parses the input file and returns problem data."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Read first line (problem parameters)
    V, E, R, C, X = map(int, lines[0].split())  # Videos, Endpoints, Requests, Caches, Cache Size
    
    # Read video sizes
    video_sizes = list(map(int, lines[1].split()))
    
    # Read endpoints
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
    
    # Read request descriptions
    requests = []
    for _ in range(R):
        video_id, endpoint_id, num_requests = map(int, lines[line_idx].split())
        requests.append((video_id, endpoint_id, num_requests))
        line_idx += 1
    
    return V, E, R, C, X, video_sizes, endpoints, requests


def initialize_solution(V, C, X, video_sizes, requests):
    """Generates an initial greedy solution."""
    cache_videos = {i: set() for i in range(C)}
    
    # Sort videos by total request count (most requested first)
    video_popularity = {v: 0 for v in range(V)}
    for video_id, _, num_requests in requests:
        video_popularity[video_id] += num_requests
    
    sorted_videos = sorted(video_popularity, key=lambda v: -video_popularity[v])
    
    # Greedily allocate videos to caches if they fit
    for video in sorted_videos:
        for cache in range(C):
            if sum(video_sizes[v] for v in cache_videos[cache]) + video_sizes[video] <= X:
                cache_videos[cache].add(video)
    
    return cache_videos


def compute_score(cache_videos, video_sizes, endpoints, requests):
    """Computes the total score of the current solution."""
    total_saved_time = 0
    total_requests = 0
    
    for video_id, endpoint_id, num_requests in requests:
        data_center_latency, caches = endpoints[endpoint_id]
        best_cache_latency = data_center_latency
        
        for cache_id, cache_latency in caches.items():
            if video_id in cache_videos[cache_id]:
                best_cache_latency = min(best_cache_latency, cache_latency)
        
        saved_time = data_center_latency - best_cache_latency
        total_saved_time += saved_time * num_requests
        total_requests += num_requests
    
    return (total_saved_time * 1000) // total_requests if total_requests > 0 else 0


def hill_climb(cache_videos, V, C, X, video_sizes, endpoints, requests, max_iters=10000):
    """Performs hill climbing to optimize cache allocation."""
    current_score = compute_score(cache_videos, video_sizes, endpoints, requests)
    
    for _ in range(max_iters):
        cache_id = random.randint(0, C - 1)
        video_id = random.randint(0, V - 1)
        
        if video_id in cache_videos[cache_id]:
            # Try removing the video
            cache_videos[cache_id].remove(video_id)
        else:
            # Try adding the video if space allows
            if sum(video_sizes[v] for v in cache_videos[cache_id]) + video_sizes[video_id] <= X:
                cache_videos[cache_id].add(video_id)
        
        new_score = compute_score(cache_videos, video_sizes, endpoints, requests)
        
        if new_score < current_score:
            # Revert the change if score worsened
            if video_id in cache_videos[cache_id]:
                cache_videos[cache_id].remove(video_id)
            else:
                cache_videos[cache_id].add(video_id)
        else:
            current_score = new_score  # Accept improvement
    
    return cache_videos


def save_solution(cache_videos, output_file):
    """Saves the final solution to a file."""
    with open(output_file, 'w') as f:
        f.write(f"{len(cache_videos)}\n")
        for cache_id, videos in cache_videos.items():
            if videos:
                f.write(f"{cache_id} " + " ".join(map(str, videos)) + "\n")


def main():
    """Main function to execute the hill-climbing algorithm."""
    if len(sys.argv) < 2:
        print("Usage: python3 hillclimbing.py <input_file>")
        return
    
    input_filename = sys.argv[1]
    input_path = os.path.join("dataset", input_filename)
    output_folder = "output_hill"
    os.makedirs(output_folder, exist_ok=True)
    
    if not os.path.exists(input_path):
        print(f"Error: {input_filename} not found in dataset/")
        return

    output_path = os.path.join(output_folder, input_filename.replace(".in", ".out"))

    # Parse input
    V, E, R, C, X, video_sizes, endpoints, requests = parse_input(input_path)

    # Generate initial greedy solution
    cache_videos = initialize_solution(V, C, X, video_sizes, requests)

    # Optimize using hill climbing
    optimized_cache_videos = hill_climb(cache_videos, V, C, X, video_sizes, endpoints, requests)

    # Save the solution
    save_solution(optimized_cache_videos, output_path)

    print(f"Processed {input_filename}, output saved to {output_path}")


if __name__ == "__main__":
    main()
