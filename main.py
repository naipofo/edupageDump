"""Simple module to dump school schedule"""
import json
import requests

def main():
    """main"""
    school_name = input("School name?")

    def edu_rcp(endpoint: str, args: str) -> dict:
        return json.loads(
            requests.post(
                f"https://{school_name}.edupage.org/timetable/server/{endpoint}",
                timeout=3000,
                data='{"__args":' + args + ',"__gsh":"00000000"}',
            ).text
        )

    tt_number = edu_rcp("ttviewer.js?__func=getTTViewerData", "[null,2022]")["r"][
        "regular"
    ]["default_num"]

    tables = dict(
        (table["id"], dict((value["id"], value) for value in table["data_rows"]))
        for table in edu_rcp(
            "regulartt.js?__func=regularttGetData", '[null,"' + tt_number + '"]'
        )["r"]["dbiAccessorRes"]["tables"]
    )
    for c in tables["classes"].values():
        print(c["id"] + " - " + c["name"])

    class_id = "*" + input("class id?")

    for card, lesson in sorted(
        (
            (x, tables["lessons"][x["lessonid"]])
            for x in tables["cards"].values()
            if class_id in tables["lessons"][x["lessonid"]]["classids"]
        ),
        key=lambda d: d[0]["days"] + str(10 - int(d[0]["period"])),
        reverse=True,
    ):
        week = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek"][
            card["days"].index("1")
        ]
        print(
            week
            + " lekcja "
            + card["period"]
            + " - "
            + str(tables["subjects"][lesson["subjectid"]]["name"])
        )


if __name__ == "__main__":
    main()
