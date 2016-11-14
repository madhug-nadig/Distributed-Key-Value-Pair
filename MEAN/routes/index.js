var express = require('express');
var router = express.Router();

var PythonShell = require('python-shell');


/* GET home page. */
router.get('/', function(req, res, next) {
  
  successmessage = "";
  if(req.query.success){
  		successmessage = "Your request was successful";
  }
  res.render('index', { title: 'Distributed key value data store', message : successmessage });

});

router.post('/get', function(req, res, next) {
	console.log("\n\t\t\t\t RUNNING THE APPLICATION MASTER\n");

	var options = {
            mode: 'json',
            args: ["get" ,req.body.getcommand]
        };

	PythonShell.run('../pyt/ApplicationMaster.py', options, function (err, results) {
            if (err) throw err;
            console.log(results[0][0].message);
            console.log("Status: "  + results[0][0].status+ "\n");
            console.log("Value: "  + results[0][0].value+ "\n");
            console.log("Data retrived from : Node " + results[0][0].from+ "\n");
            res.redirect('/?success=true');
        });

});

router.post('/post', function(req, res, next) {
	console.log("\n\t\t\t\t RUNNING THE APPLICATION MASTER\n");

	var options = {
            mode: 'json',
            args: ["post" ,req.body.postcommand]
        };

	PythonShell.run('../pyt/ApplicationMaster.py', options, function (err, results) {
            if (err) throw err;
            console.log(results[0][0].message);
            console.log("Status: "  + results[0][0].status+ "\n");
            console.log("Data stored in : Node" + results[0][0].main+ "\n");
            console.log("Data replica: Node"  + results[0][0].replica+ "\n");
            res.redirect('/?success=true');
    });

});

module.exports = router;
