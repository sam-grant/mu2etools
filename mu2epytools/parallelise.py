'''

Utilities for parallelising analysis jobs on FNAL EAF. 
Samuel Grant 2024.

'''

# TODO: add ProcessPoolExecutor, explore Dask.
from concurrent.futures import ThreadPoolExecutor, as_completed

# Submit processes a thread pool (each thread runs one process on one file)
def multithread(process_function, file_list, max_workers=381): # max_workers is 3x the cores on EAF
    
    print('\n---> Starting multithreading...\n')

    completed_files = 0
    total_files = len(file_list)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        
        # Prepare a list of futures and map them to file names
        futures = {executor.submit(process_function, filename): (filename) for filename in file_list}
        
        # Process results as they complete
        for future in as_completed(futures):
            filename = futures[future] # Get the file name associated with this future
            try:
                future.result()  # Retrieve the result 
                completed_files += 1
                percent_complete = (completed_files / (total_files)) * 100
                print(f'\n{filename} processed successfully! ({percent_complete:.1f}% complete)')
            except Exception as exc: # Handle exceptions
                print(f'\n{filename} generated an exception!\n{exc}') 
                
    print('\n---> Multithreading completed!')
    return