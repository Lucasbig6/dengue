import json

# Lists of municipalities per Territory (Standard Piauí Regionalization)

territorios = {
    "Planície Litorânea": [
        "Bom Princípio do Piauí", "Buriti dos Lopes", "Cajueiro da Praia", "Caraúbas do Piauí", 
        "Caxingó", "Cocal", "Cocal dos Alves", "Ilha Grande", "Luís Correia", "Murici dos Portelas", "Parnaíba"
    ],
    "Cocais": [
        "Barras", "Batalha", "Brasileira", "Campo Largo do Piauí", "Domingos Mourão", "Esperantina", 
        "Joaquim Pires", "Joca Marques", "Lagoa de São Francisco", "Luzilândia", "Madeiro", 
        "Matias Olímpio", "Milton Brandão", "Morro do Chapéu do Piauí", "Nossa Senhora dos Remédios", 
        "Pedro II", "Piracuruca", "Piripiri", "Porto", "São João da Fronteira", "São João do Arraial", "São José do Divino"
    ],
    "Carnaubais": [
        "Assunção do Piauí", "Boa Hora", "Boqueirão do Piauí", "Buriti dos Montes", "Cabeceiras do Piauí", 
        "Campo Maior", "Capitão de Campos", "Castelo do Piauí", "Cocal de Telha", "Jatobá do Piauí", 
        "Juazeiro do Piauí", "Nossa Senhora de Nazaré", "Novo Santo Antônio", "São João da Serra", 
        "São Miguel do Tapuio", "Sigefredo Pacheco"
    ],
    "Entre Rios": [
        "Agricolândia", "Água Branca", "Alto Longá", "Altos", "Amarante", "Angical do Piauí", "Barro Duro", 
        "Beneditinos", "Coivaras", "Curralinhos", "Demerval Lobão", "Elesbão Veloso", "Hugo Napoleão", 
        "Jardim do Mulato", "José de Freitas", "Lagoa Alegre", "Lagoa do Piauí", "Lagoinha do Piauí", 
        "Miguel Alves", "Miguel Leão", "Monsenhor Gil", "Nazária", "Olho D'Água do Piauí", "Palmeirais", 
        "Passagem Franca do Piauí", "Pau D'Arco do Piauí", "Prata do Piauí", "Regeneração", 
        "Santo Antônio dos Milagres", "São Félix do Piauí", "São Gonçalo do Piauí", "São Pedro do Piauí", 
        "Teresina", "União"
    ],
    "Vale do Sambito": [
        "Aroazes", "Barra D'Alcântara", "Inhuma", "Lagoa do Sítio", "Novo Oriente do Piauí", "Pimenteiras", 
        "Santa Cruz dos Milagres", "Valença do Piauí", "Várzea Grande"
    ],
    "Vale do Rio Guaribas": [
        "Aroeiras do Itaim", "Bocaina", "Dom Expedito Lopes", "Francisco Santos", "Geminiano", "Ipiranga do Piauí", 
        "Itainópolis", "Monsenhor Hipólito", "Paquetá", "Picos", "Santa Cruz do Piauí", "Santana do Piauí", 
        "São José do Piauí", "São Luis do Piauí", "Sussuapara", "Wall Ferraz"
    ],
    "Chapada do Vale do Rio Itaim": [
        "Acauã", "Belém do Piauí", "Betânia do Piauí", "Caldeirão Grande do Piauí", "Caridade do Piauí", 
        "Curral Novo do Piauí", "Francisco Macedo", "Jacobina do Piauí", "Jaicós", "Marcolândia", 
        "Massapê do Piauí", "Padre Marcos", "Patos do Piauí", "Paulistana", "Queimada Nova", "Simões"
    ],
    "Vale do Canindé": [
        "Campinas do Piauí", "Cajazeiras do Piauí", "Colônia do Piauí", "Conceição do Canindé", "Floresta do Piauí", 
        "Isaías Coelho", "Oeiras", "Santa Rosa do Piauí", "Santo Inácio do Piauí", "São Francisco do Piauí", 
        "São João da Varjota", "Tanque do Piauí"
    ],
    "Serra da Capivara": [
        "Anísio de Abreu", "Bonfim do Piauí", "Caracol", "Coronel José Dias", "Dirceu Arcoverde", 
        "Dom Inocêncio", "Fartura do Piauí", "Guaribas", "Jurema", "São Braz do Piauí", "São Lourenço do Piauí", 
        "São Raimundo Nonato", "Várzea Branca"
    ],
    "Vale dos Rios Piauí e Itaueiras": [
        "Arraial", "Bela Vista do Piauí", "Brejo do Piauí", "Canto do Buriti", "Colônia do Gurguéia", 
        "Eliseu Martins", "Flores do Piauí", "Floriano", "Francisco Ayres", "Itaueria", "Nazaré do Piauí", 
        "Pajeú do Piauí", "Paes Landim", "Pavussu", "Rio Grande do Piauí", "São Francisco de Assis do Piauí", 
        "São João do Piauí", "Simplício Mendes", "Socorro do Piauí", "Tamboril do Piauí"
    ],
    "Tabuleiros do Alto Parnaíba": [
        "Antônio Almeida", "Baixa Grande do Ribeiro", "Bertolínia", "Canavieira", "Guadalupe", 
        "Jerumenha", "Landri Sales", "Marcos Parente", "Porto Alegre do Piauí", "Ribeiro Gonçalves", 
        "Santa Filomena", "Sebastião Leal", "Uruçuí"
    ],
    "Chapada das Mangabeiras": [
        "Alvorada do Gurguéia", "Avelino Lopes", "Barreiras do Piauí", "Bom Jesus", "Cristalândia do Piauí", 
        "Cristino Castro", "Currais", "Curimatá", "Gilbués", "Monte Alegre do Piauí", "Morro Cabeça no Tempo", 
        "Palmeira do Piauí", "Parnaguá", "Redenção do Gurguéia", "Riacho Frio", "Santa Luz", "São Gonçalo do Gurguéia", 
        "Sebastião Barros"
    ]
}

# Macro-regions mapping (Macro -> Territories)
macro_mapping = {
    "Litoral": ["Planície Litorânea", "Cocais"],
    "Meio-Norte": ["Carnaubais", "Entre Rios"],
    "Semiárido": ["Vale do Sambito", "Vale do Rio Guaribas", "Chapada do Vale do Rio Itaim", "Vale do Canindé", "Serra da Capivara", "Vale dos Rios Piauí e Itaueiras"],
    "Cerrados": ["Tabuleiros do Alto Parnaíba", "Chapada das Mangabeiras"]
}

# Reverse mapping: Territory -> Macro
territorio_to_macro = {}
for macro, terrs in macro_mapping.items():
    for t in terrs:
        territorio_to_macro[t] = macro

# Load IBGE data
with open("municipios_pi_ibge.json", "r") as f:
    ibge_data = json.load(f)

final_mapping = {}

def normalize_name(name):
    return name.strip().replace("  ", " ")

# Map each municipality
for item in ibge_data:
    code = str(item["id"])[:6]
    name = normalize_name(item["nome"])
    
    found_terr = "Outros"
    for terr, mun_list in territorios.items():
        if any(normalize_name(m).lower() == name.lower() for m in mun_list):
            found_terr = terr
            break
    
    macro = territorio_to_macro.get(found_terr, "Outros")
    
    final_mapping[code] = {
        "nome": name,
        "territorio": found_terr,
        "macrorregiao": macro
    }

# Save the final mapping
with open("src/regionalizacao_pi.json", "w", encoding="utf-8") as f:
    json.dump(final_mapping, f, indent=4, ensure_ascii=False)

print(f"Mapped {len(final_mapping)} municipalities.")
