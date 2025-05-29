import tkinter as tk
import subprocess
import webbrowser
import threading

def search_spotlight(query):
    try:
        result = subprocess.run(['mdfind', query], capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')[:20]
    except subprocess.CalledProcessError:
        return []

def open_result(path):
    if path.startswith("http"):
        webbrowser.open(path)
    else:
        subprocess.run(['open', path])

def on_search():
    query = entry.get().strip()
    if not query:
        return
    result_list.delete(0, tk.END)

    def threaded_search():
        results = search_spotlight(query)
        if results:
            for item in results:
                result_list.insert(tk.END, item)
        else:
            result_list.insert(tk.END, "No files found.")

    threading.Thread(target=threaded_search).start()

def on_google_search():
    query = entry.get().strip()
    if not query:
        return
    result_list.delete(0, tk.END)

    def threaded_google():
        result_list.insert(tk.END, f"https://www.google.com/search?q={query}")
        result_list.insert(tk.END, f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}")
        result_list.insert(tk.END, f"https://news.google.com/search?q={query}")
        result_list.insert(tk.END, f"https://www.youtube.com/results?search_query={query}")
        result_list.insert(tk.END, f"https://duckduckgo.com/?q={query}")
    threading.Thread(target=threaded_google).start()

def on_result_double_click(event):
    selection = result_list.curselection()
    if not selection:
        return
    path = result_list.get(selection[0])
    open_result(path)

# --- UI Setup ---
root = tk.Tk()
root.title("Birdie Search")
root.geometry("700x420")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

entry = tk.Entry(frame, width=60, font=("Helvetica", 14))
entry.pack(side=tk.LEFT, padx=(0, 10))
entry.bind('<Return>', lambda event: on_search())

search_button = tk.Button(frame, text="Search Files", command=on_search)
search_button.pack(side=tk.LEFT)

result_list = tk.Listbox(root, width=100, height=20, font=("Courier", 10))
result_list.pack(padx=10, pady=(0, 5))
result_list.bind('<Double-1>', on_result_double_click)

button_frame = tk.Frame(root)
button_frame.pack(pady=(0, 10))

google_button = tk.Button(button_frame, text="Search the web...", command=on_google_search)
google_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
