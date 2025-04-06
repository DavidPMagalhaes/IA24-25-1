class Video:
    def __init__(self, id, size): #inicializa objeto Video
        self.id = id
        self.size = size

    def __hash__(self): # Videos com mesmo id sejam tratados como iguais
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Video) and self.id == other.id

class Endpoint:
    def __init__(self, id, data_center_latency):
        self.id = id
        self.dataCenterLatency = data_center_latency
        self.requests = {} #{video.id: num_requests}
        self.cacheLatencies = {} #{cache.id: latency}

    def __eq__(self, other):
        return isinstance(other, Endpoint) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
class Cache:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.videos = set() #store video ids 
        self.availableSpace = capacity
    
    def add_video(self, video):
        if self.availableSpace >= video.size: # verifica se há espaço suficiente
            self.videos.add(video.id) # se sim, adiciona video a cache
            self.availableSpace -= video.size # diminui o espaço disponivel na cache
            return True
        return False
    
    def remove_video(self, video):
        if video.id in self.videos: # verifica se o video está na cache
            self.videos.remove(video.id) # se sim, remove
            self.availableSpace += video.size # o espaço disponivel na cache aumenta
            return True
        return False