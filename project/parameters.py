from project.structures import KWGroups, max_ed

# kw -> keywords
akw = KWGroups({"dom"}, None)  # akw -> activate kw
ekw = KWGroups({"proszę"}, None)  # ekw -> end kw

off_id = 0
on_id = 1
toggle_id = 2
up_id = 3
down_id = 4
set_id = 5

off_kw = KWGroups(["wyłącz", "wstrzymaj", "odłącz", "zgaś"], off_id)
on_kw = KWGroups(["załącz", "uruchom", "włącz", "zapal", "odpal", "zaświeć"], on_id)
up_kw = KWGroups(["podgłośnij"], up_id)
down_kw = KWGroups(["przyczisz", "zcisz"], down_id)
set_kw = KWGroups(["zmień", "przestaw", "zamień", "przełącz", "ustaw", "wybierz"], set_id)

things_to_set_kw = KWGroups(["głośność", "kanał", "budzenie", "kolor"], None)
for_kw = KWGroups(["na"], None)

all_kw_groups = [off_kw, on_kw, set_kw]
