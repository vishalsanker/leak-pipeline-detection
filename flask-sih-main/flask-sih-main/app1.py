from flask import Flask , request
app = Flask(__name__)

@app.route('/post-data',methods=['POST'])
def post_data():
    data = request.data.decode('utf-8')
    data_dict = {k:int(v) for k,v in (i.split('=') for i in data.split('&'))}
    fl_sens1 = data_dict.get('fl1',None)
    fl_sens2 = data_dict.get('fl2',None)
    pr_sens = data_dict.get('pr1',None)
    if fl_sens1 is not None and fl_sens2 is not None and pr_sens is not None: 
        print("Rcvd")
        return "rcvd"
    else:return "Invalid data"
    
if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5000)