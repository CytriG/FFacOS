from dash import Dash, html, dcc, callback_context, dash_table

import dash_bootstrap_components as dbc

from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, State, ClientsideFunction
 

import numpy as np
from datetime import date

import os


today = date.today()
 

def CreateLayoutTab_Factures(Config):
 

    return dcc.Tab(

                id="Tab-Factures",

                value='TabFactures',

                label="Factures",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[

 

                    html.Div([

                        # html.H1(''),

                        html.Div(style={'height':'20px'}),

                        dbc.Row([

                            dbc.Col([

                                html.Div(
                                    id='ClientSelection-fac',
                                    className='card border-primary mb-3',
                                    style={"width":"100%"},
                                    children=[
                                        html.Div(className='card-header',
                                        children=[
                                            html.Div('Client list')
                                        ]),
                                        html.Div(className='card-body',
                                        children=[
                                            html.Button("Get All",id="GetAllClientsButton-fac",n_clicks=0,className='btn btn-lg btn-primary',style={"min-height":"20px","max-width":"300px"}),
                                            # html.Div(id="ClientListDiv",
                                            # children=""),

                                            dcc.RadioItems(id="CurrentClientId-fac",
                                                style={"width":"50%"},
                                                className="form-check",
                                                inputClassName='form-check-input',
                                                labelClassName='form-check-label',
                                                options=[{"label":"New","value":-1}],
                                                value=-1
                                            )
                                        ])
                                    ])

                            ],width=4),

 
                            dbc.Col([

                                dcc.Tabs(id="TabsFactures",
                                className='nav-item',
                                parent_className='nav nav-tabs',
                                value="TabFactureList",
                                children=[
                                    CreateTabFactureList(),
                                    CreateTabFactureCreation(Config),
                                    CreateTabFactureGeneratePDF(),
                                    CreateTabFactureDemandePaiment(),
                                ]),

                            ],width=8),
           
                        ])
                    ])
                ])


def CreateTabFactureGeneratePDF():


    return dcc.Tab(


                value='TabFactureGeneratePDF',

                label="Create PDF",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[

       
                ]
            )

def CreateTabFactureDemandePaiment():


    return dcc.Tab(


                value='TabFactureDemandePaiement',

                label="Demande Paiement Urssaf",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[
                    html.Div(
                    style={"width":"80%"},
                    children=[
                        html.Div(style={"height":"75px"}),
                        dcc.Dropdown(id="FactureListForUrssafDemandePaiement",
                        className="form-label mt-4",
                        options=[],
                        value=None,
                        ),
                        html.Div(style={"height":"30px"}),
                        html.Button("Submit To Urssaf",id="SubmitTOUrssafDemandePaiement-button",n_clicks=0,className='btn btn-lg btn-warning',style={"min-height":"20px","max-width":"300px"}),
                    ])

                ]
            )

def CreateTabFactureList():


    return dcc.Tab(


                value='TabFactureList',

                label="Facture List",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[

                    html.Div(id="FactureList")

       
                ]
            )

def CreateTabFactureCreation(Config):


    return dcc.Tab(


                value='TabFactureCreation',

                label="Facture Creation",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[

                    dcc.Input(id='FactureInfoId',className="form-control",type="text",value="-1",size="30",placeholder="FactureInfoId"),
                    dcc.Input(id='FactureInfoIdClient',className="form-control",type="text",value="",size="30",placeholder="FactureInfoIdClient"),
                    dcc.Input(id='FactureInfoNumFacture',disabled=True,className="form-control",type="text",value=Config['StartNextNumFacture'],size="30",placeholder="FactureInfoNumFacture"),
                    dcc.Input(id='FactureInfoDateFacture',className="form-control",type="text",value="",size="30",placeholder="FactureInfoDateFacture"),
                    dcc.Input(id='FactureInfoDateDebutEmploi',className="form-control",type="text",value="",size="30",placeholder="FactureInfoDateDebutEmploi"),
                    dcc.Input(id='FactureInfoDateFinEmploi',className="form-control",type="text",value="",size="30",placeholder="FactureInfoDateFinEmploi"),
                    dcc.Input(id='FactureInfoIdClientUrssaf',className="form-control",type="text",value="",size="30",placeholder="FactureInfoIdClientUrssaf"),
                    

                    html.Div(style={"height":"50px"}),
                    html.Label('Prestations :'),
                    html.Div(id='FacturePrestations-dynamic-dropdown-container', children=[]),
                    html.Div(style={"height":"20px"}),
                    html.Button("Add Prestation",id="CreateFactureAddPrestationButton",n_clicks=0,className='btn btn-lg btn-info',style={"min-height":"20px","max-width":"300px"}),
                    
                    # dcc.Dropdown(id="FactureCreationPrestationList",
                    # className="form-label mt-4",
                    # options=[],
                    # value=None,
                    # ),
                    html.Div(style={"height":"50px"}),
                    dcc.Input(id='FactureInfoAcompte',className="form-control",type="text",value="",size="30",placeholder="FactureInfoAcompte"),
                    dcc.Input(id='FactureInfoDateAcompte',className="form-control",type="text",value="",size="30",placeholder="FactureInfoDateAcompte"),
                    
                    html.Div(style={"height":"50px"}),
                    html.Button("Compute Total",id="ComputeTotalFactureButton",n_clicks=0,className='btn btn-lg btn-info',style={"min-height":"20px","max-width":"300px"}),
                    dcc.Input(id='FactureInfoMontantHT',className="form-control",type="text",value="",size="30",placeholder="FactureInfoMontantHT"),
                    dcc.Input(id='FactureInfoMontantTTC',className="form-control",type="text",value="",size="30",placeholder="FactureInfoMontantTTC"),



                    html.Div(style={"height":"50px"}),


                    html.Button("Create",id="CreateFactureButton",n_clicks=0,className='btn btn-lg btn-info',style={"min-height":"20px","max-width":"300px"}),
                    html.Button("Modify",id="ModifFactureButton",n_clicks=0,className='btn btn-lg btn-warning',style={"min-height":"20px","max-width":"300px"}),
                    # html.Button("Delete",id="DeleteFactureButton",n_clicks=0,className='btn btn-lg btn-danger',style={"min-height":"20px","max-width":"300px"}),
                    html.Div(style={"height":"5px"}),
       
                ]
            )


def CreateLayoutTab_Clients():
 

    return dcc.Tab(

                id="Tab-Clients",

                value='TabClients',

                label="Clients",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[

 

                    html.Div([

                        # html.H1(''),

                        html.Div(style={'height':'20px'}),

                        dbc.Row([


                            dbc.Col([

                                html.Div(
                                    id='ClientSelection',
                                    className='card border-primary mb-3',
                                    style={"width":"100%"},
                                    children=[
                                        html.Div(className='card-header',
                                        children=[
                                            html.Div('Client list')
                                        ]),
                                        html.Div(className='card-body',
                                        children=[
                                            html.Button("Get All",id="GetAllClientsButton",n_clicks=0,className='btn btn-lg btn-primary',style={"min-height":"20px","max-width":"300px"}),
                                            # html.Div(id="ClientListDiv",
                                            # children=""),

                                            dcc.RadioItems(id="CurrentClientId",
                                            style={"width":"50%"},
                                            className="form-check",
                                            inputClassName='form-check-input',
                                            labelClassName='form-check-label',
                                            options=[{"label":"New","value":-1}],
                                            value=-1
                                            )
                                        ])
                                    ])

                            ],width=4),

                            dbc.Col([

                                dcc.Tabs(id="TabsClient",
                                className='nav-item',
                                parent_className='nav nav-tabs',
                                children=[
                                    CreateTabClientInfo(),
                                    CreateTabClientModif(),
                                    CreateTabClientStudent()
                                ]),

                            ],width=8),
                        ])
                    ])
                ])



def CreateTabClientInfo():


    return dcc.Tab(


                value='TabClientInfo',

                label="Info",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[

       
                ]
            )


def CreateTabClientModif():

    return dcc.Tab(

                value='TabClientModif',

                label="Modif Info",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[

                    html.Div(
                        id='ClientModif',
                        className='card border-primary mb-3',
                        children=[
                            html.Div(className='card-header',
                            children=[
                                html.Div('Client Info')
                            ]),
                            html.Div(className='card-body',
                            children=[
                                dcc.Input(id='ClientInfoId',className="form-control",type="text",value="",size="30",placeholder="ClientInfoId"),
                                dcc.Input(id='ClientInfoNom',className="form-control",type="text",value="",size="30",placeholder="ClientInfoNom"),
                                dcc.Input(id='ClientInfoPrenoms',className="form-control",type="text",value="",size="30",placeholder="ClientInfoPrenoms"),
                                dcc.Input(id='ClientInfoNomUsage',className="form-control",type="text",value="",size="30",placeholder="ClientInfoNomUsage"),
                                dcc.Input(id='ClientInfoCivilite',className="form-control",type="text",value="",size="30",placeholder="ClientInfoCivilite"),
                                dcc.Input(id='ClientInfoDateNaissance',className="form-control",type="text",value="",size="30",placeholder="ClientInfoDateNaissance"),
                                dcc.Input(id='ClientInfoPaysNaissance',className="form-control",type="text",value="",size="30",placeholder="ClientInfoPaysNaissance"),
                                dcc.Input(id='ClientInfoDepNaissance',className="form-control",type="text",value="",size="30",placeholder="ClientInfoDepNaissance"),
                                dcc.Input(id='ClientInfoCodeVilleNaissance',className="form-control",type="text",value="",size="30",placeholder="ClientInfoCodeVilleNaissance"),
                                dcc.Input(id='ClientInfoVilleNaissance',className="form-control",type="text",value="",size="30",placeholder="ClientInfoVilleNaissance"),
                                dcc.Input(id='ClientInfoTel',className="form-control",type="text",value="",size="30",placeholder="ClientInfoTel"),
                                dcc.Input(id='ClientInfoEmail',className="form-control",type="text",value="",size="30",placeholder="ClientInfoEmail"),

                                dcc.Input(id='ClientAdresseNumVoie',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseNumVoie"),
                                dcc.Input(id='ClientAdresseLettreVoie',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseLettreVoie"),
                                dcc.Input(id='ClientAdresseCodeVoie',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseCodeVoie"),
                                dcc.Input(id='ClientAdresseVoie',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseVoie"),
                                dcc.Input(id='ClientAdresseComplement',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseComplement"),
                                dcc.Input(id='ClientAdresseLieuDit',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseLieuDit"),
                                dcc.Input(id='ClientAdresseVille',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseVille"),
                                dcc.Input(id='ClientAdresseCodeVille',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseCodeVille"),
                                dcc.Input(id='ClientAdresseCodePostal',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseCodePostal"),
                                dcc.Input(id='ClientAdresseCodePays',className="form-control",type="text",value="",size="30",placeholder="ClientAdresseCodePays"),

                                dcc.Input(id='ClientBIC',className="form-control",type="text",value="",size="30",placeholder="ClientBIC"),
                                dcc.Input(id='ClientIBAN',className="form-control",type="text",value="",size="30",placeholder="ClientIBAN"),
                                dcc.Input(id='ClientBanqueTitulaire',className="form-control",type="text",value="",size="30",placeholder="ClientBanqueTitulaire"),

                                html.Button("Create",id="CreateClientButton",n_clicks=0,className='btn btn-lg btn-info',style={"min-height":"20px","max-width":"300px"}),
                                html.Button("Modify",id="ModifClientButton",n_clicks=0,className='btn btn-lg btn-warning',style={"min-height":"20px","max-width":"300px"}),
                                html.Button("Delete",id="DeleteClientButton",n_clicks=0,className='btn btn-lg btn-danger',style={"min-height":"20px","max-width":"300px"}),
                                html.Button("Submit To Urssaf",id="SubmitTOUrssafClientButton",n_clicks=0,className='btn btn-lg btn-warning',style={"min-height":"20px","max-width":"300px"}),
                                html.Div(style={"height":"5px"}),
                            ])
                        ]),
                        
                                
                ]
            )

def CreateTabClientStudent():

    return dcc.Tab(

                value='TabClientStudent',

                label="Students",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[
                    html.Div(
                        id='NewStudentInfo',
                        className='card border-primary mb-3',
                        children=[
                            html.Div(className='card-header',
                            children=[
                                html.Div('New Student')
                            ]),
                            html.Div(className='card-body',
                            children=[
                                dcc.Input(id='NewStudentInfoId',className="form-control",type="text",value="",size="30",placeholder="StudentInfoId"),
                                dcc.Input(id='NewStudentInfoNom',className="form-control",type="text",value="",size="30",placeholder="StudentInfoNom"),
                                dcc.Input(id='NewStudentInfoPrenoms',className="form-control",type="text",value="",size="30",placeholder="StudentInfoPrenoms"),

                                html.Button("Create",id="CreateStudentButton",n_clicks=0,className='btn btn-lg btn-info',style={"min-height":"20px","max-width":"300px"}),
                                html.Button("Modify",id="ModifyStudentButton",n_clicks=0,className='btn btn-lg btn-warning',style={"min-height":"20px","max-width":"300px"}),
                                html.Div(style={"height":"5px"}),
                            ])
                        ])
                ]
    )


def CreateLayoutTab_Cours():
 

    return dcc.Tab(

                id="Tab-Cours",

                value='TabCours',

                label="Cours",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[

                    html.Div([

                        # html.H1(''),

                        html.Div(style={'height':'20px'}),

                        dbc.Row([

                            dbc.Col([

                                html.Div(
                                    id='StudentSelection',
                                    className='card border-primary mb-3',
                                    style={"width":"100%"},
                                    children=[
                                        html.Div(className='card-header',
                                        children=[
                                            html.Div('Student list')
                                        ]),
                                        html.Div(className='card-body',
                                        children=[
                                            html.Button("Get All",id="GetAllStudentsButton",n_clicks=0,className='btn btn-lg btn-primary',style={"min-height":"20px","max-width":"300px"}),
                                            # html.Div(id="ClientListDiv",
                                            # children=""),

                                            dcc.RadioItems(id="CurrentStudentId",
                                            style={"width":"50%"},
                                            className="form-check",
                                            inputClassName='form-check-input',
                                            labelClassName='form-check-label',
                                            options=[{"label":"New","value":-1}],
                                            value=-1
                                            )
                                        ])
                                    ])

                            ],width=2),

                            


                            dbc.Col([

                                dcc.Tabs(id="TabsCours",
                                className='nav-item',
                                parent_className='nav nav-tabs',
                                value="Tab-CoursList",
                                children=[
                                    CreateTabCoursList(),
                                    CreateTabCoursCreation(),
                                ]),

                            ],width=8),
                        ])
                    ])
                ])


def CreateTabCoursList():
    return dcc.Tab(

                id="Tab-CoursList",

                label="List",

                value="Tab-CoursList",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',
                style={"height":"100%"},

                children=[
                        html.Div(
                            className='card border-primary mb-3',
                            children=[

                                html.Div(
                                    # id='StudentInfo',
                                    className='card border-primary mb-3',
                                    children=[
                                        html.Div(className='card-header',
                                        children=[
                                            html.Div('Student Info')
                                        ]),
                                        html.Div(className='card-body',
                                        children=[
                                            # dcc.Input(id='StudentInfoId',className="form-control",type="text",value="",size="30",placeholder="StudentInfoId"),
                                            # dcc.Input(id='StudentInfoNom',className="form-control",type="text",value="",size="30",placeholder="StudentInfoNom"),
                                            # dcc.Input(id='StudentInfoPrenoms',className="form-control",type="text",value="",size="30",placeholder="StudentInfoPrenoms"),
                                            html.Div(id='StudentInfo'),

                                            # html.Div(style={"height":"5px"}),
                                            # html.Button("Modify",id="ModifStudentButton",n_clicks=0,className='btn btn-lg btn-warning',style={"min-height":"20px","max-width":"300px"}),
                                            # html.Button("Delete",id="DeleteStudentButton",n_clicks=0,className='btn btn-lg btn-danger',style={"min-height":"20px","max-width":"300px"}),

                                            html.Button("Get Cours",id="GetCoursButton",n_clicks=0,className='btn btn-lg btn-info',style={"min-height":"20px","max-width":"300px"}),

                                        ])
                                    ]),
                                
                                    # dcc.RadioItems(id="CurrentCoursId",
                                    # style={"width":"50%"},
                                    # className="form-check",
                                    # inputClassName='form-check-input',
                                    # labelClassName='form-check-label',
                                    # options=[{"label":"New","value":-1}],
                                    # value=-1
                                    # )

                                    html.Div(style={"height":"50px"}),
                                    html.Div(id='ListCours'),

                            ])

                ])

def CreateTabCoursCreation():
    return dcc.Tab(

                    id="Tab-CoursCreation",

                    label="Create",

                    className=" nav-link  active tab-pane show",

                    selected_className='tab-pane fade active show',

                    children=[

                        html.Div(
                            id='CoursInfo',
                            className='card border-primary mb-3',
                            children=[

                                    dcc.Input(id='CoursId',className="form-control",type="text",value="-1",size="30",placeholder="Id"),
                                    dcc.DatePickerSingle(
                                        id='CoursDate',
                                        min_date_allowed=date(1900, 1, 1),
                                        max_date_allowed=date(2100, 1, 1),
                                        initial_visible_month=date(2022, 1, 1),
                                        date= today# date(2017, 8, 25)
                                    ),
                                    dcc.Input(id='CoursStudentId',disabled=True,className="form-control",type="text",value="",size="30",placeholder="StudentId"),
                                    dcc.Input(id='CoursNHourReal',className="form-control",type="text",value="",size="30",placeholder="NHourReal"),
                                    dcc.Input(id='CoursNHourFacturee',className="form-control",type="text",value="",size="30",placeholder="NHourFacturee"),
                                    # dcc.Input(id='CoursSurPlace',className="form-control",type="text",value="",size="30",placeholder="SurPlace"),
                                    html.Label('Sur place :'),
                                    dcc.Dropdown(id='CoursSurPlace',className="form-control",value="Yes",
                                        options=['Yes','No']),

                                    dcc.Input(id='CoursNHourPreparation',className="form-control",type="text",value="",size="30",placeholder="NHourPreparation"),
                                    # dcc.Input(id='CoursNiveau',className="form-control",type="text",value="",size="30",placeholder="Niveau"),
                                    dcc.Dropdown(id='CoursNiveau',className="form-control",value="Terminal",
                                        options=["Pass","L3",'L2','L1',"Terminal","Premiere","Seconde","3e","4e","5e","6e"]),

                                    dcc.Input(id='CoursHourPriceHT',className="form-control",type="text",value="",size="30",placeholder="HourPriceHT"),

                                    html.Div(style={"height":"50px"}),
                                    html.Button("Create",id="CreateCoursButton",n_clicks=0,className='btn btn-lg btn-info',style={"min-height":"20px","max-width":"300px"}),
                                    html.Button("Modify",id="ModifCoursButton",n_clicks=0,className='btn btn-lg btn-warning',style={"min-height":"20px","max-width":"300px"}),
                                    html.Button("Delete",id="DeleteCoursButton",n_clicks=0,className='btn btn-lg btn-danger',style={"min-height":"20px","max-width":"300px"}),
                                    html.Div(style={"height":"5px"}),
                            
                            ])
                    ]
    )  



def CreateLayoutTab_Config(Config):

    return dcc.Tab(

                id="Tab-Config",

                label="Config",

                className=" nav-link  active tab-pane show",

                selected_className='tab-pane fade active show',

                children=[

                    html.Div(style={"height":"30px"}),

                    html.Div(
                        id='Config',
                        className='card border-primary mb-3',
                        style={"width":"80%"},
                        children=[
                            html.Div(className='card-header',
                            children=[
                                html.Div('Config Facture')
                            ]),
                            html.Div(className='card-body',
                            children=[

                            html.Div(style={"height":"25px"}),

                            html.Label("Next Facture Number"),
                            dcc.Input(id='NextNumFacture',className="form-control",type="text",value=Config['StartNextNumFacture'],size="30",placeholder="NumFacture to be created"),
                            html.Div(style={"height":"15px"}),

                            html.Label("TVA in %"),
                            dcc.Input(id='TVAvalue',className="form-control",type="text",value=0,size="30",placeholder="TVA to be applied"),
                            html.Div(style={"height":"15px"}),

                            ]
                            )

                        ])
                ])


def GetTotalLayout(Config=None):#figs):

 

    PiranhaLogo='pngegg'+str(np.random.randint(0,23))


    PiranhaFunFacts='assets/Piranhas/Funfacts.txt'

 
 

    try :

        Config_Version = str(Config['Version'])

        Config_Version_classname =""

        if not Config['Release']:

            Config_Version_classname = "text-warning"

        else:

            Config_Version_classname = "text-info"

    except Exception:

        Config_Version = " ??? "

        Config_Version_classname = "text-danger"

       

 
   

    return html.Div(

        style={"width":"99%"},  # to not have horizontal scroll bar in full screen. chercher comment faire autrement

        children=[

 

        dbc.Alert(id='API_response_success',

                    children=[

                        "Good job !",

                    ],

                    dismissable=True,

                    fade=True,

                    is_open=False,

                    duration=4000,

                    color="success",

                    style={"position":"fixed","top":"0",'zIndex':'10000'},

                   

                    ),

        dbc.Alert(id='API_response_fail',

                    children=[

                        'Ouch !',

                    ],

                    dismissable=True,

                    fade=True,

                    is_open=False,

                    duration=4000,

                    color="danger",

                    style={"position":"fixed","top":"0",'zIndex':'10000'},

 

                    ),

        dbc.Alert(id='API_response_warning',

                    children=[

                        'Carefull !',

                    ],

                    dismissable=True,

                    fade=True,

                    is_open=False,

                    duration=4000,

                    color="warning",

                    style={"position":"fixed","top":"0",'zIndex':'10000'},

 

                    ),

        dbc.Row([

            dbc.Col([

                dbc.Row([

                ])
            ])
        ]),


        dcc.Tabs(id="Tabs",value="TabFactures",
                className='nav-item',
                parent_className='nav nav-tabs',
                children=[
                    CreateLayoutTab_Clients(),
                    CreateLayoutTab_Cours(),
                    CreateLayoutTab_Factures(Config),
                    CreateLayoutTab_Config(Config),
                ]),
 


        dcc.Store(
            id="CurrentPrestasSelectedToFacture",
            storage_type="memory",
            data={}
        )

        ])

 