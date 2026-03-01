from  flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt

#app es el inicio donde flask va a iniciar el aplicativo

app = Flask(__name__)

@app.route('/')
def somos():
    return render_template ('Somos.html')

@app.route('/datos')
def Datos ():
    df = pd.read_json("productos.json")
    tabla_html = df.to_html(classes='table table-stiped', index= False)
    return render_template ('Datos.html', tabla=tabla_html)

@app.route('/Dashboard')
def dashboard():
    df = pd.read_json("productos.json")
    top5 = df.sort_values (by="vendidos", ascending =False).head(5)
    plt.figure(figsize=(10,6))
    plt.bar(top5["producto"], top5 ["vendidos"], color= 'salmon')
    plt.title("Top 5 de los productos más vendidos")
    plt.xlabel("Producto")
    plt.ylabel("Unidades")
    plt.grid(axis="y")
    plt.tight_layout()
    #como  paso la grafica  a imagen?
    plt.savefig("static/top5.png")
    return render_template("Dashboard.html")


