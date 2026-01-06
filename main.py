from database import Database


def main():
    db = Database()

    # Søg efter et monster
    term = "Rath"
    print(f"Søger efter '{term}':")
    results = db.search(term)
    print([m.get_info() for m in results])

    # Indsæt et nyt monster (kun eksempel – kan fejle hvis ID allerede findes)
    ok = db.insert(5, "Test Beast", "Large", "Elder")
    print("Indsat nyt monster:", ok)

    # Hent et specifikt monster
    m = db.load(5)
    print("\nMonster 5:", m.get_info() if m else None)

    # Hent alle monsters
    all_monsters = db.load_all()
    print(f"\nAntal monsters: {len(all_monsters)}")
    print([m.get_info() for m in all_monsters[:5]])

    db.delete(5)
    db.update(1, name="Updated Name")

    all_monsters = db.load_all()
    print(f"\nAntal monsters: {len(all_monsters)}")
    print([m.get_info() for m in all_monsters[:5]])

if __name__ == '__main__':
    main()