const express = require('express');
const app = express();
const fileUpload = require("express-fileupload");
const exec = require('child_process').exec;

app.use(express.static('public'));

app.use(fileUpload({
  useTempFiles : true,
  tempFileDir : '/tmp/'
}));

app.post("/upload", function (req, res) { 
  if (req.files && Object.keys(req.files).length !== 0) { 
    const uploadedFile = req.files.uploadFile; 
  
    // Logging uploading file 
    console.log(uploadedFile); 
    
    exec('blackbox-tools/blackbox_decode ' + uploadedFile.tempFilePath, (error, stdout, stderr) => {
      console.log('stdout: ' + stdout);
      console.log('stderr: ' + stderr);
      if (error !== null) {
        console.log('exec error: ' + error);
        res.sendStatus(500);
        return;
      }
      
      res.download(uploadedFile.tempFilePath + ".01.csv", function (err) { 
        if (err) { 
          console.log(err); 
        } 
      }); 
    });
  } else {
    res.status = 400;
    res.send("No file uploaded !!");
  }
}); 

app.listen(process.env.PORT, () => {
  console.log(`Example app listening on port ${process.env.PORT}`)
});