import logging

from churchtools_api.churchtools_api import ChurchToolsApi

# Pfila Member Fields
PFILA_ID = 462
PFILA_FIELDS = {
    1017: "schulklasse",
    1104: "funktion",
    1020: "notfallkontakt",
    1023: "krankenkasse",
    1026: "privathaftpflicht",
    1029: "hausarzt-adresse-",
    1032: "alergien",
    1035: "medikamente---dosierung",
    1038: "gesundheitszustand",
    1041: "tetanusimpfung-datum",
    1044: "zeckenimpfung-datum",
    1047: "spenden",
    1050: "anmerkung",
    1053: "ich-stimme-den-notfallmassnahmen-zu-",
    1056: "ich-stimme-der-einwilligung-fuer-die-verwendung-von-foto--und",
}

CHILD_FIELDS = {
    496: {
        "schulklasse": "1378",
        "funktion": "1420",
        "notfallkontakt": "1381",
        "krankenkasse": "1384",
        "privathaftpflicht": "1387",
        "hausarzt-adresse-": "1390",
        "alergien": "1393",
        "medikamente---dosierung": "1396",
        "gesundheitszustand": "1399",
        "tetanusimpfung-datum": "1402",
        "zeckenimpfung-datum": "1405",
        "spenden": "1408",
        "anmerkung": "1411",
        "ich-stimme-den-notfallmassnahmen-zu-": "1414",
        "ich-stimme-der-einwilligung-fuer-die-verwendung-von-foto--und": "1417",  
    }, 
    493: {
        "schulklasse": "1333",
        "funktion": "1375",
        "notfallkontakt": "1336",
        "krankenkasse": "1339",
        "privathaftpflicht": "1342",
        "hausarzt-adresse-": "1345",
        "alergien": "1348",
        "medikamente---dosierung": "1351",
        "gesundheitszustand": "1354",
        "tetanusimpfung-datum": "1357",
        "zeckenimpfung-datum": "1360",
        "spenden": "1363",
        "anmerkung": "1366",
        "ich-stimme-den-notfallmassnahmen-zu-": "1369",
        "ich-stimme-der-einwilligung-fuer-die-verwendung-von-foto--und": "1372",
    }, 
    490: {
        "schulklasse": "1288",
        "funktion": "1330",
        "notfallkontakt": "1291",
        "krankenkasse": "1294",
        "privathaftpflicht": "1297",
        "hausarzt-adresse-": "1300",
        "alergien": "1303",
        "medikamente---dosierung": "1306",
        "gesundheitszustand": "1309",
        "tetanusimpfung-datum": "1312",
        "zeckenimpfung-datum": "1315",
        "spenden": "1318",
        "anmerkung": "1321",
        "ich-stimme-den-notfallmassnahmen-zu-": "1324",
        "ich-stimme-der-einwilligung-fuer-die-verwendung-von-foto--und": "1327",
    }, 
    487: {
        "schulklasse": "1243",
        "funktion": "1285",
        "notfallkontakt": "1246",
        "krankenkasse": "1249",
        "privathaftpflicht": "1252",
        "hausarzt-adresse-": "1255",
        "alergien": "1258",
        "medikamente---dosierung": "1261",
        "gesundheitszustand": "1264",
        "tetanusimpfung-datum": "1267",
        "zeckenimpfung-datum": "1270",
        "spenden": "1273",
        "anmerkung": "1276",
        "ich-stimme-den-notfallmassnahmen-zu-": "1279",
        "ich-stimme-der-einwilligung-fuer-die-verwendung-von-foto--und": "1282",
    }, 
    484: {
        "schulklasse": "1198",
        "funktion": "1240",
        "notfallkontakt": "1201",
        "krankenkasse": "1204",
        "privathaftpflicht": "1207",
        "hausarzt-adresse-": "1210",
        "alergien": "1213",
        "medikamente---dosierung": "1216",
        "gesundheitszustand": "1219",
        "tetanusimpfung-datum": "1222",
        "zeckenimpfung-datum": "1225",
        "spenden": "1228",
        "anmerkung": "1231",
        "ich-stimme-den-notfallmassnahmen-zu-": "1234",
        "ich-stimme-der-einwilligung-fuer-die-verwendung-von-foto--und": "1237",
    },
    481: {
        "schulklasse": "1108",
        "funktion": "1150",
        "notfallkontakt": "1111",
        "krankenkasse": "1114",
        "privathaftpflicht": "1117",
        "hausarzt-adresse-": "1120",
        "alergien": "1123",
        "medikamente---dosierung": "1126",
        "gesundheitszustand": "1129",
        "tetanusimpfung-datum": "1132",
        "zeckenimpfung-datum": "1135",
        "spenden": "1138",
        "anmerkung": "1141",
        "ich-stimme-den-notfallmassnahmen-zu-": "1144",
        "ich-stimme-der-einwilligung-fuer-die-verwendung-von-foto--und": "1147",
    },
}

def get_auto_insert_member(api: ChurchToolsApi, group_id: int) -> list:
    members = api.get_group_members(group_id=group_id)
    return  [member["personId"] for member in members if member["comment"] == "Auto Insert"]


def update_child_members(api: ChurchToolsApi, group_id: int, pfila_members: list[dict]) -> None:
    for member in pfila_members:
        logging.info("Updating Child Members: " + member["person"]["title"])
        id_mapping = CHILD_FIELDS[group_id]
        fields = {
            id_mapping[PFILA_FIELDS[item["id"]]]: item["value"]
            for item in member["fields"] if item["id"] in PFILA_FIELDS.keys()
        }
        api.update_group_member(
            group_id=group_id,
            person_id=member["personId"],
            data={
                "comment": "Updated over API",
                "fields": fields,
            },
        )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)


    # Create Session
    from secure.config import ct_token
    from secure.config import ct_domain
    api = ChurchToolsApi(ct_domain, ct_token=ct_token)
    pfila_members = api.get_group_members(group_id=PFILA_ID)
    
    # for each child group
    for group_id in CHILD_FIELDS.keys():
        # check if there is a member with comment "Auto Insert" and get them
        member_ids = get_auto_insert_member(api=api, group_id=group_id)
        # get pfila members where in member_ids
        filtered_pfila_members = [member for member in pfila_members if member["personId"] in member_ids]
        # update the values of the member in the child group
        update_child_members(api=api, group_id=group_id,pfila_members=filtered_pfila_members)
    logging.info("All Child Members are Updated Successfully")
