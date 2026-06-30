import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd

products = []

def scrape():
    global products
    products = []

    url = "https://books.toscrape.com/"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for book in soup.find_all("article", class_="product_pod"):
            name = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating = book.p["class"][1]

            products.append([name, price, rating])

        tree.delete(*tree.get_children())

        for product in products:
            tree.insert("", tk.END, values=product)

        messagebox.showinfo("Success", "Products Scraped Successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def export_csv():
    if not products:
        messagebox.showwarning("Warning", "No data available!")
        return

    df = pd.DataFrame(products,
                      columns=["Product Name", "Price", "Rating"])

    df.to_csv("products.csv", index=False)

    messagebox.showinfo("Success", "Data exported to products.csv")

root = tk.Tk()
root.title("Product Information Scraper")
root.geometry("800x500")

title = tk.Label(root,
                 text="Product Information Scraper",
                 font=("Arial", 18, "bold"))
title.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame,
          text="Scrape Products",
          command=scrape).pack(side=tk.LEFT, padx=10)

tk.Button(btn_frame,
          text="Export CSV",
          command=export_csv).pack(side=tk.LEFT, padx=10)

columns = ("Name", "Price", "Rating")

tree = ttk.Treeview(root,
                    columns=columns,
                    show="headings")

tree.heading("Name", text="Product Name")
tree.heading("Price", text="Price")
tree.heading("Rating", text="Rating")

tree.column("Name", width=450)
tree.column("Price", width=100)
tree.column("Rating", width=100)

tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)

root.mainloop()