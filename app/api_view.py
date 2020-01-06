from flask import render_template, redirect, request
from app import app
import json, requests


@app.route('/api')
def api():
    return render_template('api/api.html')

@app.route('/api/treatment-predict', methods = ['GET', 'POST'])
def treatment_api():
    
    color = 'bg-blue'
    if request.method == 'POST':

        data = {}

        fname = request.form['fname']
        lname = request.form['lname']
        data['Gender'] = request.form['gender']
        data['Age'] = request.form['age']
        data['work_interfere'] = request.form['work-interfere']
        data['benefits'] = request.form['benefits']
        data['care_options'] = request.form['care_options']
        data['anonymity'] = request.form['anonymity']
        data['leave'] = request.form['leave']
        data['mental_health_consequence'] = request.form['mental']
        data['supervisor'] = request.form['supervisor']
        data['phys_health_interview'] = request.form['phy']
        data['no_employees'] = request.form['no_emp']
        data['obs_consequence'] = request.form['obs_consequence']
        data['family_history'] = request.form['family_history']   

        url = 'https://ml-api-world.herokuapp.com/predict'
        response = requests.post(url, json = json.dumps(data) )
        output = json.loads(response.text)

        if int(output['predict']) == 1 :
            color = 'bg-red'
        else:
            color = 'bg-green'

        return render_template('api/treatment/treatment_predict.html', 
                                name = fname+' '+lname, 
                                predict = int(output['predict']),
                                prob = output['prob'],
                                inputs = data,
                                color = color,
                                flag = True
                                )

    return render_template('api/treatment/treatment_predict.html', 
                            name = None,
                            predict = None,
                            prob = None,
                            inputs = None,
                            color = color,
                            flag = False
                            )

    