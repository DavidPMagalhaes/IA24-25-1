from classes import Video, Cache, Endpoint

# Calacula o tempo total economizado ao servir um video a partir de uma cache e não de um data center
def calculate_latency_savings(endpoint, video, cache, dataCenterLatency):
    if cache in endpoint.cacheLatencies: # Verifica se a cache está disponivel para o endpoint
        return max(0, endpoint.dataCenterLatency - endpoint.cacheLatencies[cache]) * endpoint.requests.get(video.id, 0) # max evita nºnegativos, caso a latência da cache seja maior que a do data center
    return 0

# Quanto tempo foi economizado no sistema ao aceder vedeos pelas caches e nao pelo datacenter
def evaluate_solution(caches, endpoints, videos, dataCenterLatency):
    total_savings = 0 # total economizado
    for endpoint in endpoints: # percorre todos os endpoints
        for videoId, numRequests in endpoint.requests.items(): # percorre todas as requisições no endpoint
            video = videos[videoId]
            bestLatency = endpoint.dataCenterLatency # inicializa com a latência do datacenter, supondo que a cache não tem nenhum video

            for cacheId, latencyToCache in endpoint.cacheLatencies.items(): # verifica se o video está armazenado numa cache próxima
                cache = caches[cacheId]
                if video in cache.videos: #se o video estiver na cache, verifica-se a menor latência possivel
                    bestLatency = min(bestLatency, latencyToCache)
            
            total_savings += (endpoint.dataCenterLatency - bestLatency) * numRequests # calcula o tempo economizado e adiciona ao total, se video na cache a latência é menor, mais requisições para um video, maior economia de tempo

    return total_savings
