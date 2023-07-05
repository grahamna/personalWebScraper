import tkinter as tk
import threading
import onlineBookScraper


def clearPlaceholder(event):
    if urlEntry.get() == "Copy/Paste Url: ":
        urlEntry.delete(0, tk.END)


def go(event=None):
    url = urlEntry.get()
    
    if urlEntry.get() == '' or urlEntry.get() == "Copy/Paste Url: ":
        return
    root.update_idletasks()
    statusIcon = tk.Message(root, font=("Arial", 8), width= int(root.winfo_width()), justify=tk.LEFT)
    statusIcon.pack()
    statusIcon.config(text=url +" (Working...)")

    
    thread = threading.Thread(target = lambda: fetchBookThreaded(url, statusIcon=statusIcon))
    thread.start()
    
    urlEntry.delete(0, tk.END)

def fetchBookThreaded(url, statusIcon):
    result = onlineBookScraper.fetchBook(urlString=url)
    if result == -1:
        statusIcon.config(text=url +" ❌")  
    else:
        statusIcon.config(text=url+" ✅")  
        
def selectAll(event):
    urlEntry.select_range(0,tk.END)
    return 'break'

def main():
    global root
    root = tk.Tk()
    root.title("onlineBookScraper GUI")

    global urlEntry
    urlEntry = tk.Entry(root, width=50, borderwidth=3)
    urlEntry.insert(0, "Copy/Paste Url: ")
    urlEntry.bind("<FocusIn>", clearPlaceholder)
    urlEntry.bind("<Return>", go)
    urlEntry.bind("<Control-a>", selectAll)
    urlEntry.pack()

    global goButton
    goButton = tk.Button(root, text="Go", command=go)
    goButton.pack()
    
    exitButton = tk.Button(root, text="Exit", command=lambda: root.quit())
    exitButton.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)  

    root.geometry("540x320")
    root.mainloop()


if __name__ == '__main__':
    main()