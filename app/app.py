from flask import Flask
import ghhops_server as hs
import owlready2 as or2
import rhino3dm as rh

app = Flask('__name__')
hops = hs.Hops(app)

# LOAD ONTOLOGY
@hops.component(
  "/loadOntology",
  name="Load",
  description="Load an ontology from URL/file",
  inputs=[
    hs.HopsString("URL", "URL", "URL of the ontology to load")
  ],
  outputs=[
    hs.HopsString("Classes", "Classes", "Classes in the ontology", access=hs.HopsParamAccess.LIST),
    hs.HopsString("Properties", "Properties", "Properties in the ontology", access=hs.HopsParamAccess.LIST),
    hs.HopsString("Individuals", "Individuals", "Individuals in the ontology", access=hs.HopsParamAccess.LIST),
  ]
)
def loadOnto(txt: str):
  log = []

  # parse ontology to xml file if file not in RDF/XML or OWL/XML formats
  if not txt.endswith('.xml') or not txt.endswith('.owl'):
    from pathlib import Path
    path = str(Path.cwd())+ '\\app\\temp\\'
    
    warn = 'attempting to load ontology in Turtle format (.ttl)...'
    print(warn)
    name = txt.split('/')[-1].split('.')[0]

    if f"{path}{name}.xml":
      print('loading temporary file...')

    else:
      from rdflib import Graph

      g = Graph()
      g.parse(txt)
      g.serialize(destination=f"{path}{name}.xml", format="xml")

      warn = 'ontology serialized to XML format.'
      print(warn)

    txt = f"{path}{name}.xml"

  onto = or2.get_ontology(txt)
  onto.load()
  print('-'*60)
  print('ontology loaded from: ', txt)

  # get classes from the ontology
  class_temp = list(onto.classes())
  classes = []
  print('\nclasses in the ontology:')
  print('-'*30)
  for c in class_temp:
    print(c.name)
    classes.append(c.name)

  # get properties from the ontology
  prop_temp = list(onto.properties())
  props = []
  print('\nproperties in the ontology:')
  print('-'*30)
  for p in prop_temp:
    print(p.name)
    props.append(p.name)    

  # get individuals from the ontology
  ind_temp = list(onto.individuals())
  inds = []
  print('\nindividuals in the ontology:')
  print('-'*30)
  for i in ind_temp:
    print(i.name)
    inds.append(i.name)

  return classes, props, inds


if __name__ == "__main__":
    app.run()