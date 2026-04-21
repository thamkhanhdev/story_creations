import subprocess
import sys

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"\033[92mProcessing link: {url}\033[0m")
        subprocess.run(["python", "tools/downloader.py", url])
        print(f"\033[92mFinished processing link: {url}\033[0m\n")
    else:
        try:
            with open('links', 'r', encoding='utf-8') as file:
                links = file.readlines()
            if not links:
                print("\033[93mWarning: No links found in 'links' file.\033[0m")
            else:
                for link in links:
                    link = link.strip()
                    if link:  # Skip empty lines
                        print(f"\033[92mProcessing link: {link}\033[0m")
                        subprocess.run(["python", "tools/downloader.py", link])
                        print(f"\033[92mFinished processing link: {link}\033[0m\n")
        except FileNotFoundError:
            print("\033[93mWarning: File 'links' not found.\033[0m")
        except Exception as e:
            print(f"\033[91mAn error occurred: {e}\033[0m")

if __name__ == "__main__":
    main()