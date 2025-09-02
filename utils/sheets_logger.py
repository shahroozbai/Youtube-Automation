import json
import os
from typing import Sequence

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

class SheetsLogger:
    def __init__(self, sheet_id: str, tab: str = "Sheet1"):
        raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not raw:
            raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON env var")
        info = json.loads(raw)
        creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        self.service = build("sheets", "v4", credentials=creds)
        self.sheet_id = sheet_id
        self.tab = tab

    def ensure_tab(self, title: str):
        try:
            meta = self.service.spreadsheets().get(spreadsheetId=self.sheet_id).execute()
            titles = {s["properties"]["title"] for s in meta.get("sheets", [])}
            if title in titles:
                return
            body = {"requests": [{"addSheet": {"properties": {"title": title}}}]}
            self.service.spreadsheets().batchUpdate(spreadsheetId=self.sheet_id, body=body).execute()
        except HttpError as e:
            raise

    def append_row(self, values: Sequence):
        self.ensure_tab(self.tab)
        body = {"values": [list(values)]}
        return self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range=f"{self.tab}!A1",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()
