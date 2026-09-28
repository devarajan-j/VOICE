from flask import Flask,render_template,request,jsonify,session
from dotenv import load_dotenv
from google import genai
import os, datetime

load_dotenv()
app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY","voicesphere-secret")

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat',methods=['POST'])
def chat():
    data=request.get_json()
    msg=data.get('message','')
    hist=session.get('history',[])
    hist.append({'role':'user','content':msg})
    try:
        r=client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=msg
        )
        text=r.text
    except Exception as e:
        text=f'Error: {e}'
    hist.append({'role':'assistant','content':text})
    session['history']=hist[-20:]
    return jsonify({'response':text})

@app.route('/command',methods=['POST'])
def command():
    cmd=request.json.get('command','').lower()
    if 'time' in cmd:
        return jsonify({'response':datetime.datetime.now().strftime('%I:%M %p')})
    if 'date' in cmd:
        return jsonify({'response':datetime.datetime.now().strftime('%d-%m-%Y')})
    return jsonify({'response':'Command received.'})

if __name__=='__main__':
    app.run(debug=True)
