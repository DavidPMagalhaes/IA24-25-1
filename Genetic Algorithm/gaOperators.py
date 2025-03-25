import random
from classes import Video, Cache, Endpoint

def create_individuals(caches, videos): # gera uma possivel solução, atribuindo videos aleatoriamente as caches
    individual = {}
    for cache in caches:
        individual[cache.id] = set() # videos armazenados na cache
        available_videos = videos[:] # cópia da lista de videos para evitar modificar a original
        random.shuffle(available_videos) # embaralha os videos garantindo que cada execução gera um individuo diferente

        current_space = cache.capacity
        for video in available_videos: # percorre os videos misturados e tenta adiciona los a cache
            if cache.add_video(video): # se couber
                individual[cache.id].add(video.id)
            else: # se nao couber
                pass
    return individual

def crossover(parent1, parent2, caches): # cria um novo individuo-filho combinando videos armazenados nas caches dos dois pais
    child = {} 
    for cache in caches: # para cada cache, inicializa um conjunto vazio no filho
        child[cache.id] = set()
        if random.random() < 0.5: # decisão aleatória 50%
            child[cache.id] = parent1.get(cache.id, set()).copy() # copy() garante que o conjunto de videos seja independente
        else:
            child[cache.id] = parent2.get(cache.id, set()).copy()
    return child

def mutate(individual, videos, caches, mutationRate): # altera um individuo (uma solução), modificando a alocação de video nas caches
    for cache_id in individual: 
        cache = next(c for c in caches if c.id == cache_id) 

        if random.random() < mutationRate:
            eligibleVideos = [video for video in videos if video.id not in individual[cache_id]] # filtra os videos ainda nao armazenados na cache
            if eligibleVideos:
                availableVideos = eligibleVideos[:]
                random.shuffle(availableVideos) # embaralha a lista para adicionar videos de forma aleatória
                for video in availableVideos: # percorre os videos disponiveis e adiciona o primeiro que couber na cache
                    if cache.add_video(video):
                        individual[cache_id].add(video.id)
                        break
        
        if random.random() < mutationRate: # tenta remover um video
            if individual[cache_id]:
                videoRemoveId = random.choice(list(individual[cache_id])) # escolhe um video aleatório da cache para remoção
                videoRemove = next(v for v in videos if v.id == videoRemoveId) # encontra o objeto video correspondente

                if cache.remove_video(videoRemove):
                    individual[cache_id].remove(videoRemoveId) # se a remoção for bem-sucedida, remove o ID do video do individuo