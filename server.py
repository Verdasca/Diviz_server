from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


#from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import traceback
import os
import xml.dom.minidom
import xml.etree.ElementTree as ET
import requests
import shutilwhich
import shutil

from xml.dom.minidom import parse

from xml.dom import minidom

from docopt import docopt

from common import assignments_as_intervals_to_xmcda, create_messages_file, \
    get_dirs, get_error_message, get_input_data, get_relation_type, write_xmcda

from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.dbref import DBRef

import simplejson as json 
from pprint import pprint

from datetime import datetime

__version__ = '0.2.0'

# Executes when the page is loaded
@app.route('/')
def index():
	return render_template('template.html')

# Go back to project section
@app.route('/projectSection/')
def projectSection():
	#Get user name from url parameter projectId
	name = request.args.get('n')
	print (name)
	# Connection to Mongo DB
	try:
	    connection = pymongo.MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd')
	    print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e 
	db = connection['cristinav_bd']
	# Get projects collection
	users = db['users']
	rightUser = users.find_one({"username" : name })
	print rightUser['_id']
	userId = str(rightUser['_id'])
	url = 'http://mcdaframework.sysresearch.org/projects.html?userId='+userId
	return redirect(url, code=302)


# Execute method Electre Tri C
@app.route('/electreTriC/')
def electreTriC():
	#Get project id from url parameter projectId
	projectID = request.args.get('projectId')
	#Get user name from url parameter n
	name = request.args.get('n')
	#url for redirecting, goes back to the result page after executing the function
	url = 'http://mcdaframework.sysresearch.org/results.html?projectId='+projectID+'&n='+name 
	#url = 'http://localhost:8080/results.html?projectId='+projectID+'&n='+name 
	# Create a json file that indicates the state of the Electre Tri-C method (if is executable or not)
 	checkData = {}
 	# Delete files from inputsOutputs before executing the function to prevent errors or getting the wrong file (if it wasn't updated)
 	# From electreTriC
 	if os.path.exists('./inputsOutputs/electreTriC/in/alternatives.xml'):
 		os.unlink('./inputsOutputs/electreTriC/in/alternatives.xml')
	if os.path.exists('./inputsOutputs/electreTriC/in/classes.xml'):
 		os.unlink('./inputsOutputs/electreTriC/in/classes.xml')
 	if os.path.exists('./inputsOutputs/electreTriC/in/classes_profiles.xml'):
 		os.unlink('./inputsOutputs/electreTriC/in/classes_profiles.xml')
 	if os.path.exists('./inputsOutputs/electreTriC/in/credibility.xml'):
 		os.unlink('./inputsOutputs/electreTriC/in/credibility.xml')
 	if os.path.exists('./inputsOutputs/electreTriC/in/outranking.xml'):
 		os.unlink('./inputsOutputs/electreTriC/in/outranking.xml')
 	if os.path.exists('./inputsOutputs/electreTriC/out/messages.xml'):
 		os.unlink('./inputsOutputs/electreTriC/out/messages.xml')
 	if os.path.exists('./inputsOutputs/electreTriC/out/assignments.xml'):
 		os.unlink('./inputsOutputs/electreTriC/out/assignments.xml')
 	# From discordance
 	if os.path.exists('./inputsOutputs/discordance/in/alternatives.xml'):
 		os.unlink('./inputsOutputs/discordance/in/alternatives.xml')
	if os.path.exists('./inputsOutputs/discordance/in/criteria.xml'):
 		os.unlink('./inputsOutputs/discordance/in/criteria.xml')
 	if os.path.exists('./inputsOutputs/discordance/in/classes_profiles.xml'):
 		os.unlink('./inputsOutputs/discordance/in/classes_profiles.xml')
 	if os.path.exists('./inputsOutputs/discordance/in/performance_table.xml'):
 		os.unlink('./inputsOutputs/discordance/in/performance_table.xml')
 	if os.path.exists('./inputsOutputs/discordance/in/profiles_performance_table.xml'):
 		os.unlink('./inputsOutputs/discordance/in/profiles_performance_table.xml')
 	if os.path.exists('./inputsOutputs/discordance/out/messages.xml'):
 		os.unlink('./inputsOutputs/discordance/out/messages.xml')
 	if os.path.exists('./inputsOutputs/discordance/out/discordance.xml'):
 		os.unlink('./inputsOutputs/discordance/out/discordance.xml')
 	if os.path.exists('./inputsOutputs/discordance/out/counter_veto_crossed.xml'):
 		os.unlink('./inputsOutputs/discordance/out/counter_veto_crossed.xml')
 	# From cutRelationCrisp
 	if os.path.exists('./inputsOutputs/cutRelationCrisp/in/alternatives.xml'):
 		os.unlink('./inputsOutputs/cutRelationCrisp/in/alternatives.xml')
 	if os.path.exists('./inputsOutputs/cutRelationCrisp/in/classes_profiles.xml'):
 		os.unlink('./inputsOutputs/cutRelationCrisp/in/classes_profiles.xml')
 	if os.path.exists('./inputsOutputs/cutRelationCrisp/in/credibility.xml'):
 		os.unlink('./inputsOutputs/cutRelationCrisp/in/credibility.xml')
 	if os.path.exists('./inputsOutputs/cutRelationCrisp/in/method_parameters.xml'):
 		os.unlink('./inputsOutputs/cutRelationCrisp/in/method_parameters.xml')
 	if os.path.exists('./inputsOutputs/cutRelationCrisp/out/messages.xml'):
 		os.unlink('./inputsOutputs/cutRelationCrisp/out/messages.xml')
 	if os.path.exists('./inputsOutputs/cutRelationCrisp/out/outranking.xml'):
 		os.unlink('./inputsOutputs/cutRelationCrisp/out/outranking.xml')
 	# From credibility
 	if os.path.exists('./inputsOutputs/credibility/in/alternatives.xml'):
 		os.unlink('./inputsOutputs/credibility/in/alternatives.xml')
 	if os.path.exists('./inputsOutputs/credibility/in/classes_profiles.xml'):
 		os.unlink('./inputsOutputs/credibility/in/classes_profiles.xml')
 	if os.path.exists('./inputsOutputs/credibility/in/concordance.xml'):
 		os.unlink('./inputsOutputs/credibility/in/concordance.xml')
 	if os.path.exists('./inputsOutputs/credibility/in/discordance.xml'):
 		os.unlink('./inputsOutputs/credibility/in/discordance.xml')
 	if os.path.exists('./inputsOutputs/credibility/out/messages.xml'):
 		os.unlink('./inputsOutputs/credibility/out/messages.xml')
 	if os.path.exists('./inputsOutputs/credibility/out/credibility.xml'):
 		os.unlink('./inputsOutputs/credibility/out/credibility.xml')
 	# From concordance
 	if os.path.exists('./inputsOutputs/concordance/in/alternatives.xml'):
 		os.unlink('./inputsOutputs/concordance/in/alternatives.xml')
 	if os.path.exists('./inputsOutputs/concordance/in/classes_profiles.xml'):
 		os.unlink('./inputsOutputs/concordance/in/classes_profiles.xml')
 	if os.path.exists('./inputsOutputs/concordance/in/criteria.xml'):
 		os.unlink('./inputsOutputs/concordance/in/criteria.xml')
 	if os.path.exists('./inputsOutputs/concordance/in/weights.xml'):
 		os.unlink('./inputsOutputs/concordance/in/weights.xml')
 	if os.path.exists('./inputsOutputs/concordance/in/performance_table.xml'):
 		os.unlink('./inputsOutputs/concordance/in/performance_table.xml')
 	if os.path.exists('./inputsOutputs/concordance/in/profiles_performance_table.xml'):
 		os.unlink('./inputsOutputs/concordance/in/profiles_performance_table.xml')
 	if os.path.exists('./inputsOutputs/concordance/out/messages.xml'):
 		os.unlink('./inputsOutputs/concordance/out/messages.xml')
 	if os.path.exists('./inputsOutputs/concordance/out/concordance.xml'):
 		os.unlink('./inputsOutputs/concordance/out/concordance.xml')
 	print 'Done deleting old files from inputsOutputs.'
	# Connection to Mongo DB
	try:
	    connection = pymongo.MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd')
	    print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
		print "Could not connect to MongoDB: %s" % e 
	db = connection['cristinav_bd']
	# Get users collection
	users = db['users']
	# Get projects collection
	projects = db['projects']
	# Set project id from the url parameter as the project we need to get the data to execute the method
	project_id = projectID
	#userProject = users.find_one({"_id" : ObjectId('576b2f353b4de674060fd244') })
	# Lists to save the data from projectId
	alternativesList = []
	criteriaList = []
	categoriesList = []
	parametersList = []
	performancetablesList = []
	profiletablesList = []
	# Get project with projectID as id
	project = projects.find_one({"_id" : ObjectId(project_id) })
	# Check if the project as all the data necessary and not empty or need to fill first
	empty1 = len(project["alternatives"]) == 0
	collectionName = "alternatives"
	checkData[collectionName] = empty1
	empty2 = len(project["criteria"]) == 0
	collectionName = "criterions"
	checkData[collectionName] = empty2
	empty3 = len(project["parameters"]) == 0
	collectionName = "parameters"
	checkData[collectionName] = empty3
	empty4 = len(project["categories"]) == 0
	collectionName = "categories"
	checkData[collectionName] = empty4
	empty5 = len(project["performancetables"]) == 0
	collectionName = "performancetables"
	checkData[collectionName] = empty5
	empty6 = len(project["profiletables"]) == 0
	collectionName = "profiletables"
	checkData[collectionName] = empty6
	# Convert the checkData so it can be saved into a json file
	checkDataDumps = json.dumps(checkData)
	# Delete folder of the project before checking if the data is empty or missing
	pathId = './static/' + str(projectID)
	chechDataFileName = pathId + '/checkData.json'
	if os.path.exists(pathId):
		if os.path.exists(chechDataFileName):
			os.remove(chechDataFileName)
		paths = pathId + '/assignments.xml'
		if os.path.exists(paths):
			# Unliks the file path because only deleting does not make the file disappear, it still be access by the XMLHttpRequest
			os.unlink(paths)
		#if os.path.exists(paths):
			#os.remove(paths)
		paths = pathId + '/messages.xml'
		if os.path.exists(paths):
			os.remove(paths)
		shutil.rmtree(pathId) 
	os.makedirs(pathId)
	with open(chechDataFileName, 'w') as fp:
			fp.write(checkDataDumps) 
	# If some data are empty then end the function and return to the html page
	if empty1 or empty2 or empty3 or empty4 or empty5 or empty6:
		print 'Error: some data are empty, so the function ends without even trying...'
		#return render_template('template.html')
		return redirect(url, code=302)
	# Create alternatives.json
	# Get alternatives data from the project
	for alternative in project["alternatives"]:
		alt = db.alternatives.find_one({"_id" : alternative } , {'_id': False})
		alternativesList.append(alt)
	alternativesDumps = json.dumps(alternativesList)
	with open(pathId+'/alternatives.json', 'w') as fp:
		fp.write(alternativesDumps) 
	# Create weights.json
	# Get criteria data from the project
	for criterion in project["criteria"]:
		cri = db.criterions.find_one({"_id" : criterion } , {'_id': False})
		criteriaList.append(cri)
		# print cri
		# print cri['weight'] == None
		# print cri['veto'] == None
		# print cri['preference'] == None
		# print cri['indifference'] == None
		# print cri['direction'] == ''
		# If any data is missing (null, empty or none), stop the function from executing because it will give an error
		#if cri['weight'] == None or cri['veto'] == None or cri['preference'] == None or cri['indifference'] == None or cri['direction'] == '':
			#print 'Some data is missing...'
			#return render_template('template.html')
			#return redirect(url, code=302)
	criteriaDumps = json.dumps(criteriaList)
	with open(pathId+'/weights.json', 'w') as fp:
		fp.write(criteriaDumps) 
	# Create categories.json
	# Get categories data from the project
	for category in project["categories"]:
		cat = db.categories.find_one({"_id" : category } , {'_id': False})
		categoriesList.append(cat)
	categoriesDumps = json.dumps(categoriesList)
	with open(pathId+'/categories.json', 'w') as fp:
		fp.write(categoriesDumps) 
	# Create parameters.json
	# Get parameters data from the project
	for parameter in project["parameters"]:
		par = db.parameters.find_one({"_id" : parameter } , {'_id': False})
		parametersList.append(par)
	parametersDumps = json.dumps(parametersList)
	with open(pathId+'/parameters.json', 'w') as fp:
		fp.write(parametersDumps) 
	# Create performances.json
	# Get performances data from the project
	for performance in project["performancetables"]:
		per = db.performancetables.find_one({"_id" : performance } , {'_id': False})
		performancetablesList.append(per)
	performancesDumps = json.dumps(performancetablesList)
	with open(pathId+'/performances.json', 'w') as fp:
		fp.write(performancesDumps) 
	# Create profiles.json
	# Get profiles data from the project
	for profile in project["profiletables"]:
		pro = db.profiletables.find_one({"_id" : profile } , {'_id': False})
		profiletablesList.append(pro)
	profilesDumps = json.dumps(profiletablesList)
	with open(pathId+'/profiles.json', 'w') as fp:
		fp.write(profilesDumps) 
	# Create alternatives.xml
	# Get alternatives collection from mongodb
	#collection = db['alternatives'] 
	# Get all alternatives without the id attribute
	#alternativeList = list(collection.find(projection={"_id": False}))
	# Convert the alternative so it can be saved into a json file
	#alternativesDumps = json.dumps(alternativeList)
	#with open('alternatives.json', 'w') as fp:
		#fp.write(alternativesDumps) 
	# Create alternatives.xml
	# Open the alternatives json file to get the content and save it into a xml file	
	with open(pathId+'/alternatives.json') as data_file:    
		data = json.load(data_file)
	#pprint(data)	
	# Start creating the alternatives xml file
	doc = minidom.Document()
	# Create xmcda tag
	xmcda = doc.createElement('xmcda:XMCDA')
	xmcda.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcda.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcda.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	doc.appendChild(xmcda)
	# Create alternatives tag
	alternatives = doc.createElement('alternatives')
	xmcda.appendChild(alternatives)
	# Create al alternative tag with the names
	for d in data:
		alternativeName = d["name"]
		alternative = doc.createElement('alternative')
		alternative.setAttribute('id', alternativeName)
		alternatives.appendChild(alternative)
	xml_str = doc.toprettyxml(indent="  ")
	#with open("alternatives.xml", "w") as f:
	    #f.write(xml_str)  
	with open("inputsOutputs/electreTriC/in/alternatives.xml", "w") as f:
	    f.write(xml_str)  	
	with open("inputsOutputs/credibility/in/alternatives.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/concordance/in/alternatives.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/alternatives.xml", "w") as f:
	    f.write(xml_str)
	with open("inputsOutputs/cutRelationCrisp/in/alternatives.xml", "w") as f:
	    f.write(xml_str)     
	# Create weights.xml
	# Get criterions collection from mongodb
	# collection = db['criterions'] 
	# # Get all criteria without the id attribute
	# criteriaList = list(collection.find(projection={"_id": False}))
	# # Convert the alternative so it can be saved into a json file
	# criteriaDumps = json.dumps(criteriaList)
	# with open('weights.json', 'w') as fp:
	# 	fp.write(criteriaDumps) 
	# Create weights.xml
	# Open the alternatives json file to get the content and save it into a xml file	
	with open(pathId+'/weights.json') as data_file:    
		data = json.load(data_file)
	# Start creating the weights xml file
	docWeight = minidom.Document()
	# Create xmcda tag
	xmcdaWeight = doc.createElement('xmcda:XMCDA')
	xmcdaWeight.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaWeight.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaWeight.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docWeight.appendChild(xmcdaWeight)
	# Create alternatives tag
	criteriaValues = docWeight.createElement('criteriaValues')
	xmcdaWeight.appendChild(criteriaValues)
	# Create al alternative tag 
	for d in data:
		criteriaName = d["name"]
		criteriaWeight = d["weight"]
		#print str(criteriaWeight)
		criterionValue = docWeight.createElement('criterionValue')
		criterionID = docWeight.createElement('criterionID')
		text = doc.createTextNode(criteriaName)
		criterionID.appendChild(text)
		criterionValue.appendChild(criterionID)
		value = docWeight.createElement('value')
		real = docWeight.createElement('real')
		text = doc.createTextNode(str(criteriaWeight))
		real.appendChild(text)
		value.appendChild(real)
		criterionValue.appendChild(value)
		criteriaValues.appendChild(criterionValue)
	xml_str = docWeight.toprettyxml(indent="  ")
	#with open("weights.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/concordance/in/weights.xml", "w") as f:
	    f.write(xml_str)      
	# Start creating the criteria xml file
	docCriteria = minidom.Document()
	# Create xmcda tag
	xmcdaCriteria = doc.createElement('xmcda:XMCDA')
	xmcdaCriteria.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaCriteria.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaCriteria.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docCriteria.appendChild(xmcdaCriteria)
	# Create alternatives tag
	criteria = docCriteria.createElement('criteria')
	xmcdaCriteria.appendChild(criteria)
	# Create al alternative tag 
	for d in data:
		criteriaName = d["name"]
		criteriaDescription = d["description"]
		criteriaDirection = d["direction"]
		criteriaIndifference = d["indifference"]
		criteriaPreference = d["preference"]
		criteriaVeto = d["veto"]
		criterion = docCriteria.createElement('criterion')
		criterion.setAttribute('id', criteriaName)
		criterion.setAttribute('name', criteriaDescription)
		scale = docCriteria.createElement('scale')
		quantitative = docCriteria.createElement('quantitative')
		preferenceDirection = docCriteria.createElement('preferenceDirection')
		text = doc.createTextNode(criteriaDirection)
		preferenceDirection.appendChild(text)
		quantitative.appendChild(preferenceDirection)
		scale.appendChild(quantitative)
		criterion.appendChild(scale)
		thresholds = docCriteria.createElement('thresholds')
		threshold = docCriteria.createElement('threshold')
		threshold.setAttribute('mcdaConcept', 'indifference')
		constant = docCriteria.createElement('constant')
		real = docCriteria.createElement('real')
		text = doc.createTextNode(str(criteriaIndifference))
		real.appendChild(text)
		constant.appendChild(real)
		threshold.appendChild(constant)
		thresholds.appendChild(threshold)
		threshold2 = docCriteria.createElement('threshold')
		threshold2.setAttribute('mcdaConcept', 'preference')
		constant = docCriteria.createElement('constant')
		real = docCriteria.createElement('real')
		text = doc.createTextNode(str(criteriaPreference))
		real.appendChild(text)
		constant.appendChild(real)
		threshold2.appendChild(constant)
		thresholds.appendChild(threshold2)
		threshold3 = docCriteria.createElement('threshold')
		threshold3.setAttribute('mcdaConcept', 'veto')
		constant = docCriteria.createElement('constant')
		real = docCriteria.createElement('real')
		text = doc.createTextNode(str(criteriaVeto))
		real.appendChild(text)
		constant.appendChild(real)
		threshold3.appendChild(constant)
		thresholds.appendChild(threshold3)
		criterion.appendChild(thresholds)
		criteria.appendChild(criterion)
	xml_str = docCriteria.toprettyxml(indent="  ")
	#with open("criteria.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/concordance/in/criteria.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/criteria.xml", "w") as f:
	    f.write(xml_str)
	# Create method_parameters.xml
	# Get parameters collection from mongodb
	# collection = db['parameters'] 
	# # Get all parameters without the id attribute
	# parametersList = list(collection.find(projection={"_id": False}))
	# # Convert the alternative so it can be saved into a json file
	# parametersDumps = json.dumps(parametersList)
	# with open('parameters.json', 'w') as fp:
	# 	fp.write(parametersDumps)
	# Create method_parameters.xml 
	# Open the alternatives json file to get the content and save it into a xml file	
	with open(pathId+'/parameters.json') as data_file:    
		data = json.load(data_file)
	# Start creating the method_parameters xml file
	docParameters = minidom.Document()
	# Create xmcda tag
	xmcdaParameters = doc.createElement('xmcda:XMCDA')
	xmcdaParameters.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2012/XMCDA-2.2.0')
	xmcdaParameters.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaParameters.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2012/XMCDA-2.2.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.2.0.xsd')
	docParameters.appendChild(xmcdaParameters)
	# Create parameters tag
	methodParameters = docParameters.createElement('methodParameters')
	xmcdaParameters.appendChild(methodParameters)
	if (len(data) == 0):
		credibility = 0
	else:
		# Create the parameter tag 
		credibility = data[0]["credibility"]
	parameter = docParameters.createElement('parameter')
	parameter.setAttribute('name', 'comparison_with')
	value = docParameters.createElement('value')
	label = docParameters.createElement('label')
	text = doc.createTextNode('central_profiles')
	label.appendChild(text)
	value.appendChild(label)
	parameter.appendChild(value)
	methodParameters.appendChild(parameter)
	parameter2 = docParameters.createElement('parameter')
	parameter2.setAttribute('name', 'cut_threshold')
	value2 = docParameters.createElement('value')
	real = docParameters.createElement('real')
	text = doc.createTextNode(str(credibility))
	real.appendChild(text)
	value2.appendChild(real)
	parameter2.appendChild(value2)
	methodParameters.appendChild(parameter2)
	xml_str = docParameters.toprettyxml(indent="  ")
	with open("inputsOutputs/cutRelationCrisp/in/method_parameters.xml", "w") as f:
	    f.write(xml_str)    
	# Create classes.xml
	# Get categories collection from mongodb
	# collection = db['categories'] 
	# # Get all categories without the id attribute
	# categoriesList = list(collection.find(projection={"_id": False}))
	# # Convert the category so it can be saved into a json file
	# categoriesDumps = json.dumps(categoriesList)
	# with open('categories.json', 'w') as fp:
	# 	fp.write(categoriesDumps) 
	# Create classes.xml
	# Open the categories json file to get the content and save it into a xml file	
	with open(pathId+'/categories.json') as data_file:    
		data = json.load(data_file)
	# Start creating classes xml file
	docClasses = minidom.Document()
	# Create xmcda tag
	xmcdaClasses = doc.createElement('xmcda:XMCDA')
	xmcdaClasses.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaClasses.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaClasses.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docClasses.appendChild(xmcdaClasses)
	# Create categories tag
	categories = docClasses.createElement('categories')
	xmcdaClasses.appendChild(categories)
	# Create all categories tag 
	for d in data:
		categoryName = d["name"]
		categoryRank = d["rank"]
		category = docClasses.createElement('category')
		category.setAttribute('id', categoryName)
		rank = docClasses.createElement('rank')
		integer = docClasses.createElement('integer')
		text = doc.createTextNode(str(categoryRank))
		integer.appendChild(text)
		rank.appendChild(integer)
		category.appendChild(rank)
		categories.appendChild(category)
	xml_str = docClasses.toprettyxml(indent="  ")
	#with open("classes.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/electreTriC/in/classes.xml", "w") as f:
	    f.write(xml_str)   
	# Start creating classes_profiles xml file
	docClassesProfiles = minidom.Document()
	# Create xmcda tag
	xmcdaClassesProfiles = doc.createElement('xmcda:XMCDA')
	xmcdaClassesProfiles.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaClassesProfiles.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaClassesProfiles.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docClassesProfiles.appendChild(xmcdaClassesProfiles)
	# Create categoriesProfiles tag
	categoriesProfiles = docClassesProfiles.createElement('categoriesProfiles')
	xmcdaClassesProfiles.appendChild(categoriesProfiles)
	# Create all categories profiles tag
	for d in data:
		categoryName = d["name"]
		actionName = d["action"]
		categoryProfile = docClassesProfiles.createElement('categoryProfile')
		alternativeID = docClassesProfiles.createElement('alternativeID')
		text = doc.createTextNode(actionName)
		alternativeID.appendChild(text)
		categoryProfile.appendChild(alternativeID)
		central = docClassesProfiles.createElement('central')
		categoryID = docClassesProfiles.createElement('categoryID')
		text = doc.createTextNode(categoryName)
		categoryID.appendChild(text)
		central.appendChild(categoryID)
		categoryProfile.appendChild(central)
		categoriesProfiles.appendChild(categoryProfile)
	xml_str = docClassesProfiles.toprettyxml(indent="  ")
	#with open("classes_profiles.xml", "w") as f:
	    #f.write(xml_str)   
	with open("inputsOutputs/electreTriC/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str)  	
	with open("inputsOutputs/credibility/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/concordance/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str)
	with open("inputsOutputs/cutRelationCrisp/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str)   
	# Create performance_table.xml
	# Get performances collection from mongodb
	# collection = db['performancetables'] 
	# # Get all performances without the id attribute
	# performancesList = list(collection.find(projection={"_id": False}))
	# # Convert the performances so it can be saved into a json file
	# performancesDumps = json.dumps(performancesList)
	# with open('performances.json', 'w') as fp:
	# 	fp.write(performancesDumps) 
	# Create performance_table.xml
	# Open the performances json file to get the content and save it into a xml file	
	with open(pathId+'/performances.json') as data_file:    
		data = json.load(data_file)
	# Start creating performance_table xml file
	docPerformances = minidom.Document()
	# Create xmcda tag
	xmcdaPerformances = doc.createElement('xmcda:XMCDA')
	xmcdaPerformances.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaPerformances.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaPerformances.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docPerformances.appendChild(xmcdaPerformances)
	# Create performances tag
	performanceTable = docPerformances.createElement('performanceTable')
	xmcdaPerformances.appendChild(performanceTable)
	# Create a check list to save which alternative name was already created in the xml file
	checkList = {}
	f = False
	t = True
	for d in data:
		altName = d["alternative"]
		checkList[altName] = f
	#print checkList
	# Create all performances tag 
	for d in data:
		alternativeId = d["alternative"]
		for alt, check in checkList.items():
			if alt == alternativeId:
				if check == False:
					checkList[alt] = t
					alternativePerformances = docPerformances.createElement('alternativePerformances')
					alternativeID = docPerformances.createElement('alternativeID')
					text = doc.createTextNode(alternativeId)
					alternativeID.appendChild(text)
					alternativePerformances.appendChild(alternativeID)
					for dd in data:
						performanceAlternative = dd["alternative"]
						performanceCriterion = dd["criterion"]
						performanceValue = dd["value"]
						if performanceAlternative == alternativeId:
							performance = docPerformances.createElement('performance')
							criterionID = docPerformances.createElement('criterionID')
							text = doc.createTextNode(performanceCriterion)
							criterionID.appendChild(text)
							performance.appendChild(criterionID)
							value = docPerformances.createElement('value')
							real = docPerformances.createElement('real')
							text = doc.createTextNode(str(performanceValue))
							real.appendChild(text)
							value.appendChild(real)
							performance.appendChild(value)
							alternativePerformances.appendChild(performance)
						else:
							#Do nothing
							pass

				else:
					pass
			else:
				pass
		
		performanceTable.appendChild(alternativePerformances)
	#print checkList
	xml_str = docPerformances.toprettyxml(indent="  ")
	#with open("performance_table.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/concordance/in/performance_table.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/performance_table.xml", "w") as f:
	    f.write(xml_str)
	# Create profiles_performance_table.xml
	# Get profiles collection from mongodb
	# collection = db['profiletables'] 
	# # Get all profiles without the id attribute
	# profilesList = list(collection.find(projection={"_id": False}))
	# # Convert the profiles so it can be saved into a json file
	# profilesDumps = json.dumps(profilesList)
	# with open('profiles.json', 'w') as fp:
	# 	fp.write(profilesDumps) 
	# Create profiles_performance_table.xml
	# Open the profiles json file to get the content and save it into a xml file	
	with open(pathId+'/profiles.json') as data_file:    
		data = json.load(data_file)
	# Start creating profiles_performance_table xml file
	docProfiles = minidom.Document()
	# Create xmcda tag
	xmcdaProfiles = doc.createElement('xmcda:XMCDA')
	xmcdaProfiles.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	docProfiles.appendChild(xmcdaProfiles)
	# Create profiles tag
	performanceTbl = docProfiles.createElement('performanceTable')
	performanceTbl.setAttribute('mcdaConcept', 'Fictive')
	xmcdaProfiles.appendChild(performanceTbl)
	# Create a check list to save which reference action name was already created in the xml file
	checkListProfiles = {}
	ff = False
	tt = True
	for d in data:
		refName = d["action"]
		checkListProfiles[refName] = ff
	#print checkListProfiles
	# Create all profiles tag 
	for d in data:
		actionId = d["action"]
		for ref, check in checkListProfiles.items():
			if ref == actionId:
				if check == False:
					checkListProfiles[ref] = tt
					alternativePerf = docProfiles.createElement('alternativePerformances')
					alternativeID2 = docProfiles.createElement('alternativeID')
					text = doc.createTextNode(actionId)
					alternativeID2.appendChild(text)
					alternativePerf.appendChild(alternativeID2)
					for dd in data:
						profileAction = dd["action"]
						profileCriterion = dd["criterion"]
						profileValue = dd["value"]
						if profileAction == actionId:
							performance2 = docProfiles.createElement('performance')
							criterionID2 = docProfiles.createElement('criterionID')
							text = doc.createTextNode(profileCriterion)
							criterionID2.appendChild(text)
							performance2.appendChild(criterionID2)
							value2 = docProfiles.createElement('value')
							integer2 = docProfiles.createElement('integer')
							text = doc.createTextNode(str(int(profileValue)))
							integer2.appendChild(text)
							value2.appendChild(integer2)
							performance2.appendChild(value2)
							alternativePerf.appendChild(performance2)
						else:
							#Do nothing
							pass

				else:
					pass
			else:
				pass
		
		performanceTbl.appendChild(alternativePerf)
	xml_str = docProfiles.toprettyxml(indent="  ")
	#with open("profiles_performance_table.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/concordance/in/profiles_performance_table.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/profiles_performance_table.xml", "w") as f:
	    f.write(xml_str) 
	try:
		os.remove('./inputsOutputs/electreTriC/out/assignments.xml')
	except OSError:
		pass
	#os.remove('./inputsOutputs/electreTriC/out/assignments.xml')
	os.system('python ./electre_diviz/ElectreConcordance/ElectreConcordance.py -i ./inputsOutputs/concordance/in -o ./inputsOutputs/concordance/out') 
	if not os.path.exists('./inputsOutputs/concordance/out/concordance.xml'):
		print 'Error from Concordance method: probably invalid data...'
		#return render_template('template.html')	
		saveResultError()
		return redirect(url, code=302)
	os.system('python ./electre_diviz/ElectreDiscordance/ElectreDiscordance.py -i ./inputsOutputs/discordance/in -o ./inputsOutputs/discordance/out') 
	if not os.path.exists('./inputsOutputs/discordance/out/discordance.xml'):
		print 'Error from Discordance method: probably invalid data...'
		#return render_template('template.html')	
		saveResultError()
		return redirect(url, code=302)
	shutil.copy2('./inputsOutputs/concordance/out/concordance.xml', './inputsOutputs/credibility/in/concordance.xml')
	shutil.copy2('./inputsOutputs/discordance/out/discordance.xml', './inputsOutputs/credibility/in/discordance.xml')
	os.system('python ./electre_diviz/ElectreCredibility/ElectreCredibility.py -i ./inputsOutputs/credibility/in -o ./inputsOutputs/credibility/out')
	if not os.path.exists('./inputsOutputs/credibility/out/credibility.xml'):
		print 'Error from Credibility method: probably invalid data...'
		#return render_template('template.html')
		saveResultError()	
		return redirect(url, code=302)
	shutil.copy2('./inputsOutputs/credibility/out/credibility.xml', './inputsOutputs/cutRelationCrisp/in/credibility.xml')
	shutil.copy2('./inputsOutputs/credibility/out/credibility.xml', './inputsOutputs/electreTriC/in/credibility.xml')
	os.system('python ./electre_diviz/cutRelationCrisp/cutRelationCrisp.py -i ./inputsOutputs/cutRelationCrisp/in -o ./inputsOutputs/cutRelationCrisp/out')  
	if not os.path.exists('./inputsOutputs/cutRelationCrisp/out/outranking.xml'):
		print 'Error from CutRelationCrisp method: probably invalid data...'
		#return render_template('template.html')	
		saveResultError()
		return redirect(url, code=302)
	shutil.copy2('./inputsOutputs/cutRelationCrisp/out/outranking.xml', './inputsOutputs/electreTriC/in/outranking.xml')
	os.system('python ./electre_diviz/ElectreTri-CClassAssignments/ElectreTri-CClassAssignments.py -i ./inputsOutputs/electreTriC/in -o ./inputsOutputs/electreTriC/out')  
	# pathId = './static/' + str(projectID)
	# chechDataFileName = pathId + '/checkData.json'
	# if os.path.exists(pathId):
	# 	if os.path.exists(chechDataFileName):
	# 		os.remove(chechDataFileName)
	# 	paths = pathId + '/assignments.xml'
	# 	if os.path.exists(paths):
	# 		# Unliks the file path because only deleting does not make the file disappear, it still be access by the XMLHttpRequest
	# 		os.unlink(paths)
	# 	#if os.path.exists(paths):
	# 		#os.remove(paths)
	# 	paths = pathId + '/messages.xml'
	# 	if os.path.exists(paths):
	# 		os.remove(paths)
	# 	shutil.rmtree(pathId) 
	# os.makedirs(pathId)
	# with open(chechDataFileName, 'w') as fp:
	# 		fp.write(checkDataDumps) 
	# pp = 'rm -rf ' + pathId
	# #os.system(pp)
	# if not os.path.exists(pathId):
	# 	os.makedirs(pathId)
	# if os.path.exists(chechDataFileName):
	# 	with open(chechDataFileName, 'w') as fp:
	# 		fp.write(checkDataDumps) 
	try:
		if os.path.exists('./inputsOutputs/electreTriC/out/assignments.xml'):
			shutil.copy2('./inputsOutputs/electreTriC/out/assignments.xml', pathId+'/assignments.xml')
	except OSError:
		#pass
		saveResultError()
		return redirect(url, code=302)
	try:
		shutil.copy2('./inputsOutputs/electreTriC/out/messages.xml', pathId+'/messages.xml')
	except OSError:
		#pass
		saveResultError()
		return redirect(url, code=302)
	print 'Method executed and files saved.'
	#return render_template('template.html')
	saveResult()
	return redirect(url, code=302)

# Save results into the project on mongodb
#@app.route('/saveResult/')
def saveResult(): 
	#Get project id from url parameter projectId
	projectID = request.args.get('projectId')
	#Get user name from url parameter n
	name = request.args.get('n')
	#Get result name from url parameter resName
	resultName = request.args.get('resName')
	#Get notes from url parameter resName
	notes = request.args.get('notes')
	#Set the ok message
	messageOk = 'Everything OK. No errors.'
	# Set the path of the project folder
	path = './static/' + str(projectID)
	# Connection to Mongo DB
	try:
	    connection = pymongo.MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd')
	    print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e 
	db = connection['cristinav_bd']
	# Get projects collection
	projects = db['projects']
	# Set project id from the url parameter as the project we need to get the data to execute the method
	project_id = projectID
	# Get project with projectID as id
	project = projects.find_one({"_id" : ObjectId(project_id) })
	# Get the current number of executions (will be used as identifier for the new result save)
	executions = project["numExecutions"]
	# Update the dateSet and number of executions of the project
	projects.update_one({'_id': ObjectId(project_id)},{'$set': {'dateSet': datetime.utcnow(), 'numExecutions': executions + 1}}, upsert=False)
	print 'Projects dateSet and numExecutions updated'
	# Add a new identifier to the new result saving 
	projects.update_one({'_id': ObjectId(project_id)}, {'$push': {'results': {'identifier': executions, 'name': resultName, 'methodError': messageOk, 'resultDate': datetime.utcnow(), 'resultNotes':notes}}})
	# Get all the data from the json file inside the projects folder to save them on mongoDB
	with open(path+'/alternatives.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.alternativeValues': {'$each': data}}})
	with open(path+'/weights.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.criterionValues': {'$each': data}}})
	with open(path+'/categories.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.categoryValues': {'$each': data}}})
	with open(path+'/parameters.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.parameterValues': {'$each': data}}})
	with open(path+'/performances.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.performanceValues': {'$each': data}}})
	with open(path+'/profiles.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.profileValues': {'$each': data}}})
	# Transform the assignments.xml into json so the results can be saved on mongodb
	# List to save all results 
	resultList = []
	tree = ET.parse(path+'/assignments.xml')
	root = tree.getroot()
	# Get the data needed, alternative and its min/max category
	for child in root.iter('alternativeAffectation'):
		# Dict to save a result 
		values = {}
		# Get alternative value
		alternative = child.find('alternativeID').text
		categoriesInterval = child.find('categoriesInterval')
		lowerBound = categoriesInterval.find('lowerBound')
		upperBound = categoriesInterval.find('upperBound')
		# Get min category value
		lowerCategory = lowerBound.find('categoryID').text
		# Get max category value
		upperCategory = upperBound.find('categoryID').text
		# Add the values into the dict to be added to the list
		values['alternativeID'] = alternative
		values['minCategory'] = lowerCategory
		values['maxCategory'] = upperCategory
		resultList.append(values)
	# Save the data into a dict format so it can be saved on mongodb
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.resultValues': {'$each': resultList}}})
	print 'Done saving results.'
	#url = 'http://vps288667.ovh.net:3901/results.html?projectId='+projectID+'&n='+name 
	#url = 'http://localhost:8080/results.html?projectId='+projectID+'&n='+name 
	#return redirect(url, code=302)

def saveResultError(): 
	#Get project id from url parameter projectId
	projectID = request.args.get('projectId')
	#Get user name from url parameter n
	name = request.args.get('n')
	#Get result name from url parameter resName
	resultName = request.args.get('resName')
	#Get notes from url parameter resName
	notes = request.args.get('notes')
	#Get the message error
	messageError = 'Method could not be successfully executed. Please be sure that all data are consistent and with the right type. Make sure to have at least 2 or more elements in criteria, alternatives and categories. Check if the performance table has the right number of criteria/alternatives (and also the right names) and the profile performance table has the right number of criteria/reference actions (and also the right names). Credibility Lambda should be in range [0,5; 1,0].'
	# Set the path of the project folder
	path = './static/' + str(projectID)
	# Connection to Mongo DB
	try:
	    connection = pymongo.MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd')
	    print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e 
	db = connection['cristinav_bd']
	# Get projects collection
	projects = db['projects']
	# Set project id from the url parameter as the project we need to get the data to execute the method
	project_id = projectID
	# Get project with projectID as id
	project = projects.find_one({"_id" : ObjectId(project_id) })
	# Get the current number of executions (will be used as identifier for the new result save)
	executions = project["numExecutions"]
	# Update the dateSet and number of executions of the project
	projects.update_one({'_id': ObjectId(project_id)},{'$set': {'dateSet': datetime.utcnow(), 'numExecutions': executions + 1}}, upsert=False)
	print 'Projects dateSet and numExecutions updated'
	# Add a new identifier to the new result saving 
	projects.update_one({'_id': ObjectId(project_id)}, {'$push': {'results': {'identifier': executions, 'name': resultName, 'methodError': messageError, 'resultDate': datetime.utcnow(), 'resultNotes':notes}}})
	# Get all the data from the json file inside the projects folder to save them on mongoDB
	with open(path+'/alternatives.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.alternativeValues': {'$each': data}}})
	with open(path+'/weights.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.criterionValues': {'$each': data}}})
	with open(path+'/categories.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.categoryValues': {'$each': data}}})
	with open(path+'/parameters.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.parameterValues': {'$each': data}}})
	with open(path+'/performances.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.performanceValues': {'$each': data}}})
	with open(path+'/profiles.json') as data_file:    
		data = json.load(data_file)
	projects.update_one({'_id': ObjectId(project_id), 'results.identifier': executions}, {'$push': {'results.$.profileValues': {'$each': data}}})
	print 'Done saving error results.'

# ......................................................................................
# Test functions... for practise xml2json --input "cd_catalog.xml" --output "cd_catalog.json"

@app.route('/my-link/')
def my_link():
	os.remove('./inputsOutputs/electreTriC/out/assignments.xml')
	return 'Click.'

# Read final results obtained by the method Electre Tri C
@app.route('/readXMLFile/')
def readXMLFile(): 
	#xmldoc = minidom.parse('templates/cd_catalog.xml')
	#xmldoc = minidom.parse('inputsOutputs/electreTriC/out/assignments.xml')
	#itemlist = xmldoc.getElementsByTagName('alternativeID')[0]
	#t = itemlist.childNodes[0].data
	#return t
	#url="http://localhost:5000"
	#r = requests.get(url)
	#soup = BeautifulSoup(r.content)
	#links = soup.find("div", {"id":"content"})
	#t = links.contents[0].find("p", {"id":"demo"})[0].text
	#return t
	mech = Browser()
	url = "http://localhost:5000/read"
	page = mech.open(url)

	html = page.read()
	soup = BeautifulSoup(html)
	#soup.findAll('div', {"class":"jumbotron"}) 
	t = soup.find('body').text
	return t 

@app.route('/createDir/')
def createDir(): 
	projectID = request.args.get('projectId')
	pathId = './static/' + str(projectID)
	#print pathId
	if os.path.exists(pathId):
		shutil.rmtree(pathId) 
	os.makedirs(pathId)
	try:
		shutil.copy2('./inputsOutputs/electreTriC/out/assignments.xml', pathId)
	except OSError:
		pass
	try:
		shutil.copy2('./inputsOutputs/electreTriC/out/messages.xml', pathId)
	except OSError:
		pass
	print 'Done creating folder and files...'
	return render_template('template.html')

@app.route('/copiar/')
def copiar():
	#shutil.copy2('./inputsOutputs/concordance/out/concordance.xml', './inputsOutputs/concordance.xml')
	#shutil.copy2('./inputsOutputs/concordance/out/concordance.xml', 'http://localhost:8080/assignments.xml')
	filePath = "./inputsOutputs/concordance/out/concordance.xml"
	serverPath = "http://localhost:8080"
	shutil.copy2('./inputsOutputs/concordance/out/concordance.xml', 'http://localhost:8080')
	return render_template('template.html')

@app.route('/tri/')
def tri():
	os.system('python ./electre_diviz/ElectreTri-CClassAssignments/ElectreTri-CClassAssignments.py -i ./inputs -o ./outputs')  
	#DOMTree = xml.dom.minidom.parse("./outputs/assignments.xml")
	#collection = DOMTree.documentElement
	#movies = collection.getElementsByTagName("alternativeAffectation")
	#for movie in movies:
	   	#print '*****Alternatives*****'
	   	#if movie.hasAttribute("alternativeID"):
	      #print "ID: %s" % movie.getAttribute("alternativeID")
	#return 'Done!'
		#alternativeID = movie.getElementsByTagName('alternativeID')[0]
   		#teste = "Alternative: %s" % alternativeID.childNodes[0].data
   	#print teste 
	return render_template('template.html')


# Create xml files (with data obtained from the framework) necessary to execute the method Electre Tri C
@app.route('/createXMLFiles/')
def createXMLFiles():
	# Connection to Mongo DB
	try:
	    connection = pymongo.MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd')
	    print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e 
	db = connection['cristinav_bd']
	# Create alternatives.xml
	# Get alternatives collection from mongodb
	collection = db['alternatives'] 
	# Get all alternatives without the id attribute
	alternativeList = list(collection.find(projection={"_id": False}))
	# Convert the alternative so it can be saved into a json file
	alternativesDumps = json.dumps(alternativeList)
	with open('alternatives.json', 'w') as fp:
		fp.write(alternativesDumps) 
	# Open the alternatives json file to get the content and save it into a xml file	
	with open('alternatives.json') as data_file:    
		data = json.load(data_file)
	pprint(data)	
	print "-----------"
	#print data[0]["name"]
	#print "-----------"
	#print "-----------"
	#for d in data:
		#print d["name"]
	# Start creating the alternatives xml file
	doc = minidom.Document()
	# Create xmcda tag
	xmcda = doc.createElement('xmcda:XMCDA')
	xmcda.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcda.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcda.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	doc.appendChild(xmcda)
	# Create alternatives tag
	alternatives = doc.createElement('alternatives')
	xmcda.appendChild(alternatives)
	# Create al alternative tag with the names
	for d in data:
		alternativeName = d["name"]
		alternative = doc.createElement('alternative')
		alternative.setAttribute('id', alternativeName)
		alternatives.appendChild(alternative)
	xml_str = doc.toprettyxml(indent="  ")
	#with open("alternatives.xml", "w") as f:
	    #f.write(xml_str)  
	with open("inputsOutputs/electreTriC/in/alternatives.xml", "w") as f:
	    f.write(xml_str)  	
	with open("inputsOutputs/credibility/in/alternatives.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/concordance/in/alternatives.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/alternatives.xml", "w") as f:
	    f.write(xml_str)
	with open("inputsOutputs/cutRelationCrisp/in/alternatives.xml", "w") as f:
	    f.write(xml_str)     
	# Create weights.xml
	# Get criterions collection from mongodb
	collection = db['criterions'] 
	# Get all criteria without the id attribute
	criteriaList = list(collection.find(projection={"_id": False}))
	# Convert the alternative so it can be saved into a json file
	criteriaDumps = json.dumps(criteriaList)
	with open('weights.json', 'w') as fp:
		fp.write(criteriaDumps) 
	# Open the alternatives json file to get the content and save it into a xml file	
	with open('weights.json') as data_file:    
		data = json.load(data_file)
	#print "-----------"
	#pprint(data)	
	#print "-----------"
	#print data[0]["weight"]
	# Start creating the weights xml file
	docWeight = minidom.Document()
	# Create xmcda tag
	xmcdaWeight = doc.createElement('xmcda:XMCDA')
	xmcdaWeight.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaWeight.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaWeight.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docWeight.appendChild(xmcdaWeight)
	# Create alternatives tag
	criteriaValues = docWeight.createElement('criteriaValues')
	xmcdaWeight.appendChild(criteriaValues)
	# Create al alternative tag 
	for d in data:
		criteriaName = d["name"]
		criteriaWeight = d["weight"]
		#print str(criteriaWeight)
		criterionValue = docWeight.createElement('criterionValue')
		criterionID = docWeight.createElement('criterionID')
		text = doc.createTextNode(criteriaName)
		criterionID.appendChild(text)
		criterionValue.appendChild(criterionID)
		value = docWeight.createElement('value')
		real = docWeight.createElement('real')
		text = doc.createTextNode(str(criteriaWeight))
		real.appendChild(text)
		value.appendChild(real)
		criterionValue.appendChild(value)
		criteriaValues.appendChild(criterionValue)
	xml_str = docWeight.toprettyxml(indent="  ")
	#with open("weights.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/concordance/in/weights.xml", "w") as f:
	    f.write(xml_str)      
	# Start creating the criteria xml file
	docCriteria = minidom.Document()
	# Create xmcda tag
	xmcdaCriteria = doc.createElement('xmcda:XMCDA')
	xmcdaCriteria.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaCriteria.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaCriteria.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docCriteria.appendChild(xmcdaCriteria)
	# Create alternatives tag
	criteria = docCriteria.createElement('criteria')
	xmcdaCriteria.appendChild(criteria)
	# Create al alternative tag 
	for d in data:
		criteriaName = d["name"]
		criteriaDescription = d["description"]
		criteriaDirection = d["direction"]
		criteriaIndifference = d["indifference"]
		criteriaPreference = d["preference"]
		criteriaVeto = d["veto"]
		criterion = docCriteria.createElement('criterion')
		criterion.setAttribute('id', criteriaName)
		criterion.setAttribute('name', criteriaDescription)
		scale = docCriteria.createElement('scale')
		quantitative = docCriteria.createElement('quantitative')
		preferenceDirection = docCriteria.createElement('preferenceDirection')
		text = doc.createTextNode(criteriaDirection)
		preferenceDirection.appendChild(text)
		quantitative.appendChild(preferenceDirection)
		scale.appendChild(quantitative)
		criterion.appendChild(scale)
		thresholds = docCriteria.createElement('thresholds')
		threshold = docCriteria.createElement('threshold')
		threshold.setAttribute('mcdaConcept', 'indifference')
		constant = docCriteria.createElement('constant')
		real = docCriteria.createElement('real')
		text = doc.createTextNode(str(criteriaIndifference))
		real.appendChild(text)
		constant.appendChild(real)
		threshold.appendChild(constant)
		thresholds.appendChild(threshold)
		threshold2 = docCriteria.createElement('threshold')
		threshold2.setAttribute('mcdaConcept', 'preference')
		constant = docCriteria.createElement('constant')
		real = docCriteria.createElement('real')
		text = doc.createTextNode(str(criteriaPreference))
		real.appendChild(text)
		constant.appendChild(real)
		threshold2.appendChild(constant)
		thresholds.appendChild(threshold2)
		threshold3 = docCriteria.createElement('threshold')
		threshold3.setAttribute('mcdaConcept', 'veto')
		constant = docCriteria.createElement('constant')
		real = docCriteria.createElement('real')
		text = doc.createTextNode(str(criteriaVeto))
		real.appendChild(text)
		constant.appendChild(real)
		threshold3.appendChild(constant)
		thresholds.appendChild(threshold3)
		criterion.appendChild(thresholds)
		criteria.appendChild(criterion)
	xml_str = docCriteria.toprettyxml(indent="  ")
	#with open("criteria.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/concordance/in/criteria.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/criteria.xml", "w") as f:
	    f.write(xml_str)
	# Create method_parameters.xml
	# Get parameters collection from mongodb
	collection = db['parameters'] 
	# Get all parameters without the id attribute
	parametersList = list(collection.find(projection={"_id": False}))
	# Convert the alternative so it can be saved into a json file
	parametersDumps = json.dumps(parametersList)
	with open('parameters.json', 'w') as fp:
		fp.write(parametersDumps) 
	# Open the alternatives json file to get the content and save it into a xml file	
	with open('parameters.json') as data_file:    
		data = json.load(data_file)
	# Start creating the method_parameters xml file
	docParameters = minidom.Document()
	# Create xmcda tag
	xmcdaParameters = doc.createElement('xmcda:XMCDA')
	xmcdaParameters.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2012/XMCDA-2.2.0')
	xmcdaParameters.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaParameters.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2012/XMCDA-2.2.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.2.0.xsd')
	docParameters.appendChild(xmcdaParameters)
	# Create parameters tag
	methodParameters = docParameters.createElement('methodParameters')
	xmcdaParameters.appendChild(methodParameters)
	# Create the parameter tag 
	credibility = data[0]["credibility"]
	parameter = docParameters.createElement('parameter')
	parameter.setAttribute('name', 'comparison_with')
	value = docParameters.createElement('value')
	label = docParameters.createElement('label')
	text = doc.createTextNode('central_profiles')
	label.appendChild(text)
	value.appendChild(label)
	parameter.appendChild(value)
	methodParameters.appendChild(parameter)
	parameter2 = docParameters.createElement('parameter')
	parameter2.setAttribute('name', 'cut_threshold')
	value2 = docParameters.createElement('value')
	real = docParameters.createElement('real')
	text = doc.createTextNode(str(credibility))
	real.appendChild(text)
	value2.appendChild(real)
	parameter2.appendChild(value2)
	methodParameters.appendChild(parameter2)
	xml_str = docParameters.toprettyxml(indent="  ")
	with open("inputsOutputs/cutRelationCrisp/in/method_parameters.xml", "w") as f:
	    f.write(xml_str)    
	# Create classes.xml
	# Get categories collection from mongodb
	collection = db['categories'] 
	# Get all categories without the id attribute
	categoriesList = list(collection.find(projection={"_id": False}))
	# Convert the category so it can be saved into a json file
	categoriesDumps = json.dumps(categoriesList)
	with open('categories.json', 'w') as fp:
		fp.write(categoriesDumps) 
	# Open the categories json file to get the content and save it into a xml file	
	with open('categories.json') as data_file:    
		data = json.load(data_file)
	# Start creating classes xml file
	docClasses = minidom.Document()
	# Create xmcda tag
	xmcdaClasses = doc.createElement('xmcda:XMCDA')
	xmcdaClasses.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaClasses.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaClasses.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docClasses.appendChild(xmcdaClasses)
	# Create categories tag
	categories = docClasses.createElement('categories')
	xmcdaClasses.appendChild(categories)
	# Create all categories tag 
	for d in data:
		categoryName = d["name"]
		categoryRank = d["rank"]
		category = docClasses.createElement('category')
		category.setAttribute('id', categoryName)
		rank = docClasses.createElement('rank')
		integer = docClasses.createElement('integer')
		text = doc.createTextNode(str(categoryRank))
		integer.appendChild(text)
		rank.appendChild(integer)
		category.appendChild(rank)
		categories.appendChild(category)
	xml_str = docClasses.toprettyxml(indent="  ")
	#with open("classes.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/electreTriC/in/classes.xml", "w") as f:
	    f.write(xml_str)   
	# Start creating classes_profiles xml file
	docClassesProfiles = minidom.Document()
	# Create xmcda tag
	xmcdaClassesProfiles = doc.createElement('xmcda:XMCDA')
	xmcdaClassesProfiles.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaClassesProfiles.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaClassesProfiles.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docClassesProfiles.appendChild(xmcdaClassesProfiles)
	# Create categoriesProfiles tag
	categoriesProfiles = docClassesProfiles.createElement('categoriesProfiles')
	xmcdaClassesProfiles.appendChild(categoriesProfiles)
	# Create all categories profiles tag
	for d in data:
		categoryName = d["name"]
		actionName = d["action"]
		categoryProfile = docClassesProfiles.createElement('categoryProfile')
		alternativeID = docClassesProfiles.createElement('alternativeID')
		text = doc.createTextNode(actionName)
		alternativeID.appendChild(text)
		categoryProfile.appendChild(alternativeID)
		central = docClassesProfiles.createElement('central')
		categoryID = docClassesProfiles.createElement('categoryID')
		text = doc.createTextNode(categoryName)
		categoryID.appendChild(text)
		central.appendChild(categoryID)
		categoryProfile.appendChild(central)
		categoriesProfiles.appendChild(categoryProfile)
	xml_str = docClassesProfiles.toprettyxml(indent="  ")
	#with open("classes_profiles.xml", "w") as f:
	    #f.write(xml_str)   
	with open("inputsOutputs/electreTriC/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str)  	
	with open("inputsOutputs/credibility/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/concordance/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str)
	with open("inputsOutputs/cutRelationCrisp/in/classes_profiles.xml", "w") as f:
	    f.write(xml_str)   
	# Create performance_table.xml
	# Get performances collection from mongodb
	collection = db['performancetables'] 
	# Get all performances without the id attribute
	performancesList = list(collection.find(projection={"_id": False}))
	# Convert the performances so it can be saved into a json file
	performancesDumps = json.dumps(performancesList)
	with open('performances.json', 'w') as fp:
		fp.write(performancesDumps) 
	# Open the performances json file to get the content and save it into a xml file	
	with open('performances.json') as data_file:    
		data = json.load(data_file)
	# Start creating performance_table xml file
	docPerformances = minidom.Document()
	# Create xmcda tag
	xmcdaPerformances = doc.createElement('xmcda:XMCDA')
	xmcdaPerformances.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	xmcdaPerformances.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
	xmcdaPerformances.setAttribute('xsi:schemaLocation', 'http://www.decision-deck.org/2009/XMCDA-2.1.0 http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd')
	docPerformances.appendChild(xmcdaPerformances)
	# Create performances tag
	performanceTable = docPerformances.createElement('performanceTable')
	xmcdaPerformances.appendChild(performanceTable)
	# Create a check list to save which alternative name was already created in the xml file
	checkList = {}
	f = False
	t = True
	for d in data:
		altName = d["alternative"]
		checkList[altName] = f
	#print checkList
	# Create all performances tag 
	for d in data:
		alternativeId = d["alternative"]
		for alt, check in checkList.items():
			if alt == alternativeId:
				if check == False:
					checkList[alt] = t
					alternativePerformances = docPerformances.createElement('alternativePerformances')
					alternativeID = docPerformances.createElement('alternativeID')
					text = doc.createTextNode(alternativeId)
					alternativeID.appendChild(text)
					alternativePerformances.appendChild(alternativeID)
					for dd in data:
						performanceAlternative = dd["alternative"]
						performanceCriterion = dd["criterion"]
						performanceValue = dd["value"]
						if performanceAlternative == alternativeId:
							performance = docPerformances.createElement('performance')
							criterionID = docPerformances.createElement('criterionID')
							text = doc.createTextNode(performanceCriterion)
							criterionID.appendChild(text)
							performance.appendChild(criterionID)
							value = docPerformances.createElement('value')
							real = docPerformances.createElement('real')
							text = doc.createTextNode(str(performanceValue))
							real.appendChild(text)
							value.appendChild(real)
							performance.appendChild(value)
							alternativePerformances.appendChild(performance)
						else:
							#Do nothing
							pass

				else:
					pass
			else:
				pass
		
		performanceTable.appendChild(alternativePerformances)
	#print checkList
	xml_str = docPerformances.toprettyxml(indent="  ")
	#with open("performance_table.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/concordance/in/performance_table.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/performance_table.xml", "w") as f:
	    f.write(xml_str)
	# Create profiles_performance_table.xml
	# Get profiles collection from mongodb
	collection = db['profiletables'] 
	# Get all profiles without the id attribute
	profilesList = list(collection.find(projection={"_id": False}))
	# Convert the profiles so it can be saved into a json file
	profilesDumps = json.dumps(profilesList)
	with open('profiles.json', 'w') as fp:
		fp.write(profilesDumps) 
	# Open the profiles json file to get the content and save it into a xml file	
	with open('profiles.json') as data_file:    
		data = json.load(data_file)
	# Start creating profiles_performance_table xml file
	docProfiles = minidom.Document()
	# Create xmcda tag
	xmcdaProfiles = doc.createElement('xmcda:XMCDA')
	xmcdaProfiles.setAttribute('xmlns:xmcda', 'http://www.decision-deck.org/2009/XMCDA-2.1.0')
	docProfiles.appendChild(xmcdaProfiles)
	# Create profiles tag
	performanceTbl = docProfiles.createElement('performanceTable')
	performanceTbl.setAttribute('mcdaConcept', 'Fictive')
	xmcdaProfiles.appendChild(performanceTbl)
	# Create a check list to save which reference action name was already created in the xml file
	checkListProfiles = {}
	ff = False
	tt = True
	for d in data:
		refName = d["action"]
		checkListProfiles[refName] = ff
	print checkListProfiles
	# Create all profiles tag 
	for d in data:
		actionId = d["action"]
		for ref, check in checkListProfiles.items():
			if ref == actionId:
				if check == False:
					checkListProfiles[ref] = tt
					alternativePerf = docProfiles.createElement('alternativePerformances')
					alternativeID2 = docProfiles.createElement('alternativeID')
					text = doc.createTextNode(actionId)
					alternativeID2.appendChild(text)
					alternativePerf.appendChild(alternativeID2)
					for dd in data:
						profileAction = dd["action"]
						profileCriterion = dd["criterion"]
						profileValue = dd["value"]
						if profileAction == actionId:
							performance2 = docProfiles.createElement('performance')
							criterionID2 = docProfiles.createElement('criterionID')
							text = doc.createTextNode(profileCriterion)
							criterionID2.appendChild(text)
							performance2.appendChild(criterionID2)
							value2 = docProfiles.createElement('value')
							integer2 = docProfiles.createElement('integer')
							text = doc.createTextNode(str(int(profileValue)))
							integer2.appendChild(text)
							value2.appendChild(integer2)
							performance2.appendChild(value2)
							alternativePerf.appendChild(performance2)
						else:
							#Do nothing
							pass

				else:
					pass
			else:
				pass
		
		performanceTbl.appendChild(alternativePerf)
	xml_str = docProfiles.toprettyxml(indent="  ")
	#with open("profiles_performance_table.xml", "w") as f:
	    #f.write(xml_str) 
	with open("inputsOutputs/concordance/in/profiles_performance_table.xml", "w") as f:
	    f.write(xml_str) 
	with open("inputsOutputs/discordance/in/profiles_performance_table.xml", "w") as f:
	    f.write(xml_str)   
	return render_template('template.html') 


@app.route('/tableTeste/')
def tableTeste():
	mech = Browser()
	#url = "http://3.sysresearch.org:3901/configurations.html"
	#url = "http://localhost:8080/configurations.html"
	url = "http://localhost:8080/results.html"
	page = mech.open(url)

	html = page.read()
	soup = BeautifulSoup(html)
	#soup.findAll('div', {"class":"jumbotron"}) 
	#t = soup.find('h2').text
	t = soup.find('p', {"id":"demo"}).text
	#t = soup.findAll('td')[0].text
	doc = minidom.Document()
	leaf = doc.createElement('h1')
	text = doc.createTextNode(t)
	leaf.appendChild(text)
	#table = doc.createElement('table')
	#text1 = doc.createTextNode(t1)
	#table.appendChild(text1)
	doc.appendChild(leaf)
	#doc.appendChild(table)
	xml_str = doc.toprettyxml(indent="  ")
	with open("templates/example.xml", "w") as f:
	    f.write(xml_str)  
	return render_template('template.html') 		


@app.route('/xml/')
def xml():
	doc = minidom.Document()

	root = doc.createElement('root')
	doc.appendChild(root)

	leaf = doc.createElement('leaf')
	text = doc.createTextNode('Text element with attributes')
	leaf.appendChild(text)
	leaf.setAttribute('color', 'white')
	root.appendChild(leaf)

	leaf_cdata = doc.createElement('leaf_cdata')
	cdata = doc.createCDATASection('<em>CData</em> can contain <strong>HTML tags</strong> without encoding')
	leaf_cdata.appendChild(cdata)
	root.appendChild(leaf_cdata)

	branch = doc.createElement('branch')
	branch.appendChild(leaf.cloneNode(True))
	root.appendChild(branch)

	mixed = doc.createElement('mixed')
	mixed_leaf = leaf.cloneNode(True)
	mixed_leaf.setAttribute('color', 'black')
	mixed_leaf.setAttribute('state', 'modified')
	mixed.appendChild(mixed_leaf)
	mixed_text = doc.createTextNode('Do not use mixed elements if it possible.')
	mixed.appendChild(mixed_text)
	root.appendChild(mixed)

	xml_str = doc.toprettyxml(indent="  ")
	with open("example.xml", "w") as f:
	    f.write(xml_str)  
	return render_template('template.html') 


@app.route('/mongo/')
def mongo():
	#client = MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd')
	#db = client['criterions']
	#cursor = client.criterions.find({"name": "g1 - Price"},{ name: 1, _id:0 })
	#cursor = db.find_one()
	#client = MongoClient()
	#db = client.new_db
	#db
	#Database(MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd'), u'new_db')
	client = MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net')
	db = client.cristinav_bd
	cri = db.criterions
	cursor = cri.find({"name": "g1 - Price"})
	print cursor
	print "Hiiiiii"
	print cri
	#collection = db['api/criterions']
	#collection.find_one({"name": "g1 - Price"})
	#client = connect(cristinav_bd, host='mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd', username="cristinav", password="mbdcristinav")
	#client.admin.authenticate("cristinav", "mbdcristinav")
	#db = connect(cristinav_bd, host='mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd', username="cristinav", password="mbdcristinav")
	#db["/api/criterions"].authenticate("cristinav", password="mbdcristinav")
	#document = client.db.collection.find_one({"name": "g1 - Price"})
	#doc = minidom.Document()
	#leaf = doc.createElement('leaf')
	#text = doc.createTextNode(cursor)
	#leaf.appendChild(text)
	#c = doc.createElement(cursor)
	#doc.appendChild(c)
	#xml_str = doc.toprettyxml(indent="  ")
	#with open("example.xml", "w") as f:
	    #f.write(xml_str)  
	return render_template('template.html') 	

@app.route('/mongo2/')
def mongo2():
	# Connection to Mongo DB
	try:
	    conn=pymongo.MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd')
	    print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e 
	conn
	db = conn['cristinav_bd']
	collection = db['alternatives'] 
	t = collection.find({"name": "a4"})
	c = list(collection.find(projection={"_id": False}))
	ttt = collection.find({"user.name": "a4"})
	#db.alternatives.find({"name": "a4"})
	#col = Collection(Database(MongoClient('vps80648.ovh.net', 27017), u'cristinav_bd'), u'criterions')
	print "--------------"
	print db
	print "--------------"
	print collection 
	print "--------------"
	print t
	print "--------------"
	for item in collection.find({"name": "a4"}): 
		print item
	print "--------------"
	print c
	print "--------------"
	print "--------------"
	print ttt
	print "--------------"
	print json.dumps(c)
	print "--------------"
	print "--------------"
	print "--------------"
	p = json.dumps(c)
	with open('result.json', 'w') as fp:
		fp.write(p) 	
    	#json.dump(p, fp)
	with open('result.json') as data_file:    
		data = json.load(data_file)
	
	pprint(data)	
	print "lllllllll----"
	print data[0]["name"]
	nome = data[0]["name"]
	doc = minidom.Document()
	leaf = doc.createElement('h1')
	text = doc.createTextNode(nome)
	leaf.appendChild(text)
	doc.appendChild(leaf)
	xml_str = doc.toprettyxml(indent="  ")
	with open("mongo.xml", "w") as f:
	    f.write(xml_str)  
	#json.dumps(result,default=json_util.default)
	#print conn.database_names() 
	#print conn.collection_names()
	return render_template('template.html') 

@app.route('/createXMLTeste/')
def createXMLTeste():
	doc = minidom.Document()

	root = doc.createElement('root')
	doc.appendChild(root)

	leaf = doc.createElement('leaf')
	text = doc.createTextNode('Text element with attributes')
	leaf.appendChild(text)
	leaf.setAttribute('color', 'white')
	root.appendChild(leaf)

	leaf_cdata = doc.createElement('leaf_cdata')
	cdata = doc.createCDATASection('<em>CData</em> can contain <strong>HTML tags</strong> without encoding')
	leaf_cdata.appendChild(cdata)
	root.appendChild(leaf_cdata)

	branch = doc.createElement('branch')
	branch.appendChild(leaf.cloneNode(True))
	root.appendChild(branch)

	mixed = doc.createElement('mixed')
	mixed_leaf = leaf.cloneNode(True)
	mixed_leaf.setAttribute('color', 'black')
	mixed_leaf.setAttribute('state', 'modified')
	mixed.appendChild(mixed_leaf)
	mixed_text = doc.createTextNode('Do not use mixed elements if it possible.')
	mixed.appendChild(mixed_text)
	root.appendChild(mixed)

	xml_str = doc.toprettyxml(indent="  ")
	with open("example2.xml", "w") as f:
	    f.write(xml_str)  
	with open("templates/example2.xml", "w") as f:
	    f.write(xml_str)     
	return render_template('template.html') 


@app.route('/createHtml/')
def createHtml(): 
	#xmldoc = minidom.parse('templates/cd_catalog.xml')
	#xmldoc = minidom.parse('inputsOutputs/electreTriC/out/assignments.xml')
	#itemlist = xmldoc.getElementsByTagName('alternativeID')[0]
	#t = itemlist.childNodes[0].data
	#return t
	root = ET.Element('html')
	table = ET.SubElement(root, 'table')
	tr = ET.SubElement(table, 'tr')
	td = ET.SubElement(tr, 'td')
	td.text = "This is the first line "
	# note how to end td tail
	td.tail = None
	br = ET.SubElement(td, 'br')
	# now continue your text with br.tail
	br.tail = " and the second"

	tree = ET.tostring(root)
	# see the string
	tree
	'<html><table><tr><td>This is the first line <br /> and the second</td></tr></table></html>'

	with open('test.html', 'w+') as f:
	    f.write(tree)
	return render_template('template.html')

@app.route('/read/')
def read(): 
	xmldoc = minidom.parse('templates/cd_catalog.xml')
	xmldoc = minidom.parse('inputsOutputs/electreTriC/out/assignments.xml')
	itemlist = xmldoc.getElementsByTagName('alternativeID')[0]
	t = itemlist.childNodes[0].data
	return t

@app.route('/testeID/', methods=['GET', 'POST'])
def testeID(): 
	#Get project id from url parameter projectId
	projectID = request.args.get('projectId')
	print '------- Project ID --------'
	print projectID
	# Connection to Mongo DB
	try:
	    connection = pymongo.MongoClient('mongodb://cristinav:mbdcristinav@vps80648.ovh.net/cristinav_bd')
	    print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e 
	db = connection['cristinav_bd']
	# Get users collection
	users = db['users']
	# Get projects collection
	projects = db['projects']
	# Set project id from the url parameter as the project we need to get the data to execute the method
	project_id = projectID
	userProject = users.find_one({"_id" : ObjectId('576b2f353b4de674060fd244') })
	# Lists to save the data from projectId
	alternativesList = [];
	criteriaList = [];
	categoriesList = [];
	parametersList = [];
	performancetablesList = [];
	profiletablesList = [];
	print "Jim's tasks are:"
	project = projects.find_one({"_id" : ObjectId(project_id) })
	print project
	print project["alternatives"]
	print '--------------------'
	for alternative in project["alternatives"]:
		alt = db.alternatives.find_one({"_id" : alternative } , {'_id': False})
		print alt
		alternativesList.append(alt)
	alternativesDumps = json.dumps(alternativesList)
	with open('alternatives.json', 'w') as fp:
		fp.write(alternativesDumps) 
	print alternativesList
	print '-----------++++++++---------'
	for criterion in project["criteria"]:
		cri = db.criterions.find_one({"_id" : criterion } , {'_id': False})
		print cri
		criteriaList.append(cri)
	criteriaDumps = json.dumps(criteriaList)
	with open('weights.json', 'w') as fp:
		fp.write(criteriaDumps) 
	print criteriaList
	print '-----------++++++++---------'
	for category in project["categories"]:
		cat = db.categories.find_one({"_id" : category } , {'_id': False})
		print cat
		categoriesList.append(cat)
	categoriesDumps = json.dumps(categoriesList)
	with open('categories.json', 'w') as fp:
		fp.write(categoriesDumps) 
	print categoriesList
	print '-----------++++++++---------'
	for parameter in project["parameters"]:
		par = db.parameters.find_one({"_id" : parameter } , {'_id': False})
		print par
		parametersList.append(par)
	parametersDumps = json.dumps(parametersList)
	with open('parameters.json', 'w') as fp:
		fp.write(parametersDumps) 
	print parametersList
	print '-----------++++++++---------'
	for performance in project["performancetables"]:
		per = db.performancetables.find_one({"_id" : performance } , {'_id': False})
		print per
		performancetablesList.append(per)
	performancesDumps = json.dumps(performancetablesList)
	with open('performances.json', 'w') as fp:
		fp.write(performancesDumps) 
	print performancetablesList
	print '-----------++++++++---------'
	for profile in project["profiletables"]:
		pro = db.profiletables.find_one({"_id" : profile } , {'_id': False})
		print pro
		profiletablesList.append(pro)
	profilesDumps = json.dumps(profiletablesList)
	with open('profiles.json', 'w') as fp:
		fp.write(profilesDumps) 
	print profiletablesList
	print '-----------++++++++---------'
	with open('profiles.json') as data_file:    
		data = json.load(data_file)
	print data
	print '+++++++'
	return render_template('template.html')


if __name__ == '__main__':
	#app.run(debug=True)
	app.run(host= '0.0.0.0', port=5010)
