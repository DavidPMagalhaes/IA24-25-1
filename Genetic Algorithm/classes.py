class Video:
    def __init__(self, id, size): #inicializa objeto Video
        self.id = id
        self.size = size

    def __hash__(self): # Videos com mesmo id sejam tratados como iguais
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id

class Endpoint:
    def __init__(self, id, data_center_latency):
        self.id = id
        self.dataCenterLatency = data_center_latency
        self.requests = {} #{video.id: num_requests}
        self.cacheLatencies = {} #{cache.id: latency}

class Cache:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.videos = set()
        self.availableSpace = capacity
    
    def add_video(self, video):
        if self.availableSpace >= video.size: # verifica se há espaço suficiente
            self.videos.add(video) # se sim, adiciona video a cache
            self.availableSpace -= video.size # diminui o espaço disponivel na cache
            return True
        return False
    
    def remove_video(self, video):
        if video in self.videos: # verifica se o video está na cache
            self.videos.remove(video) # se sim, remove
            self.availableSpace += video.size # o espaço disponivel na cache aumenta
            return True
        return False