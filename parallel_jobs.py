
from multiprocessing import Pool
import sys


def parallel_jobs(func_to_run, job_args, num_parallel_jobs=8):
    """
    parallel_jobs
    This function runs a function with the specified arguments in different processes
    
    func_to_run: This function should take a single input which is a tuple of args
    job_args: List of all the argument tuples that should be run
    """
    job_results = None
    
    pool = Pool(num_parallel_jobs)
    job_results = pool.map(func_to_run, job_args)
    print "Job done. Completed "+str(len(job_results))+" jobs"
    sys.stdout.flush()
    return job_results