import json

from flask import Flask, render_template, request

app = Flask(__name__)


def read_entities():
        with open('entities.json', encoding='utf-8') as f:
            entities = json.load(f)
            number_of_pages = int(round(len(entities)/3 + 0.5))
            return entities, number_of_pages


# def list_entities_id():
#     entities_id_list = []
#     for item in entities:
#         entities_id_list.append(item['id'])
#     return sorted(entities_id_list)


entities, number_of_pages = read_entities()
# entities_id_list = list_entities_id()


@app.route('/')
def index():
    if request.args.get('page'):
        page_to_show = int(request.args.get('page'))
        if number_of_pages == page_to_show:
            entities_to_show = entities[page_to_show*3-3:]
        else:
            entities_to_show = entities[page_to_show*3-3:page_to_show*3]
        return render_template("main-all-items.html",
                               entities=entities_to_show, page_to_show=page_to_show, number_of_pages=number_of_pages)
    entities_to_show = entities[0:3]
    return render_template("main-all-items.html",
                           entities=entities_to_show, page_to_show="1", number_of_pages=number_of_pages)

@app.route('/paging')
def paging():
    return render_template("main.html")


@app.route('/search')
def search():
    model = request.args.get('model')
    response = []
    print(model, 'model')
    if not model:
        response = entities
    else:
        model_list = model.split()
        print(model_list,'model_list')
        for e in entities:
            if e["model"] == model:
                response.append(e)
            elif e["model"] == model_list[0]:
                response.append(e)
            elif len(model_list) > 1:
                if e["model"] == model_list[1]:
                    response.append(e)
    return render_template("search_ause.html", entities=response)


@app.route('/card/<int:eid>')
def card(eid: int):
    for ent in entities:
        if ent["id"] == eid:
            return render_template("card_full.html", entity=ent)

@app.route('/short-card/<int:eid>')
def card_short(eid: int):
    for ent in entities:
        if ent["id"] == eid:
            return render_template("card_short.html", entity=ent)

if __name__ == '__main__':
    app.run(debug=True)
