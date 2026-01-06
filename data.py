class Monster:
    def __init__ (self, monster_id: int, name: str, size: str, type_: str):
        self.monster_id = monster_id
        self.name = name
        self.size = size
        self.type_ = type_
        
    def get_info(self):
        return {
            "MonsterID": self.monster_id,
            "Name": self.name,
            "Size": self.size,
            "Type": self.type_
        }
    
    def some_method(self):
        pass

    def __str__(self):
        return f"Monster: {self.name} (id: {self.monster_id}, size: {self.size}, type: {self.type_})"



