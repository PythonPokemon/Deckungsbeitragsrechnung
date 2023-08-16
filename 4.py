import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def berechne_deckungsbeitrag(umsatz, variable_kosten):
    return umsatz - variable_kosten

def berechne_break_even_point(feste_kosten, deckungsbeitrag):
    if deckungsbeitrag != 0:
        return feste_kosten / deckungsbeitrag
    else:
        return float('inf')

def berechne_variable_kosten(stueckzahl, gesamtkosten):
    return gesamtkosten / stueckzahl if stueckzahl != 0 else 0.0

def zeichne_diagramm(umsatz, variable_kosten, feste_kosten, break_even_color='green'):
    gewinn = []
    mengen = range(0, int(umsatz / variable_kosten) + 1)
    for menge in mengen:
        gewinn.append(umsatz * menge - variable_kosten * menge - feste_kosten)

    fig = plt.figure()
    plt.plot(mengen, gewinn)
    plt.xlabel('Menge')
    plt.ylabel('Gewinn')
    plt.title('Gewinn in Abhängigkeit der Menge')
    plt.axhline(0, color='red', linestyle='--')
    plt.axvline(berechne_break_even_point(feste_kosten, berechne_deckungsbeitrag(umsatz, variable_kosten)), color=break_even_color, linestyle='--', label='Break-Even-Point')
    plt.legend()

    return fig

def calculate_and_plot():
    try:
        stueckzahl = float(stueckzahl_entry.get())
        preis = float(preis_entry.get())
        gesamtkosten = float(feste_kosten_entry.get())

        umsatz = stueckzahl * preis
        variable_kosten = berechne_variable_kosten(stueckzahl, gesamtkosten)
        deckungsbeitrag = berechne_deckungsbeitrag(umsatz, variable_kosten)
        break_even_point = berechne_break_even_point(gesamtkosten, deckungsbeitrag)

        ergebnis_label.config(text=f'Deckungsbeitrag: {deckungsbeitrag:.2f}\nBreak-Even-Point: {break_even_point:.2f}')

        # Löschen der alten Plot-Anzeige (falls vorhanden)
        for widget in diagramm_frame.winfo_children():
            widget.destroy()

        # Erstelle das neue Diagramm und zeige es in der Tkinter-GUI an
        break_even_color = break_even_color_var.get()
        diagramm = zeichne_diagramm(umsatz, variable_kosten, gesamtkosten, break_even_color)
        canvas = FigureCanvasTkAgg(diagramm, master=diagramm_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except ValueError:
        ergebnis_label.config(text='Bitte gültige Zahlen eingeben.')

def speichern():
    with open('einstellungen.txt', 'w') as file:
        file.write(stueckzahl_entry.get() + '\n')
        file.write(preis_entry.get() + '\n')
        file.write(feste_kosten_entry.get() + '\n')
        file.write(break_even_color_var.get())

def laden():
    try:
        with open('einstellungen.txt', 'r') as file:
            stueckzahl_entry.delete(0, tk.END)
            preis_entry.delete(0, tk.END)
            feste_kosten_entry.delete(0, tk.END)
            break_even_color_var.set('green')

            stueckzahl_entry.insert(0, file.readline().strip())
            preis_entry.insert(0, file.readline().strip())
            feste_kosten_entry.insert(0, file.readline().strip())
            break_even_color_var.set(file.readline().strip())
            calculate_and_plot()
    except FileNotFoundError:
        ergebnis_label.config(text='Einstellungen nicht gefunden.')


# GUI erstellen
app = tk.Tk()
app.title('Deckungsbeitrag und Break-Even-Point Rechner')

stueckzahl_label = tk.Label(app, text='Stückzahl:')
stueckzahl_label.pack()
stueckzahl_entry = tk.Entry(app)
stueckzahl_entry.pack()

preis_label = tk.Label(app, text='Preis pro Stück:')
preis_label.pack()
preis_entry = tk.Entry(app)
preis_entry.pack()

feste_kosten_label = tk.Label(app, text='Gesamtkosten:')
feste_kosten_label.pack()
feste_kosten_entry = tk.Entry(app)
feste_kosten_entry.pack()

break_even_color_var = tk.StringVar(value='green')
break_even_color_label = tk.Label(app, text='Farbe für Break-Even-Point:')
break_even_color_label.pack()
break_even_color_entry = tk.Entry(app, textvariable=break_even_color_var)
break_even_color_entry.pack()

berechnen_button = tk.Button(app, text='Berechnen und Diagramm anzeigen', command=calculate_and_plot)
berechnen_button.pack()

speichern_button = tk.Button(app, text='Einstellungen speichern', command=speichern)
speichern_button.pack()

laden_button = tk.Button(app, text='Einstellungen laden', command=laden)
laden_button.pack()

ergebnis_label = tk.Label(app, text='')
ergebnis_label.pack()

diagramm_frame = tk.Frame(app)
diagramm_frame.pack()

app.mainloop()
