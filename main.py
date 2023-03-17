"""Simple module to dump school schedule"""
import json
import requests


def main():
    """main"""
    school_name = input("School name?")
    tables = dict(
        (table["id"], dict((value["id"], value) for value in table["data_rows"]))
        for table in json.loads(
            requests.post(
                f"https://{school_name}.edupage.org/timetable/server/regulartt.js?__func=regularttGetData",
                timeout=3000,
                data='{"__args":[null,"32"],"__gsh":"00000000"}',
            ).text
        )["r"]["dbiAccessorRes"]["tables"]
    )
    for c in tables["classes"].values():
        print(c["id"] + " - " + c["name"])


    class_id = "*"+input("class id?")

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
