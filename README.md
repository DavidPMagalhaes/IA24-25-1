# TO DO  
---

## **Class: Videos (DataVideos)**
- Reads and parses video-related data from a file.  
- Extracts values like number of videos, endpoints, requests, caches, and cache size.  
- Reads video sizes.  
- Processes latency values and request information.  
- Stores latencies and ping data in a structured way.  
  - `V` - Number of videos.  
  - `E` - Number of endpoints.  
  - `R` - Number of request descriptions.  
  - `C` - Number of cache servers.  
  - `X` - Capacity of each cache server (MB).  
- Handles edge cases:  
  - If an **endpoint has no cache servers**, handle it properly.  

---

## **Baseline Caching Strategy (`findBaseline`)**
- Assigns videos sequentially to caches.  
- Ensures memory constraints are followed.  
- **Potential improvement**: prioritize videos based on **requests or latency savings** instead of sequential filling.  

---

## **Caching Optimization Algorithm (`UgoOptim`)**
### **1. Copy Requests**
- Avoid modifying the original request data.  

### **2. Cache Solution**
- Store which videos are assigned to which cache.  
- Loop over each cache.  

### **3. Aggregate Wanted Videos for the Current Cache**
- Minimize **overall request latency**.  
- Evaluate each video’s importance to endpoints connected to the cache.  
- **MOST REQUESTED AND LATENCY-SAVING VIDEOS FIRST**.  

### **4. Sort Videos by Cost**
- Prioritize videos based on **request frequency × latency saved**.  

### **5. Fit Videos into Cache**
- Store as many high-priority videos as possible within cache size limits.  
- **Avoid Index Errors**: Ensure `while availableSize > 0` does not exceed list bounds.  

### **6. Remove Cached Videos from Requests (Optional)**
- Prevents the same videos from being cached everywhere.  
- Reduces redundant storage, making room for other important videos.  

### **7. Save the Solution**
- Store the optimized cache assignments.  
- Output the final solution to a results file.  

---

## **Edge Cases & Fixes**
- **Prevent Infinite Loops or Index Errors**  
  - Ensure `sortedSizes[lastVideo]` does not cause an out-of-bounds error.  
- **Ensure Compatibility with Python 3**  
  - Replace `iteritems()` with `items()`.  
- **Handle Caches That Are Too Small**  
  - If no videos fit inside a cache, mark it as unused instead of failing.  
