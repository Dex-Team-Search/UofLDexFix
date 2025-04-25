from pathlib import Path

def generate_ldif(output_file="generated-nested-groups.ldif"):
    base_dn = "dc=example,dc=org"
    ldif_output = []

    # creating Organizational Units
    ldif_output += [
        f"dn: ou=People,{base_dn}",
        "objectClass: organizationalUnit",
        "ou: People",
        "",
        f"dn: ou=Groups,{base_dn}",
        "objectClass: organizationalUnit",
        "ou: Groups",
        ""
    ]

    def add_user(uid, cn, sn, password):
        dn = f"uid={uid},ou=People,{base_dn}"
        ldif_output.extend([
            f"dn: {dn}",
            "objectClass: top",
            "objectClass: person",
            "objectClass: organizationalPerson",
            "objectClass: inetOrgPerson",
            f"cn: {cn}",
            f"sn: {sn}",
            f"uid: {uid}",
            f"mail: {uid}@example.org",
            f"userPassword: {password}",
            ""
        ])
        return dn

    def add_group(cn, members):
        dn = f"cn={cn},ou=Groups,{base_dn}"
        ldif_output.extend([
            f"dn: {dn}",
            "objectClass: top",
            "objectClass: groupOfNames",
            f"cn: {cn}",
            *[f"member: {m}" for m in members],
            ""
        ])
        return dn

    # Adding users total  5 users
    users = [add_user(f"user{i}", f"User {i}", f"User{i}", f"password{i}") for i in range(1, 6)]

    # group with no recursion
    add_group("FlatGroup", [users[0]])

    #  recursion with user2 at the base
    prev = add_group("Group10_0", [users[1]])
    for i in range(1, 10):
        prev = add_group(f"Group10_{i}", [prev])

    #  recursion with user3 at the base
    prev = add_group("Group15_0", [users[2]])
    for i in range(1, 15):
        prev = add_group(f"Group15_{i}", [prev])

    # Shared group appearing in multiple parents
    g4 = add_group("Group4", [users[3]])
    g2 = add_group("Group2", [g4])
    g3 = add_group("Group3", [g4])

    #  group referencing both g2 and g3
    g1 = add_group("Group1", [g2, g3])

    # deep chain: from group 100
    prev = add_group("Group100", [users[4]])
    for i in range(101, 201):
        prev = add_group(f"Group{i}", [prev])

    # Saving the file
    Path(output_file).write_text("\n".join(ldif_output))
    print(f" LDIF file generated: {output_file}")

if __name__ == "__main__":
    generate_ldif()
