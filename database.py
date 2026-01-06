import sqlite3
from typing import Optional, List
from data import Monster


DB_FILE = "MHW.db"
TABLE_NAME = "Monsters"

class Database:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self._ensure_table()

    def _connect(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def _execute(self, query: str, params: tuple = ()): 
        conn = self._connect()
        try:
            cur = conn.execute(query, params)
            conn.commit()
            return cur
        finally:
            conn.close()

    def _run_query(self, query: str, params: tuple = ()) -> List[dict]:
        conn = self._connect()
        try:
            cur = conn.execute(query, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def _rows_to_monsters(self, rows: List[dict]) -> List[Monster]:
        return [
            Monster(
                monster_id=r.get("MonsterID"),
                name=r.get("Name"),
                size=r.get("Size"),
                type_=r.get("Type")
            )
            for r in rows
        ]

    def search(self, term: str) -> List[Monster]:
        """Søg efter monsters hvor navn eller ID matcher (delvist)."""
        like = f"%{term}%"
        q = f"SELECT * FROM {TABLE_NAME} WHERE Name LIKE ? OR CAST(MonsterID AS TEXT) LIKE ?"
        rows = self._run_query(q, (like, like))
        return self._rows_to_monsters(rows)
        

    def load(self, monster_id: int) -> Optional[Monster]:
        """Hent et monster efter MonsterID."""
        q = f"SELECT * FROM {TABLE_NAME} WHERE MonsterID = ?"
        rows = self._run_query(q, (monster_id,))
        return self._rows_to_monsters(rows)[0] if rows else None

    def load_all(self) -> List[Monster]:
        """Returnér alle monsters."""
        q = f"SELECT * FROM {TABLE_NAME}"
        rows = self._run_query(q)
        return self._rows_to_monsters(rows)

    def insert(self, uid: int, name: str, size: str, type_: str) -> bool:
        """Indsæt et nyt monster. Returnerer True hvis succes, ellers False."""
        q = f"INSERT INTO {TABLE_NAME} (MonsterID, Name, Size, Type) VALUES (?, ?, ?, ?)"
        try:
            self._execute(q, (uid, name, size, type_))
            return True
        except sqlite3.IntegrityError:
            return False
        
    def _ensure_table(self):
        """Opret Monsters-tabellen hvis den ikke findes."""
        q = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            MonsterID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Size TEXT,
            Type TEXT
        )
        """
        self._execute(q)
    
    def delete(self, monster_id: int) -> bool:
        """Slet et monster efter MonsterID. Returnerer True hvis et monster blev slettet."""
        q = f"DELETE FROM {TABLE_NAME} WHERE MonsterID = ?"
        cur = self._execute(q, (monster_id,))
        return cur.rowcount > 0
    
    def update(self, monster_id: int, name: Optional[str] = None, size: Optional[str] = None, type_: Optional[str] = None) -> bool:
        """Opdater et monsters oplysninger. Returnerer True hvis et monster blev opdateret."""
        fields = []
        params = []
        if name is not None:
            fields.append("Name = ?")
            params.append(name)
        if size is not None:
            fields.append("Size = ?")
            params.append(size)
        if type_ is not None:
            fields.append("Type = ?")
            params.append(type_)
        
        if not fields:
            return False  # Ingen felter at opdatere
        
        params.append(monster_id)
        q = f"UPDATE {TABLE_NAME} SET {', '.join(fields)} WHERE MonsterID = ?"
        cur = self._execute(q, tuple(params))
        return cur.rowcount > 0