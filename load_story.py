import subprocess

def main():
    try:
        with open('links', 'r', encoding='utf-8') as file:
            links = file.readlines()

        for link in links:
            link = link.strip()
            if link:  # Skip empty lines
                print(f"\033[92mProcessing link: {link}\033[0m")
                subprocess.run(["python", "tools/downloader.py", link])
                print(f"\033[92mFinished processing link: {link}\033[0m\n")
    except FileNotFoundError:
        print("\033[93mFile 'links' not found.\033[0m")
    except Exception as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")

if __name__ == "__main__":
    main()