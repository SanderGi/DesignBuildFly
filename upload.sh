#! /bin/bash
xcopy . DesignBuildFly /exclude:except.txt
cd DesignBuildFly
git commit -m "script upload"
git push origin
cd ..