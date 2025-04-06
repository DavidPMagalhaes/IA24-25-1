import random
import time # To time execution
from classes import Video, Cache, Endpoint
# Import the corrected evaluation function
from fitness import evaluate_solution
# Import corrected GA operators
from gaOperators import create_individuals, crossover, mutate
from parsing import parse_input

# Fitness wrapper: Takes an individual (solution representation) and calculates its score
def calculate_fitness(individual, caches, endpoints, videos_dict):
    # Create temporary Cache objects based on the individual's configuration
    temp_cache_objects = {} # Use dict for potentially sparse cache usage if needed
    for cache_info in caches: # Iterate original caches to get all IDs and capacities
         cache_id = cache_info.id
         # Create a new temp Cache object for evaluation
         temp_cache = Cache(cache_id, cache_info.capacity)
         if cache_id in individual:
             # Populate the temporary cache using its add_video method
             for video_id in individual[cache_id]:
                 if video_id in videos_dict:
                     video = videos_dict[video_id]
                     temp_cache.add_video(video) # Use method on temp object
                 else: 
                     print(f"Warning: Video {video_id} in individual but not in videos_dict.")
         temp_cache_objects[cache_id] = temp_cache

    # Ensure temp_caches passed to evaluate_solution is a list indexed correctly
    temp_caches_list = [None] * len(caches)
    for i in range(len(caches)):
        if i in temp_cache_objects:
             temp_caches_list[i] = temp_cache_objects[i]
        else:
             # If a cache wasn't in the individual, create an empty temp cache
             original_cache = next((c for c in caches if c.id == i), None)
             if original_cache:
                 temp_caches_list[i] = Cache(i, original_cache.capacity)
    return evaluate_solution(temp_caches_list, endpoints)

def genetic_algorithm(caches, endpoints, videos, videos_dict, population_size, mutation_rate, generations):
    # Generate initial population - pass videos_dict
    population = [create_individuals(caches, videos, videos_dict) for _ in range(population_size)]

    best_fitness_overall = -1 # Initialize with a value lower than any possible fitness
    best_individual_overall = None

    start_time = time.time()

    for generation in range(generations):
        gen_start_time = time.time()
        # Calculate fitness for the current population
        fitnesses = []
        for individual in population:
             fit = calculate_fitness(individual, caches, endpoints, videos_dict)
             fitnesses.append((individual, fit))

        # Find best in current generation for tracking
        current_best_individual, current_best_fitness = max(fitnesses, key=lambda item: item[1])
        if current_best_fitness > best_fitness_overall:
             best_fitness_overall = current_best_fitness
             best_individual_overall = current_best_individual # Store the actual best individual


        # Selection (Tournament Selection)
        selected_parents = []
        for _ in range(population_size):
            # Select k individuals randomly for the tournament
            tournament_size = 5
            # Handle cases where population size is less than tournament size
            actual_tournament_size = min(tournament_size, len(fitnesses))
            if actual_tournament_size > 0:
                 tournament = random.sample(fitnesses, actual_tournament_size)
                 # Winner is the one with the highest fitness
                 winner = max(tournament, key=lambda item: item[1])[0] # Get the individual
                 selected_parents.append(winner)
            elif fitnesses: # If population exists but smaller than tournament size
                 selected_parents.append(fitnesses[0][0]) # Fallback: select the first one


        # Create the next generation using Crossover and Mutation
        new_population = []
        # Ensure even number for pairing, handle odd population size
        num_pairs = population_size // 2
        for i in range(num_pairs):
            parent1 = selected_parents[i*2]
            parent2 = selected_parents[i*2+1]

            # Apply crossover - pass videos_dict
            child1 = crossover(parent1, parent2, caches, videos_dict)
            child2 = crossover(parent2, parent1, caches, videos_dict) # Can swap parents for potentially different child

            # Apply mutation - pass videos_dict
            mutate(child1, videos, caches, videos_dict, mutation_rate)
            mutate(child2, videos, caches, videos_dict, mutation_rate)

            new_population.extend([child1, child2])

        # If population size is odd, add one more individual (e.g., a mutated copy of a winner)
        if population_size % 2 != 0 and selected_parents:
            parent_extra = selected_parents[-1] # Use the last selected parent
            child_extra = parent_extra.copy() # Start with a copy
             # Mutate the extra child
            mutate(child_extra, videos, caches, videos_dict, mutation_rate)
            new_population.append(child_extra)


        population = new_population # Update population for the next generation

        gen_end_time = time.time()
        print(f"Generation {generation + 1}/{generations}: Best Fitness = {best_fitness_overall}. Time: {gen_end_time - gen_start_time:.2f}s")

    end_time = time.time()
    print(f"\nGA finished in {end_time - start_time:.2f} seconds.")

    # Re-evaluate the final population to ensure we have the absolute best
    final_fitnesses = []
    for individual in population:
        fit = calculate_fitness(individual, caches, endpoints, videos_dict)
        final_fitnesses.append((individual, fit))

    if final_fitnesses: # Ensure population is not empty
        best_individual_final, best_fitness_final = max(final_fitnesses, key=lambda item: item[1])
        # Compare with the best found during generations
        if best_fitness_final > best_fitness_overall:
            print(f"Best individual found in final evaluation improved fitness to: {best_fitness_final}")
            return best_individual_final
        else:
             print(f"Best individual from generations ({best_fitness_overall}) remains the best.")
             return best_individual_overall # Return the one tracked during generations
    else:
        print("Warning: Final population is empty.")
        return best_individual_overall # Return the best found so far


if __name__ == "__main__":
    inputFile = "dataset/videos_worth_spreading.in" 
    # GA Parameters
    POPULATION_SIZE = 10
    MUTATION_RATE = 0.05 # Often lower mutation rates are better
    GENERATIONS = 10    # More generations might be needed for complex problems

    print(f"Parsing input file: {inputFile}...")
    # Parse the input file - Renamed variables for clarity
    num_videos, num_endpoints, num_requests_desc, num_caches, cache_capacity, \
        video_sizes_list, endpoint_data_list, request_data_list = parse_input(inputFile)
    print("Parsing complete.")
    print(f" V={num_videos}, E={num_endpoints}, R={num_requests_desc}, C={num_caches}, X={cache_capacity}")


    # Create Video objects and a dictionary for quick lookup by ID
    videos = [Video(i, size) for i, size in enumerate(video_sizes_list)]
    videos_dict = {v.id: v for v in videos}
    print(f"Created {len(videos)} Video objects.")

    # Create Cache objects (original state)
    caches = [Cache(i, cache_capacity) for i in range(num_caches)]
    print(f"Created {len(caches)} Cache objects with capacity {cache_capacity}.")

    # Create Endpoint objects
    endpoints = []
    for i, (dc_latency, cache_connections) in enumerate(endpoint_data_list):
        # Create endpoint with its specific data center latency
        endpoint = Endpoint(id=i, data_center_latency=dc_latency)
        # Assign cache latencies directly
        endpoint.cacheLatencies = cache_connections
        endpoints.append(endpoint)

    print(f"Created {len(endpoints)} Endpoint objects.")

    # Assign requests to their respective Endpoints
    requests_assigned_count = 0
    for video_id, endpoint_id, num_requests in request_data_list:
        # Find the endpoint object by ID
        # Using list comprehension + next is safer than assuming endpoint_id is a direct index
        endpoint = next((e for e in endpoints if e.id == endpoint_id), None)
        if endpoint:
            # Check if video_id is valid
            if video_id in videos_dict:
                endpoint.requests[video_id] = num_requests
                requests_assigned_count += 1
            else:
                print(f"Warning: Video ID {video_id} from request not found in videos_dict.")
        else:
            print(f"Warning: Endpoint ID {endpoint_id} from request not found.")
    print(f"Assigned {requests_assigned_count} requests to endpoints.")

    print(f"\nStarting Genetic Algorithm...")
    print(f" Population Size: {POPULATION_SIZE}")
    print(f" Mutation Rate: {MUTATION_RATE}")
    print(f" Generations: {GENERATIONS}")

    # Pass necessary data to the GA function
    best_solution_individual = genetic_algorithm(
        caches, endpoints, videos, videos_dict,
        POPULATION_SIZE, MUTATION_RATE, GENERATIONS
    )

    # --- Evaluate and Print Final Result ---
    print("\nCalculating fitness of the best solution found...")
    best_fitness = calculate_fitness(best_solution_individual, caches, endpoints, videos_dict)
    print(f"\nBest Solution Fitness (Total Time Saved): {best_fitness}")

    # --- Prepare Output File (Optional but good practice for Hash Code) ---
    output_filename = inputFile.replace(".in", ".out")
    print(f"\nPreparing output file: {output_filename}")
    try:
        with open(output_filename, 'w') as f_out:
            # Count how many caches are actually used in the best solution
            used_caches = {cache_id: videos for cache_id, videos in best_solution_individual.items() if videos}
            f_out.write(f"{len(used_caches)}\n") # First line: number of caches used

            # For each used cache, write a line: cache_id video_id1 video_id2 ...
            for cache_id, video_ids_set in used_caches.items():
                # Convert set to list and then to space-separated string
                videos_str = " ".join(map(str, sorted(list(video_ids_set)))) # Sort for consistent output
                f_out.write(f"{cache_id} {videos_str}\n")
        print(f"Successfully wrote output to {output_filename}")

    except IOError as e:
        print(f"Error writing output file: {e}")

    print("\nExecution finished.")