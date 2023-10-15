const express = require('express');
const app = express();
const fileUpload = require("express-fileupload"); 

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
    
  } else res.send("No file uploaded !!"); 
}); 

app.listen(process.env.PORT, () => {
  console.log(`Example app listening on port ${process.env.PORT}`)
});