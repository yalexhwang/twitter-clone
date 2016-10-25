angular.module('starter.controllers', [])

.service('googleMap', function() {
  var data ={};
  this.makeMarker = function(coords, map) {
    var marker = new google.maps.Marker({
          position: coords,
          map: map
    });
    return marker;
  };
})

.controller('MainCtrl', function($scope, $cordovaGeolocation, $ionicLoading, googleMap) {
  // var coords = {};
  // var positionOptions = {timeout: 10000, enableHighAccuracy: true};
  // $ionicLoading.show();
  // $cordovaGeolocation.getCurrentPosition(positionOptions)
  // .then(function(position) {
  //   coords = {
  //     lat: position.coords.latitude,
  //     lng: position.coords.longitude
  //   };
  //   var mapElement = document.getElementById('map');
  //   var mapOptions = {
  //     center: coords,
  //     zoom: 15,
  //     mapTypeId: google.maps.MapTypeId.ROADMAP
  //   };
  //   $ionicLoading.hide();
  //   var map = new google.maps.Map(mapElement, mapOptions);
  //   googleMap.makeMarker(coords, map);
  // });
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 40.00, lng: -98.00},
    zoom: 4
  });
})

.controller('PostCtrl', function($scope) {
  
})

.controller('DashCtrl', function($scope) {})
.controller('LogInCtrl', function($scope, $http, $location) {
  var url = "http://localhost:3000";
  $scope.user = {};
  $scope.login = function() {
    console.log($scope.user);
    $http.post(url + '/login', {
      user: $scope.user
    }).then(function success(rspns) {
      console.log(rspns);
      $location.path('/main');
    }, function sutccess(rspns) {
      console.log(rspns);
    });
  };
})

.controller('RegisterCtrl', function($scope, $http) {
  var url = "http://localhost:3000";
  $scope.user = {};
  $scope.confirm = {};
  var pw = $scope.confrimPW;
  var temp = {
    fname: 'Alex',
    lname: 'Hwang',
    username: 'ah',
    email: 'ah@test.com',
    password: 111
  };

  $scope.register = function() {
    console.log($scope.test);
    console.log($scope.user);
    console.log($scope.confirm);
    if (temp.password == 111) {
      console.log("Password match");
      $http.post(url + '/register', {
        user: temp
      }).then(function success(rspns) {
        console.log(rspns);
      }, function fail(rspns) { 
        console.log("error")
      });
    } else {
      console.log("Try confirmPW again");
    }
  };

})
.controller('ChatsCtrl', function($scope, Chats) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.chats = Chats.all();
  $scope.remove = function(chat) {
    Chats.remove(chat);
  };
})

.controller('ChatDetailCtrl', function($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})

.controller('AccountCtrl', function($scope) {
  $scope.settings = {
    enableFriends: true
  };
});
