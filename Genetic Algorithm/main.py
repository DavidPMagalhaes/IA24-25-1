import random
from classes import Video, Cache, Endpoint
from fitness import evaluate_solution, calculate_latency_savings
from gaOperators import create_individuals, crossover, mutate
from parsing import parse_input

def fitness(individual, caches, endpoints, videosDict, datacenterLatency):
    cacheObjects = {}

    for cacheId in individual:
        cacheObjects[cacheId] = Cache(cacheId, caches[cacheId].capacity) # para cada cache presente no individuo, cria um novo objeto cache com a mesma capacidade original
        for videoId in individual[cacheId]:
            if videoId in videosDict:
                video = videosDict[videoId]
                cacheObjects[cacheId].add_video(video) #para cada video armazenado na cache, adiciona-o ao novo objeto Cache
                                                        # garante o cálculo do fitness seja feito com caches contendo apenas videos da solução

    cacheList = [cacheObjects[i] if i in cacheObjects else Cache(i, caches[i].capacity) for i in range(len(caches))] # se uma cache estiver no individuo, usa a versão com os videos atribuidos, se nao cria uma cache vazia com a capacidade original
                                                                                                                    # garante que a avaliação da solução considere todas as caches disponiveis

    return evaluate_solution(cacheList, endpoints, videosDict, datacenterLatency) # calcula o ganho total de latência baseado na distribuição dos videos nas caches, quanto maior o valor retornado, melhor a solução

def genetic_algorithm(caches, endpoints, videos, videosDict, datacenterLatency, populationSize, mutationRate, generations):
    population = [create_individuals(caches, videos) for _ in range(populationSize)] #gera individuos aleatórios

    for generation in range(generations):
        fitnesses = [(individual, fitness(individual, caches, endpoints, videosDict, datacenterLatency)) for individual in population] # para cada individuo, calcula o valor de fitness

        selected = []
        for _ in range(populationSize):
            tournament = random.sample(fitnesses, 5) #seleciona pais para a próxima geração usando torneio de 5 individuos aleatórios
            winner = max(tournament, key=lambda item: item[1])[0] # o melhor deles(com maior fitness) é escolhido como pai
            selected.append(winner)
        # mantem a diversidade ao evitar escolher sempre os mesmos individuos

        new_population = []
        for i in range(0, populationSize, 2):
            parent1 = selected[i]
            if i + 1 < populationSize:
                parent2 = selected[i+1]
            else:
                parent2 = selected[i]
            # forma pares de pais 

            # aplica crossover para gerar dois filhos
            child1 = crossover(parent1, parent2, caches)
            child2 = crossover(parent2, parent1, caches)

            # aplica mutação para aumentar a diversidade
            mutate(child1, videos, caches, mutationRate)
            mutate(child2, videos, caches, mutationRate)

            new_population.extend([child1, child2]) # adiciona os filhos na nova populaçao

        population = new_population

        bestFitness = max(fitnesses, key=lambda item: item[1])[1]
        print(f"Generation {generation + 1}: Best Fitness = {bestFitness}") # a cada geração, imprime o melhor fitness encontrado, o que ajuda a acompanhar a evolução do algoritmo

    bestIndividual = max(fitnesses, key=lambda item: item[1])[0] # apoós todas as gerações, retorna o melhor individuo encontrado, que contém a melhor distribuição de videos entre caches
    return bestIndividual

if __name__ == "__main__":
    inputFile = "dataset/me_at_the_zoo.in"

    V, E, R, C, X, videoSizes, endpointData, requestsData = parse_input(inputFile)

    videos = [Video(i, size) for i, size in enumerate(videoSizes)]
    videosDict = {v.id: v for v in videos}

    caches = [Cache(i, X) for i in range(C)]

    endpoints = []
    datacenterLatency = {}

    for i, (data_centerLatency, cacheConnections) in enumerate(endpointData):
        endpoint = Endpoint(i, datacenterLatency)
        endpoints.append(endpoint)
        datacenterLatency[endpoint] = data_centerLatency
        endpoint.cacheLatencies = cacheConnections

    for videoId, endpointId, numRequests in requestsData:
        endpoint = next((e for e in endpoints if e.id == endpointId), None)
        if endpoint:
            endpoint.requests[videoId] = numRequests
        else:
            print(f"Warning: Endpoint {endpointId} not found for request (Video {videoId})")

    POPULATION_SIZE = 50
    MUTATION_RATE = 0.1
    GENERATIONS = 30    

    bestSolution = genetic_algorithm(caches, endpoints, videos, videosDict, datacenterLatency, POPULATION_SIZE, MUTATION_RATE, GENERATIONS)

    bestFitness = fitness(bestSolution, caches, endpoints, videosDict, datacenterLatency)
    print(f"\nBest Solution Fitness: {bestFitness}")

    for cacheId, videosInCache in bestSolution.items():
        print(f"Cache {cacheId}: {videosInCache}")