from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import database as dbase
from product import Product

db = dbase.dbConnection()

app = Flask(__name__)

# Rutas de la aplicación
@app.route('/')
def home():
    data = db['data']
    productsReceived = data.find()
    return render_template('index.html', products=productsReceived)

# Método insertar
@app.route('/products', methods=['POST'])
def addProduct():
    data = db['data']
    area = request.form['area']
    prob = request.form['prob']
    type = request.form['type']
    did_serv = request.form['did_serv']
    sm = request.form['sm']
    hw_impact = request.form['hw_impact']
    customer = request.form['customer']
    proyect_name = request.form['proyect_name']
    book_date2 = request.form['book_date2']
    book_period = request.form['book_period']
    bcs_months = request.form['bcs_months']
    tcv_00 = request.form['tcv_00']
    rev_fy22q3 = request.form['rev_fy22q3']
    rev_fy22q4 = request.form['rev_fy22q4']
    columna1 = request.form['columna1']

    if area and prob and type and did_serv and sm and hw_impact and customer and proyect_name and book_date2 and book_period and bcs_months and tcv_00 and rev_fy22q3 and rev_fy22q4 and columna1:
        product = Product(area, prob, type, did_serv, sm, hw_impact, customer, proyect_name, book_date2, book_period, bcs_months, tcv_00, rev_fy22q3, rev_fy22q4, columna1)
        data.insert_one(product.toDBCollection())
        response = jsonify({
            'area': area,
            'prob': prob,
            'type': type,
            'did_serv': did_serv,
            'sm': sm,
            'hw_impact': hw_impact,
            'customer': customer,
            'proyect_name': proyect_name,
            'book_date2': book_date2,
            'book_period': book_period,
            'bcs_months': bcs_months,
            'tcv_00': tcv_00,
            'rev_fy22q3': rev_fy22q3,
            'rev_fy22q4': rev_fy22q4,
            'columna1': columna1
        })
        return redirect(url_for('home'))
    else:
        return notFound()

# Método eliminar
@app.route('/delete/<string:product_name>')
def delete(product_name):
    data = db['data']
    data.delete_one({'proyect_name': product_name})
    return redirect(url_for('home'))

# Método actualizar
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    data = db['data']
    area = request.form['area']
    prob = request.form['prob']
    type = request.form['type']
    did_serv = request.form['did_serv']
    sm = request.form['sm']
    hw_impact = request.form['hw_impact']
    customer = request.form['customer']
    proyect_name = request.form['proyect_name']
    book_date2 = request.form['book_date2']
    book_period = request.form['book_period']
    bcs_months = request.form['bcs_months']
    tcv_00 = request.form['tcv_00']
    rev_fy22q3 = request.form['rev_fy22q3']
    rev_fy22q4 = request.form['rev_fy22q4']
    columna1 = request.form['columna1']

    if area and prob and type and did_serv and sm and hw_impact and customer and proyect_name and book_date2 and book_period and bcs_months and tcv_00 and rev_fy22q3 and rev_fy22q4 and columna1:
        data.update_one({'proyect_name': product_name}, {'$set': {
            'area': area,
            'prob': prob,
            'type': type,
            'did_serv': did_serv,
            'sm': sm,
            'hw_impact': hw_impact,
            'customer': customer,
            'proyect_name': proyect_name,
            'book_date2': book_date2,
            'book_period': book_period,
            'bcs_months': bcs_months,
            'tcv_00': tcv_00,
            'rev_fy22q3': rev_fy22q3,
            'rev_fy22q4': rev_fy22q4,
            'columna1': columna1
        }})
        response = jsonify({'message': 'Producto ' + proyect_name + ' actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=4000) 