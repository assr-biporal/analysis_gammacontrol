IPYNBNAME=$1
DIRNAME=$2
cp *.json $DIRNAME
cp $IPYNBNAME $DIRNAME
cd $DIRNAME
jupyter nbconvert --execute $IPYNBNAME --to html --ExecutePreprocessor.timeout=1800