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

 
Config = None

package_directory = os.path.dirname(os.path.abspath(__file__))

 

StartWarnings = []

StartErrors = []




Db_password=os.environ['DB_passwd']






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

            FROM factures Order by NumFacture desc  Limit 1 ;

            '''

    print()
    print("-- GetMasterNextNumFacture")


    res = ReadAPIQuery(query_sql=query_sql)

    if res.empty:
        return 0
    else:
        return int(res.iloc[0])+1

 





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
            Output('ClientInfoNomUsage',"value"),
            Output('ClientInfoCivilite',"value"),
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
            'Civilite',
            'NomUsage',
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

        if(r['StatusDemandePaiementUrssaf'] is None) : 
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



 
if __name__=="__main__":


    app.run_server(debug=True,host='0.0.0.0',port=Config['Connexion']['Port'])

    print('Done')



 

 

 