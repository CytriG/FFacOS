from pydoc import classname
from dash import Dash, html, dcc, callback_context, dash_table
import plotly.express as px
import pandas as pd
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, State, ClientsideFunction, MATCH, ALL
 

pd.options.plotting.backend = "plotly"


import sys
# import subprocess
import time

import os

import numpy as np

import json


import matplotlib

matplotlib.use('Agg') # to make matplotlib works in Flask server thread


from matplotlib import pyplot as plt

from pprint import pprint

 
import dash_bootstrap_components as dbc


import mysql.connector

 

import Layout


import requests

from datetime import datetime
 
Config = None

package_directory = os.path.dirname(os.path.abspath(__file__))

 

StartWarnings = []

StartErrors = []

print(type(os.environ))
print(os.environ)


Db_password=os.environ.get('DB_passwd')


print(Db_password)



def CheckDb():

    # global mydb

    return RunAPI()


def ReadAPIQuery(query_sql):


    mydb = CheckDb()
    
    result_sql = pd.read_sql_query(query_sql, mydb)

    print(result_sql)

    mydb.close()

    return result_sql


def InsertAPIQuery(query_sql):


    mydb = CheckDb()

    mydb.reconnect()

    mycursor = mydb.cursor()

    mycursor.execute(query_sql)

    mydb.commit()
    mydb.close()
 

def RunAPI():
    

    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd=Db_password,
        port=3307,
        database="ffacosdb"
    )
    
    return mydb

  

def GetMasterNextNumFacture():

    query_sql = '''

            SELECT NumFacture

            FROM factures ;

            '''
            # Order by NumFacture desc ;
            #  Limit 1 ;

    print()
    print("-- GetMasterNextNumFacture")


    res = ReadAPIQuery(query_sql=query_sql)

    res['NumFacture'] = res['NumFacture'].astype('float')

    maxf = res['NumFacture'].max()


    if res.empty:
        return 0
    else:
        # return int(res['NumFacture'].iloc[0])+1
        return maxf+1
 





print()

print()

print('************************************')

print('*')

print('*       Welcome to FFacOS')

print('*')

print('************************************')

print('Config:')

 

 


try :

    with open(package_directory+'/Infos.json','r') as f:

        Config  = json.load(f)



except FileNotFoundError :

    print('Infos.json not found ! ')

    exit()



try :

    Config['StartNextNumFacture'] = GetMasterNextNumFacture()

except Exception as e:

    print(e)
    print("Fail To Load MasterNextNumFacture")
 
pprint(Config)

#DashProxy can use multiple callback for same output !

app = DashProxy(prevent_initial_callbacks=True,

                    transforms=[MultiplexerTransform()],

                    # external_stylesheets=[dbc.themes.SLATE],
                    external_stylesheets=[dbc.themes.LITERA],

                    # external_scripts=external_scripts

                )

# app = Dash(__name__)

 

app.layout = Layout.GetTotalLayout(Config=Config)#figs)


print()
print('FFacOS is running')






 

 

def ReturnFailNotif(Message="Oops"):
    return ReturnNotif(Type="Fail",Message=Message)
def ReturnWarningNotif(Message="Oops"):
    return ReturnNotif(Type="Warning",Message=Message)
def ReturnSuccessNotif(Message="Done"):
    return ReturnNotif(Type="Success",Message=Message)
def ReturnNoNotif(Message="Done"):
    return ReturnNotif(Type="No",Message=Message)
 
def ReturnNotif(Type="Fail",Message="Error"):

    if Type=="Success":
        return False, "" , False, '', True, Message

    if Type=="Warning":
        return False, "" ,  True, Message,False, '',

    if Type=="Fail":
        return  True, Message, False, '', False, "" , 

    if Type=="No":
        return  False, "", False, '', False, "" , 


 

 
 #************************************************************************************


 #  Clients
def GetClientFromClientId(ClientId):

    Clients = []

    query_sql = '''

                SELECT *

                FROM Clients

                WHERE Id=XXXIdXXX;

                '''

    # query_sql = query_sql.replace('XXXEmailXX', Email) #'""')

    query_sql = query_sql.replace('XXXIdXXX', str(ClientId))#','.join(['email','long_id']))

    print()
    print("-- GetClient "+str(ClientId))
    print(query_sql)


    try:

        res = ReadAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return False

    return res



def GetClients(trigger,Email=None):

    # if not Email or Email =='None':

    # return  True , 'No Email selected !'

 
    # BoxId = GetBoxId(Filename)

    # Email = Email.replace(' ','')
    Clients = []

    query_sql = '''

                SELECT XXXcolsXXX

                FROM Clients;

                '''

                # JOIN users ON users.id = pairings.user_id

                # JOIN masters ON masters.id = pairings.master_id

                # WHERE email =  "XXXEmailXX"

                # LIMIT 100'''

 

    global API_cols

    # query_sql = query_sql.replace('XXXEmailXX', Email) #'""')

    query_sql = query_sql.replace('XXXcolsXXX', 'Id, Nom, Prenoms')#','.join(['email','long_id']))

    print()
    print("-- GetClients ")
    print(query_sql)


    try:

        res = ReadAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return Clients,*ReturnFailNotif('Can\'t access Local Db')

    if res.empty:
        return Clients, *ReturnWarningNotif('No Client found !')


    
    for i,r in res.iterrows():
        # divsClients.append(
        #     html.Div(
        #         className="card border-secondary mb-3",
        #         n_clicks =0,
        #         style={"max-width": "80%"},
        #         children = [
        #             html.Div(
        #                     html.H4(r['Nom']+" "+r['Prenoms'],
        #                     className="card-title",
        #                     ),
        #                     className="card-body")
        #         ])
        # )

        Clients.append({"label":r['Nom']+" "+r['Prenoms'],"value":r['Id']})

    return Clients, *ReturnSuccessNotif('Done !')

    try :

        email  =  res.iloc[-1].to_frame().T.to_dict("records")[0]['email']

        return  False, ''

    except IndexError:

        email = 'No BoxId found'

        return True, 'No BoxId found'


@app.callback(

        output=[
            Output("ClientInfoContainer","children"),
            Output("StudentInfoContainer","children"),

            Output('ClientInfoId',"value"),
            Output('ClientInfoNom',"value"),
            Output('ClientInfoPrenoms',"value"),
            Output('ClientInfoCivilite',"value"),
            Output('ClientInfoNomUsage',"value"),
            Output('ClientInfoDateNaissance',"date"),
            Output('ClientInfoPaysNaissance',"value"),
            Output('ClientInfoDepNaissance',"value"),
            Output('ClientInfoCodeVilleNaissance',"value"),
            Output('ClientInfoVilleNaissance',"value"),
            Output('ClientInfoTel',"value"),
            Output('ClientInfoEmail',"value"),
            Output('ClientAdresseNumVoie',"value"),
            Output('ClientAdresseLettreVoie',"value"),
            Output('ClientAdresseCodeVoie',"value"),
            Output('ClientAdresseVoie',"value"),
            Output('ClientAdresseComplement',"value"),
            Output('ClientAdresseLieuDit',"value"),
            Output('ClientAdresseVille',"value"),
            Output('ClientAdresseCodeVille',"value"),
            Output('ClientAdresseCodePostal',"value"),
            Output('ClientAdresseCodePays',"value"),
            Output('ClientBIC',"value"),
            Output('ClientIBAN',"value"),
            Output('ClientBanqueTitulaire',"value"),

            [
                Output('API_response_fail','is_open'),
                Output('API_response_fail','children'), 
                Output('API_response_warning','is_open'),
                Output('API_response_warning','children'), 
                Output('API_response_success','is_open'),
                Output('API_response_success','children'), 
            ]
        ],

        inputs=[   
            Input('CurrentClientId', 'value')   
        ],

        state=[  
            # State('CustomEmail_input','value')
        ],

        prevent_initial_call=True,

 

)
def GetClient(trigger):
    NumColClientInfo=25
    ClientInfo = []#["oui","oui","oui"]#str(np.ones(NumColClientInfo))


    query_sql = '''

            SELECT *

            FROM Clients WHERE Id=XXXIdxXX;

            '''

            # JOIN users ON users.id = pairings.user_id

            # JOIN masters ON masters.id = pairings.master_id

            # WHERE email =  "XXXEmailXX"

            # LIMIT 100'''

 

    global API_cols

    # query_sql = query_sql.replace('XXXEmailXX', Email) #'""')

    query_sql = query_sql.replace('XXXIdxXX', str(trigger))#','.join(['email','long_id']))

    print()
    print("-- GetClientInfo")
    try:

        res = ReadAPIQuery(query_sql=query_sql)

        for i in range(0,NumColClientInfo):
            ClientInfo.append(res.iloc[0,i])
            print(res.iloc[0,i])

        temp = res.to_dict('records')[0]

        Students = GetStudentsFromClientId(temp['Id']).to_dict('records')
        print('............')
        print(Students)

        ClientInfoChildren = WriteClientInfo(temp)
        StudentInfoChildren = WriteStudentInfo(Students)




    except mysql.connector.errors.InterfaceError :

        return ClientInfo,*ReturnFailNotif('Can\'t access Local Db')


    print(len(ClientInfo))


    return ClientInfoChildren,StudentInfoChildren,*ClientInfo,*ReturnNoNotif()
 


def WriteClientInfo(ClientInfo):

    ch=[]
    for ik in ClientInfo.keys():
        ch.append(html.Div(str(ik)+" : "+str(ClientInfo[ik])))

    return ch


def WriteStudentInfo(StudentsInfo):

    contain = []
    
    for stud in StudentsInfo:
        ch=[]
        for ik in stud.keys():
            ch.append(html.Div(str(ik)+" : "+str(stud[ik])))

        contain.append(html.Div(ch))
        contain.append(html.Div(style={"height":"20px"}))

    return contain


def GetStudentsFromClientId(ClientId):

        query_sql = '''

                SELECT *

                FROM students WHERE ClientId=XXXIdxXX;

                '''

        query_sql = query_sql.replace('XXXIdxXX', str(ClientId))#','.join(['email','long_id']))

        print()
        print("-- GetStudentsFromClientId")

        res = ReadAPIQuery(query_sql=query_sql)

        return res




@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('CurrentClientId','options'),
            [
                Output('API_response_fail','is_open'),
                Output('API_response_fail','children'), 
                Output('API_response_warning','is_open'),
                Output('API_response_warning','children'), 
                Output('API_response_success','is_open'),
                Output('API_response_success','children'), 
            ]
            ],

        inputs=[   
            Input('GetAllClientsButton', 'n_clicks')   
        ],

        state=[  
            # State('CustomEmail_input','value')
        ],

        prevent_initial_call=True,

 

)
def GetClientsForClientInfo(trigger,Email=None):

    return GetClients(trigger,Email)

   



@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('API_response_fail','is_open'),
            Output('API_response_fail','children'), 
            Output('API_response_warning','is_open'),
            Output('API_response_warning','children'), 
            Output('API_response_success','is_open'),
            Output('API_response_success','children'), 

            ],

        inputs=[   
            Input('CreateClientButton', 'n_clicks')   
        ],

        state=[  
            # State('ClientInfoId','value'),   #! same order as Db
            State('ClientInfoNom','value'),
            State('ClientInfoPrenoms','value'),
            State('ClientInfoCivilite','value'),
            State('ClientInfoNomUsage','value'),
            State('ClientInfoDateNaissance','date'),
            State('ClientInfoPaysNaissance','value'),
            State('ClientInfoDepNaissance','value'),
            State('ClientInfoCodeVilleNaissance','value'),
            State('ClientInfoVilleNaissance','value'),
            State('ClientInfoTel','value'),
            State('ClientInfoEmail','value'),
            State('ClientAdresseNumVoie','value'),
            State('ClientAdresseLettreVoie','value'),
            State('ClientAdresseCodeVoie','value'),
            State('ClientAdresseVoie','value'),
            State('ClientAdresseComplement','value'),
            State('ClientAdresseLieuDit','value'),
            State('ClientAdresseVille','value'),
            State('ClientAdresseCodeVille','value'),
            State('ClientAdresseCodePostal','value'),
            State('ClientAdresseCodePays','value'),
            State('ClientBIC','value'),
            State('ClientIBAN','value'),
            State('ClientBanqueTitulaire','value'),
        ],

        prevent_initial_call=True,

 

)
def AddClient(trigger,*values):
    Values = [None]  #Id

    query_sql = '''

            INSERT INTO clients

            values(XXXXValuesComaXXX);

            '''

    for v in values:
        Values.append('"'+str(v)+'"')

    Values.append(None) #IdUrsaaf


    for i,v in enumerate(Values) :
        if v is None:
            Values[i]='DEFAULT'


    SQLValues = ','.join([ v for v in Values])

    query_sql = query_sql.replace('XXXXValuesComaXXX', SQLValues) #'""')

    print(query_sql)


    try:

        res = InsertAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return ReturnFailNotif('Can\'t access Local Db')

    except mysql.connector.errors.DatabaseError as e:
        print(e)
        return ReturnFailNotif('SQL ERROR :  '+str(e))

    return ReturnSuccessNotif('Done!')



 
@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('API_response_fail','is_open'),
            Output('API_response_fail','children'), 
            Output('API_response_warning','is_open'),
            Output('API_response_warning','children'), 
            Output('API_response_success','is_open'),
            Output('API_response_success','children'), 

            ],

        inputs=[   
            Input('ModifClientButton', 'n_clicks')   
        ],

        state=[  
            State('ClientInfoId','value'),   #! same order as Db
            State('ClientInfoNom','value'),
            State('ClientInfoPrenoms','value'),
            State('ClientInfoNomUsage','value'),
            State('ClientInfoCivilite','value'),
            State('ClientInfoDateNaissance','date'),
            State('ClientInfoPaysNaissance','value'),
            State('ClientInfoDepNaissance','value'),
            State('ClientInfoCodeVilleNaissance','value'),
            State('ClientInfoVilleNaissance','value'),
            State('ClientInfoTel','value'),
            State('ClientInfoEmail','value'),
            State('ClientAdresseNumVoie','value'),
            State('ClientAdresseLettreVoie','value'),
            State('ClientAdresseCodeVoie','value'),
            State('ClientAdresseVoie','value'),
            State('ClientAdresseComplement','value'),
            State('ClientAdresseLieuDit','value'),
            State('ClientAdresseVille','value'),
            State('ClientAdresseCodeVille','value'),
            State('ClientAdresseCodePostal','value'),
            State('ClientAdresseCodePays','value'),
            State('ClientBIC','value'),
            State('ClientIBAN','value'),
            State('ClientBanqueTitulaire','value'),
        ],

        prevent_initial_call=True,

 

)
def ModifClient(trigger,id,*values):
    Values = []

    query_sql = '''

            UPDATE clients

            set XXXXCol=ValuesComaXXX
            
            WHERE Id= XXidXX;
            '''

    Cols=[ 
            'Nom',
            'Prenoms',
            'NomUsage',
            'Civilite',
            'DateNaissance',
            'PaysNaissance',
            'DepNaissance',
            'CodeVilleNaissance',
            'VilleNaissance',
            'Tel',
            'Email',
            'AdresseNumVoie',
            'AdresseLettreVoie',
            'AdresseCodeVoie',
            'AdresseVoie',
            'AdresseComplement',
            'AdresseLieuDit',
            'AdresseVille',
            'AdresseCodeVille',
            'AdresseCodePostal',
            'AdresseCodePays',
            'BanqueBIC',
            'BanqueIBAN',
            'BanqueTitulaire',
            'IdUrssaf'
            ]

    for v in values:
        Values.append('"'+str(v)+'"')

    Values.append(None) #IdUrsaaf

    SQLValues=[]

    print(len(Values))
    print(len(Cols))
    print(len(values))

    for i,v in enumerate(Values) :
        if v is None:
            Values[i]='DEFAULT'

        SQLValues.append(Cols[i]+"="+Values[i])

    SQLValues = ','.join(SQLValues)

    query_sql = query_sql.replace('XXXXCol=ValuesComaXXX', SQLValues) #'""')
    query_sql = query_sql.replace('XXidXX', str(id)) #'""')

    print(query_sql)


    try:

        res = InsertAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return ReturnFailNotif('Can\'t access Local Db')


    return ReturnSuccessNotif('Done!')


 
 
@app.callback(

        output=[
            
            Output('API_response_fail','is_open'),
            Output('API_response_fail','children'), 
            Output('API_response_warning','is_open'),
            Output('API_response_warning','children'), 
            Output('API_response_success','is_open'),
            Output('API_response_success','children'), 

            ],

        inputs=[   
            Input('DeleteClientButton', 'n_clicks')   
        ],

        state=[  
            State('ClientInfoId','value'),   
        ],

        prevent_initial_call=True,

 

)
def DeleteClient(trigger,id):

    query_sql = '''

            DELETE from clients

            WHERE Id= XXidXX;
            '''

    if id is None or int(id) < 0:
        return ReturnFailNotif('Impossible bad input Id :'+str(id))


    query_sql = query_sql.replace('XXidXX', str(id)) #'""')

    print(query_sql)


    try:

        res = InsertAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return ReturnFailNotif('Can\'t access Local Db')


    return ReturnSuccessNotif('Done!')






@app.callback(

        output=[
            Output('API_response_fail','is_open'),
            Output('API_response_fail','children'), 
            Output('API_response_warning','is_open'),
            Output('API_response_warning','children'), 
            Output('API_response_success','is_open'),
            Output('API_response_success','children'), 

            ],
        inputs=[   
            Input('CreateStudentButton', 'n_clicks')   
        ],

        state=[  
            # State('NewStudentInfoId','value'),   
            State('NewStudentInfoNom','value'),   
            State('NewStudentInfoPrenoms','value'),   
            State('ClientInfoId','value'),   
        ],

        prevent_initial_call=True,

)
def AddStudentsToClient(trigger,*values):


    Values = [None]  #Id

    query_sql = '''

            INSERT INTO students

            values(XXXXValuesComaXXX);

            '''

    for v in values:
        Values.append('"'+str(v)+'"')

    for i,v in enumerate(Values) :
        if v is None:
            Values[i]='DEFAULT'


    SQLValues = ','.join([ v for v in Values])

    query_sql = query_sql.replace('XXXXValuesComaXXX', SQLValues) #'""')


    print()
    print("-- Create Student ")
    print(query_sql)

    try:

        res = InsertAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return ReturnFailNotif('Can\'t access Local Db')


    return ReturnSuccessNotif('Done!')



 

 

 #************************************************************************************


 #  Students






@app.callback(

        output=[
            Output('API_response_fail','is_open'),
            Output('API_response_fail','children'), 
            Output('API_response_warning','is_open'),
            Output('API_response_warning','children'), 
            Output('API_response_success','is_open'),
            Output('API_response_success','children'), 

            ],
        inputs=[   
            Input('ModifyStudentButton', 'n_clicks')   
        ],

        state=[  
            State('NewStudentInfoId','value'),   
            State('NewStudentInfoNom','value'),   
            State('NewStudentInfoPrenoms','value'),   
            State('ClientInfoId','value'),   
        ],

        prevent_initial_call=True,

)
def ModifyStudentsToClient(trigger,StudentId,*Values):


    query_sql = '''

            UPDATE students

            set XXXXCol=ValuesComaXXX
            
            WHERE Id=XXidXX;
            '''

    Cols=[ 
            'Nom',
            'Prenoms',
            'ClientId',
            ]



    if Values is None or Values[0] is None or Values[0]=="" or (type(Values[0]) is int and Values[0]<0) :
    
        return ReturnWarningNotif('Bad Id to modify !')


    SQLValues=[]


    for i,v in enumerate(Values) :
        if v is None:
            Values[i]='DEFAULT'

        SQLValues.append(str(Cols[i])+"=\""+str(Values[i])+"\"")

    print(SQLValues)
    SQLValues = ','.join(SQLValues)

    query_sql = query_sql.replace('XXXXCol=ValuesComaXXX', SQLValues) #'""')
    query_sql = query_sql.replace('XXidXX', str(StudentId)) #'""')

    print()
    print("-- ModifStudent ")
    print(query_sql)

    try:

        res = InsertAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return ReturnFailNotif('Can\'t access Local Db')


    return ReturnSuccessNotif('Done!')









 
@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('CurrentStudentId','options'),
            [
                Output('API_response_fail','is_open'),
                Output('API_response_fail','children'), 
                Output('API_response_warning','is_open'),
                Output('API_response_warning','children'), 
                Output('API_response_success','is_open'),
                Output('API_response_success','children'), 
            ]
            ],

        inputs=[   
            Input('GetAllStudentsButton', 'n_clicks')   
        ],

        state=[  
            # State('CustomEmail_input','value')
        ],

        prevent_initial_call=True,

 

)
def GetStudents(trigger,Email=None):

    # if not Email or Email =='None':

    # return  True , 'No Email selected !'

 
    # BoxId = GetBoxId(Filename)

    # Email = Email.replace(' ','')
    Students = []

    query_sql = '''

                SELECT XXXcolsXXX

                FROM students;

                '''

                # JOIN users ON users.id = pairings.user_id

                # JOIN masters ON masters.id = pairings.master_id

                # WHERE email =  "XXXEmailXX"

                # LIMIT 100'''

 

    global API_cols

    # query_sql = query_sql.replace('XXXEmailXX', Email) #'""')

    query_sql = query_sql.replace('XXXcolsXXX', 'Id, Nom, Prenoms')#','.join(['email','long_id']))

    print()
    print("-- GetStudents ")
    print(query_sql)


    try:

        res = ReadAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return Students,*ReturnFailNotif('Can\'t access Local Db')

 

    if res.empty:
        return Students, *ReturnWarningNotif('No Client found !')


    
    for i,r in res.iterrows():
        Students.append({"label":r['Nom']+" "+r['Prenoms'],"value":r['Id']})


    return Students, *ReturnSuccessNotif('Done !')

@app.callback(

        output=[
            
            # Output('StudentInfoId',"value"),
            # Output('StudentInfoNom',"value"),
            # Output('StudentInfoPrenoms',"value"),
            Output('StudentInfo',"children"),

            # [
            #     Output('API_response_fail','is_open'),
            #     Output('API_response_fail','children'), 
            #     Output('API_response_warning','is_open'),
            #     Output('API_response_warning','children'), 
            #     Output('API_response_success','is_open'),
            #     Output('API_response_success','children'), 
            # ],
            # Output('CurrentCoursId','options'),

        ],

        inputs=[   
            Input('CurrentStudentId', 'value')   
        ],

        state=[  
            # State('CustomEmail_input','value')
        ],

        prevent_initial_call=True,

 

)
def GetStudent(trigger):
    NumColStudentsInfo=3
    StudentInfo = []#["oui","oui","oui"]#str(np.ones(NumColClientInfo))


    query_sql = '''

            SELECT *

            FROM students WHERE Id=XXXIdxXX;

            '''

            # JOIN users ON users.id = pairings.user_id

            # JOIN masters ON masters.id = pairings.master_id

            # WHERE email =  "XXXEmailXX"

            # LIMIT 100'''

 

    global API_cols

    # query_sql = query_sql.replace('XXXEmailXX', Email) #'""')

    query_sql = query_sql.replace('XXXIdxXX', str(trigger))#','.join(['email','long_id']))

    print()
    print("-- GetStudentInfo")



    res = ReadAPIQuery(query_sql=query_sql)
    res= res.iloc[0].to_dict()#"records")

    # for i in range(0,NumColStudentsInfo):
    #     StudentInfo.append(res.iloc[0,i])
    #     print(res.iloc[0,i])

    for k in res :
        StudentInfo.append(html.Div(str(k)+' : '+str(res[k])))

    StudentInfos = html.Div(StudentInfo)


    print(len(StudentInfos))
 
    return StudentInfos#,*ReturnNoNotif()


#************************************************************************************


#  Cours





@app.callback(
        output=[
            Output('ModalModifCours','is_open'),
        ],
        inputs=[   
            Input('AddCoursButton', 'n_clicks')  , 
        ],

        state=[  
            State('ModalModifCours','is_open')
        ],

        prevent_initial_call=True,

)
def OpenCoursModal(trigger,is_open):

    return not is_open





def GetCoursFromCoursId(CoursId):
    query_sql = '''

                SELECT *

                FROM cours
                WHERE Id=XXIdXX   order by Date Desc;

                '''

    # query_sql = query_sql.replace('XXXcolsXXX', 'Id, Date, StudentId')#','.join(['email','long_id']))
    query_sql = query_sql.replace('XXIdXX', str(CoursId))#','.join(['email','long_id']))

    print()
    print("-- GetCours ")
    print(query_sql)


    res = ReadAPIQuery(query_sql=query_sql)
    print(res)

    return res.iloc[0]




def GetCoursFromStudentId(StudentId):

    query_sql = '''

                SELECT *

                FROM cours
                WHERE StudentId=XXIdXX   order by Date Desc;

                '''

    # query_sql = query_sql.replace('XXXcolsXXX', 'Id, Date, StudentId')#','.join(['email','long_id']))
    query_sql = query_sql.replace('XXIdXX', str(StudentId))#','.join(['email','long_id']))

    print()
    print("-- GetCours ")
    print(query_sql)


    res = ReadAPIQuery(query_sql=query_sql)
    print(res)

    return res



@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            # Output('CurrentCoursId','options'),
            Output('ListCours','children'),
            Output('CoursStudentId','value'),
            # [
            #     Output('API_response_fail','is_open'),
            #     Output('API_response_fail','children'), 
            #     Output('API_response_warning','is_open'),
            #     Output('API_response_warning','children'), 
            #     Output('API_response_success','is_open'),
            #     Output('API_response_success','children'), 
            # ]
            ],

        inputs=[   
            Input('GetCoursButton', 'n_clicks')  , 
            Input('CurrentStudentId', 'value')   
        ],

        state=[  
            State('CurrentStudentId','value')
        ],

        prevent_initial_call=True,

 

)
def GetCours(trigger,StudentId,Email=None):

    Cours = []



    res = GetCoursFromStudentId(StudentId)

    if not res.empty:

        res = res.to_dict("records")

        divs=[]
        for i,r in enumerate(res):
            ch=[]
            for k in r:
                ch.append(html.P(className="mb-1",children=str(k)+" : "+str(r[k])))

            ch.append(html.Div(id="ModifyButtonCours_"+str(r['Id']),className="btn btn-info",children="Modify"))

            classname = "list-group-item list-group-item-action flex-column align-items-start"
            if i%2==0:
                classname+=" active"
            divs.append(html.A(
                # style={"width":"100%"},
                className=classname,#"list-group-item list-group-item-action flex-column align-items-start",
                children = ch,
                ))
            
        container = html.Div(divs,
        className="list-group",
        style={"height":"100%","overflow-y":"auto"},
        )

    else:

        container = html.Div("Pas de cours !",className="text-warning")



    return  container,StudentId#, *ReturnSuccessNotif('Done !')





# @app.callback(

#         output=[
#             # Output('BoxIdFromCustomAPISearchData','data')  , 
#             # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
#             Output('CoursNiveau',"value"),
#             Output('CoursNHeureFacturee',"value"),
#             Output('CoursNHeureReelle',"value"),
#             Output('CoursSurPlace',"value"),
#             Output('CoursNHeurePreparation',"value"),
#             Output('CoursDate',"date"),
            
#             [
#                 Output('API_response_fail','is_open'),
#                 Output('API_response_fail','children'), 
#                 Output('API_response_warning','is_open'),
#                 Output('API_response_warning','children'), 
#                 Output('API_response_success','is_open'),
#                 Output('API_response_success','children'), 
#             ]
#             ],

#         inputs=[   
#             Input('CurrentCoursId', 'value')   
#         ],

#         state=[  
#             # State('CustomEmail_input','value')
#         ],

#         prevent_initial_call=True,

 

# )
# def GetCoursInfo(trigger,Email=None):
    NumCol=6
    # if not Email or Email =='None':

    # return  True , 'No Email selected !'

 
    # BoxId = GetBoxId(Filename)

    # Email = Email.replace(' ','')
    CoursInfo = []
    CoursId = trigger

    print(trigger)

    query_sql = '''

                SELECT XXXcolsXXX

                FROM cours
                WHERE Id=XXIdXX   ;

                '''

                # JOIN users ON users.id = pairings.user_id

                # JOIN masters ON masters.id = pairings.master_id

                # WHERE email =  "XXXEmailXX"

                # LIMIT 100'''

 

    global API_cols

    # query_sql = query_sql.replace('XXXEmailXX', Email) #'""')

    query_sql = query_sql.replace('XXXcolsXXX', 'Niveau,NHeuresFacturee,NHeuresReelle,SurPlace,NHeuresPreparation,Date')#','.join(['email','long_id']))
    query_sql = query_sql.replace('XXIdXX', str(CoursId))#','.join(['email','long_id']))

    print()
    print("-- GetCours ")
    print(query_sql)


    try:

        res = ReadAPIQuery(query_sql=query_sql)
        print(res)
        for i in range(0,NumCol):
            CoursInfo.append(res.iloc[0,i])
            print(res.iloc[0,i])

    except mysql.connector.errors.InterfaceError :

        return *CoursInfo,*ReturnFailNotif('Can\'t access Local Db')

 
    if res.empty:
        return *CoursInfo, *ReturnWarningNotif('No Cours found !')

    


    return  *CoursInfo, *ReturnSuccessNotif('Done !')




def ModifyCoursValuesFromInputs(Values,values):
    for v in values:
        if v is None or v=="":
            Values.append(None)
        elif v=="Yes" or v=="No":
            Values.append(v)
        else:
            Values.append('"'+str(v)+'"')

    Values.append(None) #FactureId
    Values[9] = Values[8] 
    Values[8] = None      #inverse facture id and HourPrice

    if Values[4]=="Yes":
        Values[4] = "1"
    elif Values[4]=="No":
        Values[4] = "0"
    else:
        raise ValueError('Bad Value for CoursSurPlace  : '+str(Values[4]))

    return Values

@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('API_response_fail','is_open'),
            Output('API_response_fail','children'), 
            Output('API_response_warning','is_open'),
            Output('API_response_warning','children'), 
            Output('API_response_success','is_open'),
            Output('API_response_success','children'), 
            ],

        inputs=[   
            Input('CreateCoursButton', 'n_clicks')   
        ],

        state=[  
            State('CoursNiveau','value'),
            State('CoursNHourFacturee','value'),
            State('CoursNHourReal','value'),
            State('CoursSurPlace','value'),
            State('CoursNHourPreparation','value'),
            State('CoursStudentId','value'),  #! same order as Db
            State('CoursDate','date'),  
            State('CoursHourPriceHT','value'),
        ],

        prevent_initial_call=True,

 

)
def AddCours(trigger,*values):
    Values = [None]  #Id

    query_sql = '''

            INSERT INTO cours

            values(XXXXValuesComaXXX);

            '''
    try : 

        Values =  ModifyCoursValuesFromInputs(Values,values)

    except ValueError as e:
        return ReturnFailNotif(str(e))


    for i,v in enumerate(Values) :
        if v is None:
            Values[i]='DEFAULT'


    SQLValues = ','.join([ v for v in Values])





    query_sql = query_sql.replace('XXXXValuesComaXXX', SQLValues) #'""')

    print()
    print("-- AddCours ")
    print(query_sql)


    try:

        res = InsertAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return ReturnFailNotif('Can\'t access Local Db')

    except mysql.connector.errors.DatabaseError as e:
        print(e)
        return ReturnFailNotif('ERROR  : '+str(e))


    return ReturnSuccessNotif('Done!')



@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('API_response_fail','is_open'),
            Output('API_response_fail','children'), 
            Output('API_response_warning','is_open'),
            Output('API_response_warning','children'), 
            Output('API_response_success','is_open'),
            Output('API_response_success','children'), 

            ],

        inputs=[   
            Input('ModifCoursButton', 'n_clicks')   
        ],

        state=[  
            State('CoursId','value'),
            State('CoursNiveau','value'),
            State('CoursNHourFacturee','value'),
            State('CoursNHourReal','value'),
            State('CoursSurPlace','value'),
            State('CoursNHourPreparation','value'),
            State('CoursStudentId','value'),  #! same order as Db
            State('CoursDate','date'),  
            State('CoursHourPriceHT','value'),
        ],

        prevent_initial_call=True,

 

)
def ModifCours(trigger,*values):
    Values = []

    query_sql = '''

            UPDATE cours

            set XXXXCol=ValuesComaXXX
            
            WHERE Id= XXidXX;
            '''

    Cols=[ 
            'Id',
            'Niveau',
            'NHourFacturee',
            'NHourReal',
            'SurPlace',
            'NHourPreparation',
            'StudentId',
            'Date',
            'FactureId',
            'HourPriceHT',
            ]

    Values = ModifyCoursValuesFromInputs(Values,values)

    if Values is None or Values[0] is None or Values[0]=="" or (type(Values[0]) is int and Values[0]<0) :
    
        return ReturnWarningNotif('Bad Id to modify !')



    SQLValues=[]


    for i,v in enumerate(Values) :
        if v is None:
            Values[i]='DEFAULT'

        SQLValues.append(Cols[i]+"="+Values[i])

    SQLValues = ','.join(SQLValues)

    query_sql = query_sql.replace('XXXXCol=ValuesComaXXX', SQLValues) #'""')
    query_sql = query_sql.replace('XXidXX', str(Values[0])) #'""')

    print()
    print("-- ModifCours ")
    print(query_sql)


    try:

        res = InsertAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return ReturnFailNotif('Can\'t access Local Db')

    except mysql.connector.errors.DatabaseError as e:
        print(e)
        return ReturnFailNotif('ERROR  : '+str(e))

    return ReturnSuccessNotif('Done!')



@app.callback(

        output=[
            
            Output('CoursNiveau','value'),
            Output('CoursNHourFacturee','value'),
            Output('CoursNHourReal','value'),
            Output('CoursSurPlace','value'),
            Output('CoursNHourPreparation','value'),
            Output('CoursStudentId','value'),  #! same order as Db
            Output('CoursDate','date'),  
            Output('CoursFactureId','value'),  
            Output('CoursHourPriceHT','value'),
            ],

        inputs=[   
            Input('CoursId', 'value')   
        ],

        state=[  
        ],

        prevent_initial_call=True,

 

)
def UpdateCoursInfoFromCoursSelected(CoursId):

    res = GetCoursFromCoursId(CoursId).to_list()    
    print(res)

    res = res[1:] # remove Id
    return res


@app.callback(

        output=[
            Output('CoursId','options')  ,
            ],

        inputs=[   
            Input('CurrentStudentId', 'value')   
        ],

        prevent_initial_call=True,

)    
def SelectCoursToModify(StudentId):


    res = GetCoursFromStudentId(StudentId)

    options = res['Id'].to_list()

    return options



#************************************************************************************

#  Facture

@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('FactureInfoNumFacture','value'),
            ],

        inputs=[   
            Input('NextNumFacture','value'),
        ],

        state=[  
            # State('CustomEmail_input','value')
        ],

        prevent_initial_call=True,

 

)
def UpdateNextNumFacture(value):

    return value




def GetStudentFromClientId(ClientId):
    query_sql = '''

                SELECT *

                FROM students Where ClientId=XXXClientIdXXX;

                '''

                # JOIN users ON users.id = pairings.user_id

                # JOIN masters ON masters.id = pairings.master_id

                # WHERE email =  "XXXEmailXX"

                # LIMIT 100'''

 


    query_sql = query_sql.replace('XXXClientIdXXX', str(ClientId) )

    print()
    print("-- GetStudentsForThisClients ")
    print(query_sql)

    res = ReadAPIQuery(query_sql=query_sql)


    return res



def GetPrestaListNotLinkedToFacture(ClientId):

    Prestas = {}
    count=0

    Students  = GetStudentFromClientId(ClientId)


    for i,r in Students.iterrows():
        
        res = GetCoursFromStudentId(r['Id'])
    
        res = res[res['FactureId'].isna()]

        for ii,rr in res.iterrows():
            
            PrestaInfo = rr.to_dict()
            PrestaInfo['StudentName'] = r['Nom']
            PrestaInfo['StudentFirstName'] = r['Prenoms']
            
            Prestas[count] = PrestaInfo
            count+=1

    print(Prestas)


    return Prestas


@app.callback(
    output= [
        Output('FacturePrestations-dynamic-dropdown-container', 'children'),
        Output('CurrentPrestasSelectedToFacture', 'data'),
        
    ],
    inputs=[
        Input('CreateFactureAddPrestationButton', 'n_clicks'),
    ],
    state=[
        State('FacturePrestations-dynamic-dropdown-container', 'children'),
        State('CurrentClientId-fac', 'value'),
    ],
    prevent_initial_call=True,

)
def AddPrestationToFactureCreationPage(n_clicks,children,ClientId):

    Prestas =  GetPrestaListNotLinkedToFacture(ClientId)

    options = []
    if Prestas is not None and len(Prestas)>0:
        for i,p in enumerate(Prestas):
            # options.append("Id="+str(Prestas[p]["Id"])+" , "+str(Prestas[p]["StudentName"])+" "+str(Prestas[p]["StudentFirstName"])+" , "+str(Prestas[p]["Date"]))
            options.append(i)#str(Prestas[p]["Id"]))

    new_element = html.Div([
        dcc.Dropdown(
            options=options,
            id={
                'type': 'facturecreationaddpresta-dynamic-dropdown',
                'index': n_clicks
            }
        ),
        html.Div(
            id={
                'type': 'facturecreationaddpresta-dynamic-output',
                'index': n_clicks
            }
        )
    ])
    children.append(new_element)
    return children,Prestas




@app.callback(
    Output({'type': 'facturecreationaddpresta-dynamic-output', 'index': MATCH}, 'children'),
    Input({'type': 'facturecreationaddpresta-dynamic-dropdown', 'index': MATCH}, 'value'),
    State({'type': 'facturecreationaddpresta-dynamic-dropdown', 'index': MATCH}, 'id'),
    State("CurrentPrestasSelectedToFacture", 'data'),
)
def DisplaySelectedPrestationInfoInFactureCreationPage(value, id,selectedprestas):

    print(selectedprestas)

    presta = selectedprestas[str(value)]
    print(presta)

    infos = []
    for k in presta:
        infos.append(html.Div(str(k)+' : '+str(presta[k])))

    children= html.Div(
        infos
    )


    return children 
    #html.Div('Dropdown {} = {}'.format(id['index'], value))





@app.callback(
    output = [
        Output('FactureInfoMontantHT', 'value'),
        Output('FactureInfoMontantTTC', 'value'),
    ],
    inputs=[
        Input('ComputeTotalFactureButton', 'n_clicks'),

        
    ],
    state=[

        State({'type': 'facturecreationaddpresta-dynamic-dropdown', 'index': ALL}, 'value'),
        State({'type': 'facturecreationaddpresta-dynamic-dropdown', 'index': ALL}, 'id'),
        State('TVAvalue', 'value'),
        State("CurrentPrestasSelectedToFacture", 'data'),

    ]
)
def ComputeTotalFacture(trigger,value, id,tva,selectedprestas):

    print('ooooooooooooooooooooo')
    print(trigger)
    print(value)
    print(id)
    print(tva)

    tva=float(tva)/100
    tvafactor = 1+tva
    TotalHT=0

    for v in value:
        if v is None:
            continue
        presta = selectedprestas[str(v)]
        print(presta)

        TotalHT += presta['HourPriceHT'] * presta['NHourFacturee'] 


    TotalTTC = tvafactor * TotalHT

    return TotalTTC, TotalHT










@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('CurrentClientId-fac','options'),
            [
                Output('API_response_fail','is_open'),
                Output('API_response_fail','children'), 
                Output('API_response_warning','is_open'),
                Output('API_response_warning','children'), 
                Output('API_response_success','is_open'),
                Output('API_response_success','children'), 
            ]
            ],

        inputs=[   
            Input('GetAllClientsButton-fac', 'n_clicks')   
        ],

        state=[  
            # State('CustomEmail_input','value')
        ],

        prevent_initial_call=True,

 

)
def GetClientsForFacturation(trigger,Email=None):



    return GetClients(trigger,Email)



@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('FactureList','children'),
            Output('FactureInfoIdClient','value'),
            Output('FactureListForUrssafDemandePaiement','options'),
            Output('FactureListForUrssafDemandePaiement','value'),
            Output('FacturePrestations-dynamic-dropdown-container','children'),
            Output('CreateFactureAddPrestationButton','n_clicks'),
            
            ],

        inputs=[   
            Input('CurrentClientId-fac', 'value')   
        ],

        state=[  
            # State('CustomEmail_input','value')
        ],

        prevent_initial_call=True,

 

)
def GetFactureList(ClientId):

    ClientInfo = []#["oui","oui","oui"]#str(np.ones(NumColClientInfo))

    Children=[]
    DropDownOptions=[]

    query_sql = '''

            SELECT *

            FROM factures WHERE IdClient=XXXIdxXX order by NumFacture DESC;

            '''


    query_sql = query_sql.replace('XXXIdxXX', str(ClientId))#','.join(['email','long_id']))

    print()
    print("-- GetFactureList")


    res = ReadAPIQuery(query_sql=query_sql)


    if res.empty:
        Children.append(
            html.Div("No factures found for this client ",className="text-warning")

        )


    for i,r in res.iterrows():
        
        FactureInfos=[]
        for c in list(res.columns):
            FactureInfos.append(
                html.Div(
                    str(c)+" : "+str(r[c]),
                )
            )  


        Children.append(
            html.Div(
                className='card border-primary mb-3',
                style={"width":"100%"},
                children = FactureInfos,
            )

        )

        if(r['StatutDemandePaiementUrssaf'] is None) : 
            StrOption = "Id :"+str(r['Id'])+" , Num : "+str(r['NumFacture'])
            DropDownOptions.append(StrOption)
    
    if len(DropDownOptions)>0:
        DropDownValue=DropDownOptions[0]
    else:
        DropDownValue = None

    print(Children)
 
    return Children,ClientId,DropDownOptions,DropDownValue,[],0




@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('API_response_fail','is_open'),
            Output('API_response_fail','children'), 
            Output('API_response_warning','is_open'),
            Output('API_response_warning','children'), 
            Output('API_response_success','is_open'),
            Output('API_response_success','children'), 
            Output('NextNumFacture','value'),

            ],

        inputs=[   
            Input('CreateFactureButton', 'n_clicks')   
        ],

        state=[  
            # State('FactureInfoId','value'),  #! same order as Db
            State('FactureInfoIdClient','value'),
            State('FactureInfoNumFacture','value'),
            State('FactureInfoDateFacture','value'),
            State('FactureInfoDateDebutEmploi','value'),
            State('FactureInfoDateFinEmploi','value'),
            State('FactureInfoAcompte','value'),
            State('FactureInfoDateAcompte','value'),
            State('FactureInfoMontantTTC','value'),
            State('FactureInfoMontantHT','value'),
            State('FactureInfoIdClientUrssaf','value'),
        ],

        prevent_initial_call=True,

 

)
def AddFacture(trigger,*values):
    Values = [None,None]  #Id

    query_sql = '''

            INSERT INTO factures

            values(XXXXValuesComaXXX);

            '''

    for v in values:
        if v is None or v=="":
            Values.append(None)
        else:
            Values.append('"'+str(v)+'"')

    Values.append(None) #Statut demande paiement


    for i,v in enumerate(Values) :
        if v is None:
            Values[i]='DEFAULT'


    SQLValues = ','.join([ v for v in Values])

    query_sql = query_sql.replace('XXXXValuesComaXXX', SQLValues) #'""')

    print(query_sql)


    try:

        res = InsertAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return ReturnFailNotif('Can\'t access Local Db')



    NextNumFacture = GetMasterNextNumFacture()



    return *ReturnSuccessNotif('Done!'),NextNumFacture



 
@app.callback(

        output=[
            # Output('BoxIdFromCustomAPISearchData','data')  , 
            # Output('CurrentFileBoxIdLastPairedUserEmail','data')  ,
            
            Output('API_response_fail','is_open'),
            Output('API_response_fail','children'), 
            Output('API_response_warning','is_open'),
            Output('API_response_warning','children'), 
            Output('API_response_success','is_open'),
            Output('API_response_success','children'), 

            ],

        inputs=[   
            Input('ModifFactureButton', 'n_clicks')   
        ],

        state=[  
            State('FactureInfoId','value'),  #! same order as Db
            State('FactureInfoIdClient','value'),
            State('FactureInfoNumFacture','value'),
            State('FactureInfoDateFacture','value'),
            State('FactureInfoDateDebutEmploi','value'),
            State('FactureInfoDateFinEmploi','value'),
            State('FactureInfoAcompte','value'),
            State('FactureInfoDateAcompte','value'),
            State('FactureInfoMontantTTC','value'),
            State('FactureInfoMontantHT','value'),
            State('FactureInfoIdClientUrssaf','value'),
        ],

        prevent_initial_call=True,

 

)
def ModifFacture(trigger,id,*values):
    Values = []

    query_sql = '''

            UPDATE factures

            set XXXXCol=ValuesComaXXX
            
            WHERE Id= XXidXX;
            '''

    Cols=[ 
            'FactureInfoId',
            'FactureInfoIdClient',
            'FactureInfoNumFacture',
            'FactureInfoDateFacture',
            'FactureInfoDateDebutEmploi',
            'FactureInfoDateFinEmploi',
            'FactureInfoAcompte',
            'FactureInfoDateAcompte',
            'FactureInfoMontantTTC',
            'FactureInfoMontantHT',
            'FactureInfoIdClientUrssaf',
            ]

    for v in values:
        Values.append('"'+str(v)+'"')

    Values.append(None) #IdUrsaaf

    SQLValues=[]

    print(len(Values))
    print(len(Cols))
    print(len(values))

    for i,v in enumerate(Values) :
        if v is None:
            Values[i]='DEFAULT'

        SQLValues.append(Cols[i]+"="+Values[i])

    SQLValues = ','.join(SQLValues)

    query_sql = query_sql.replace('XXXXCol=ValuesComaXXX', SQLValues) #'""')
    query_sql = query_sql.replace('XXidXX', str(id)) #'""')

    print(query_sql)


    try:

        res = InsertAPIQuery(query_sql=query_sql)
    except mysql.connector.errors.InterfaceError :

        return ReturnFailNotif('Can\'t access Local Db')


    return ReturnSuccessNotif('Done!')








def GetBearer():

    print()
    print("---- GetBearer")

    hed = {"Content-Type":"application/x-www-form-urlencoded"}
    data = {
        "scope":"homeplus.tiersprestations",
        "grant_type": "client_credentials",
        "client_id" :os.environ.get('URSSAF_client_id'),
        "client_secret":os.environ.get('URSSAF_client_secret')
    }
    url='https://api-edi.urssaf.fr/api/oauth/v1/token'

    req = requests.post(url,data=data,headers=hed)# ("Bearer","4BK5WVGVqb9hER5mWNnIIgDdbcw0s_pkz5in9N4AKyE"))

    print(json.loads(req.text)['access_token'])
    return json.loads(req.text)['access_token']


def CreateHttpRequest(url,data):



    bearer = GetBearer()

    print()
    print("---- CreateHttpRequest")

    # req = requests.get(url)   
    hed = {'Authorization': 'Bearer ' + bearer,
            "Content-Type":"application/json"}# "4BK5WVGVqb9hER5mWNnIIgDdbcw0s_pkz5in9N4AKyE"}
    req = requests.post(url,json=data,headers=hed)# ("Bearer","4BK5WVGVqb9hER5mWNnIIgDdbcw0s_pkz5in9N4AKyE"))
    

    reqq = requests.Request('POST',url,json=data,headers=hed)
    prepped  = reqq.prepare()

    print(reqq)
    print(prepped.__dict__)
    # print(prepped.body)
    print("---- ")


    print(req)
    print(req.status_code)
    print(req.text)
    # print(req.content)

    print("---- ")

    return req



def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


    
def PrepareRequest(url,data):
    hed = {'Authorization': 'Bearer ' + "XXXX",
            "Content-Type":"application/json"}# "4BK5WVGVqb9hER5mWNnIIgDdbcw0s_pkz5in9N4AKyE"}


    req = requests.Request('POST',url,json=json.dumps(data),headers=hed)
    prepared = req.prepare()


    pretty_print_POST(prepared)






####################################################



# URSSAF


###################################################

 

def ModifyDateNaissanceForURSSAF(date):

    date = datetime.strptime(date,"%Y-%m-%d")
    date = date.isoformat()+'.000Z' 

    return date

@app.callback(

    output=[
        Output('API_response_fail','is_open'),
        Output('API_response_fail','children'), 
        Output('API_response_warning','is_open'),
        Output('API_response_warning','children'), 
        Output('API_response_success','is_open'),
        Output('API_response_success','children'), 
    ],
    inputs = [


            Input('SubmitTOUrssafClientButton', 'n_clicks') ,  

            State('ClientInfoId',"value"),
            State('ClientInfoEmail',"value"),
            State('ClientInfoTel',"value"),

            State('ClientInfoNom',"value"),
            State('ClientInfoNomUsage',"value"),
            State('ClientInfoPrenoms',"value"),
            State('ClientInfoCivilite',"value"),

            State('ClientInfoDateNaissance',"date"),
            State('ClientInfoPaysNaissance',"value"),
            State('ClientInfoDepNaissance',"value"),
            State('ClientInfoVilleNaissance',"value"),
            State('ClientInfoCodeVilleNaissance',"value"),



            State('ClientAdresseNumVoie',"value"),
            State('ClientAdresseLettreVoie',"value"),
            State('ClientAdresseCodeVoie',"value"),
            State('ClientAdresseVoie',"value"),
            State('ClientAdresseComplement',"value"),
            State('ClientAdresseLieuDit',"value"),
            State('ClientAdresseVille',"value"),
            State('ClientAdresseCodeVille',"value"),
            State('ClientAdresseCodePostal',"value"),
            State('ClientAdresseCodePays',"value"),



            State('ClientBIC',"value"),
            State('ClientIBAN',"value"),
            State('ClientBanqueTitulaire',"value"),


    ],
    prevent_initial_call = True


)
def SubmitClientToUrssaf(Trigger,clientId,email,tel,nom,nomusage,prenoms,civilite,
                            datenaissance,paysnaissance,depnaissance,villenaissance,codevillenaissance,
                            adressnumvoie,adresslettre, adresscodevoie,adressevoie,adresscomplement,adresslieudit,adressville,adresscodeville,adresscodepostal,adresscodepays,
                            BIC,IBAN,BankTitulaire):


    # datenaissance = datetime.strptime(datenaissance,"%Y-%m-%d")
    # datenaissance = datenaissance.isoformat()+'.000Z' 
    datenaissance = ModifyDateNaissanceForURSSAF(datenaissance)
    print()
    print()
    print("------------ SubmitClientToUrssaf")

    print(datenaissance)

    data =     {
        "civilite": str(civilite),#"\""+str(civilite)+"\"",#"\"1\"",
        "nomNaissance": nom,
        "nomUsage": nomusage,
        "prenoms": prenoms,
        "dateNaissance": datenaissance,
        "lieuNaissance": {
            "codePaysNaissance": paysnaissance,#"99100",
            "departementNaissance": depnaissance,#"069",
            "communeNaissance": {
                "codeCommune" : codevillenaissance,
                "libelleCommune": villenaissance,
            }
        },
        "numeroTelephonePortable": tel,#"0605040302",
        "adresseMail": email,#"jeanne.durand@contact.fr",
        "adressePostale": {
            "numeroVoie": adressnumvoie,
            "lettreVoie": adresslettre,
            "codeTypeVoie": adresscodevoie,#"R",
            "libelleVoie": adressevoie,#"du Soleil",
            "complement": adresscomplement,#"Batiment A",
            "lieuDit": adresslieudit,#"Le Beyssat",
            "libelleCommune": adressville,#"LYON 01",
            "codeCommune": adresscodeville,#"69101",
            "codePostal": adresscodepostal,#"69001",
            "codePays": adresscodepays,# "99100"
        },
        "coordonneeBancaire": {
            "bic": BIC,#"BNAPFRPPXXX",
            "iban": IBAN,#"FR7630006000011234567890189",
            "titulaire": BankTitulaire,#"Mme Jeanne Martin"
        }
    }

    print(data)
    print(json.dumps(data))


    # req = PrepareRequest(url="https://api-edi.urssaf.fr/atp/v1/tiersPrestations/particulier",data=data)


    req = CreateHttpRequest(url="https://api-edi.urssaf.fr/atp/v1/tiersPrestations/particulier",data=data)


    print(req.text)

    if req.status_code == 200:

        idUrssaf= json.loads(req.text)["idClient"]

        query_sql = '''

        UPDATE clients

        set IdUrssaf=XXXValueXXX
        
        WHERE Id= XXidXX;
        '''
        query_sql = query_sql.replace('XXidXX', str(clientId)) #'""')
        query_sql = query_sql.replace('XXXValueXXX','"'+str(idUrssaf)+'"') #'""')

        print(query_sql)

        try:

            res = InsertAPIQuery(query_sql=query_sql)

            return ReturnSuccessNotif('Done!')

        except mysql.connector.errors.InterfaceError :

            return ReturnFailNotif('Could not update Db with Urssaf Id : '+str(idUrssaf))
    
    elif req.status_code == 400:

        infos  = json.loads(req.text)[0]
        print(infos)
        Code= infos["code"]
        Message= infos["message"]
        Desc= infos["description"]
        return ReturnFailNotif('Failed Bad request (400) : '+str(Code)+" => "+str(Message)+' ... '+str(Desc))
    elif req.status_code == 401:
        return ReturnFailNotif('Failed : Bad authentification ! (401)')
    elif req.status_code == 503:
        return ReturnFailNotif('Failed : API unavailable ! (503)')
    elif req.status_code == 500:
        return ReturnFailNotif('Failed : API server internal error ! (500)')
    else:
        print(req)
        # print(req.body)

        return ReturnFailNotif('Failed request to API Urssaf : '+str(req.status_code))

# https://api-edi.urssaf.fr





@app.callback(

    output=[
        Output('API_response_fail','is_open'),
        Output('API_response_fail','children'), 
        Output('API_response_warning','is_open'),
        Output('API_response_warning','children'), 
        Output('API_response_success','is_open'),
        Output('API_response_success','children'), 
    ],
    inputs = [


            Input('SubmitTOUrssafDemandePaiement-button', 'n_clicks') ,  

            State('ClientInfoId',"value"),
            State('ClientInfoEmail',"value"),
            State('ClientInfoTel',"value"),

            State('ClientInfoNom',"value"),
            State('ClientInfoNomUsage',"value"),
            State('ClientInfoPrenoms',"value"),
            State('ClientInfoCivilite',"value"),

            State('ClientInfoDateNaissance',"date"),
            State('ClientInfoPaysNaissance',"value"),
            State('ClientInfoDepNaissance',"value"),
            State('ClientInfoVilleNaissance',"value"),
            State('ClientInfoCodeVilleNaissance',"value"),



            State('ClientAdresseNumVoie',"value"),
            State('ClientAdresseLettreVoie',"value"),
            State('ClientAdresseCodeVoie',"value"),
            State('ClientAdresseVoie',"value"),
            State('ClientAdresseComplement',"value"),
            State('ClientAdresseLieuDit',"value"),
            State('ClientAdresseVille',"value"),
            State('ClientAdresseCodeVille',"value"),
            State('ClientAdresseCodePostal',"value"),
            State('ClientAdresseCodePays',"value"),



            State('ClientBIC',"value"),
            State('ClientIBAN',"value"),
            State('ClientBanqueTitulaire',"value"),


    ],
    prevent_initial_call = True


)
def SubmitDemandePaiementToUrssaf(Trigger,clientId,email,tel,nom,nomusage,prenoms,civilite,
                            datenaissance,paysnaissance,depnaissance,villenaissance,codevillenaissance,
                            adressnumvoie,adresslettre, adresscodevoie,adressevoie,adresscomplement,adresslieudit,adressville,adresscodeville,adresscodepostal,adresscodepays,
                            BIC,IBAN,BankTitulaire):


    datenaissance = datetime.strptime(datenaissance,"%Y-%m-%d")
    datenaissance = datenaissance.isoformat()+'.000Z' 

    print()
    print()
    print("------------ SubmitDemandePaiementToUrssaf")

    print(clientId)

    cli = GetClientFromClientId(clientId)

    if cli.empty:
        return ReturnFailNotif('Cant find Client with Id '+str(clientId))


    cli = cli.iloc[0]

    cli['DateNaissance'] = ModifyDateNaissanceForURSSAF(cli['DateNaissance'])

    print(cli)
    print(type(cli['Email']))

    # return ReturnSuccessNotif('TempSuccess')


    #! numfacture
    #! Id Facture
    #! presta infos => list cours
    #! lier les cours à la facture !
    

    data =     {
        # "civilite": str(civilite),#"\""+str(civilite)+"\"",#"\"1\"",
        # "nomNaissance": cli['Nom'],
        # "nomUsage": cli['NomUsage'],
        # "prenoms": cli['Prenoms'],
        "dateNaissanceClient":  cli['DateNaissance'],
        # "adresseMail":  "\""+cli['Email']+"\"",
        # "numeroTelephonePortable":  str(cli['Tel']),
        # "lieuNaissance": {
        #     "codePaysNaissance": cli['PaysNaissance'],#"99100",
        #     "departementNaissance": cli['DepNaissance'],#"069",
        #     "communeNaissance": {
        #         "codeCommune" : cli['CodeVilleNaissance'],
        #         "libelleCommune": cli['VilleNaissance'],
        #     }
        # },
        # "numeroTelephonePortable": tel,#"0605040302",
        # "adresseMail": email,#"jeanne.durand@contact.fr",
        # "adressePostale": {
        #     "numeroVoie": cli['AdresseNumVoie'],
        #     "lettreVoie": cli['AdresseLettreVoie'],
        #     "codeTypeVoie":  cli['AdresseCodeVoie'],
        #     "libelleVoie": cli['AdresseVoie'],
        #     "complement": cli['AdresseComplement'],
        #     "lieuDit": cli['AdresseLieuDit'],
        #     "libelleCommune": cli['AdresseVille'],
        #     "codeCommune": cli['AdresseCodeVille'],
        #     "codePostal": cli['AdresseCodePostal'],
        #     "codePays": cli['AdresseCodePays'],
        # },
        # "coordonneeBancaire": {
        #     "bic": cli['BanqueBIC'],
        #     "iban":cli['BanqueIBAN'],
        #     "titulaire": cli['BanqueTitulaire'],
        # },
        "idClient":cli['IdUrssaf'],
    }


    data.update( {
    #         "idTiersFacturation": "1081230",
    #         # "idClient": "11000000000104",
    #         # "dateNaissanceClient": "1986-11-30T00:00:00Z",
    #         # "numFactureTiers": "11000000000104",
    #         "dateFacture": "2019-12-01T00:00:00Z",
    #         "dateDebutEmploi": "2019-11-01T00:00:00Z",
    #         "dateFinEmploi": "2019-11-30T00:00:00Z",
    #         "mntAcompte": 100,
    #         "dateVersementAcompte": "2019-11-25T00:00:00Z",
    #         "mntFactureTTC": 2000,
    #         "mntFactureHT": 1800,
            "inputPrestations": [
            {
                # "codeActivite": "01",
                "codeActivite": "",
                "codeNature": "10",
                "quantite": 1.0,
                "unite": "HEURE",
                "mntUnitaireTTC": 20,
                "mntPrestationTTC": 20,
                "mntPrestationHT": 20,
                "mntPrestationTVA": 0,
                "dateDebutEmploi": "2023-02-08T00:00:00Z",
                "dateFinEmploi": "2023-02-08T00:00:00Z",
                "complement1": "Complément 1 ",
                "complement2": "Complément 2 "
            }
            ]
        }
    )

    data.update({
		# "idTiersFacturation": "90197663900012",#"d52274e2-af3a-4157-a4b7-3d5ac5709c19",
		"idTiersFacturation": "menage.fr",#"d52274e2-af3a-4157-a4b7-3d5ac5709c19",
		# "idClient": "11000000000104",
		# "dateNaissanceClient": "1986-11-30T00:00:00Z",
		"numFactureTiers": "11000050000114",
		"dateFacture": "2023-02-08T00:00:00Z",
		"dateDebutEmploi": "2023-02-08T00:00:00Z",
		# "dateFinEmploi": "2023-01-22T00:00:00Z",
		"dateFinEmploi": "2023-02-08T00:00:00Z",
		# "mntAcompte": 0,
		# "dateVersementAcompte": "2022-11-25T00:00:00Z",
		"mntFactureTTC": 20,
		"mntFactureHT": 20,
		# "inputPrestations": [
		# 	{
		# 		"codeActivite": "01",
		# 		# "codeActivite": "85",
		# 		"codeNature": "ENF",
		# 		"quantite": 1,
		# 		"unite": "HEURE",
		# 		"mntUnitaireTTC": 100,
		# 		"mntPrestationTTC": 100,
		# 		"mntPrestationHT": 100,
		# 		"mntPrestationTVA": 0,
		# 		# "dateDebutEmploi": "2022-11-01T00:00:00Z",
		# 		# "dateFinEmploi": "2022-11-30T00:00:00Z",
		# 		# "complement1": "Complement 1 ",
		# 		# "complement2": "Complement 2 "
		# 	}
		# ]
	}
    )
    data = [data]

    print("uuuuuuuuuuuuuuuuuuu")
    print(data)
    print(json.dumps(data))
    print("uuuuuuuuuuuuuuuuuuu")


    # req = PrepareRequest(url="https://api-edi.urssaf.fr/atp/v1/tiersPrestations/particulier",data=data)


    # req = CreateHttpRequest(url="https://api-edi.urssaf.fr/atp/v1/tiersPrestations/particulier",data=data)
    req = CreateHttpRequest(url="https://api-edi.urssaf.fr/atp/v1/tiersPrestations/demandePaiement",data=data)


    print("Req response")
    # print(json.load(req))
    print(req.text)
    # print(req.content)


    if req.status_code == 200:

        idUrssaf= json.loads(req.text)[0]["idDemandePaiement"]
        StatutUrssaf= json.loads(req.text)[0]["statut"]


        print(idUrssaf)
        query_sql = '''

        UPDATE factures

        set IdUrssaf=XXXValueIdXXX,  StatutDemandePaiementUrssaf=XXXValueStatusXXX
        
        WHERE Id= XXidXX;
        '''
        query_sql = query_sql.replace('XXidXX', str(14)) #'""') #! id facture !!!
        query_sql = query_sql.replace('XXXValueIdXXX','"'+str(idUrssaf)+'"') #'""')
        query_sql = query_sql.replace('XXXValueStatusXXX','"'+str(StatutUrssaf)+'"') #'""')

        print(query_sql)

        try:

            res = InsertAPIQuery(query_sql=query_sql)

            return ReturnSuccessNotif('Done!')

        except mysql.connector.errors.InterfaceError :

            return ReturnFailNotif('Could not update Db with Urssaf Id : '+str(idUrssaf))
    
    elif req.status_code == 400:

        infos  = json.loads(req.text)[0]
        print(infos)
        Code= infos["code"]
        Message= infos["message"]
        Desc= infos["description"]
        return ReturnFailNotif('Failed Bad request (400) : '+str(Code)+" => "+str(Message)+' ... '+str(Desc))
    elif req.status_code == 401:
        return ReturnFailNotif('Failed : Bad authentification ! (401)')
    elif req.status_code == 503:
        return ReturnFailNotif('Failed : API unavailable ! (503)')
    elif req.status_code == 500:
        return ReturnFailNotif('Failed : API server internal error ! (500)')
    else:
        print(req)
        # print(req.body)

        return ReturnFailNotif('Failed request to API Urssaf : '+str(req.status_code))






if __name__=="__main__":


    app.run_server(debug=True,host='0.0.0.0',port=Config['Connexion']['Port'])

    print('Done')



 

 

 