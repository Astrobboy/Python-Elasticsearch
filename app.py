import json
from flask import Flask, request, render_template, make_response
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
#from elasticsearch_dsl.query import MultiMatch, Match


es = Elasticsearch()
s = Search(using=es)
app = Flask(__name__)

#funcion que verifica si consulto en alguna consola en especifica
def lim_text(text):
    consolas = ["xbox one", "xbox 360", "ps4", "ps3", "ps2", "wii", "wii u", "ps vita", "switch", "3ds", "games"]
    juegos = ''
    cont = 0
    for consola in consolas:
        if text.lower().find(consola) != -1:
            cont += 1
            juegos =  juegos+ " " + consola
    return (juegos, cont)

def convert_data(array_cambiar):
    array = [] #será el nuevo array que se mostrara, bien estructurado como la vista fue diseñada
    control = 2 #numero de control, luego se le sumara constantemente 3, para validar la carga de 3 objetos dentro de un objeto
      
    for i in range(0, len(array_cambiar)):
        if (i == control):
            #carga de 3 objetos dentro de un nuevo objeto
            #que será un nuevo ítem dentro del array
            array.append({
                'archi1': array_cambiar[i - 2],
                'archi2': array_cambiar[i - 1],
                'archi3': array_cambiar[i]
            })
            control = control + 3
        else :
            #consulta si quedán 2 objetos, si, si los almacena y sale
            if ((len(array_cambiar) - i) == 2):
                array.append({
                    'archi1': array_cambiar[i],
                    'archi2': array_cambiar[i + 1]
                })
                return array
            else:
                #consulta si queda 1 objeto, si, si los almacena y sale
                if ((len(array_cambiar) - i) == 1):
                    array.append({
                        'archi1': array_cambiar[i]
                    })
                    return array
    return array


@app.route("/")
def hello():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <style>
                * {box-sizing: border-box;}

                body {
                margin: 0;
                font-family: Arial, Helvetica, sans-serif;
                }

                .topnav {
                overflow: hidden;
                background-color: #e9e9e9;
                }

                .topnav a {
                float: left;
                display: block;
                color: black;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
                font-size: 17px;
                }

                .topnav a:hover {
                background-color: #ddd;
                color: black;
                }

                .topnav a.active {
                background-color: #2196F3;
                color: white;
                }

                .topnav .search-container {
                float: right;
                }

                .topnav input[type=text] {
                padding: 6px;
                margin-top: 8px;
                font-size: 17px;
                border: none;
                }

                .topnav .search-container button {
                float: right;
                padding: 6px 10px;
                margin-top: 8px;
                margin-right: 16px;
                background: #ddd;
                font-size: 17px;
                border: none;
                cursor: pointer;
                }

                .topnav .search-container button:hover {
                background: #ccc;
                }

                @media screen and (max-width: 600px) {
                .topnav .search-container {
                    float: none;
                }
                .topnav a, .topnav input[type=text], .topnav .search-container button {
                    float: none;
                    display: block;
                    text-align: left;
                    width: 100%;
                    margin: 0;
                    padding: 14px;
                }
                .topnav input[type=text] {
                    border: 1px solid #ccc;  
                }
                }
            </style>
        </head>
        <body>
            <div class="topnav">
            <a class="active" href="#home">Home</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
            <div class="search-container">
                <form action="/buscar" method="post">
                    <input type="text" placeholder="Search.." name="search">
                    <button type="submit"><i class="fa fa-search"></i></button>
                </form>
            </div>
            </div>

        </body>
        </html>
    """


@app.route("/as", methods=['POST', 'GET'])
def ats():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        params = request.form['search']
        s = Search().using(es).query(
            "multi_match", query=params, fields=['title', 'console'])
        res = s.execute()
        print(res)
        obj = []
        x = 0
        for i in res:
            print(i)
            obj.append({
                "title": res[x]["title"],
                "console": res[x]["console"],
                "description": res[x]["description"],
                "price": res[x]["price"],
            })
            x += 1
        return render_template('index.html', resultado=json.dumps(obj))


@app.route("/buscar", methods=['POST', 'GET'])
def buscarats():
    #devuelve el index
    if request.method == 'GET':
        return render_template('index2.html')
    else:
        br = False #variable de validacion
        params = request.form['search']
        print(lim_text(params))
        consolas, cont = lim_text(params)
        #ver como hacer funcionar para buscar solo dentro de dos index
        #condiciones para ver dentro de que consola va a buscar, si no cumple busca de forma general
        if consolas.lower().find('xbox one') != -1:
            res = es.search(
            index="juego_xbox_one",
            doc_type="xbox_one",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})

        elif consolas.lower().find('xbox 360') != -1:
            res = es.search(
            index="juego_xbox_360",
            doc_type="xbox_360",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})

        elif consolas.lower().find('ps4') != -1:
            res = es.search(
            index="juego_ps4",
            doc_type="ps4",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})

        elif consolas.lower().find('ps3') != -1:
            res = es.search(
            index="juego_ps3",
            doc_type="ps3",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})

        elif consolas.lower().find('ps2') != -1:
            res = es.search(
            index="juego_ps2",
            doc_type="ps2",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})

        elif consolas.lower().find('wii') != -1:
            res = es.search(
            index="juego_wii",
            doc_type="wii",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})


        elif consolas.lower().find('wii u') != -1:
            res = es.search(
            index="juego_wii_u",
            doc_type="wii_u",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})

        elif consolas.lower().find('ps vita') != -1:
            res = es.search(
            index="juego_ps_vita",
            doc_type="ps_vita",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})
        
        elif consolas.lower().find('switch') != -1:
            res = es.search(
            index="juego_switch",
            doc_type="switch",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})
        
        elif consolas.lower().find('3ds') != -1:
            res = es.search(
            index="juego_3ds",
            doc_type="3ds",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})
        elif consolas.lower().find('games') != -1:
            res = es.search(
            index="juego_games",
            doc_type="games",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})
        else:
            s = Search().using(es).query(
                "multi_match", query=params, fields=['title', 'console'])
            res = s.execute() 
            br = True

        #variables para alimentar la vista
        obj = []
        titles = []
        if br:#si es verdadero busca de forma gral
            num = 0
            for i in res:
                obj.append({
                    "title": res[num]["title"],
                    "console": res[num]["console"],
                    "description": res[num]["description"],
                    "price": res[num]["price"],
                })
                titles.append(res[num]["title"])
                num += 1
        else:#si no en alguna ruta especifica
            x = len(res["hits"])
            print(x)
            i = 0
            #print(res["hits"]["hits"])
            while i < int(x):
                obj.append({
                    "title": res["hits"]["hits"][i]["_source"]["title"],
                    "console": res["hits"]["hits"][i]["_source"]["console"],
                    "description": res["hits"]["hits"][i]["_source"]["description"],
                    "price": res["hits"]["hits"][i]["_source"]["price"],
                })
                titles.append(res["hits"]["hits"][i]["_source"]["title"])
                i += 1
                

        return render_template('index2.html', resultado=json.dumps(obj), titles = titles)
        """
        xbox = params.find('xbox')
        ps4 = params.find('xbox')
        if xbox != -1 and ps4 != -1:
            jogos = True
        elif xbox != -1:
            res = es.search(index="test-index", body={"query": {"match_all": {}}})
        
        res = es.search(
            index="juegops4",
            doc_type="ps4",
            body={"query": {
                "multi_match": { "query": params, "fields":['title', 'console']}
            }})
        #print(type(res["hits"]["hits"][0]))
        #print(res["hits"]["hits"][0]["_source"])

        obj = []
        x = res["hits"]["total"]
        i = 0
        while i < int(x):
            print(i)
            obj.append({
                "title": res["hits"]["hits"][i]["_source"]["title"],
                "console": res["hits"]["hits"][i]["_source"]["console"],
                "description": res["hits"]["hits"][i]["_source"]["description"],
                "price": res["hits"]["hits"][i]["_source"]["price"],
            })
            i += 1
        print(obj)
        """







@app.route("/buscar2", methods=['POST'])
def buscar():
    if request.method == 'POST':
        params = request.form['search']

        """
        s = Search().using(es).query({"match": {"title": params}})
        res= s.execute()
        print(res)
        """
        s = Search().using(es).query(
            "multi_match", query= params, fields=['title', 'console'])
        res= s.execute()
        print(res)
        obj = []
        x = 0
        for i in res:

            print(i)
            obj.append({
                "title":res[x]["title"],
                "console": res[x]["console"],
                "description": res[x]["description"],
                "price": res[x]["price"],
            })
            x+=1
        #Match(title={"query": "jogo", "type": "phrase"})


        """
        res = es.search(
            index="juego", doc_type="juego", body={
            "query": {
                "multi_match": {
                    "fields": ["title", "link_images", "description", "console"],
                    "query": params,
                    "type": "cross_fields",
                    "use_dis_max": False
                }
            },
            "size": 6
            }
        )
        """

        """
        formas de pedir con curl
        curl -XGET http://localhost:9200/juego
        curl -XGET http://localhost:9200/juego/juego/_search?q=ark
        curl -XGET http://localhost:9200/juego/juego/442978

        """
        #print("Got %d Hits:" % res['console']['total'])"
        #return json.dumps(res)
        return json.dumps(obj)



#officiales
@app.route("/todo", methods=['POST', 'GET'])
def todo():
    if request.method == 'POST':
        params = request.get_json()['text']
        #print (params)
        consoles = ["juego_xbox_one", "juego_xbox_360", "juego_ps4", "juego_ps3", "juego_ps2", "juego_switch", "juego_3ds", "juego_ps_vita", "juego_wii", "juego_wii_u", "juego_games"]
        #params = "mortal"
        s = es.search(index = consoles, body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else: 
        consoles = ["juego_xbox_one", "juego_xbox_360", "juego_ps4", "juego_ps3", "juego_ps2", "juego_switch", "juego_3ds", "juego_ps_vita", "juego_wii", "juego_wii_u", "juego_games"]
        params = "jogo"
        s = es.search(index = consoles, body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))

@app.route("/xboxone", methods=['POST', 'GET'])
def xboxone():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_xbox_one", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else:
        s = es.search(index="juego_xbox_one", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))

@app.route("/xbox360", methods=['POST', 'GET'])
def xbox360():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_xbox_360", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else: 
        s = es.search(index="juego_xbox_360", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))



@app.route("/ps4", methods=['POST', 'GET'])
def ps4():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_ps4", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else:    
        s = es.search(index="juego_ps4", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        #res= s.execute()
        #print(s)
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))


@app.route("/ps3", methods=['POST', 'GET'])
def ps3():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_ps3", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else:  
        s = es.search(index="juego_ps3", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))

@app.route("/ps2", methods=['POST', 'GET'])
def ps2():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_ps2", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else:  
        s = es.search(index="juego_ps2", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))


@app.route("/switch", methods=['POST', 'GET'])
def switch():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_switch", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else:  
        s = es.search(index="juego_switch", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))


@app.route("/ds3", methods=['POST', 'GET'])
def ds3():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_3ds", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else:  
        s = es.search(index="juego_3ds", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))

@app.route("/psvita", methods=['POST', 'GET'])
def psvita():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_ps_vita", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else: 
        s = es.search(index="juego_ps_vita", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))

@app.route("/wii", methods=['POST', 'GET'])
def wii():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_wii", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else:  
        s = es.search(index="juego_wii", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))

@app.route("/wiiu", methods=['POST', 'GET'])
def wiiu():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_wii_u", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else:  
        s = es.search(index="juego_wii_u", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

        return make_response(json.dumps(array))

        
@app.route("/games", methods=['POST', 'GET'])
def games():
    if request.method == 'POST':
        
        params = request.get_json()['text']
        s = es.search(index="juego_games", body={ 'from': 0, 'size':1500, "query": {"multi_match": { "query": params }}})
        array = convert_data(s["hits"]["hits"])
        print (array)
        #array = {"hola": "hola"}
        return make_response(json.dumps(array))
    else:  
        s = es.search(index="juego_games", body={ 'from': 0, 'size':1000, "query": {"match_all": {}}})
        array = convert_data(s["hits"]["hits"])

    return make_response(json.dumps(array))    


"""
@app.route("/buscar", methods=['POST', 'GET'])
def buscar():
    res = es.search(index="juego", doc_type="juego", body={"query": {"match_all": {}}})
    print (res)
    #print("Got %d Hits:" % res['console']['total'])"
    return json.dumps(res)
"""



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)





"""
el real que funciona
s = Search().using(es).query(
    "multi_match", query=params, fields=['title', 'console'])
res = s.execute()

obj = []
x = 0
for i in res:
    print(i)
    obj.append({
        "title": res[x]["title"],
        "console": res[x]["console"],
        "description": res[x]["description"],
        "price": res[x]["price"],
    })
    x += 1
return render_template('index2.html', resultado=json.dumps(obj))
"""

#CARS 3 games
#LACRIMOSA OF PS VITA
#ACE COMBAT WII
#007 LEGENDS WII U
#ARMS SWITCH
#7TH DRAGON III 3DS
#7 DAYS TO DIE PS4
#ACE COMBAT ASSAULT HORIZON PS3
#SYPHONFILTER DARK MIRROR PS2
# 7 DAYS TO DIE XBOX ONE
#ALICE MADNESS RETURN XBOX 360
