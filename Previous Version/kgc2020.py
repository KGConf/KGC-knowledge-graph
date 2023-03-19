from rdflib import URIRef, BNode, Literal, Graph, plugin, Namespace
from rdflib.serializer import Serializer 
from rdflib.namespace import FOAF, DC, RDF, RDFS, OWL, SKOS, NamespaceManager
import csv

labelDict = {}

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


KGC = URIRef("http://www.knowledgegraph.tech")
KGC2019 = URIRef("http://www.knowledgegraph.tech/conference-2019")
KGC2020 = URIRef(("http://www.knowledgegraph.tech/conference-2020"))
g.add((KGC, RDF.type, schema.EventSeries))
g.add((KGC, schema.name, Literal("Knowledge Graph Conference")))
g.add((KGC, OWL.sameAs, wd.Q86935657))
g.add((KGC2019, OWL.sameAs, wd.Q87486633))
g.add((KGC2020, OWL.sameAs, wd.Q76451254))
g.add((KGC2019, schema.name, Literal("Knowledge Graph Conference 2019")))
g.add((KGC2020, schema.name, Literal("Knowledge Graph Conference 2020")))
g.add((KGC2019, RDF.type, schema.Event))
g.add((KGC2020, RDF.type, schema.Event))
g.add((KGC2019, schema.superEvent, KGC))
g.add((KGC2020, schema.superEvent, KGC))
g.add((KGC2019, schema.eventAttendanceMode, schema.OfflineEventAttendanceMode))
g.add((KGC2020, schema.eventAttendanceMode, schema.OnlineEventAttendanceMode))

speaker_file = csv.DictReader(open('KGC-2020-Speakers-Recon.csv'))
for row in speaker_file:
	
	name = row['Name']
	if name != "":
		if name in labelDict:
			speaker = labelDict[name]
		else:
			speaker = BNode()
			g.add((speaker, RDF.type, schema.Person))
			g.add((speaker, schema.name, Literal(row["Name"])))
			if row["personQID"] != "":
				g.add((speaker, OWL.sameAs, URIRef(wd + row["personQID"])))
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
			school = labelDict["schoolName"]
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
			co = BNode()
			g.add((co, schema.name, Literal(coName)))
			g.add((co, RDF.type, schema.Organization))
			if row["companyQID"]!= "":
				g.add((co, OWL.sameAs, URIRef(wd + row["companyQID"])))
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



talkfile = csv.DictReader(open("KGC-2020-Presentations-Recon.csv"))
for row in talkfile:

	title = row['Title']
	if title != "":
		if title in labelDict:
			talk = labelDict[title]
		else:
			talk = BNode()
			g.add((talk, RDF.type, schema.Event))
			g.add((talk, schema.name, Literal(title)))
			g.add((talk, schema.superEvent, KGC2020))
			if row["Description"] != "":
				g.add((talk, schema.description, Literal(row["Description"])))
			labelDict[title] = talk


	presenterName = row['Name']
	if presenterName != "":
		if presenterName in labelDict:
			presenter = labelDict[presenterName]
		else:
			presenter = BNode()
			g.add((presenter, RDF.type, schema.Person))
			g.add((presenter, schema.name, Literal(title)))
			labelDict[presenterName] = presenter
		g.add((talk, schema.performer, presenter))


	tagText = row["tag"]
	if tagText != "":
		if tagText in labelDict:
			tag = labelDict[tagText]
		else:
			tag = BNode()
			g.add((tag, RDF.type, SKOS.Concept))
			g.add((tag, schema.name, Literal(tagText)))
			if row["tagQID"] != "":
				g.add((tag, OWL.sameAs, URIRef(wd + row["tagQID"])))
		g.add((talk, schema.about, tag))

	broader = row["facet of"]
	if broader != "":
		if broader in labelDict:
			b = labelDict["broader"]
		else:
			b = BNode()
			g.add((b, RDF.type, SKOS.Concept))
			g.add((b, schema.name, Literal(broader)))
			g.add((b, OWL.sameAs, URIRef(wd + row["facetOfQID"])))
		g.add((tag, SKOS.broader, b))




g.serialize(destination = "kgc2020.ttl", format = "turtle")