
from multiprocessing import Pool
import sys

#func_to_run should take a single input which is a tuple of args
#job_args is the list of all the argument tuples that should be run
def parallel_jobs(func_to_run, job_args, num_parallel_jobs=8):
    job_results = None
    
    pool = Pool(num_parallel_jobs)
    job_results = pool.map(func_to_run, job_args)
    print "Job done. Completed "+str(len(job_results))+" jobs"
    sys.stdout.flush()
    return job_results