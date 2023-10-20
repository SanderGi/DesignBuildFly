xcopy . ..\DesignBuildFly\data\windTunnel /e /y
cd ..\DesignBuildFly\data\windTunnel
git add .
git commit -m "script upload"
git push origin
cd "AP 23-24"