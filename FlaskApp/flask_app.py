from flask import (Flask, abort, redirect, render_template,
                   request, url_for,abort)
from flask.blueprints import Blueprint
from database import Session as DB,Base,engine
from db_tables import *
from sqlalchemy import insert
from flask_qrcode import QRcode
from flask.helpers import send_file
# endregion imports


def flask_app():

    # region config
    app = Flask(__name__,template_folder="html", static_folder="css")
    #app.config["APPLICATION_ROOT"] = "/nachhilfeboerse"
    # # region server_localhost_switch
    # if os.environ.get("FLASK_LOCALHOST") != "True":
    #     # TODO Get servername
    #     app.config["SERVER_NAME"] = "rpl-51485-0.dn.mnsnet.de"
    #     webProtocolScheme = "https"
    # else:
    #     webProtocolScheme = "http"
    # # endregion server_localhost_switch
    Base.metadata.create_all(engine)
    qrcode=QRcode(app)
    # region Blueprints
    imagesBlueprint = Blueprint('images', __name__, static_folder='images')
    app.register_blueprint(imagesBlueprint)
    # endregion Blueprints


    #Base.metadata.create_all(engine)

    # endregion config

    # region quiz
    @app.route("/quiz/<quiz_id>",methods=["GET","POST"])
    def index(quiz_id):

        dbSession = DB()
        quiz_data = dbSession.query(ReliSpiel).filter(
            ReliSpiel.id == quiz_id).first()
        dbSession.close()
        if quiz_data is not None:
            if request.method=="POST":
                if request.form.get("quizResult")==quiz_data.solution:
                    return quiz_data.result
                
            return render_template("quiz.html",quizId=quiz_data.id)
        return abort(404)
    # endregion index

        # region quiz
    @app.route("/editQuiz",methods=["GET","POST"])
    def adminArea():
        dbSession = DB()
        if request.method=="POST":
            
            if "Adminpassword" in request.form:
                if request.form.get("Adminpassword")=="Jan":
                    quiz_data=dbSession.query(ReliSpiel).all()
                    return render_template("adminArea.html",quiz_data=quiz_data)
                
            qr=[qr[3:] for qr in request.form if qr[:3] == "qr_"]

            if len(qr)>0:
                return send_file(qrcode(url_for('index' ,quiz_id=qr[0],_external=True), mode="raw"), mimetype="image/png",as_attachment=True,attachment_filename="QuizQr-"+qr[0])
            
            if "modify" in request.form:
                newData = {}
                keys = [key[4:] for key in request.form if key[:3] == "key"]

                for k in keys:
                    dbSession.query(ReliSpiel).filter(ReliSpiel.id==k).update({
                        "id":request.form.get(f"key_{k}"),
                        "solution":request.form.get(f"solution_{k}"),
                        "result":request.form.get(f"result_{k}")
                        })
                dbSession.commit()
                    
                if request.form.get("add_key") != "":
                    dbSession.add(ReliSpiel(id=request.form.get("add_key"),solution=request.form.get("add_data"),result=request.form.get("add_result")))
                    dbSession.commit()
                    
                quiz_data=dbSession.query(ReliSpiel).all()
                return render_template("adminArea.html",quiz_data=quiz_data)
        return render_template("login.html")
    # endregion index

    return app
