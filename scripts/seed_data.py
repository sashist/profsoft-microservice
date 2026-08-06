#!/usr/bin/env python3
import json
import time
import urllib.request

BASE_URL = "http://localhost:8000"

SAMPLE_DOCUMENTS = [
    {
        "source": "wiki://hr-vacation-policy",
        "text": (
            "Положение об отпусках и больничных в компании TechCorp:\n"
            "1. Ежегодный оплачиваемый отпуск составляет 28 календарных дней. "
            "Отпуск можно делить на части, одна из которых не менее 14 дней.\n"
            "2. Заявление подается в личный кабинет за 14 дней до начала.\n"
            "3. Отпускные выплачиваются за 3 рабочих дня до начала отпуска."
        ),
    },
    {
        "source": "wiki://it-equipment-guide",
        "text": (
            "Порядок выдачи и обслуживания IT-оборудования:\n"
            "1. Ноутбуки и мониторы выдаются IT-отделом (кабинет 204) по будням с 10:00 до 17:00.\n"
            "2. При поломке создается тикет в Jira Service Desk в разделе IT Helpdesk.\n"
            "3. Замена техники при неисправности производится в течение 4 рабочих часов."
        ),
    },
    {
        "source": "wiki://security-pass-access",
        "text": (
            "Правила безопасности и пропускного режима:\n"
            "1. Доступ в офис осуществляется по электронным бейджам.\n"
            "2. При утере карты нужно заблокировать ее в приложении и вызвать бюро пропусков (тел. 1024).\n"
            "3. Заявка на гостей подается за 2 часа через бота @TechCorpGuestBot."
        ),
    },
    {
        "source": "wiki://remote-work-regulations",
        "text": (
            "Регламент удаленной работы:\n"
            "1. Сотрудники могут работать удаленно до 3 дней в неделю.\n"
            "2. Обязательное присутствие в офисе требуется по вторникам (Sync Tuesday).\n"
            "3. Компания компенсирует расходы на связь и интернет в размере 2500 рублей в месяц."
        ),
    },
]


def seed_documents():
    print("Posting sample documents to microservice...")
    created_ids = []

    for doc in SAMPLE_DOCUMENTS:
        req = urllib.request.Request(
            f"{BASE_URL}/documents/",
            data=json.dumps(doc).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                created_ids.append(data["id"])
                print(f"Created document ID {data['id']}: {doc['source']}")
        except Exception as err:
            print(f"Failed to post {doc['source']}: {err}")

    print("\nWaiting for indexing worker...")
    time.sleep(5)

    print("\nDocument status:")
    for doc_id in created_ids:
        try:
            with urllib.request.urlopen(f"{BASE_URL}/documents/{doc_id}") as resp:
                data = json.loads(resp.read().decode("utf-8"))
                print(f"  Document {data['id']} ({data['source']}): {data['status']}")
        except Exception as err:
            print(f"  Document {doc_id}: Error ({err})")


if __name__ == "__main__":
    seed_documents()
