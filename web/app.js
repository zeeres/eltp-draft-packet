var app = angular.module('draftPacketApp', []);

app.controller('draftPacketController', function($scope, $http) {
    $scope.packet = [];
    $scope.loading = true;

    $scope.selection = -1;

    $scope.select = function(i) {
        $scope.selection = i;
    };

    $http.get('packet.json').then(data => {
        $scope.packet = data.data;
        $scope.loading = false;
    });
});
