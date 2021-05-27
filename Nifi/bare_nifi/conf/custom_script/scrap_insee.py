import requests
import urllib.parse
import re
import sys


def scrap_insee(argv):
    """
    Scrap data from Insee website
    :param argv: first: url with query data (string), ex : https://www.insee.fr/fr/statistiques?q=iris+logement&taille=10000&debut=0&theme=7&categorie=3
                second: filter based on 'titre' field from the answer (regex), ex : logement en 2...|mayotte
    :return: Return list of downloadable links on sys.stdout
    """
    if len(argv) > 1:
        url = argv[1]
        # Hard coded link to Insee server:
        url2 = 'https://www.insee.fr/fr/solr/consultation?q={q}'
        document_url = 'https://www.insee.fr/fr/statistiques/{id}'

        # parse the query (url provided)
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        json_payload = {"q": params['q'][0], "start": "00", "sortFields": [{"field": "score", "order": "desc"}],
                        "filters": [{"field": "themeId", "tag": "tagThemeId", "values": params['theme']},
                                    {"field": "categorieId", "tag": "tagCategorieId", "values": params['categorie']},
                                    {"field": "rubrique", "tag": "tagRubrique", "values": ["statistiques"]},
                                    {"field": "diffusion", "values": [True]}], "rows": "10000", "facetsQuery": []}
        # Request the datas from the query
        data = requests.post(url2.format(q=params['q'][0]), json=json_payload).json()
        output = ""
        # For each data apply the filter
        for document in data['documents']:
            if re.match(argv[2], document['titre'].lower()):
                output += document_url.format(id=document['id']) + '\n'
        return output

    else:
        print("provide an valid url")
        return None


if __name__ == '__main__':
    print(scrap_insee(sys.argv))