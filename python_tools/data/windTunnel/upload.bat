xcopy . ..\DesignBuildFly\python_tools\data\windTunnel /e /y
cd ..\DesignBuildFly\python_tools\data\windTunnel
git add .
git commit -m "script upload"
git push origin
cd "..\..\..\..\AP 23-24"