from MachineLearning.analyze_question import AnalysisQuestion
from KnowledgeGraph.get_answer import Get_answer
from sqlconnect import PyMySQL
from py2neo import *
from flask import *
from Word_Cloud import Word_Cloud

app = Flask(__name__, template_folder='./static/templates')

@app.route('/',methods=["POST","GET"])
def hello():
    mydb = PyMySQL('localhost','root','ysj528528','chatbot')
    answer = {
        "question":'',
        "content":''
    }
    if request.method=="POST":
        name = request.form.get("user")
        pwd = request.form.get("password")
        if mydb.get_message(name, pwd):
            return render_template("index.html", answer = answer)
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/registers", methods=['POST',"GET"])
def register():
    mydb = PyMySQL('localhost','root','ysj528528','chatbot')
    if request.method=="POST":
        name = request.form.get("user")
        pwd = request.form.get("password")
        if mydb.insert_date(name, pwd):
            return render_template("login.html")
        else:
            return render_template("registers.html")
    else:
        return render_template("registers.html")

@app.route("/web_answer", methods = ["GET","POST"])
def get_answer():
    mydb = PyMySQL('localhost','root','ysj528528','chatbot')
    aq = AnalysisQuestion()
    ga = Get_answer()
    question = request.form['question']
    index, params = aq.analysis_question(question)
    result = ga.get_data(index, params)
    ls = []
    for ans in result:
        ls.append(ans[0])
    s = " ---- "
    answers = s.join([str(item) for item in ls])
    answer = {
        "question":question,
        "content":answers
    }
    mydb.select_question(str(question))
    mydb.insert_question(str(question))
    for l in ls:
        mydb.select_question(l)
    return render_template("index.html" ,answer = answer)
    
@app.route('/static/templates/me.html/')
def display_table():
    mydb = PyMySQL('localhost','root','ysj528528','chatbot')
    data = mydb.get_information()
    return render_template("me.html", data = data)

@app.route('/web_modify', methods = ["GET","POST"])
def new_password():
    mydb = PyMySQL('localhost','root','ysj528528','chatbot')
    ID = request.form.get("id")
    new_pwd = request.form.get("new_pwd")
    mydb.update_data(new_pwd, ID)
    data = mydb.get_information()
    mydb.updata_id()
    return render_template("me.html", data = data)

@app.route('/web_delete', methods = ["GET","POST"])
def delete_me():
    mydb = PyMySQL('localhost','root','ysj528528','chatbot')
    ID = request.form.get("id")
    name = request.form.get("name")
    mydb.delete_data(ID)
    data = mydb.get_information()
    mydb.updata_id()
    return render_template("me.html", data = data)
        
@app.route('/static/templates/cloud.html/', methods = ["GET","POST"])
def word_cloud():
    mydb = PyMySQL('localhost','root','ysj528528','chatbot')
    mydb.get_tables()
    wc = Word_Cloud()
    wc.run()
    return render_template("cloud.html")

if __name__ == "__main__":
    app.run(debug=False)