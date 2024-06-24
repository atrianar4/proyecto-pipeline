import os
from flask import Flask, render_template, request, jsonify, redirect, send_from_directory, url_for, send_file, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import database as dbase
from bson import ObjectId
from mcr_pipeline import McrPipeline
from sm import Sm
import random
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO



db = dbase.dbConnection()
mcr_pipeline_list = []
page_persist = 1
page_size_persist = 10
data = db['data'] ##Data de los pipelines
sm = db['sm'] ##Data de los sales managers
collection = db['data']
app = Flask(__name__)


# Rutas de la aplicación
@app.route('/')
def home():    
    sm_list = sm.find()
    return render_template('index.html', sm_list=sm_list)

    
@app.route('/table')
def table_page():
    
    # Aquí obtienes los datos necesarios para mostrar en la tabla
    items = list(data.find().limit(page_size_persist))
    mcr_pipeline_list = [item for item in items]
    
    sm_list = sm.find()  
    # Luego renderizas la plantilla table.html y pasas los datos como contexto
    return render_template('table.html', pipeline_list=mcr_pipeline_list, sm_list=sm_list, page=page_persist, page_size=page_size_persist)


@app.route('/details', methods=['GET'])
def detail_page():
    # Obtener el objeto pipeline de los argumentos de la solicitud
    pipeline = request.args.get('data_object')
    id = request.args.get('data_id')
    
    
    # Trabajar con el objeto pipeline como necesites
    # Por ejemplo, si necesitas convertirlo a un diccionario, puedes usar eval(pipeline)
    pipeline_dict = eval(pipeline)
    sm_list = sm.find()
    # Ahora puedes hacer lo que necesites con el objeto pipeline_dict
    # Por ejemplo, renderizar una plantilla con esos datos
    return render_template('edit.html', pipeline=pipeline_dict, id= id,sm_list=sm_list)



# Método insertar
@app.route('/data', methods=['POST'])
def addMcrPipeline():
    data = db['data']
    area = request.form['area']
    prob = request.form['prob']
    type = request.form['type']
    did_serv = request.form['did_serv']
    sm = request.form['sm']
    customer = request.form['customer']
    project_name = request.form['project_name']
    book_date2 = request.form['book_date2']
    book_period = request.form['book_period']
    bcs_months = request.form['bcs_months']
    tcv_00 = request.form['tcv_00']
    rev_fy22q3 = request.form['rev_fy22q3']
    rev_fy22q4 = request.form['rev_fy22q4']
    columna1 = request.form['columna1']

    if area and prob and type and did_serv and sm and customer and project_name and book_date2 and book_period and bcs_months and tcv_00 and rev_fy22q3 and rev_fy22q4 and columna1:
        pipeline = McrPipeline(area, prob, type, did_serv, sm, customer, project_name, book_date2, book_period, bcs_months, tcv_00, rev_fy22q3, rev_fy22q4, columna1)
        data.insert_one(pipeline.toDBCollection())
        response = jsonify({
            'area': area,
            'prob': prob,
            'type': type,
            'did_serv': did_serv,
            'sm': sm,
            'customer': customer,
            'project_name': project_name,
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
    
    
@app.route('/exportar_excel')
def exportar_excel():
    area = request.args.get('area', '')
    prob = request.args.get('prob', '')
    type = request.args.get('type', '')
    sm = request.args.get('sm', '')

    query = {}
    if area:
        query['area'] = area
    if prob:
        query['prob'] = prob
    if type:
        query['type'] = type
    if sm:
        query['sm'] = sm

    todos_los_documentos = list(data.find(query))

    df = pd.DataFrame(todos_los_documentos)

    nombre_archivo = 'exportacion_base_datos.xlsx'
    ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)
    df.to_excel(ruta_archivo, index=False)

    return send_from_directory(os.getcwd(), nombre_archivo, as_attachment=True)

@app.route('/exportar_pdf')
def exportar_pdf():
    # Parámetros de consulta
    area = request.args.get('area', '')
    prob = request.args.get('prob', '')
    type = request.args.get('type', '')
    sm = request.args.get('sm', '')

    query = {}
    if area:
        query['area'] = area
    if prob:
        query['prob'] = prob
    if type:
        query['type'] = type
    if sm:
        query['sm'] = sm

    todos_los_documentos = list(data.find(query))

    df = pd.DataFrame(todos_los_documentos)

    buffer = BytesIO()
    # Crear un lienzo (canvas) PDF utilizando ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)

     # Colores y estilos de Cisco
    cisco_blue = colors.HexColor("#005073")
    cisco_gray = colors.HexColor("#4D4F53")
    cisco_white = colors.HexColor("#FFFFFF")

     # Configurar el tamaño de fuente y otros estilos
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(cisco_blue)
    c.drawString(50, 750, "Reporte de Datos - Cisco")


    # Ajustar márgenes y espacio para escribir
    margen_izquierdo = 50
    margen_derecho = letter[0] - 50
    y_inicial = 710

    # Convertir DataFrame a formato de tabla
    data_as_table = df.to_string(index=False)
    lineas = data_as_table.split('\n')
    espacio_entre_lineas = 15

    # Escribir cada línea en el lienzo PDF
    for idx, linea in enumerate(lineas):
        y_pos = y_inicial - (idx * espacio_entre_lineas)
        c.setFillColor(cisco_gray if idx % 2 == 0 else cisco_white)
        c.setFont("Helvetica", 8)
        c.drawString(margen_izquierdo, y_pos, linea)

         # Si alcanza el borde inferior de la página, añadir nueva página
        if y_pos <= 50:
            c.showPage()
            c.setFont("Helvetica", 8)  # Reajustar tamaño de fuente para nueva página
            y_inicial = 750 # Resetear posición inicial para nueva página

    # Finalizar el lienzo PDF
    c.showPage()
    c.save()

     # Obtener los datos del buffer y enviar el archivo al usuario para su descarga
    buffer.seek(0) # Asegurar que el buffer esté al inicio
    return send_file(buffer, as_attachment=True, download_name='exportacion_base_datos.pdf')




@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'excel_file' not in request.files:
            return f"<script>alert('Invalid file'); window.location.replace('/')</script>"
        
        file = request.files['excel_file']
        if file.filename == '':
            return f"<script>alert('No selected file'); window.location.replace('/')</script>"
        
        if file:
            df = pd.read_excel(file)
            # Convertir nombres de columnas a cadenas
            df.columns = df.columns.astype(str)
            data = df.to_dict(orient='records')
            collection.insert_many(data)
            return f"<script>alert('Data imported successfully!'); window.location.replace('/')</script>"
    
    except Exception as e:
        return f"<script>alert('Error: {str(e)}'); window.location.replace('/')</script>"

    
    
# Método eliminar
@app.route('/delete/<string:data_id>')
def delete(data_id):
    print("product_id:"+data_id)
    data = db['data']
    data.delete_one({'_id': ObjectId(data_id)})
    return redirect(url_for('table_page'))


@app.route('/items/<int:page_number_param>/<int:page_size_number_param>', methods=['GET'])
def get_items(page_number_param, page_size_number_param):
    global page_size_persist
    page_size_persist = page_size_number_param
    # Calcular el número de documentos a saltar
    skips = page_size_number_param * (page_number_param - 1)
    
    # Obtener los documentos paginados
    items = list(data.find().skip(skips).limit(page_size_number_param))
    
    # Convertir los documentos de MongoDB a una lista de diccionarios
    result = [item for item in items]
    sm_list = sm.find()
    print(f"result: {result}")
    print(f"size{page_size_number_param} y number {page_number_param}")
    return render_template('table.html', pipeline_list=result, sm_list=sm_list, page=page_number_param, page_size=page_size_number_param)
    
@app.route('/save_data/<string:data_id>', methods=['POST'])
def save_data(data_id):
    data = db['data']
    # Obtener los datos actualizados del formulario
    updated_data = {
        'area': request.form['area'],
        'prob': request.form['prob'],
        'type': request.form['type'],
        'did_serv': request.form['did_serv'],
        'sm': request.form['sm'],
        'customer': request.form['customer'],
        'project_name': request.form['project_name'],
        'book_date2': request.form['book_date2'],
        'book_period': request.form['book_period'],
        'bcs_months': request.form['bcs_months'],
        'tcv_00': request.form['tcv_00'],
        'rev_fy22q3': request.form['rev_fy22q3'],
        'rev_fy22q4': request.form['rev_fy22q4'],
        'columna1': request.form['columna1']
    }

    print(f'TEXTO{updated_data}')
    
    # Actualizar el objeto en la base de datos
    data.update_one({'_id': ObjectId(data_id)}, {'$set': updated_data})
    
    return redirect(url_for('home'))


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
    app.run(debug=True, port=5000) 