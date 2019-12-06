# main.py
# !/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess
import sys
import time
import flask
# from ansi2html import Ansi2HTMLConverter
from flask import request, current_app, logging
from flask_mail import Message
from pathlib import Path
from .docfile import PDF
from . import Mail, create_app
from .auth import login_post
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)
app = create_app(

)


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)


@main.route("/was")
@login_required
def was():
    return render_template("was.html")


@main.route('/was', methods=['GET', 'POST'])
@login_required
def handle_data():
    email = request.form.get('email')
    if request.method == 'POST':
        url = request.form.get('url')
        print('started executing command ...')

        def inner():
            res = ['python2', 'project/rapidscan.py', url]

            a = subprocess.Popen(" ".join(res), shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 stdin=subprocess.PIPE
                                 )
            # stdout = a.communicate()
            pdf = PDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            print('entering for loop ...')

            for line in iter(a.stdout.readline, b''):
                line = str(line, 'utf-8')
                line2 = line.encode('latin-1', 'replace').decode('latin-1')
                sys.stdout.flush()
                # pdf.write(5, str(line2))
                # pdf.ln()
                time.sleep(1)

                yield line2.strip() + "<br>\n"

                if line2.startswith(".") is False:
                    pdf.write(5, str(line2))
                    pdf.ln()

            pdf.output("General_Report", "F")

            scan_report = Path("/General_Report.pdf")

            if scan_report.is_file():

             try:
                with create_app().app_context():

                    mail = Mail()

                    msg = Message(subject="Hello",
                                  sender="Infosec App",
                                  recipients="tsiibest@gmail.com",  # replace with your email for testing
                                  body="Your scan results are ready!")

                    with app.open_resource("General_Report.pdf") as fp:
                        msg.attach('General_Report.pdf', 'application/pdf', fp.read())
                    #msg.attach('AIC-Vulnerability-Report.txt', 'text/plain')
                    #msg.attach('AIC-Debug-Scanlog.txt', 'text/plain')

                    mail.send(msg)

             except Exception as e:
                print(e)
            else:
                print("no such file")
            while a.poll() is None:
                print("Still working...")

        # return flask.Response(inner(), mimetype='text/html')

        # return flask.render_template("handle_data.html", response=inner())
        env = Environment(loader=FileSystemLoader('project/templates'))
        tmp1 = env.get_template('handle_data.html')
        # css_url = url_for('static', filename='css/template.css')
        # was_url = url_for(filename='was.html')
        # waf_url = url_for(filename='waf.html')
        # handle_url = url_for(filename='handle_data.html')

        return flask.Response(tmp1.generate(response=inner()), mimetype='text/html')

        # return flask.Response(tmp1.generate(response=response if response is None else response()))


    else:
        print("There was an error with post")


@main.route("/waf")
@login_required
def waf():
    return render_template("waf.html")
