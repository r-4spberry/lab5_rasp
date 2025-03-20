import tkinter as tk
import pika
import os


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='test_queue')
def send_message():
    message = entry.get()
    if message:
        channel.basic_publish(exchange='', routing_key='test_queue', body=message)
        entry.delete(0, tk.END) 
        
def on_closing():
    connection.close()
    root.destroy()

root = tk.Tk()
root.title("Producer")

entry = tk.Entry(root, width=40)
entry.pack(padx=10, pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
