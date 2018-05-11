farmApp.controller("MenuAboutController",
  function($scope) {
    console.log("Entered MenuAboutController");
  
    var thoughts = ["I am a seasoned Python Backend Developer comfortable with message queues, RDBMS and NoSQL.",
                    "I have developed MPA features, deployed them and when necessary debugged production issues.",
                    "I prefer working from an Product team defined MRD and always begin with a Design Document.",
                    "I prefer to validate my features with UI, API and unit tests before deployment.",
                    "I have built environments for code development and test using Linux, bash, python and AWS EC2.",
                    "I am comfortable with MongoDB, Cassandra, ElasticSearch, Django, Flask and familiar with AngularJS v1.0.",
                    "I am also comfortable with Docker, AWS EC2, S3, SimpleDB, SQS and SNS.",
                    "I enjoy working as an independent contributor but have also led small Agile teams."];

    $scope.text = thoughts.join(" ");
    console.log("text: " + $scookie.text);
    $scope.url = "/static/images/menu/about.jpg";
    console.log("url: " + $scope.url);
});
