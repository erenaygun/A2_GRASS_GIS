# Aufgabe 1: Create new location in GRASS GIS  

Eine neue Location namens "BadenWuerttemberg" angelegt und dieser wurde das Koordinatenreferenzsystem der tif-Datei  
"GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3.tif" zugewiesen. Dieses wurde bereits bei der Erstellung der Location  
von der tif-Datei herausgelesen.

# Aufgabe 2: Import data  

## 2.1 Motorways  
Mit dem Befehl  $v.import input="\Users\Eren\Desktop\Wintersemester 2021\fossgis\A2_GRASS_GIS\data\motorways.shp" output=motorways  
importiert man die erste Datei ins GRASSGIS.

## 2.2 Administrative Districts of Baden-Württemberg  
Vor dem Import der Gemeinde Baden-Württembergs muss man erst von der Shapefile nur die Gemeine Baden-Württembergs  
auswählen und die Datei umprojizieren.Dies geschieht durch die Eingabe des Befehls:  
$ogr2ogr -f "ESRI Shapefile" districts_bw.shp gadm28_adm2_germany.shp -sql "SELECT * FROM gadm28_adm2_germany where NAME_1 = 'Baden-Württemberg'" -t_srs ESRI:54009.

Für die Auswahl der Gebiete und das Umprojizieren habe ich mich für OsgeoShell entschieden, da ich sonst erst eine neue  
Location im GRASS-GIS hätte erstellen müssen, in der man die Gebiete der Baden-Württemberg erst auswählte und speichterte  
und danach in die urspüngliche Location importieren müsste, da die Koordinatensysteme der ShapeFile-Datei und der  
upsprünglichen anders sind. 

Mit dem Befehl $v.import input="/Users/Eren/Desktop/Wintersemester 2021/fossgis/A2_GRASS_GIS/data/districts_bw.shp" output=districts_bw snap=0.0001 importiert  
man die erstellte zugeschnitte Datei auf GRASS GIS hoch

## 2.3 Global Human Settlement Layer  
Man importiert die Raster-Datei mit dem Befehl: $r.import input="/Users/Eren/Desktop/Wintersemester 2021/fossgis/A2_GRASS_GIS/data/GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3/GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3.tif" output=global_human_settlement_data hoch.  

# Aufgabe 3: Calculate the total population of the districts  

## 3.1 Set the region  
$g.region vect=districts_bw row=1018 col=879 stellt die Auflösung auf 250m x 250 m ein und schneidet die Region auf den gegebenen Vektor_Layer zu
 
## 3.2. Rasterize the districts  
Zur Rasterisierung wird benötigt: $v.to.rast input=districts_bw output=districts_raster use=attr attribute_column="OBJECTID"

## 3.3 Calculate the population of each district
Zur Berechnung der Einwohnerzahl pro Gebiet: $r.stats.zonal -r -l -n base=districts_raster cover=global_human_settlement_data method=sum output=district_population separator=tab

## 3.4 Evaluate the population estimate  
Für den Vergleich der ausgerechneten Einwohnerzahl und der offiziellen Einwohnerzahlen werden die Städte Mannheim, Heidelberg  
und Stuttgart ausgewählt. Zonal Statistics liefert für die besagten Städte jeweils 299.000, 150.000 und 609.000 Einwohner,  
während die besagten Städte jeweils von 322.000, 160.000 und 620.000 Einwohnern für das 2020 ausgehen. Während die Unterschiede  
für Stuttgart und Heidelberg knapp bei 10.000 Einwohnern liegen, beträgt der Unterschied für Mannheim über 20.000. Daher  
ist unsere Berechnung nicht sehr gut einzustufen.

#Aufgabe 4: Calculate total population living within 1km of motorways  

$g.region vect=motorways, stellt die Region auf den Vector-Layer "motorways.shp".  
$v.to.rast input=motorways output=motorways_raster use=cat label_column=ref rasterisiert den Vector layer.    
$r.buffer input=motorways_raster output=buffer_1000 distances=1000, legt Pufferbereiche um motorways herum  
$r.stats.zonal -r base=buffer_1000 cover=global_human_settlement_data method=sum output=population_buffer1000 rechnet die Anzahl an Einwohnern, die  
innerhalb eines Kilometers von "motorways" wohnen.
