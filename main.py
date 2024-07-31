from tpblite import TPB
from tabulate import tabulate
import os

def search_torrents(query):
    try:
        tpb = TPB()
        search = tpb.search(query)
        
        results = list(search)
        
        if results:
            table = []
            for i, result in enumerate(results):
                ratio = result.seeds / result.leeches if result.leeches > 0 else float('inf')
                table.append([i + 1, result.title, result.seeds, result.leeches, ratio])
            
            headers = ["#", "Title", "Seeds", "Leeches", "Ratio"]
            print(tabulate(table, headers, tablefmt="grid"))
            
            choice = int(input("Enter the number of the torrent you want to download: ")) - 1
            selected_torrent = results[choice]
            
            torrent_url = selected_torrent.magnetlink
            
            os.system(f"webtorrent \"{torrent_url}\" --select")
            
            file_choice = int(input("Enter the number of the file you want to play: ")) - 1
            
            return torrent_url, file_choice
        else:
            print("No torrents found.")
            return None, None
    except AttributeError as e:
        print(f"Attribute error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def stream_torrent(torrent_url, file_choice):
    try:
        os.system(f"webtorrent \"{torrent_url}\" --select {file_choice} --mpv")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    query = input("Enter the movie or series name to search: ")
    result = search_torrents(query)
    if result:
        torrent_url, file_choice = result
        print(f"Torrent URL: {torrent_url}")
        print(f"Selected File Index: {file_choice}")
        print("Streaming the torrent...")
        stream_torrent(torrent_url, file_choice)
    else:
        print("No valid result returned.")
