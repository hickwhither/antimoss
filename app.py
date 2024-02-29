from dotenv import load_dotenv
load_dotenv()
import os
import time
import random
import atexit

from flask import *
from flask_socketio import *
from flask_ipban import IpBan


from apscheduler.schedulers.background import BackgroundScheduler
import antimoss, antimoss2


EXPIRETIME = 69

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

ip_ban = IpBan(ban_seconds=200, ban_count=2)
ip_ban.init_app(app)

app.result = {}

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def amm():
    if request.values['mosstype'] not in ['1', '2']:
        flash('Invalid mosstype')
        return render_template('index.html')
    code = "co cai nit ma hack"
    cd = random.randint(100000,999999)
    app.result[cd] = (code, time.time())

    return redirect(f"/result/{cd}")


@app.route('/result/<int:cd>')
def result(cd):
    if cd not in app.result:
        return render_template('result.html', code="Not found", expiretime="This result is no longer avaiable")
    res = app.result[cd]
    expiretime = EXPIRETIME - (time.time() - res[1])
    return render_template('result.html', code=res[0], expiretime=f"{expiretime:.2f}s left before delete")

def expire_result():
    t = time.time()
    listtodel = []
    for k, v in app.result.items():
        if t - v[1] > EXPIRETIME: listtodel.append(k)
    for i in listtodel:
        app.result.pop(i)


scheduler = BackgroundScheduler()
scheduler.add_job(func=expire_result, trigger="interval", seconds=2)
scheduler.start()

if __name__ == "__main__":
    from waitress import serve
    # app.run('0.0.0.0', 80, debug=True)
    serve(app, host='0.0.0.0', port=80)

    atexit.register(lambda: scheduler.shutdown())

