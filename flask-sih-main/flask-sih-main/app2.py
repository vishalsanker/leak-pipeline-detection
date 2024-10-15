# from flask import Flask,render_template,request
# from google.oauth2 import service_account
# import requests
# import csv
# import io
# import psycopg2
# import gspread 

# app = Flask(__name__)

# conn = psycopg2.connect(        database="railway",
#     user="postgres",
#     password="EB-63EECcBf1*3Cgg*bAc6-*e4C31Dab",
#     host="viaduct.proxy.rlwy.net",
#     port="58482"
# )
# cursor = conn.cursor()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/import',methods=['POST','GET'])
# def import_csv():
#     f = request.files['file']
#     if f:
#         stream = io.StringIO(f.stream.read().decode('UTF-8'),newline=None)
#         csv_data = csv.reader(stream)
#         for row in csv_data:
#             cursor.execute("INSERT INTO table_name (PARAM1,PARAM2,PARAM1) VALUES(%s %s %s)",(row[1],row[2],row[3]))
#         conn.commit()
#         return "CSV data added succesfully to postgres"
    
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# creds = service_account.Credentials.from_service_account_file('///cred.json',scopes=SCOPES)
# client = gspread.authorize(creds)
# # #client = gspread.authorize(creds)

# @app.route('/import', methods=['POST'])
# def import_google_sheet():
#     file_id = request.form['file_id']  # Get the Google Sheet ID from the form
#     sheet = client.open_by_key(file_id).sheet1
#     values = sheet.get_all_values()

#     for row in values:
#         # Assuming the Google Sheet has three columns: col1, col2, col3
#         cursor.execute("INSERT INTO your_table_name (col1, col2, col3) VALUES (%s, %s, %s);", (row[0], row[1], row[2]))

#     conn.commit()
#     return 'Google Sheet data imported successfully.'

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template
from threading import Thread
import time
from database_handler import check_and_update_training_set
import plotly.express as px
import plotly.io as pio
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
Base = declarative_base()
DATABASE_URI = 'sqlite:///your_database.db'  # change db name
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('  ', scope)
client = gspread.authorize(creds)
sheet_url = 'url'
sheet = client.open_by_url(sheet_url).sheet1
class DataModel(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    column1 = Column(String)
    column2 = Column(String)
def initialize_database():
    global engine
    Base.metadata.create_all(engine)

# Function to update the database from the Google Sheet
def update_database():
    global session
    global sheet
    sheet_values = sheet.get_all_values()
    header = sheet_values[0]
    sheet_values = sheet_values[1:]
    for row in sheet_values:
        data_entry = DataModel(column1=row[0], column2=row[1])
        session.merge(data_entry)
    session.commit()
initialize_database()
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_database, trigger='interval', seconds=5)
scheduler.start()

"""
def update_database():
    global session
    global sheet
    global model
    sheet_values = sheet.get_all_values()
    header = sheet_values[0]
    sheet_values = sheet_values[1:]
    data_for_detection = np.array(sheet_values, dtype=np.float32)
    predictions = model.predict(data_for_detection)
    for i, row in enumerate(sheet_values):
        anomaly_score = predictions[i]  # Replace this with the correct way to obtain anomaly scores
        data_entry = DataModel(column1=row[0], column2=row[1], anomaly_score=anomaly_score)
        session.merge(data_entry)
    session.commit()

# init
initialize_database()

# run every 5 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_database, trigger='interval', seconds=5)
scheduler.start()

@app.route('/anomaly_scores')
def get_anomaly_scores():
    global session
    anomaly_scores = session.query(DataModel.anomaly_score).all()
    return jsonify({'anomaly_scores': [score[0] for score in anomaly_scores]})
"""


# Define a simple route to check if the server is running
@app.route('/')
def index():
    return 'Flask server is running!'
def get_sample_data():
    labels = ['Category A', 'Category B', 'Category C']
    values = [30, 40, 30]
    return labels, values
def background_task():
    while True:
        check_and_update_training_set()
        time.sleep(3600)
background_thread = Thread(target=background_task)
background_thread.start()

# Dashboard route
@app.route('/dashboard')
def dashboard():
    # Get sample data (replace with your actual data retrieval logic)
    labels, values = get_sample_data()

    # Create a pie chart using Plotly Express
    fig = px.pie(labels=labels, values=values, title='Sample Data')

    # Convert the Plotly figure to HTML
    chart_html = pio.to_html(fig, full_html=False)

    return render_template('dashboard.html', chart_html=chart_html)

if __name__ == '__main__':
    app.run(debug=True)
