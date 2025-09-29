import os
archivo = "ticket.txt"
with open(archivo, "w") as f:
    f.write("Hola impresora COL-POS!\n")
    f.write("Ticket de prueba desde Python.\n")
os.startfile(archivo, "print")

 