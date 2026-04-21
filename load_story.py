import sys
import subprocess
import time

def process_link(link: str):
    link = link.strip()
    if not link:
        return
    print(f"\033[92m** Processing link: {link}\033[0m")
    start = time.time()
    print(f"\033[96m[LOG] Time started: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))}\033[0m")
    subprocess.run(["python", "tools/downloader.py", link])
    end = time.time()
    print(f"\033[96m[LOG] Time end: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end))}\033[0m")
    print(f"\033[94m** Finished processing link: {link} in {end - start:.2f} seconds\033[0m\n")

def main():
    if len(sys.argv) > 1:
        # Process url from command line argument
        process_link(sys.argv[1])
    else:
        try:
            with open('links', 'r', encoding='utf-8') as file:
                links = file.readlines()
            if not links:
                print("\033[93mWarning: No links found in 'links' file.\033[0m")
            else:
                for link in links:
                    process_link(link)
        except FileNotFoundError:
            print("\033[93mWarning: File 'links' not found.\033[0m")
        except Exception as e:
            print(f"\033[91mAn error occurred: {e}\033[0m")

if __name__ == "__main__":
    main()