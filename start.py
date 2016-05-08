from flask.ext.wtf import Form

from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required

from flask import Flask
from flaskext.mysql import MySQL
from flask import render_template
from flask import jsonify
from flask import request
import json
import random
import os

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'wn_pro_mysql'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# @app.route("/")
# def one_html():
# 	return render_template("Bar_Chat.html", title = 'Projects')@app.route("/")
@app.route("/test")
def test():
	return jsonify({"hello":"dear"})

@app.route("/")
def one_html():
	return render_template("Bar_Chat.html", title = 'Projects')

@app.route("/word_count")
def word_count():
	cursor = mysql.connect().cursor()
	list_of_dict = []
	key = ''
	val = ''
	for word in range(97,123):
		var1 = chr(word)
		subSet  = {}
		#print var1
  		cursor.execute("SELECT count(word) from wn_synset WHERE word LIKE '{:s}%%'".format(var1))
  		data = cursor.fetchone()
	  	key = str(var1)
	  	val = data[0]
	  	subSet['index'] = key
	  	subSet['0'] = val
	  	list_of_dict.append(subSet)	
	return json.dumps(list_of_dict)
@app.route('/my-form.html')
def my_form():
    return render_template("my-form.html")

@app.route('/abcd', methods=['GET'])
def my_form_post():

	i = 0
	text = request.args.get('text')
	elementsSet ={}
	dataList = []
	dataSet = {}
	subSet ={}
	dataList1 = []
	cursor = mysql.connect().cursor()
	list_of_dict = []
	word = text
	var1 = word
	shapes = ["rectangle","roundrectangle","ellipse","triangle","square","pentagon","hexagon","heptagon","octagon","star","diamond","vee","rhomboid","polygon"]
	subSet['id'] = word
	subSet['name'] = word
	subSet['weight'] = 90
	color = lambda: random.randint(0,255)
	subSet['faveColor'] = ('#%02X%02X%02X' % (color(),color(),color()))#'#6FB1FC'
	subSet['faveShape'] = 'triangle'
	dataSet['data'] = subSet
	dataList.append(dataSet)
	cursor.execute("SELECT substr(synset_id,1,10) from wn_synset WHERE word ='{:s}'".format(word))
	data = cursor.fetchall()
	for row in data:
		print (row[0])
		list_of_dict.append(str(row[0]))
	idList = ",".join(list_of_dict)	
	list_l =['wn_antonym','wn_attr_adj_noun','wn_cause','wn_class_member','wn_entails','wn_hyponym','wn_hypernym','wn_mbr_meronym','wn_part_meronym','wn_subst_meronym','wn_participle','wn_pertainym','wn_see_also','wn_similar','wn_verb_group']
	for r in list_l:
		cursor.execute("SELECT count(*) from {:s} where synset_id_1 in ({:s})".format(r,idList))
 		antonym_data = cursor.fetchone()
 		if antonym_data[0] != 0:
 			dataSeta = {}
			subSeta ={}
			print (r,antonym_data[0])
			
			if i > 13:
				i=0
			
			subSeta['id'] = r
			subSeta['name'] = r
			subSeta['weight'] = antonym_data[0]
			color = lambda: random.randint(0,255)
			subSeta['faveColor'] = ('#%02X%02X%02X' % (color(),color(),color()))#'#EDA1ED'
			subSeta['faveShape'] = shapes[i]
			dataSeta['data'] = subSeta
			dataList.append(dataSeta)
			#print (dataList)
			
			dataSet1 = {}
			subSet1 ={}

			subSet1['source'] = word
			subSet1['target'] = r
			subSet1['faveColor'] = '#6FB1FC'
			subSet1['strength'] = 90
			dataSet1['data'] = subSet1
			dataList1.append(dataSet1)
			i = i+1
			#print (dataList1)
	
	elementsSet['nodes'] = dataList
 
	elementsSet['edges'] = dataList1

	return jsonify(elementsSet) 

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0",port=port,debug=True)
