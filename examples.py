# Examples for the Cypher query generator
examples = [
    {
        "question": "Which airplanes are in the database?",
        "query": "MATCH (p:Airplane_type) RETURN p.id AS plane_id ORDER BY p.id ASC;",
    },
    {
        "question": "What is the maximum useful load for the cessna 172?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'introduction'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'performance specifications'}})-[:BELONGS_TO]->(ps) MATCH(iv:item_values{{id:'maximum useful load'}})-[:BELONGS_TO]->(pss) RETURN iv.instruction",
    },
    {
        "question": "What is the cessna's 172 rate of climb at sea level?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'introduction'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'performance specifications'}})-[:BELONGS_TO]->(ps) MATCH(iv:item_values{{id:'rate of climb at sea level'}})-[:BELONGS_TO]->(pss) RETURN iv.instruction",
    },
    {
        "question": "What is the cessna's 172 power loading?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'introduction'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'performance specifications'}})-[:BELONGS_TO]->(ps) MATCH(iv:item_values{{id:'power loading'}})-[:BELONGS_TO]->(pss) RETURN iv.instruction",
    },
    {
        "question": "What is the cessna's 172 ground roll on landing?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'introduction'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'performance specifications'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'landing performance'}})-[:BELONGS_TO]->(pss) MATCH(iv:item_values{{id:'ground roll'}})-[:BELONGS_TO]->(psi) RETURN iv.instruction",
    },
    {
        "question": "What is the definition of standard temperature in the cessna 172's poh?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'symbols, abbreviations and terminology'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'meteorological terminology'}})-[:BELONGS_TO]->(pss) MATCH(iv:item_values{{id:'standard temperature'}})-[:BELONGS_TO]->(psi) RETURN iv.instruction",
    },
    {
        "question": "What is the definition of vne in the cessna 172's poh?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'symbols, abbreviations and terminology'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'general airspeed terminology'}})-[:BELONGS_TO]->(pss) MATCH(iv:item_values{{id:'vne'}})-[:BELONGS_TO]->(psi) RETURN iv.instruction",
    },
    {
        "question": "What is the definition of vx in the cessna 172's poh?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'symbols, abbreviations and terminology'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'general airspeed terminology'}})-[:BELONGS_TO]->(pss) MATCH(iv:item_values{{id:'vx'}})-[:BELONGS_TO]->(psi) RETURN iv.instruction",
    },
    {
        "question": "What is the definition of kcas in the cessna 172's poh?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'symbols, abbreviations and terminology'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'general airspeed terminology'}})-[:BELONGS_TO]->(pss) MATCH(iv:item_values{{id:'kcas'}})-[:BELONGS_TO]->(psi) RETURN iv.instruction",
    },
    {
        "question": "What is the definition of lean mixture in the cessna 172's poh?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'symbols, abbreviations and terminology'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'engine power terminology'}})-[:BELONGS_TO]->(pss) MATCH(iv:item_values{{id:'lean mixture'}})-[:BELONGS_TO]->(psi) RETURN iv.instruction",
    },
    {
        "question": "What is the definition of mean aerodynamic chord in the cessna 172's poh?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'symbols, abbreviations and terminology'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'weight and balance terminology'}})-[:BELONGS_TO]->(pss) MATCH(iv:item_values{{id:'mean aerodynamic chord'}})-[:BELONGS_TO]->(psi) RETURN iv.instruction",
    },
    {
        "question": "What is the definition of basic empty weight in the cessna 172's poh?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'symbols, abbreviations and terminology'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'weight and balance terminology'}})-[:BELONGS_TO]->(pss) MATCH(iv:item_values{{id:'basic empty weight'}})-[:BELONGS_TO]->(psi) RETURN iv.instruction",
    },
    {
        "question": "What are the center of gravity limits in the normal category for the cessna 172?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'operating limitations'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'center of gravity limits'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id:'normal category'}})-[:BELONGS_TO]->(pss) MATCH(iv)-[:BELONGS_TO]->(psi) RETURN iv.id, iv.instruction",
    },
    {
        "question": "What are the flight load factor limits in the utility category for the cessna 172?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'operating limitations'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'flight load factor limits'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id:'utility category'}})-[:BELONGS_TO]->(pss) MATCH(iv)-[:BELONGS_TO]->(psi) RETURN iv.id, iv.instruction",
    },
    {
        "question": "What is the approved landing range for the cessna 172's flaps?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'operating limitations'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'flap limitations'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id:'approved landing range'}})-[:BELONGS_TO]->(pss) MATCH(iv)-[:BELONGS_TO]->(psi) RETURN iv.id, iv.instruction",
    },
    {
        "question": "What are the engine operating limits for the cessna 172?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'operating limitations'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'powerplant limitations'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id:'engine operating limits for takeoff and continuous operations'}})-[:BELONGS_TO]->(pss) MATCH(iv)-[:BELONGS_TO]->(psi) RETURN iv.id, iv.instruction",
    },
    {
        "question": "What is the maximum engine speed for the cessna 172?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'operating limitations'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'powerplant limitations'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id:'engine operating limits for takeoff and continuous operations'}})-[:BELONGS_TO]->(pss) MATCH(iv{{id:'maximum engine speed'}})-[:BELONGS_TO]->(psi) RETURN iv.id, iv.instruction",
    },
    {
        "question": "what are the approved fuel grades for the cessna 172?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'descriptive data'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'fuel'}})-[:BELONGS_TO]->(pss) RETURN psi.description",
    },
    {
        "question": "What are the maximum certified weights for the cessna 172?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'descriptive data'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'maximum certified weights'}})-[:BELONGS_TO]->(pss) MATCH(iv)-[:BELONGS_TO]->(psi) RETURN iv.id, iv.instruction",
    },
    {
        "question": "What is the engine specification for the cessna 172?",
        "query": "MATCH(poh:poh{{id: 'cessna 172 poh'}}) MATCH(ps:poh_section{{id:'general'}})-[:BELONGS_TO]->(poh) MATCH(pss:poh_subsection{{id:'descriptive data'}})-[:BELONGS_TO]->(ps) MATCH(psi:poh_subsection_item{{id: 'engine'}})-[:BELONGS_TO]->(pss) RETURN ps.description",
    },
]