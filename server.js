const express = require("express");
const app = express();
const fileUpload = require("express-fileupload");
const exec = require("child_process").exec;

app.use(express.static("public"));

app.use(
  fileUpload({
    useTempFiles: true,
    tempFileDir: "/tmp/",
  })
);

app.post("/parse_windtunnel", (req, res) => {
  if (req.files && Object.keys(req.files).length !== 0) {
    const blackboxZip = req.files.blackboxZip;
    const windtunnelZip = req.files.windtunnelZip;

    // Logging uploading files
    console.log(blackboxZip);
    console.log(windtunnelZip);

    exec(
      "python3 -m python_tools.scripts.parse_windtunnel " +
        blackboxZip.tempFilePath +
        " " +
        windtunnelZip.tempFilePath +
        " " +
        "/tmp/processed.zip",
      (error, stdout, stderr) => {
        console.log("stdout: " + stdout);
        console.log("stderr: " + stderr);
        if (error !== null) {
          console.log("exec error: " + error);
          res.sendStatus(500);
          return;
        }

        res.download("/tmp/processed.zip", function (err) {
          if (err) {
            console.log(err);
          }
        });
      }
    );
  } else {
    res.status = 400;
    res.send("No file uploaded!!");
  }
});

app.post("/decode_blackbox", (req, res) => {
  if (req.files && Object.keys(req.files).length !== 0) {
    const uploadedFile = req.files.uploadFile;

    // Logging uploading file
    console.log(uploadedFile);

    exec(
      "python3 -m python_tools.scripts.decode_blackbox " +
        uploadedFile.tempFilePath +
        " " +
        uploadedFile.tempFilePath +
        ".csv",
      (error, stdout, stderr) => {
        console.log("stdout: " + stdout);
        console.log("stderr: " + stderr);
        if (error !== null) {
          console.log("exec error: " + error);
          res.sendStatus(500);
          return;
        }

        res.download(uploadedFile.tempFilePath + ".csv", function (err) {
          if (err) {
            console.log(err);
          }
        });
      }
    );
  } else {
    res.status = 400;
    res.send("No file uploaded!!");
  }
});

app.post("/decode_thrust", (req, res) => {
  if (req.files && Object.keys(req.files).length !== 0) {
    const uploadedFile = req.files.uploadFile;

    // Logging uploading file
    console.log(uploadedFile);

    exec(
      "python3 -m python_tools.scripts.decode_thrust " +
        uploadedFile.tempFilePath +
        " " +
        uploadedFile.tempFilePath +
        "_csvs.zip",
      (error, stdout, stderr) => {
        console.log("stdout: " + stdout);
        console.log("stderr: " + stderr);
        if (error !== null) {
          console.log("exec error: " + error);
          res.sendStatus(500);
          return;
        }

        res.download(uploadedFile.tempFilePath + "_csvs.zip", function (err) {
          if (err) {
            console.log(err);
          }
        });
      }
    );
  } else {
    res.status = 400;
    res.send("No file uploaded!!");
  }
});

app.listen(process.env.PORT, () => {
  console.log(`Example app listening on port ${process.env.PORT}`);
});
