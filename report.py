import psutil
import os

def get_report():
    train_procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any('train.py' in arg for arg in cmdline):
                train_procs.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    virtual_mem = psutil.virtual_memory()
    ram_percent = virtual_mem.percent
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            rss_mb = proc.info['memory_info'].rss / (1024 * 1024)
            processes.append({
                'name': proc.info['name'],
                'pid': proc.info['pid'],
                'rss_mb': rss_mb
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    top_5 = sorted(processes, key=lambda x: x['rss_mb'], reverse=True)[:5]
    
    print(f"Active train.py processes: Count={len(train_procs)}, PIDs={train_procs}")
    print(f"RAM used percent: {ram_percent}%")
    print("Top 5 memory-consuming processes:")
    for p in top_5:
        print(f"Name: {p['name']}, PID: {p['pid']}, RSS: {p['rss_mb']:.2f} MB")

if __name__ == '__main__':
    get_report()
