import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import pika
import threading
import os
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST", "localhost"))
)

channel = connection.channel()
channel.queue_declare(queue="test_queue", durable=True)

stop_event = threading.Event()


def listen_for_messages():
    
    for _, _, body in channel.consume(
        "test_queue", inactivity_timeout=1
    ):
        if stop_event.is_set():
            break
        if body:
            text_box.insert(tk.END, body.decode() + "\n")
            text_box.see(tk.END)
    channel.cancel()


def on_closing():
    stop_event.set()
    thread.join() 
    connection.close()
    root.destroy()


root = tk.Tk()
root.title("Consumer")

text_box = ScrolledText(root, width=50, height=20)
text_box.pack(padx=10, pady=10)

thread = threading.Thread(target=listen_for_messages, daemon=True)
thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
