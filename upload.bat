xcopy . DesignBuildFly /exclude:except.txt /y
cd DesignBuildFly
git add .
git commit -m "script upload"
git push origin
cd ..