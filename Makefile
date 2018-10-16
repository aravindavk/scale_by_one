all:
	echo "== Summary" > README.adoc
	echo "----" >> README.adoc
	echo "Initial number of nodes          : 3"  >> README.adoc
	echo "Max nodes added                  : 24(+21)"  >> README.adoc
	echo "Initial number of bricks per node: 8"  >> README.adoc
	echo "Max device size per node         : 100G"  >> README.adoc
	echo "Volume Type                      : Replica 3"  >> README.adoc
	echo  >> README.adoc
	python3 scale_by_one.py | grep "Volume Size" | sed 's/\.\*\*//' | sed 's/\*\*//' >> README.adoc
	echo "----" >> README.adoc
	echo >> README.adoc
	echo "== Details" >> README.adoc
	echo "**Note**: Number prefix shown with brick name represents sub volume number. Bricks belonging to same sub volume should not exists in same node"  >> README.adoc
	python3 scale_by_one.py >> README.adoc
