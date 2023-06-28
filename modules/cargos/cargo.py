def adiciona_cargo(member, cargo_id):
    """Adiciona cargo ao membro via ID. Retorna membro com o cargo adicionado.
    
    :param member: discord.class
    :param cargo_id: int
    
    :return discord.class member.add_roles()
    """

    guilda = member.guild
    cargo = guilda.get_role(cargo_id)

    return member.add_roles(cargo)

def remove_cargo(member, cargo_id):
    """Remove cargo do membro via ID. Retorna membro com o cargo removido.
    
    :param member: discord.class
    :param cargo_id: int
    
    :return discord.class member.remove_roles()
    """

    guilda = member.guild
    cargo = guilda.get_role(cargo_id)

    return member.remove_roles(cargo)
