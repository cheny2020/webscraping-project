from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

from wtforms.validators import DataRequired, Length
from wtforms.fields import *
from flask_wtf import FlaskForm, CSRFProtect
import time
from bnf import main_bnf
from europea import main_europeana
import pyplot
import table

app = Flask(__name__)
Bootstrap5(app)
csrf = CSRFProtect(app)
app.secret_key = 'dev'

class SearchForm(FlaskForm):
    keyword = StringField('Enter keyword:', validators=[DataRequired(), Length(1, 50)])
    submit = SubmitField()

@app.route('/', methods=['GET', 'POST'])
def index():
    searchform = SearchForm()
    if searchform.validate_on_submit():
        keyword = searchform.keyword.data
        res_bnf = main_bnf(keyword)
        if not res_bnf:
            res_bnf = "No result"
        res_europeana = main_europeana(keyword)
        err_msg = ""
        if type(res_bnf) == str:
            err_msg = res_bnf
            res_bnf = []
        if type(res_europeana) ==  str:
            err_msg += res_europeana
            res_europeana = []

        img1= pyplot.get_all_providers(res_europeana, res_bnf)
        img2= pyplot.bar_graph(res_europeana, res_bnf)

        table_europea = table.table_europea(res_europeana)
        table_bnf = table.table_bnf(res_bnf)

        return render_template("index.html",keyword=keyword,img1=img1,img2=img2, table_europea=table_europea, table_bnf=table_bnf, errmsg=err_msg, button_form=searchform, is_result=True)
    return render_template("index.html",keyword="", button_form=searchform)


if __name__ == '__main__':
    app.run(debug=True)
