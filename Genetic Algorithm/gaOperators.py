import random
from classes import Video, Cache, Endpoint # Keep imports

# Helper function to calculate size of videos in a set
def calculate_set_size(video_ids_set, videos_dict):
    current_size = 0
    for video_id in video_ids_set:
        if video_id in videos_dict:
            current_size += videos_dict[video_id].size
    return current_size

# Creates a potential solution by randomly assigning videos to caches respecting capacity
def create_individuals(caches, videos, videos_dict):
    individual = {}
    for cache in caches:
        individual[cache.id] = set() # videos stored in this cache for this individual
        current_cache_size = 0
        cache_capacity = cache.capacity

        available_videos = list(videos) # copy of the video list
        random.shuffle(available_videos) # shuffle for randomness

        for video in available_videos:
            # Check if adding the video exceeds capacity
            if current_cache_size + video.size <= cache_capacity:
                individual[cache.id].add(video.id)
                current_cache_size += video.size

    return individual

# Creates a child individual by combining parts of two parents, respecting capacity
def crossover(parent1, parent2, caches, videos_dict):
    child = {}
    for cache in caches:
        cache_id = cache.id
        cache_capacity = cache.capacity
        
        # 1. Inherit video set from one parent randomly
        if random.random() < 0.5:
            # copy() is essential to avoid modifying the parent's set
            child[cache_id] = parent1.get(cache_id, set()).copy()
        else:
            child[cache_id] = parent2.get(cache_id, set()).copy()

        # 2. Check and enforce capacity constraint
        current_child_cache_size = calculate_set_size(child[cache_id], videos_dict)

        # While over capacity, randomly remove videos
        videos_in_cache_list = list(child[cache_id]) # List to allow random removal
        while current_child_cache_size > cache_capacity and videos_in_cache_list:
            video_to_remove_id = random.choice(videos_in_cache_list)
            
            child[cache_id].remove(video_to_remove_id)
            videos_in_cache_list.remove(video_to_remove_id) # Remove from temp list too
            
            if video_to_remove_id in videos_dict:
                 current_child_cache_size -= videos_dict[video_to_remove_id].size
            else: 
                print(f"Warning: Video {video_to_remove_id} not in videos_dict during crossover removal.")


    return child

# Mutates an individual by randomly adding or removing videos, respecting capacity
def mutate(individual, videos, caches, videos_dict, mutationRate):
    for cache in caches:
        cache_id = cache.id
        cache_capacity = cache.capacity
        videos_in_cache = individual[cache_id] # The set for this cache

        # Attempt to ADD a video
        if random.random() < mutationRate:
            # Find videos *not* already in this cache
            eligible_videos = [v for v in videos if v.id not in videos_in_cache]
            random.shuffle(eligible_videos)

            current_cache_size = calculate_set_size(videos_in_cache, videos_dict)

            for video_to_add in eligible_videos:
                # Check if it fits
                if current_cache_size + video_to_add.size <= cache_capacity:
                    videos_in_cache.add(video_to_add.id)
                    # No need to update current_cache_size here unless adding multiple
                    break # Stop after adding one video

        # Attempt to REMOVE a video
        if random.random() < mutationRate:
            if videos_in_cache: # Can only remove if the set is not empty
                video_remove_id = random.choice(list(videos_in_cache))
                videos_in_cache.remove(video_remove_id)
                # No need to update cache size variable as it's recalculated if needed again