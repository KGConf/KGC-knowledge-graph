from rdflib import URIRef, BNode, Literal, Graph, plugin, Namespace
from rdflib.serializer import Serializer 
from rdflib.namespace import FOAF, DC, RDF, RDFS, OWL, SKOS, NamespaceManager
import csv

labelDict = {}

kgc2020 = Graph()
kgc2020.parse('./kgc2020.ttl', format='ttl')
nm2020 = NamespaceManager(kgc2020)
schema = Namespace("http://schema.org/")
nm2020.bind("schema", schema)
wd = Namespace("http://www.wikidata.org/entity/")
nm2020.bind("wd", wd)
owl = Namespace("http://www.w3.org/2002/07/owl#")
nm2020.bind("owl", owl)
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
nm2020.bind("skos", skos)

# retrieve speaker entities from previous year 
res = kgc2020.query('''select distinct ?p ?name where {?p a schema:Person; schema:name ?name}''')
for row in res:
    labelDict[str(row[1])] = row[0]

#retrieve last id # to increment from
res = kgc2020.query('''select ?s where {?s ?p ?o. filter(regex(str(?s),"http://www.knowledgegraph.tech/iri"))}''' )
ids = [int(str(r[0])[-5:]) for r in res]
ids.sort()
lastId = ids[-1]+1

g = Graph()
nm = NamespaceManager(g)
schema = Namespace("http://schema.org/")
nm.bind("schema", schema)
wd = Namespace("http://www.wikidata.org/entity/")
nm.bind("wd", wd)
owl = Namespace("http://www.w3.org/2002/07/owl#")
nm.bind("owl", owl)
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
nm.bind("skos", skos)
kgc = Namespace("http://www.knowledgegraph.tech/iri/")
nm.bind("kgc", kgc)

KGC = URIRef("http://www.knowledgegraph.tech")
#KGC2019 = URIRef("http://www.knowledgegraph.tech/conference-2019")
#KGC2020 = URIRef(("http://www.knowledgegraph.tech/conference-2020"))
KGC2021 = URIRef(("http://www.knowledgegraph.tech/conference-2021"))
g.add((KGC, RDF.type, schema.EventSeries))
g.add((KGC, schema.name, Literal("Knowledge Graph Conference")))
g.add((KGC, OWL.sameAs, wd.Q86935657))
g.add((KGC2021, OWL.sameAs, wd.Q106704796))
g.add((KGC2021, schema.name, Literal("Knowledge Graph Conference 2021")))
g.add((KGC2021, RDF.type, schema.Event))
g.add((KGC2021, schema.superEvent, KGC))
g.add((KGC2021, schema.eventAttendanceMode, schema.OnlineEventAttendanceMode))

speaker_file = csv.DictReader(open('KGC-2021-Speakers-Recon.csv'))
for row in speaker_file:
    
    name = row['Name']
    if name != "":
        if name in labelDict:
            speaker = labelDict[name]
            #print(name)
        else:
            speaker = URIRef(kgc + str(lastId))
            lastId += 1
            g.add((speaker, RDF.type, schema.Person))
            g.add((speaker, schema.name, Literal(row["Name"])))
            for qid in row["personQID"].split(';'):
                g.add((speaker, OWL.sameAs, URIRef(wd + qid.strip())))
            labelDict[name] = speaker
    
    countryName = row["countryOfCitizenship"]
    if countryName != "":
        if countryName in labelDict:
            country = labelDict[countryName]
        else:
            country = BNode()
            g.add((country, RDF.type, schema.Country))
            g.add((country, schema.name, Literal(countryName)))
            if row["countryOfCitizenshipQID"]!= "":
                g.add((country, OWL.sameAs, URIRef(wd + row["countryOfCitizenshipQID"])))
            labelDict[countryName] = country
        g.add((speaker, schema.nationality, country))

    schoolName = row["educatedAt"]
    if schoolName != "":
        if schoolName in labelDict:
            school = labelDict[schoolName]
        else:
            school = BNode()
            g.add((school, schema.name, Literal(schoolName)))
            g.add((school, RDF.type, schema.EducationalOrganization))
            if row["educatedAtQID"]!= "":
                g.add((school, OWL.sameAs, URIRef(wd + row["educatedAtQID"])))
            labelDict[schoolName] = school
        g.add((speaker, schema.alumniOf, school))
            

    pfowName = row["personFieldOfWork"]
    if pfowName != "":
        if pfowName in labelDict:
            pfow = labelDict[pfowName]
        else:
            pfow = BNode()
            g.add((pfow, schema.name, Literal(pfowName)))
            g.add((pfow, RDF.type, schema.Thing))
            if row["personFieldOfWorkQID"]!= "":
                g.add((pfow, OWL.sameAs, URIRef(wd + row["personFieldOfWorkQID"])))
            labelDict[pfowName] = pfow
        g.add((speaker, schema.knowsAbout, pfow))


    coName = row["Company"]
    if coName != "":
        if coName in labelDict:
            co = labelDict[coName]
        else:
            co = URIRef(kgc + str(lastId))
            lastId += 1
            g.add((co, schema.name, Literal(coName)))
            g.add((co, RDF.type, schema.Organization))
            for qid in row["companyQID"].split(';'):
                g.add((co, OWL.sameAs, URIRef(wd + qid.strip())))
            labelDict[coName] = co
        g.add((speaker, schema.worksFor, co))


    consortiumName = row["member of"]
    if consortiumName != "":
        if consortiumName in labelDict:
            consortium = labelDict[consortiumName]
        else:
            consortium = BNode()
            g.add((consortium, schema.name, Literal(consortiumName)))
            g.add((consortium, RDF.type, schema.Organization))
            if row["memberOfQID"]!= "":
                g.add((consortium, OWL.sameAs, URIRef(wd + row["memberOfQID"])))
            labelDict[consortiumName] = consortium
        g.add((co, schema.memberOf, consortium))


    HQName = row["HQ"]
    if HQName != "":
        if HQName in labelDict:
            HQ = labelDict[HQName]
        else:
            HQ = BNode()
            g.add((HQ, schema.name, Literal(HQName)))
            g.add((HQ, RDF.type, schema.Place))
            if row["HQQID1"]!= "":
                g.add((HQ, OWL.sameAs, URIRef(wd + row["HQQID1"])))
            labelDict[HQName] = HQ
        g.add((co, schema.location, HQ))

    HQ2Name = row["HQ2"]
    if HQ2Name != "":
        if HQ2Name in labelDict:
            HQ2 = labelDict[HQ2Name]
        else:
            HQ2 = BNode()
            g.add((HQ2, schema.name, Literal(HQ2Name)))
            g.add((HQ2, RDF.type, schema.Place))
            if row["HQQID2"]!= "":
                g.add((HQ2, OWL.sameAs, URIRef(wd + row["HQQID2"])))
            labelDict[HQ2Name] = HQ2
        g.add((HQ, schema.geoWithin, HQ2))


    HQ3Name = row["HQ3"]
    if HQ3Name != "":
        if HQ3Name in labelDict:
            HQ3 = labelDict[HQ3Name]
        else:
            HQ3 = BNode()
            g.add((HQ3, schema.name, Literal(HQ3Name)))
            g.add((HQ3, RDF.type, schema.Place))
            if row["HQQID3"]!= "":
                g.add((HQ3, OWL.sameAs, URIRef(wd + row["HQQID3"])))
            labelDict[HQ3Name] = HQ3
        g.add((HQ2, schema.geoWithin, HQ3))

    HQ4Name = row["HQ4"]
    if HQ4Name != "":
        if HQ4Name in labelDict:
            HQ4 = labelDict[HQ4Name]
        else:
            HQ4 = BNode()
            g.add((HQ4, schema.name, Literal(HQ4Name)))
            g.add((HQ4, RDF.type, schema.Place))
            if row["HQQID4"]!= "":
                g.add((HQ4, OWL.sameAs, URIRef(wd + row["HQQID4"])))
            labelDict[HQ4Name] = HQ4
        g.add((HQ3, schema.geoWithin, HQ4))


    HQ5Name = row["HQ5"]
    if HQ5Name != "":
        if HQ5Name in labelDict:
            HQ5 = labelDict[HQ5Name]
        else:
            HQ5 = BNode()
            g.add((HQ5, schema.name, Literal(HQ5Name)))
            g.add((HQ5, RDF.type, schema.Place))
            if row["HQQID4"]!= "":
                g.add((HQ5, OWL.sameAs, URIRef(wd + row["HQQID4"])))
            labelDict[HQ5Name] = HQ5
        g.add((HQ4, schema.geoWithin, HQ5))


    additionalTypeName = row["instance of"]
    if additionalTypeName != "":
        if additionalTypeName in labelDict:
            additionalType = labelDict[additionalTypeName]
        else:
            additionalType = BNode()
            g.add((additionalType, schema.name, Literal(additionalTypeName)))
            g.add((additionalType, RDF.type, URIRef(owl + "Class")))
            if row["instanceOfQID"]!= "":
                g.add((additionalType, OWL.sameAs, URIRef(wd + row["instanceOfQID"])))
            labelDict[additionalTypeName] = additionalType
        g.add((co, schema.additionalType, additionalType))

    cfowName = row["companyFieldOfWork"]
    if cfowName != "":
        if cfowName in labelDict:
            cfow = labelDict[cfowName]
        else:
            cfow = BNode()
            g.add((cfow, schema.name, Literal(cfowName)))
            g.add((cfow, RDF.type, schema.Thing))
            if row["companyFieldOfWorkQID"]!= "":
                g.add((cfow, OWL.sameAs, URIRef(wd + row["companyFieldOfWorkQID"])))
            labelDict[cfowName] = cfow
        g.add((co, schema.knowsAbout, cfow))

    industryName = row["industry"]
    if industryName != "":
        if industryName in labelDict:
            industry = labelDict[industryName]
        else:
            industry = BNode()
            g.add((industry, schema.name, Literal(industryName)))
            g.add((industry, RDF.type, schema.Thing))
            if row["industryQID"]!= "":
                g.add((industry, OWL.sameAs, URIRef(wd + row["industryQID"])))
            labelDict[industryName] = industry
        g.add((co, schema.knowsAbout, industry))


    if row["LinkedIn"] != "":
        g.add((speaker, owl.sameAs, URIRef(row["LinkedIn"])))

#speaker_file.close()

tagsDict={}

#retrieve the list of tags
res = kgc2020.query('''select distinct ?c ?name where {?c a skos:Concept; schema:name ?name}''')
for row in res:
    tagsDict[str(row[1])] = row[0]

talkfile = csv.DictReader(open("KGC-2021-Presentations-Recon.csv", encoding="utf-8"))
for row in talkfile:

    title = row['Title']
    #print(title)
    if title != "":
        if title in labelDict:
            talk = labelDict[title]
        else:
            talk = URIRef(kgc + str(lastId))
            lastId += 1
            g.add((talk, RDF.type, schema.Event))
            g.add((talk, RDF.type, schema.CreativeWork))
            g.add((talk, schema.name, Literal(title)))
            g.add((talk, schema.superEvent, KGC2021))
            if row["Description"] != "":
                g.add((talk, schema.description, Literal(row["Description"])))
            labelDict[title] = talk


    presenterName = row['Name']
    if presenterName != "":
        if presenterName in labelDict:
            presenter = labelDict[presenterName]
        else:
            print("Error: Presenter {} not in the list of speakers!".format(presenterName))
            next
            #presenter = BNode()
            #g.add((presenter, RDF.type, schema.Person))
            #g.add((presenter, schema.name, Literal(title)))
            #labelDict[presenterName] = presenter
        g.add((talk, schema.performer, presenter))


    # for tagText in row["tag"].split():
    #     if tagText in labelDict:
    #         tag = labelDict[tagText]
    #     else:
    #         tag = URIRef(kgc + str(lastId))
    #         lastId += 1
    #         g.add((tag, RDF.type, SKOS.Concept))
    #         g.add((tag, schema.name, Literal(tagText)))
    #         #if row["tagQID"] != "":
    #         #    g.add((tag, OWL.sameAs, URIRef(wd + row["tagQID"])))
    #     g.add((talk, schema.about, tag))

    #broader = row["facet of"]
    #if broader != "":
        # if broader in labelDict:
        #     b = labelDict["broader"]
        # else:
        #     b = BNode()
        #     g.add((b, RDF.type, SKOS.Concept))
        #     g.add((b, schema.name, Literal(broader)))
        #     g.add((b, OWL.sameAs, URIRef(wd + row["facetOfQID"])))
        # g.add((tag, SKOS.broader, b))

    videoURL = row["Video URL"]
    if videoURL:
        video = BNode()
        g.add((talk, schema.recordedIn, video))
        g.add((video, RDF.type, schema.VideoObject))
        g.add((video, schema.embedUrl, Literal(videoURL)))

    slidesURL = row["Slides URL"]
    if slidesURL:
        slides = BNode()
        g.add((slides, schema.about, talk))
        g.add((slides, RDF.type, schema.PresentationDigitalDocument))
        g.add((slides, schema.archivedAt, Literal(slidesURL)))



g.serialize(destination = "kgc2021.ttl", format = "turtle")