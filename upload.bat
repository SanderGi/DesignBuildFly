xcopy . ..\DesignBuildFly /e /y
cd ..\DesignBuildFly
git add .
git commit -m "script upload"
git push origin
cd "AP 23-24"