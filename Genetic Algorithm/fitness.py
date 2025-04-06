from classes import Video, Cache, Endpoint # Keep imports for context, even if Video isn't directly used

def evaluate_solution(temp_caches, endpoints):
    total_savings = 0 # total economizado
    total_requests = 0 # To calculate the final score as per HashCode rules (savings / total requests * 1000)

    for endpoint in endpoints: # percorre todos os endpoints
        if not endpoint.requests: # Skip endpoints with no requests
             continue

        for videoId, numRequests in endpoint.requests.items(): # percorre todas as requisições no endpoint
            total_requests += numRequests # Accumulate total requests
            # bestLatency initially assumes fetching from the data center
            bestLatency = endpoint.dataCenterLatency

            # Check connected caches for the video
            for cacheId, latencyToCache in endpoint.cacheLatencies.items():
                # Ensure cacheId is valid index for temp_caches
                if 0 <= cacheId < len(temp_caches):
                    cache = temp_caches[cacheId]
                    if videoId in cache.videos: # se o video estiver na cache
                        bestLatency = min(bestLatency, latencyToCache) # Find the minimum latency
                # else: print(f"Warning: cacheId {cacheId} out of bounds for temp_caches") # Optional debug

            # Calculate savings for this specific request (video * numRequests)
            # and add to total
            time_saved_for_request = (endpoint.dataCenterLatency - bestLatency) * numRequests
            if time_saved_for_request > 0: # Only add positive savings
                 total_savings += time_saved_for_request

    # HashCode score calculation: (Total Time Saved / Total Number of Requests) * 1000
    if total_requests == 0:
        return 0 # Avoid division by zero if there are no requests
    
    # The problem asks for total saved time, not average. Let's return total_savings.
    # If average score needed: return (total_savings * 1000) / total_requests
    return total_savings # Return the total time saved in microseconds