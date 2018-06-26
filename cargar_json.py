import json
from datetime import datetime
from elasticsearch import Elasticsearch



es = Elasticsearch([{'host': '10.10.10.35', 'port': 9200}])
#lee el json del archivo local
juegos = json.loads(open('productos_games.json').read())

#variables para tener una cuenta de tipo de consolas
contxbox_one = 0
contxbox_360 = 0
contps3 = 0
contps2 = 0
contps4 = 0
contswitch = 0
contps_vita = 0
cont3ds = 0
contwii = 0
contwii_u = 0
contgames = 0

#para ver que cantidad total hay
#print(len(juegos.keys()))

i = 0
for key in juegos.keys():
    #condiciones para que guarde dentro de su respectiva ruta de consola
    if juegos[key]["console"].lower() == 'xbox one':
        contxbox_one += 1
        res = es.index(
            index="juego_xbox_one",
            doc_type="xbox_one",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })
    elif juegos[key]["console"].lower() == 'xbox 360':
        contxbox_360 += 1
        res = es.index(
            index="juego_xbox_360",
            doc_type="xbox_360",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })
    elif juegos[key]["console"].lower() == 'ps4':
        contps4 += 1
        res = es.index(
            index="juego_ps4",
            doc_type="ps4",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })
    elif juegos[key]["console"].lower() == 'ps3':
        contps3 += 1
        res = es.index(
            index="juego_ps3",
            doc_type="ps3",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })
    elif juegos[key]["console"].lower() == 'ps2':
        contps2 += 1
        res = es.index(
            index="juego_ps2",
            doc_type="ps2",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })
    elif juegos[key]["console"].lower() == 'wii':
        contwii += 1
        res = es.index(
            index="juego_wii",
            doc_type="wii",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })

    elif juegos[key]["console"].lower() == 'wii u':
        contwii_u += 1
        res = es.index(
            index="juego_wii_u",
            doc_type="wii_u",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })

    elif juegos[key]["console"].lower() == 'switch':
        contswitch += 1
        res = es.index(
            index="juego_switch",
            doc_type="switch",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })

    elif juegos[key]["console"].lower() == '3ds':
        cont3ds += 1
        res = es.index(
            index="juego_3ds",
            doc_type="3ds",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })
    elif juegos[key]["console"].lower() == 'ps vita':
        contps_vita += 1
        res = es.index(
            index="juego_ps_vita",
            doc_type="ps_vita",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })
    elif juegos[key]["console"].lower() == 'games':
        contgames += 1
        res = es.index(
            index="juego_games",
            doc_type="games",
            id=key,
            body={
                "title": juegos[key]["title"],
                "console": juegos[key]["console"],
                "description": juegos[key]["description"],
                "link_images": juegos[key]["link_images"],
                "price": juegos[key]["price"],
                "stock": juegos[key]["stock"]
            })



#impresiones para terner un mejor control
print("cont games= "+str(contgames))
print("cont xbox_one= "+str(contxbox_one))
print("cont xbox_360= "+str(contxbox_360))
print("cont ps3= "+str(contps3))
print("cont ps2= "+str(contps2))
print("cont ps4= "+str(contps4))
print("cont switch= "+str(contswitch))
print("cont ps_vita= "+str(contps_vita))
print("cont 3ds= "+str(cont3ds))
print("cont wii= "+str(contwii))
print("cont wii_u= "+str(contwii_u))
total = contgames + contxbox_one + contxbox_360 + contps3 + contps4 + contps2 + contps_vita + contswitch + cont3ds + contwii + contwii_u
print("total = "+str(total))
print("termine")


#print (len(juegos.keys()))

#para borrar un index
#es.indices.delete(index='carrera', ignore=[400, 404])
#es.indices.delete(index='accion', ignore=[400, 404])



#res = es.get(index="accion", doc_type='juego', id=443142)
#print (res)
#res = es.get(index="carrera", doc_type='juego', id=442978)
#print (res)
